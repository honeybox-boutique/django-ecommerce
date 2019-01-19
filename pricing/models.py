from django.db import models
from products.models import Product, Category

# Create your models here.

class Pricing(models.Model):
    pricingID = models.AutoField(primary_key=True)
    pricingBasePrice = models.DecimalField(max_digits=8, decimal_places=3)
    pricingDateCreated = models.DateTimeField('date created')
    pricingStartDate = models.DateTimeField('start date')
    pricingEndDate = models.DateTimeField('end date')
    pricingNote = models.TextField(max_length=200)

    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pricing'

    def __str__(self):
        return self.pricingNote

class PDiscount(models.Model):
    pDiscountID = models.AutoField(primary_key=True)
    pDiscountName = models.CharField(max_length=40)
    pDiscountDescription = models.TextField(max_length=200)
    pDiscountType = models.CharField(max_length=30)
    pDiscountValue = models.DecimalField(max_digits=8, decimal_places=3)
    pDiscountDateCreated = models.DateTimeField('date created', auto_now_add=True)
    pDiscountDateValidFrom = models.DateTimeField('valid from')
    pDiscountDateValidUntil = models.DateTimeField('valid until')
    pDiscountCouponCode = models.CharField(max_length=20)
    pDiscountMaxDiscount = models.DecimalField(max_digits=8, decimal_places=3)
    pDiscountMinOrderValue = models.DecimalField(max_digits=8, decimal_places=3)

    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pdiscount'

    def __str__(self):
        return self.pDiscountName

    @property
    def get_discount_price(self, price):
        if self.pDiscountType == 'Percent':
            discount_amount = price - (price * self.pDiscountValue)
            return discount_amount
        elif self.pDiscountType == 'Amount':
            discount_amount = price - self.pDiscountValue
            return discount_amount

class CDiscount(models.Model):
    cDiscountID = models.AutoField(primary_key=True)
    cDiscountName = models.CharField(max_length=40)
    cDiscountDescription = models.TextField(max_length=200)
    cDiscountType = models.CharField(max_length=30)
    cDiscountValue = models.DecimalField(max_digits=8, decimal_places=3)
    cDiscountDateCreated = models.DateTimeField('date created', auto_now_add=True)
    cDiscountDateValidFrom = models.DateTimeField('valid from')
    cDiscountDateValidUntil = models.DateTimeField('valid until')
    cDiscountCouponCode = models.CharField(max_length=20)
    cDiscountMaxDiscount = models.DecimalField(max_digits=8, decimal_places=3)
    cDiscountMinOrderValue = models.DecimalField(max_digits=8, decimal_places=3)

    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cdiscount'

    def __str__(self):
        return self.cDiscountName

    def get_discount_price(self, price):
        if self.cDiscountType == 'Percent':
            discount_amount = price - (price * self.cDiscountValue)
            return discount_amount
        elif self.cDiscountType == 'Amount':
            discount_amount = price - self.cDiscountValue
            return discount_amount

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
