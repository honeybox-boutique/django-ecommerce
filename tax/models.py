from django.db import models

# Create your models here.

# Location

# to calc tax
# take shipping addressState, addressCity, addressZip
# get applicable tax rates
# tax_qs = TaxRate.objects.filter(
#   taxRateIsActive=True,
#   jurisdictionID__jurisdictionState=addressState,
#   jurisdictionID__jurisdictionCity=addressCity,
#   jurisdictionID__jurisdictionZip=addressZip,
# )
# tax_multiplier = decimal.Decimal("0.00")
# collecting = False
# if tax_qs.count() == 0:
    # return tax_multiplier, collecting
# if tax_qs.count() == 1:
    # tax_obj = tax_qs.first()
    # tax_multiplier = tax_obj.taxRateMultiplier
    # collecting = True
    # return tax_multiplier, collecting
# if tax_qs.count() > 1:
    # print('error, multiple active tax rates for jurisdiction')


# Jurisdiction
# class Jurisdiction(models.Model):
    # jurisdictionID = models.AutoField(primary_key=True)
    # jurisdictionLabel = models.CharField(max_length=70)

    # unique for a jurisdiction
    # jurisdictionState = models.CharField(max_length=50, blank=True, null=True)
    # jurisdictionCity = models.CharField(max_length=50, blank=True, null=True)
    # jurisdictionZip = models.CharField(max_length=12, blank=True, null=True)


    # class Meta:
        # db_table = 'jurisdiction'

    # def __str__(self):
        # return self.jurisdictionLabel


# class TaxRate(models.Model):
    # taxRateID = models.AutoField(primary_key=True)
    # taxRateName = models.CharField(max_length=50)
    # taxRateMultiplier = models.DecimalField(max_digits=12, decimal_places=2)
    # taxRateDateCreated = models.DateTimeField('date created', auto_now_add=True)
    # taxRateValidFrom = models.DateTimeField('start date')
    # taxRateValidUntil = models.DateTimeField('end date')
    # taxRateNote = models.TextField(max_length=200)
    # taxRateIsActive = models.BooleanField(default=False)

    # jurisdictionID = models.ForeignKey(Product, on_delete=models.CASCADE)

    # class Meta:
        # db_table = 'tax_rate'

    # def __str__(self):
        # return self.taxRateName

# def pre_save_tax_active(sender, instance, *args, **kwargs):
    # current_time = timezone.now()
    # # check if timezone.now is between start and endate of instance
    # print("checking if pricing active")
    # if instance.taxRateValidFrom < current_time < instance.taxRateValidUntil: 
        # #set active
        # instance.pricingIsActive = True
    # else:
        # # set not active
        # instance.pricingIsActive = False
# pre_save.connect(pre_save_tax_active, sender=TaxRate)
