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
    pDiscountAmount = models.DecimalField(max_digits=8, decimal_places=3)
    pDiscountDateCreated = models.DateTimeField('date created')
    pDiscountDateValidFrom = models.DateTimeField('date created')
    pDiscountDateValidUntil = models.DateTimeField('date created')
    pDiscountCouponCode = models.CharField(max_length=20)
    pDiscountMaxDiscount = models.DecimalField(max_digits=8, decimal_places=3)
    pDiscountMinOrderValue = models.DecimalField(max_digits=8, decimal_places=3)

    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pdiscount'

    def __str__(self):
        return self.pDiscountName

class CDiscount(models.Model):
    cDiscountID = models.AutoField(primary_key=True)
    cDiscountName = models.CharField(max_length=40)
    cDiscountDescription = models.TextField(max_length=200)
    cDiscountType = models.CharField(max_length=30)
    cDiscountAmount = models.DecimalField(max_digits=8, decimal_places=3)
    cDiscountDateCreated = models.DateTimeField('date created')
    cDiscountDateValidFrom = models.DateTimeField('date created')
    cDiscountDateValidUntil = models.DateTimeField('date created')
    cDiscountCouponCode = models.CharField(max_length=20)
    cDiscountMaxDiscount = models.DecimalField(max_digits=8, decimal_places=3)
    cDiscountMinOrderValue = models.DecimalField(max_digits=8, decimal_places=3)

    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cdiscount'

    def __str__(self):
        return self.cDiscountName

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