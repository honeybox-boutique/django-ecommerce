from django.db import models
from django.db.models.signals import pre_save, post_save

from speedtest.utils import unique_sale_id_generator
from purchases.models import PurchaseItems
from shopcart.models import ShopCart


class Sale(models.Model):
    SALE_STATUS_CHOICES = (
        ('created', 'Order created and being processed'),
        ('payed', 'Order payment completed and shipment being prepared'),
        ('shipped', 'Order has been shipped'),
        ('returned', 'Order was returned and has been received. Refunds will be issued upon approval'), 
        ('refunded', 'Return was accepted and appropriate refunds have been applied'),
    ) 
    saleID = models.AutoField(primary_key=True)
    saleStringID = models.CharField(max_length=120, blank=True)# change: add sensor to generate this
    saleDate = models.DateTimeField('sale date', auto_now_add=True)
    saleNote = models.CharField(max_length=120, default='Sale')
    # billingProfile = ?
    # shippingAddress = ?
    # billingAddress = ?
    saleStatus = models.CharField(max_length=120, default='created', choices=SALE_STATUS_CHOICES) # purchaseDate = models.DateTimeField('date purchased')
    saleSubTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# Amount should be sum(saleitemprice - p-cDiscount)
    # saleDiscountAmount = ? # change: determine if value appropriate: only sale-level discount amount, doesn't include p or c discount
    # saleSalesTaxAmount = ? # change: add logic for sales tax calculation
    saleShipCostAmountCharged = models.DecimalField(default=7.00, max_digits=12, decimal_places=2)# change: integrate shipping API
    saleTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: generate total from other fields

    saleItems = models.ManyToManyField(PurchaseItems, through='SaleItems')

    class Meta:
        db_table = 'sale'

    def __str__(self):
        return self.saleStringID
    
    # Should probably be in model manager?
    # Computes final order total
    def get_final_total(self, request):
        cart_obj, new_obj = ShopCart.objects.get_or_new(request)
        # if new_obj? return you have nothing in cart?
        cart_sub_total = cart_obj.shopCartSubTotal
        # sale_discount_amount = ?
        # sale_tax_amount = ?
        # shipping_charged = ?
        # new_sale_total = cart_sub_total - sale_discount_amount + sale_tax_amount + sale_shipping_charged
        # self.saleTotal = new_sale_total
        # self.save()
        # return new_sale_total
        return cart_sub_total

# Example add many to many relationship

# m1 = Membership(person=ringo, group=beatles,
# ...     date_joined=date(1962, 8, 16),
# ...     invite_reason="Needed a new drummer.")
# >>> m1.save()

class SaleItems(models.Model):
    saleItemID = models.AutoField(primary_key=True)
    siBasePrice = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    siDiscountAmount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    # siSalePrice = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: add sensor to calculate this
    siNote = models.CharField(default='SaleItem', max_length=120, blank=True)# change: add sensor to populate this

    saleID = models.ForeignKey(Sale, on_delete=models.PROTECT)
    prodStockID = models.ForeignKey(PurchaseItems, on_delete=models.PROTECT)

    class Meta:
        db_table = 'sale_items'

    def __str__(self):
        return self.siNote

def pre_save_create_sale_id(sender, instance, *args, **kwargs):
    if not instance.saleStringID:
        instance.saleStringID = unique_sale_id_generator(instance)
pre_save.connect(pre_save_create_sale_id, sender=Sale)

# Might be used to call instance.get_final_total and retrieve all the calculated fields
# def post_save_sale(sender, instance, created, *args, **kwargs):
    # if created:# if order just created
        # # do stuff
        # pass
# post_save.connect(post_save_sale, sender=Sale)