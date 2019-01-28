from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from purchases.models import PurchaseItems

User = settings.AUTH_USER_MODEL
# Create your models here.

class ShopCartManager(models.Manager):

    def get_or_new(self, request):
        shopcart_id = request.session.get('shopcart_id', None)
        qs = self.get_queryset().filter(id=shopcart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_obj = True
            cart_obj = ShopCart.objects.new_cart(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

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

# class ShopCartItems(models.Model):
    # shopCartItemID = models.AutoField(primary_key=True)

    # shopCartID = models.ForeignKey(ShopCart, on_delete=models.PROTECT)
    # prodStockID = models.ForeignKey(PurchaseItems, on_delete=models.PROTECT)

    # def __str__(self):
        # return str(self.id)

    # class Meta:
        # db_table = 'shopcart_items'
