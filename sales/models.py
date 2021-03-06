import decimal
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from speedtest.utils import unique_sale_id_generator
from purchases.models import PurchaseItems
from shopcart.models import ShopCart
from billing.models import BillingProfile, Card
from addresses.models import Address
from pricing.models import SDiscount
from tax.models import Jurisdiction

class CustomerShipMethod(models.Model):
    cSMID = models.AutoField(primary_key=True)
    cSMName = models.CharField(max_length=120)
    cSMDescription = models.TextField(max_length=200)
    cSMChargeAmount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'customer_ship_method'

    def __str__(self):
        return self.cSMName

class SaleManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = None
        cart_items = cart_obj.shopCartItems.all()
        qs = self.get_queryset().filter(
            saleStatus='created',
            saleBillingProfile=billing_profile,
            # saleItems__prodStockID=cart_items.first().prodStockID
        )
        if qs.count() == 1:
            obj = qs.first()
            # sale_items = obj.saleItems.all()

            # # check if cart_items and saleitems are still avail
            # for item in sale_items:
                # #check
                # if item.piIsAvailable == False:
                    # sale_item_qs = SaleItems.objects.filter(
                        # prodStockID=item.prodStockID,
                        # saleID=obj.saleID
                    # )
                    # # if unavailable item, remove from sale
                    # if sale_item_qs.count() == 1:
                        # sale_item_qs.delete()

            # update sale from cart
            obj.update_sale_from_cart(cart_items)
            return obj, created

        elif qs.count() > 1:
            #multiple sales in created status
            pass


        else: # its a new order so make it and return it
            created = True
            obj = Sale(
                saleBillingProfile=billing_profile,
                saleStatus='created',
                saleNote='default sale note',
            )
            obj.save()

            obj.update_sale_from_cart(cart_items)
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
    saleTaxAmount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    # change: add saleShippingMethod
    customerShipMethodID = models.ForeignKey(CustomerShipMethod, on_delete=models.PROTECT, null=True, blank=True)
    # customer shipping and total
    saleShipCostAmountCharged = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: integrate shipping API
    # saleCustomerTotal - not inclusive of shipping cost that we are paying

    # actual total
    saleTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    # saleTotalShippingCost - total shipping cost including portion we are paying

    saleShippingAddress = models.ForeignKey(Address, related_name='saleShippingAddress', null=True, blank=True, on_delete=models.PROTECT)
    saleBillingAddress = models.ForeignKey(Address, related_name='saleBillingAddress', null=True, blank=True, on_delete=models.PROTECT)
    saleDiscounts = models.ManyToManyField(SDiscount, blank=True)
    saleItems = models.ManyToManyField(PurchaseItems, through='SaleItems')
    saleBillingProfile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    salePaymentCard = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True)

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
            self.saleTaxAmount = self.get_tax_amount()
            self.saleTotal = self.get_total()
        super(Sale, self).save(*args, **kwargs)

    def check_done(self):
        """ checks if sale has all info necessary """
        billing_profile = self.saleBillingProfile
        shipping_address = self.saleShippingAddress
        billing_address = self.saleBillingAddress
        sub_total = self.saleSubTotal
        total = self.saleTotal
        card = self.salePaymentCard
        cust_ship_method = self.customerShipMethodID

        if billing_profile and card and cust_ship_method and shipping_address and billing_address and sub_total > 0 and total > 0:
            return True
        return False

    def mark_paid(self):
        """ marks the sale paid """
        if self.check_done():
            self.saleStatus = 'payed'
            self.save()
            # set saleItems to unavailable
            sale_items = self.saleItems.all()
            for item in sale_items:
                item.piIsAvailable = False
                item.save()
        return self.saleStatus

    # calculates total based on present values.
    def get_total(self):
        total = decimal.Decimal("0.00")
        sub_total = self.saleSubTotal
        sale_discount_amount = self.saleDiscountAmount
        sale_shipping_charged = self.saleShipCostAmountCharged
        sale_tax_amount = self.saleTaxAmount
        # add saleDiscount calculation
        total = sub_total - sale_discount_amount + sale_shipping_charged + sale_tax_amount # + remaining shipping cost
        return total

    def get_sub_total(self):
        items = self.saleItems.all()
        sub_total = decimal.Decimal("0.00")
        # calculates sub_total 
        # if saleitem count is more than 0
        for item in items:
            sub_total += item.productID.productSalePrice
        self.saleSubTotal = sub_total
        # add saleDiscount calculation
        return sub_total

    def get_discount_amount(self):
        # get discount obj
        amount = decimal.Decimal("0.00")

        s_discounts = self.saleDiscounts.filter(
            sDiscountIsShippingDiscount=False,
            sDiscountIsActive=True,
        ).all()

        # if saleitem count is more than 0
        for discount in s_discounts:
            # get discount value or multiplier
            discount_value, is_multiplier = discount.get_active_sdiscount_amount_or_multiplier()

            # if percentage discount
            if is_multiplier:
                # add subTotal * discount_multiplier
                amount += self.saleSubTotal * discount_value
            # if decimal discount 
            else:
                amount += discount_value
        return amount

    def get_shipping_ammount(self):
        # get discount obj
        ship_amount = decimal.Decimal("0.00")
        ship_discount_amount = decimal.Decimal("0.00")
        
        # get ship_amount
            # EASPOST HERE change: 
        if self.customerShipMethodID:
            ship_amount = self.customerShipMethodID.cSMChargeAmount
        else:
            ship_amount = decimal.Decimal("7.00")

        

        # get shipping discounts
        ship_discounts = self.saleDiscounts.filter(
            sDiscountIsShippingDiscount=True,
            sDiscountIsActive=True,
            ).all()

        for discount in ship_discounts:
            # get discount value or multiplier
            discount_value, is_multiplier = discount.get_active_sdiscount_amount_or_multiplier()

            # if percentage discount
            if is_multiplier:
                # add subTotal * discount_multiplier
                ship_discount_amount += ship_amount * discount_value
            # if decimal discount 
            else:
                ship_discount_amount += discount_value

        # add discount
        ship_amount = ship_amount - ship_discount_amount
        return ship_amount


    # get tax amount
    def get_tax_amount(self):
        tax_amount = decimal.Decimal("0.00")
        # get jurisdiction
        jurisdiction_obj = self.get_jurisdiction()
        # jurisdiction_obj, jurisdiction_exists = self.get_jurisdiction()
        if jurisdiction_obj is not None:
            # call calc_tax
            tax_multiplier, tax_rate_exists = jurisdiction_obj.calc_tax()
            if tax_rate_exists:
                tax_amount = (self.saleSubTotal - self.saleDiscountAmount) * tax_multiplier
        # call get_tax on jurisdiction
        return tax_amount

    # get jurisdiction of sale
    def get_jurisdiction(self):
        # initialize vars
        jurisdiction_obj = None
        # jurisdiction_exists = False
        # get address stuff
        shipping_address_obj = self.saleShippingAddress
        # pull out city, state, zip
        if shipping_address_obj is not None:
            shipping_city = shipping_address_obj.addressCity
            shipping_state = shipping_address_obj.addressState
            shipping_zip = shipping_address_obj.addressPostalCode
            # Find jurisdiction
            jurisdiction_qs = Jurisdiction.objects.filter(
                jurisdictionState=shipping_state,
                jurisdictionCity=shipping_city,
                jurisdictionZip=shipping_zip,
                taxrate__taxRateIsActive=True,
            )

            # if no jurisdiction
            if jurisdiction_qs.count() == 0:
                # query only using state city
                jurisdiction_qs = Jurisdiction.objects.filter(
                    jurisdictionState=shipping_state,
                    jurisdictionCity=shipping_city,
                    taxrate__taxRateIsActive=True,
                )
                if jurisdiction_qs.count() == 0:
                    # query using only state
                    jurisdiction_qs = Jurisdiction.objects.filter(
                        jurisdictionState=shipping_state,
                        taxrate__taxRateIsActive=True,
                    )
                    if jurisdiction_qs.count() == 0:
                        return jurisdiction_obj# , jurisdiction_exists
            # # if jurisdiction in db
            if jurisdiction_qs.count() == 1:
                # return 
                jurisdiction_obj = jurisdiction_qs.first()
                # collecting = True
                jurisdiction_exists = True
                return jurisdiction_obj# , jurisdiction_exists
            # if no tax rates for the jurisdiction
            if jurisdiction_qs.count() > 1:
                pass

    def update_sale_from_cart(self, cart_items):
        """ clears saleitems and salediscounts, re-adds items passed in cart_items if available, and re-applies automatic discounts """
        # clear sale items
        self.saleDiscounts.clear()
        self.saleItems.clear()
        # re add items from cart
        for item in cart_items:
            # check if item available
            if item.piIsAvailable:
                SaleItems.objects.create(
                    saleID=self,
                    prodStockID=item,
                    siBasePrice=item.productID.productBasePrice,
                    siDiscountAmount=item.productID.productDiscountAmount,
                    siSalePrice=item.productID.productSalePrice,
                    siNote=item.productID.productName
                    )
            else:
                #item unavailable, attempt to add identical from stock
                pass
        #save to recalc sale totals
        self.save()
        # update auto discounts
        self.apply_auto_discounts()
        return True

    def apply_auto_discounts(self):
        # check for automatic discounts
        auto_sdiscounts_qs = SDiscount.objects.filter(
            sDiscountAutomatic=True,
            sDiscountIsActive=True,
        )
        if auto_sdiscounts_qs.exists():
            for sdiscount in auto_sdiscounts_qs:
                discount_conditions_met, reason = self.check_discount_conditions(sdiscount)
                # if conditions met then apply discount (create many to many)
                if discount_conditions_met:
                    self.saleDiscounts.add(sdiscount)
        return True

    def check_discount_conditions(self, discount):
        # get discount_obj
        discount_obj = discount
        # get sale_items
        sale_items = self.saleItems.all()
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
            # num_required
            num_required = condition.sDCNumRequired
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
                                if category.categoryName == condition_value:
                                    is_met_counter += 1
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
                        if is_met_counter >= num_required:
                            is_met_super_counter += 1
                            reason = ''
            # if type == 'User'
                # do stuff
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
