from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

class Address(models.Model):
    addressBillingProfile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    addressType = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    addressLine1 = models.CharField(max_length=120)
    addressLine2 = models.CharField(max_length=120, null=True, blank=True)
    addressCity = models.CharField(max_length=120)
    addressCountry = models.CharField(max_length=120, default='United States')
    addressState = models.CharField(max_length=120)
    addressPostalCode = models.CharField(max_length=120)


    def __str__(self):
        return str(self.addressBillingProfile)
