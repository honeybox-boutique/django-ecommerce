import decimal
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from products.models import Product, Category

ONE_HUNDRED_D = decimal.Decimal('100.00')
# Create your models here.
DISCOUNT_TYPE_CHOICES = (
    ('Percent', 'Percent'),
    ('Amount', 'Amount'),
) 

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

class PDiscount(models.Model):
    pDiscountID = models.AutoField(primary_key=True)
    pDiscountName = models.CharField(max_length=40)
    pDiscountDescription = models.TextField(max_length=200)
    pDiscountType = models.CharField(max_length=30, choices=DISCOUNT_TYPE_CHOICES)# change: add choices for percent and decimal
    pDiscountValue = models.DecimalField(max_digits=12, decimal_places=2)
    pDiscountDateCreated = models.DateTimeField('date created', auto_now_add=True)
    pDiscountDateValidFrom = models.DateTimeField('valid from')
    pDiscountDateValidUntil = models.DateTimeField('valid until')
    pDiscountCouponCode = models.CharField(max_length=20)
    pDiscountMaxDiscount = models.DecimalField(max_digits=12, decimal_places=2)
    pDiscountMinOrderValue = models.DecimalField(max_digits=12, decimal_places=2)
    pDiscountIsActive = models.BooleanField(default=False)

    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pdiscount'

    def __str__(self):
        return self.pDiscountName

    def get_active_p_discount_amount_or_multiplier(self):
        if self.pDiscountIsActive:
            discount_type = self.pDiscountType
            discount_value = decimal.Decimal(self.pDiscountValue)
            discount_returned = decimal.Decimal("0.00")
            is_multiplier = False
            #if decimal
            if discount_type == 'Decimal':
                # return discount_value
                discount_returned = discount_value
            #if percent
            elif discount_type == 'Percent':
                is_multiplier = True
                # return discount_value
                discount_returned = discount_value / ONE_HUNDRED_D
            return discount_returned, is_multiplier

def pre_save_pdiscount_active(sender, instance, *args, **kwargs):
    current_time = timezone.now()
    # check if timezone.now is between start and endate of instance
    if instance.pDiscountDateValidFrom < current_time < instance.pDiscountDateValidUntil: 
        # change: check if product has other active discounts
        # if has other active pricings then don't save and return error "already active pricing"
        instance.pDiscountIsActive = True
    else:
        # set not active
        instance.pDiscountIsActive = False
pre_save.connect(pre_save_pdiscount_active, sender=PDiscount)

class CDiscount(models.Model):
    cDiscountID = models.AutoField(primary_key=True)
    cDiscountName = models.CharField(max_length=40)
    cDiscountDescription = models.TextField(max_length=200)
    cDiscountType = models.CharField(max_length=30, choices=DISCOUNT_TYPE_CHOICES)
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

    def get_active_cdiscount_amount_or_multiplier(self):
        """ Returns discount_returned, the discount amount or multiplier """
        if self.cDiscountIsActive:
            discount_type = self.cDiscountType
            discount_value = decimal.Decimal(self.cDiscountValue)
            is_multiplier = False
            discount_returned = decimal.Decimal("0.00")# amount or multiplier to return
            #if decimal
            if discount_type == 'Decimal':
                # return discount_value
                discount_returned = discount_value
            #if percent
            elif discount_type == 'Percent':
                is_multiplier = True
                # change: add logic to get category value
                discount_returned = discount_value / ONE_HUNDRED_D
            return discount_returned, is_multiplier
        else:
            print('not active')

def pre_save_cdiscount_active(sender, instance, *args, **kwargs):
    current_time = timezone.now()
    # check if timezone.now is between start and endate of instance
    if instance.cDiscountDateValidFrom < current_time < instance.cDiscountDateValidUntil: 
        # change: check if product has other active discounts
        # if has other active pricings then don't save and return error "already active pricing"
        instance.cDiscountIsActive = True
    else:
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

# Pricing post_save
def post_save_pricing(sender, instance, created, *args, **kwargs):
    # get prod_obj
    product_id = instance.productID.productID

    prod_query = Product.objects.filter(productID=product_id)
    # call update_pricing to update pricing
    if prod_query.count() == 1:
        prod_obj = prod_query.first()
        prod_obj.update_pricing()
post_save.connect(post_save_pricing, sender=Pricing)

# PDiscount post_save
def post_save_p_discount(sender, instance, created, *args, **kwargs):
    # get prod_obj
    product_id = instance.productID.productID
    prod_query = Product.objects.filter(productID=product_id)
    # call update_pricing to update pricing
    if prod_query.count() == 1:
        prod_obj = prod_query.first()
        prod_obj.update_pricing()
post_save.connect(post_save_p_discount, sender=PDiscount)

# CDiscount post_save
def post_save_c_discount(sender, instance, created, *args, **kwargs):
    # get category
    category_id = instance.categoryID
    # get category products_set
    category_products = Product.objects.filter(productCategories=category_id)
    for product in category_products.all():
        product.update_pricing()
post_save.connect(post_save_c_discount, sender=CDiscount)