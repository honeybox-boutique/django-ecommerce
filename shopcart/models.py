from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save, m2m_changed
from purchases.models import PurchaseItems

User = settings.AUTH_USER_MODEL
# Create your models here.

# ShopCart Statuses
OPEN, SAVED, FROZEN, SUBMITTED = ("Open", "Saved", "Frozen", "Submitted")
STATUS_CHOICES = (
    (OPEN, _("Open - currently active")),
    (SAVED, _("Saved - for items to be purchased later")),
    (FROZEN, _("Frozen - the basket cannot be modified")),
    (SUBMITTED, _("Submitted - has been ordered at the checkout")),
)
class ShopCartManager(models.Manager):

    def get_or_new(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:# Check if session cart exists
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:# If authed and shoppincart user not set
                # filter for user cart
                user_cart = self.get_queryset().filter(user=request.user)
                if user_cart.count() >= 1:
                    user_cart_obj = user_cart.first()# user cart
                    items_to_add = cart_obj.shopCartItems.filter(piIsAvailable=True).all()# added available filter here

                    # filter out items already present in user cart
                    for cart_item in user_cart_obj.shopCartItems.all():
                        # if in usercart, exclude, then save
                        items_to_add = items_to_add.exclude(pk=cart_item.pk)

                    # add filtered items to user cart
                    for item in items_to_add:
                        user_cart_obj.shopCartItems.add(item)

                    # set cart_obj to modified usercartobj
                    cart_obj = user_cart_obj
                    del request.session['cart_id']

                # if user cart doesn't exist just save session cart to user
                else:
                    cart_obj.user = request.user
                    cart_obj.save()
                    del request.session['cart_id']
            # else: # if user is not authed and cart_obj.user is None:
                # maybe add check for item availability here?

        else:# if session cart doesn't exist
            if not request.user.is_authenticated:           # and user is not authenticated
                new_obj = True
                cart_obj = ShopCart.objects.new(user=request.user)
                request.session['cart_id'] = cart_obj.id
            else:
                # return user cart
                user_cart = self.get_queryset().filter(user=request.user)
                if user_cart.count() == 1:
                    new_obj = False
                    cart_obj = user_cart.first()
                else:
                    new_obj = True
                    cart_obj = ShopCart.objects.new(user=request.user)

        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class ShopCart(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    shopCartDateCreated = models.DateTimeField(auto_now_add=True)
    shopCartLastModified = models.DateTimeField(auto_now=True)

    shopCartStatus = models.CharField(max_length=40, default=OPEN, choices=STATUS_CHOICES)

    shopCartSubTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    shopCartItems = models.ManyToManyField(PurchaseItems, blank=True)
    objects = ShopCartManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'shopcart'

    def empty_shopcart(self):
        is_empty = False
        self.shopCartItems.clear()
        if self.shopCartItems.count() == 0:
            is_empty = True
        return is_empty


# calculates shopcart subtotal on m2m change
def m2m_changed_shopcart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        shopcart_items = instance.shopCartItems.all().select_related('productID')# may need optimizing
        subtotal = 0
        for item in shopcart_items:# may need optimizing
            subtotal += item.productID.productSalePrice
        instance.shopCartSubTotal = subtotal
        instance.save()
m2m_changed.connect(m2m_changed_shopcart_receiver, sender=ShopCart.shopCartItems.through)
