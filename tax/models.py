import decimal
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save

# Create your models here.

# Jurisdiction
class Jurisdiction(models.Model):
    jurisdictionID = models.AutoField(primary_key=True)
    jurisdictionLabel = models.CharField(max_length=70)

    # unique for a jurisdiction
    jurisdictionState = models.CharField(max_length=50, blank=True, null=True)
    jurisdictionCity = models.CharField(max_length=50, blank=True, null=True)
    jurisdictionZip = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
      db_table = 'jurisdiction'

    def __str__(self):
        return self.jurisdictionLabel

    # get tax
    def calc_tax(self):
        tax_multiplier = decimal.Decimal("0.00")
        active_rate_exists = False
        # get tax multiplier from object
        tax_qs = TaxRate.objects.filter(
            jurisdictionID=self.jurisdictionID,
            taxRateIsActive=True,
        )
        if tax_qs.count() == 1:
            active_rate_exists = True
            # get tax obj
            tax_obj = tax_qs.first()
            # get multiplier
            tax_multiplier = tax_obj.taxRateMultiplier
        if tax_qs.count() > 1:
            active_rate_exists = True
            tax_obj = tax_qs.last()
            # get multiplier
            tax_multiplier = tax_obj.taxRateMultiplier
        return tax_multiplier, active_rate_exists


class TaxRate(models.Model):
    taxRateID = models.AutoField(primary_key=True)
    taxRateName = models.CharField(max_length=50)
    taxRateMultiplier = models.DecimalField(max_digits=12, decimal_places=4)
    taxRateDateCreated = models.DateTimeField('date created', auto_now_add=True)
    taxRateValidFrom = models.DateTimeField('start date')
    taxRateValidUntil = models.DateTimeField('end date')
    taxRateNote = models.TextField(max_length=200)
    taxRateIsActive = models.BooleanField(default=False)

    jurisdictionID = models.ForeignKey(Jurisdiction, on_delete=models.CASCADE)


    class Meta:
        db_table = 'tax_rate'

    def __str__(self):
        return self.taxRateName

def pre_save_tax_active(sender, instance, *args, **kwargs):
    current_time = timezone.now()
    # check if timezone.now is between start and endate of instance
    if instance.taxRateValidFrom < current_time < instance.taxRateValidUntil:
        #set active
        instance.taxRateIsActive = True
    else:
        # set not active
        instance.taxRateIsActive = False
pre_save.connect(pre_save_tax_active, sender=TaxRate)
