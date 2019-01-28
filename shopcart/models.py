from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save, m2m_changed
from purchases.models import PurchaseItems

User = settings.AUTH_USER_MODEL
# Create your models here.

class ShopCartManager(models.Manager):

    def get_or_new(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_obj = True
            cart_obj = ShopCart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class ShopCart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    shopCartDateCreated = models.DateTimeField(auto_now_add=True)
    shopCartLastModified = models.DateTimeField(auto_now=True)

    # ShopCart Statuses
    OPEN, SAVED, FROZEN, SUBMITTED = ("Open", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN, _("Open - currently active")),
        (SAVED, _("Saved - for items to be purchased later")),
        (FROZEN, _("Frozen - the basket cannot be modified")),
        (SUBMITTED, _("Submitted - has been ordered at the checkout")),
    )
    shopCartStatus = models.CharField(max_length=40, default=OPEN, choices=STATUS_CHOICES)

    shopCartDiscount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shopCartSubTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    shopCartItems = models.ManyToManyField(PurchaseItems, blank=True)
    objects = ShopCartManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'shopcart'

def pre_save_shopcart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        shopcart_items = instance.shopCartItems.all().select_related('productID')
        subtotal = 0
        for item in shopcart_items:
            subtotal += item.productID.pricing_set.first().pricingBasePrice
        instance.shopCartSubTotal = subtotal
        instance.save()
m2m_changed.connect(pre_save_shopcart_receiver, sender=ShopCart.shopCartItems.through)