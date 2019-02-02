from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from products.models import Product, Category

# Create your models here.

class Pricing(models.Model):
    pricingID = models.AutoField(primary_key=True)
    pricingBasePrice = models.DecimalField(max_digits=12, decimal_places=2)
    pricingDateCreated = models.DateTimeField('date created', auto_now_add=True)
    pricingValidFrom = models.DateTimeField('start date')
    pricingValidUntil = models.DateTimeField('end date')
    pricingNote = models.TextField(max_length=200)
    pricingIsActive = models.BooleanField(default=False)

    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pricing'

    def __str__(self):
        return self.pricingNote

def pre_save_pricing_active(sender, instance, *args, **kwargs):
    current_time = timezone.now()
    # check if timezone.now is between start and endate of instance
    print("checking if pricing active")
    if instance.pricingValidFrom < current_time < instance.pricingValidUntil: 
        # change: check if product has other active pricings
        # if has other active pricings then don't save and return error "already active pricing"
        #set active
        instance.pricingIsActive = True
    else:
        # set not active
        instance.pricingIsActive = False
pre_save.connect(pre_save_pricing_active, sender=Pricing)

class PDiscountQuerySet(models.QuerySet):
    # Available on both Manager and QuerySet.
    def get_largest_active(self, request):
        largest_discount = 0
        product_slug = request.kwargs['productSlug']
        qs = self.filter(pDiscountIsActive=True, productID__productSlug__iexact=product_slug)# .order_by('pDiscount')
        print(qs.count())
        if qs.count() == 0:
            print('no active discounts')
        elif qs.count() == 1:
            print('getting ONLY active discount')
            # get first and return it
            largest_discount = qs.first().get_active_discount_amount(self)
        else:
            print('getting largest of multiple')
            discount_amount = 0
            for item in qs.all():
                print(item)
                # get item discount amount
                new_discount_amount = item.get_active_discount_amount(self)
                print(new_discount_amount)
                # check if bigger than discount_amount
                if new_discount_amount > discount_amount:
                    # assign to discount_amount
                    discount_amount = new_discount_amount
            # get largest and return
            largest_discount = discount_amount
            # print(largest_discount)
        return largest_discount

class PDiscount(models.Model):
    pDiscountID = models.AutoField(primary_key=True)
    pDiscountName = models.CharField(max_length=40)
    pDiscountDescription = models.TextField(max_length=200)
    pDiscountType = models.CharField(max_length=30)# change: add choices for percent and decimal
    pDiscountValue = models.DecimalField(max_digits=12, decimal_places=2)
    pDiscountDateCreated = models.DateTimeField('date created', auto_now_add=True)
    pDiscountDateValidFrom = models.DateTimeField('valid from')
    pDiscountDateValidUntil = models.DateTimeField('valid until')
    pDiscountCouponCode = models.CharField(max_length=20)
    pDiscountMaxDiscount = models.DecimalField(max_digits=12, decimal_places=2)
    pDiscountMinOrderValue = models.DecimalField(max_digits=12, decimal_places=2)
    pDiscountIsActive = models.BooleanField(default=False)

    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    largestActive = PDiscountQuerySet.as_manager()
    class Meta:
        db_table = 'pdiscount'

    def __str__(self):
        return self.pDiscountName

    def get_active_discount_amount(self, request):
        print('getting discount amount from pdiscounts')
        discount_type = self.pDiscountType
        discount_value = self.pDiscountValue
        product_base_price = self.productID.pricing_set.filter(pricingIsActive=True).first().pricingBasePrice
        discount_amount = 0
        #if decimal
        if discount_type == 'Decimal':
            # return discount_value
            discount_amount = discount_value
        #if percent
        elif discount_type == 'Percent':
            # return discount_value
            discount_amount = (product_base_price * (discount_value / 100))
        return discount_amount

def pre_save_pdiscount_active(sender, instance, *args, **kwargs):
    current_time = timezone.now()
    # check if timezone.now is between start and endate of instance
    print("checking if pricing active")
    if instance.pDiscountDateValidFrom < current_time < instance.pDiscountDateValidUntil: 
        # change: check if product has other active discounts
        # if has other active pricings then don't save and return error "already active pricing"
        print('set active')
        instance.pDiscountIsActive = True
    else:
        print('set inactive')
        # set not active
        instance.pDiscountIsActive = False
pre_save.connect(pre_save_pdiscount_active, sender=PDiscount)

class CDiscount(models.Model):
    cDiscountID = models.AutoField(primary_key=True)
    cDiscountName = models.CharField(max_length=40)
    cDiscountDescription = models.TextField(max_length=200)
    cDiscountType = models.CharField(max_length=30)
    cDiscountValue = models.DecimalField(max_digits=12, decimal_places=2)
    cDiscountDateCreated = models.DateTimeField('date created', auto_now_add=True)
    cDiscountDateValidFrom = models.DateTimeField('valid from')
    cDiscountDateValidUntil = models.DateTimeField('valid until')
    cDiscountCouponCode = models.CharField(max_length=20)
    cDiscountMaxDiscount = models.DecimalField(max_digits=12, decimal_places=2)
    cDiscountMinOrderValue = models.DecimalField(max_digits=12, decimal_places=2)
    cDiscountIsActive = models.BooleanField(default=False)

    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cdiscount'

    def __str__(self):
        return self.cDiscountName

    def get_active_cdiscount_amount_or_multiplier(self, request):
        """ Returns discount_returned, the discount amount or multiplier """
        if self.cDiscountIsActive:
            print('getting discount amount from cdiscounts')
            discount_type = self.cDiscountType
            discount_value = self.cDiscountValue
            is_multiplier = False
            discount_returned = 0# amount or multiplier to return
            #if decimal
            if discount_type == 'Decimal':
                # return discount_value
                discount_returned = discount_value
            #if percent
            elif discount_type == 'Percent':
                is_multiplier = True
                # change: add logic to get category value
                discount_returned = discount_value / 100
            return discount_returned, is_multiplier
        else:
            print('not active')

def pre_save_cdiscount_active(sender, instance, *args, **kwargs):
    current_time = timezone.now()
    # check if timezone.now is between start and endate of instance
    print("checking if cdiscount active")
    if instance.cDiscountDateValidFrom < current_time < instance.cDiscountDateValidUntil: 
        # change: check if product has other active discounts
        # if has other active pricings then don't save and return error "already active pricing"
        print('set active')
        instance.cDiscountIsActive = True
    else:
        print('set inactive')
        # set not active
        instance.cDiscountIsActive = False
pre_save.connect(pre_save_cdiscount_active, sender=CDiscount)

# class TDiscount(models.Model):
    # tDiscountID = models.AutoField(primary_key=True)
    # tDiscountName = models.CharField(max_length=40)
    # tDiscountDescription = models.TextField(max_length=200)
    # tDiscountType = models.CharField(max_length=30)
    # tDiscountAmount = models.DecimalField(max_digits=8, decimal_places=3)
    # tDiscountDateCreated = models.DateTimeField('date created')
    # tDiscountDateValidFrom = models.DateTimeField('date created')
    # tDiscountDateValidUntil = models.DateTimeField('date created')
    # tDiscountCouponCode = models.CharField(max_length=20)
    # tDiscountMaxDiscount = models.DecimalField(max_digits=8, decimal_places=3)
    # tDiscountMinOrderValue = models.DecimalField(max_digits=8, decimal_places=3)

    # transactionID = models.ForeignKey(Category, on_delete=models.CASCADE)

    # class Meta:
        # db_table = 'cdiscount'

    # def __str__(self):
        # return self.cDiscountName
