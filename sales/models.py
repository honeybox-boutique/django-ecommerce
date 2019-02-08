import decimal
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from speedtest.utils import unique_sale_id_generator
from purchases.models import PurchaseItems
from shopcart.models import ShopCart
from billing.models import BillingProfile
from addresses.models import Address
from pricing.models import SDiscount


class SaleManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = None
        cart_items = cart_obj.shopCartItems.all()
        available = True
        # if cart has 
        for item in cart_items:
            if not item.piIsAvailable:
                available = False
        if not available:
            qs = self.get_queryset().filter(
                saleStatus='created',
                saleBillingProfile=billing_profile,
                saleItems__prodStockID=cart_items.first().prodStockID
            )
            if qs.count() == 1:
                obj = qs.first()
                # change:  maybe add if cart not submitted
                if cart_items.count() != obj.saleItems.count():
                    print('clearing items from sale')
                    print('clearing discounts')
                    # clear sale items
                    obj.saleDiscounts.clear()
                    obj.saleItems.clear()# change: this causes saletotals to be recalced. Maybe rethink to improve performance
                    # re add items from cart
                    for item in cart_items:
                        SaleItems.objects.create(
                            saleID=obj,
                            prodStockID=item,
                            siBasePrice=item.productID.productBasePrice,
                            siDiscountAmount=item.productID.productDiscountAmount,
                            siSalePrice=item.productID.productSalePrice,
                            siNote=item.productID.productName
                            )
                        item.piIsAvailable = False
                        item.save()
                    #save to recalc
                    obj.save()
                # check for automatic discounts
                auto_sdiscounts_qs = SDiscount.objects.filter(
                    sDiscountAutomatic=True,
                    sDiscountIsActive=True,
                )
                if auto_sdiscounts_qs.exists():
                    for sdiscount in auto_sdiscounts_qs:
                        discount_conditions_met, reason = obj.check_discount_conditions(sdiscount)
                        # if conditions met then apply discount (create many to many)
                        if discount_conditions_met:
                            obj.saleDiscounts.add(sdiscount)
                            print('auto-added a discount')
                print(obj)
                return obj, created

            elif qs.count() == 0:
                print('no sale,')

        #cart already used, checkout not finished
        else: # its a new order so make it and return it
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
            obj.save()

            # add cart_items to sale
            for item in cart_items:
                SaleItems.objects.create(
                    saleID=obj,
                    prodStockID=item,
                    siBasePrice=item.productID.productBasePrice,
                    siDiscountAmount=item.productID.productDiscountAmount,
                    siSalePrice=item.productID.productSalePrice,
                    siNote=item.productID.productName
                    )
                item.piIsAvailable = False
                item.save()
            obj.save()
            print('num items in sale', obj.saleItems.count())
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
    saleStatus = models.CharField(max_length=120, default='created', choices=SALE_STATUS_CHOICES) # purchaseDate = models.DateTimeField('date purchased')
    saleSubTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# Amount should be sum(saleitemprice - p-cDiscount)
    saleDiscountAmount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    # saleShipDiscountAmount = ? # change: should this be a thing? currently no way to tell free shipping as it isn't included in discountamount
    # saleSalesTaxAmount = ? # change: add logic for sales tax calculation
    saleShipCostAmountCharged = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: integrate shipping API
    saleTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: generate total from other fields

    saleShippingAddress = models.ForeignKey(Address, related_name='saleShippingAddress', null=True, blank=True, on_delete=models.PROTECT)
    saleBillingAddress = models.ForeignKey(Address, related_name='saleBillingAddress', null=True, blank=True, on_delete=models.PROTECT)
    saleDiscounts = models.ManyToManyField(SDiscount)
    saleItems = models.ManyToManyField(PurchaseItems, through='SaleItems')
    saleBillingProfile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)

    objects = SaleManager()

    class Meta:
        db_table = 'sale'

    def __str__(self):
        return self.saleStringID

    def save(self, *args, **kwargs):
        if self.saleID is not None and self.saleStatus == 'created':
            # call calculated field methods here
            self.saleSubTotal = self.get_sub_total()
            self.saleDiscountAmount = self.get_discount_amount()
            self.saleShipCostAmountCharged = self.get_shipping_ammount()
            self.saleTotal = self.get_total()
        super(Sale, self).save(*args, **kwargs)

    def check_done(self):
        """ checks if sale has all info necessary """
        billing_profile = self.saleBillingProfile
        shipping_address = self.saleShippingAddress
        billing_address = self.saleBillingAddress
        sub_total = self.saleSubTotal
        total = self.saleTotal

        if billing_profile and shipping_address and billing_address and sub_total > 0 and total > 0:
            return True
        return False

    def mark_paid(self):
        """ marks the sale paid """
        print('marking paid')
        if self.check_done():
            self.saleStatus = 'payed'
            self.save()
        return self.saleStatus

    # calculates total based on present values. if ANY null return error?
    def get_total(self):
        print('getting total')
        total = decimal.Decimal("0.00")
        sub_total = self.saleSubTotal
        sale_discount_amount = self.saleDiscountAmount
        # add saleDiscount calculation
        total = sub_total - sale_discount_amount# + sale_shipping_charged + sale_tax_amount
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
        self.saleSubTotal = sub_total
        # add saleDiscount calculation
        print('saving subtotal: ', sub_total)
        return sub_total

    def get_discount_amount(self):
        # get discount obj
        print('updating discount')
        amount = decimal.Decimal("0.00")
        s_discounts = self.saleDiscounts.filter(sDiscountIsShippingDiscount=False,
                                                sDiscountIsActive=True,
                                            ).all()

        # if saleitem count is more than 0
        for discount in s_discounts:
            # get discount value or multiplier
            discount_value, is_multiplier = discount.get_active_sdiscount_amount_or_multiplier()
            print('discount value: ', discount_value)

            # if percentage discount
            if is_multiplier:
                # add subTotal * discount_multiplier
                amount += self.saleSubTotal * discount_value
            # if decimal discount 
            else:
                amount += discount_value
        print('saving discount: ', amount)
        return amount

    def get_shipping_ammount(self):
        # get discount obj
        print('updating shipping')
        ship_amount = decimal.Decimal("0.00")
        ship_discount_amount = decimal.Decimal("0.00")
        
        # get ship_amount
            # EASPOST HERE change: 
        ship_amount = decimal.Decimal("7.00")

        # get shipping discounts
        ship_discounts = self.saleDiscounts.filter(
            sDiscountIsShippingDiscount=True,
            sDiscountIsActive=True,
            ).all()

        for discount in ship_discounts:
            # get discount value or multiplier
            discount_value, is_multiplier = discount.get_active_sdiscount_amount_or_multiplier()
            print('shipping discount value: ', discount_value)

            # if percentage discount
            if is_multiplier:
                # add subTotal * discount_multiplier
                ship_discount_amount += ship_amount * discount_value
            # if decimal discount 
            else:
                ship_discount_amount += discount_value

        # add discount
        ship_amount = ship_amount - ship_discount_amount
        print('saving shipamount: ', ship_amount)
        return ship_amount

    def check_discount_conditions(self, discount):
        print('checking discount conditions')
        # get discount_obj
        discount_obj = discount
        # get sale_items
        sale_items = self.saleItems.all()
        print('num saleitems: ', sale_items.count())
        # get discount_conditions
        discount_conditions = discount_obj.sdiscountcondition_set.all()
        num_discount_conditions = discount_conditions.count()
        is_met = False
        reason = ''
        is_met_super_counter = 0

        # for each condition
        for condition in discount_conditions:
            # type
            condition_type = condition.sDCType
            # field_name
            field_name = condition.sDCFieldName
            # compare_operator
            compare_operator = condition.sDCCompareOperator
            # value
            condition_value = condition.sDCValue
            print('Condition Value: ', condition_value)
            # num_required
            num_required = condition.sDCNumRequired
            print('Number items required to meet condition: ', num_required)
            reason = condition.sDCFailMessage
            if condition_type == 'Sale':
                if field_name == 'saleSubTotal':
                    # convert value to decimal
                    value_decimal = decimal.Decimal(condition_value.strip(' "'))
                    if compare_operator == 'equal_to':
                        if self.saleSubTotal == value_decimal:
                            is_met_super_counter += 1
                            reason = ''
                    if compare_operator == 'greater_than':
                        if self.saleSubTotal >= value_decimal:
                            is_met_super_counter += 1
                            reason = ''
                    if compare_operator == 'less_than':
                        if self.saleSubTotal <= value_decimal:
                            is_met_super_counter += 1
                            reason = ''
            if condition_type == 'Item':
                if field_name == 'productCategories':
                    if compare_operator == 'equal_to':
                        is_met_counter = 0
                        for item in sale_items:
                            # get categories
                            item_categories = item.productID.productCategories.all()
                            for category in item_categories:
                                print(category.categoryName)
                                if category.categoryName == condition_value:
                                    is_met_counter += 1
                                    print('met condition')
                        print('items that met condition: ', is_met_counter)
                        if is_met_counter >= num_required:
                            is_met_super_counter += 1
                            reason = ''

                if field_name == 'productName':
                    if compare_operator == 'equal_to':
                        is_met_counter = 0
                        for item in sale_items:
                            # get categories
                            if item.productID == condition_value:
                                is_met_counter += 1
                                print('met condition')
                        print('items that met condition: ', is_met_counter)
                        if is_met_counter >= num_required:
                            is_met_super_counter += 1
                            reason = ''
            # if type == 'User'
                # do stuff
        print('conditions met | total conditions')
        print(is_met_super_counter, num_discount_conditions)
        if is_met_super_counter == num_discount_conditions:
            is_met = True
        return is_met, reason

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

def m2m_changed_sale_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        instance.save()# save sale to trigger calc field calcs
m2m_changed.connect(m2m_changed_sale_receiver, sender=Sale.saleItems.through)

def m2m_changed_discount_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        instance.save()# save sale to trigger calc field calcs
m2m_changed.connect(m2m_changed_sale_receiver, sender=Sale.saleDiscounts.through)

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
