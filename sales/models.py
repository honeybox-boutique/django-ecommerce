import decimal
from django.db import models
from django.db.models.signals import pre_save, post_save

from speedtest.utils import unique_sale_id_generator
from purchases.models import PurchaseItems
from shopcart.models import ShopCart
from billing.models import BillingProfile
from addresses.models import Address

class SaleManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = None
        cart_items = cart_obj.shopCartItems.all()
        available = True
        # if cart has 
        for item in cart_items:
            if item.piIsAvailable == False:# wrong, need to check if there is sale
                print('getting new sale')
                # change: logic error here or where the cart is
                # its not new, query for it and return it   
                available = False
        if not available:
            qs = self.get_queryset().filter(
                            saleBillingProfile=billing_profile,
                            saleItems__prodStockID=cart_items.first().prodStockID
            )
            if qs.count() == 1:
                obj = qs.first()
                print('queried for')
                print(obj)
                print(obj.saleSubTotal)
                return obj, created
            if qs.count() == 0:
                print('no sale,')
                
        #cart already used, checkout not finished
        else: # its a new order so make it and return it
            print('model manager creating new sale')
            created = True
            obj = Sale(
                        saleBillingProfile=billing_profile,
                        saleStatus='created',
                        saleNote='default sale note',
                        # saleSubTotal= # calc in post_save
                        # saleDiscountAmount = # in post_save
                        # saleSalesTaxAmount = # in post_save
                        # saleShipCostAmountCharged = # calc in post_save
                        # saleTotal= # calc in post_save 
            )
            obj.save(created)
            # add cart_items to sale
            for item in cart_items:
                # change: maybe add checking logic to make sure pricing is active, prodStockItems don't haven't been sold, etc.
                new_sale_item = SaleItems(
                                saleID=obj,
                                prodStockID=item,
                                siBasePrice=item.productID.productBasePrice,
                                siDiscountAmount=item.productID.productDiscountAmount,
                                siSalePrice=item.productID.productSalePrice,
                                siNote=item.productID.productName
                            )
                new_sale_item.save()
                # set piIsAvailable to False
                item.piIsAvailable = False
                item.save()
            print('created: ')
            print(obj)
            return obj, created

class Sale(models.Model):
    SALE_STATUS_CHOICES = (
        ('created', 'Order created and being processed'),
        ('payed', 'Order payment completed and shipment being prepared'),
        ('shipped', 'Order has been shipped'),
        ('returned', 'Order was returned and has been received. Refunds will be issued upon approval'),
        ('refunded', 'Return was accepted and appropriate refunds have been applied'),
    )
    saleID = models.AutoField(primary_key=True)
    saleStringID = models.CharField(max_length=120, blank=True)
    saleDate = models.DateTimeField('sale date', auto_now_add=True)
    saleNote = models.CharField(max_length=120, default='Sale')
    saleShippingAddress = models.ForeignKey(Address, related_name='saleShippingAddress', null=True, blank=True, on_delete=models.PROTECT)
    saleBillingAddress = models.ForeignKey(Address, related_name='saleBillingAddress', null=True, blank=True, on_delete=models.PROTECT)
    saleStatus = models.CharField(max_length=120, default='created', choices=SALE_STATUS_CHOICES) # purchaseDate = models.DateTimeField('date purchased')
    saleSubTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# Amount should be sum(saleitemprice - p-cDiscount)
    # saleDiscount = many to many
    # saleDiscountAmount = ? actual calculated discount amount
    # saleSalesTaxAmount = ? # change: add logic for sales tax calculation
    saleShipCostAmountCharged = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: integrate shipping API
    saleTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: generate total from other fields

    saleItems = models.ManyToManyField(PurchaseItems, through='SaleItems')
    saleBillingProfile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)

    objects = SaleManager()

    class Meta:
        db_table = 'sale'

    def __str__(self):
        return self.saleStringID
    
    def save(self, *args, **kwargs):
        if self.saleID is not None:
            # call calculated field methods here
            self.saleSubTotal = self.get_sub_total()
            self.saleTotal = self.get_total()
        super(Sale, self).save(*args, **kwargs)
    
    def check_done(self):
        billing_profile = self.saleBillingProfile
        shipping_address = self.saleShippingAddress
        billing_address = self.saleBillingAddress
        sub_total = self.saleSubTotal
        total = self.saleTotal

        if billing_profile and shipping_address and billing_address and sub_total > 0 and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.saleStatus = 'payed'
            self.save()
        return self.saleStatus

    # calculates total based on present values. if ANY null return error?
    def get_total(self):
        print('getting total')
        total = decimal.Decimal("0.00")
        sub_total = self.saleSubTotal
        # add saleDiscount calculation
        total = sub_total# - sale_discount_amount + sale_shipping_charged + sale_tax_amount
        print(total)
        return total

    def get_sub_total(self):
        print('updating subtotal')
        items = self.saleItems.all()
        sub_total = decimal.Decimal("0.00")
        # calculates sub_total 
        # if saleitem count is more than 0
        for item in items:
            sub_total += item.productID.productSalePrice
        self.shopCartSubTotal = sub_total
        # add saleDiscount calculation
        print('saving subtotal: ', sub_total)
        return sub_total

    # def get_discount_amount(self):
        # # get discount obj
        # # s_discount_obj = self.saleDiscount
        # # check that sale meets conditions
            # #if met, get saleDiscountAmount

        # sub_total = 0
        # # calculates sub_total 
        # # if saleitem count is more than 0
        # if items.count() > 0:
            # for item in items:
                # subtotal += item.productID.productSalePrice
            # self.shopCartSubTotal = sub_total
            # # add saleDiscount calculation
            # self.save()
            # return sub_total

class SaleItems(models.Model):
    saleItemID = models.AutoField(primary_key=True)
    siBasePrice = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    siDiscountAmount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    siSalePrice = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: add sensor to calculate this
    siNote = models.CharField(default='SaleItem', max_length=120, blank=True)# change: add sensor to populate this

    saleID = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prodStockID = models.ForeignKey(PurchaseItems, on_delete=models.PROTECT)

    class Meta:
        db_table = 'sale_items'

    def __str__(self):
        return self.siNote

def pre_save_create_sale_id(sender, instance, *args, **kwargs):
    if not instance.saleStringID:
        instance.saleStringID = unique_sale_id_generator(instance)
pre_save.connect(pre_save_create_sale_id, sender=Sale)

# Change: maybe remove this as can't use signals to get calc field values for same model
# Might be used to call instance.get_final_total and retrieve all the calculated fields
# def post_save_sale(sender, instance, created, *args, **kwargs):
    # if instance.saleStatus == 'created':# already creatd once, get shipping cost
        # print('post save worked')
        # instance.saleSubTotal = instance.get_sub_total()
        # instance.saleTotal = instance.get_total()
        # # add instnace.update_sale_discount()
        # # if instance.saleStatus == 'payed':# already payed, probably do nothing, maybe do some ashley stuff
            # # pass
            # # calc shipping if billing, shipping, and shipmethod are null
            # #if instance.saleShippingAddress and instance.saleBillingAddress and instance.saleShipMethod:
                # # call calcShipping
            # # calc tax if shipcharged is already there
            # # if both addresses, shipMethod, and ship charged are not null: calc tax
                # # sale_tax_amount = ?
            # # calc total if everything is there
            # # if everything is ready, calculate total
    # # if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        # # add saleDiscount calculation
# post_save.connect(post_save_sale, sender=Sale)
