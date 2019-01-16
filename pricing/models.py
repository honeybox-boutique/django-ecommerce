from django.db import models
from products.models import Product

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