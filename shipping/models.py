from django.db import models

from sales.models import Sale
from addresses.models import Address

class Shipment(models.Model):
    FROM_ADDRESS_CHOICES = (
        ('home', 'House in Pasadena'),
    )
    CARRIER_OPTIONS = (
        ('usps', 'USPS'),
    )
    RATE_OPTIONS = (
        ('priority', 'Priority'),
        ('express', 'Express'),
    )
    shipmentID = models.AutoField(primary_key=True)
    shipmentDateCreated = models.DateTimeField('shipment date created')
    shipmentNote = models.CharField(max_length=120, default='Default Shipment Note')
    # shipmentFromAddress = models.CharField(max_length=120, choices=FROM_ADDRESS_CHOICES)# change: make choices and have ashleys be the only one
    shipmentFromAddress = models.ForeignKey(Address, related_name='shipmentFromAddress', null=True, blank=True, on_delete=models.PROTECT)
    shipmentToAddress = models.ForeignKey(Address, related_name='shipmentToAddress', null=True, blank=True, on_delete=models.PROTECT)
    # shipmentToAddress = models.ForeignKey(Address, on_delete=models.PROTECT)
    shipmentLabelIsBought = models.BooleanField(default=False)

    # maybe add shipmentStatus to clarify IsBought
    
    saleID = models.ForeignKey(Sale, on_delete=models.PROTECT)

    shipmentCarrier = models.CharField(max_length=120, choices=CARRIER_OPTIONS)
    shipmentRate = models.CharField(max_length=120, choices=RATE_OPTIONS)
    # easypost providedstuff
    shipmentCost = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipmentTrackingNumber = models.CharField(max_length=120)
    shipmentLabelURL = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'shipment'

    def __str__(self):
        return self.shipmentNote


class Parcel(models.Model):
    PARCEL_NAME_CHOICES = (
        ('card', 'Card'),
        ('letter', 'Letter'),
        ('flat', 'Flat'),
        ('flatRateEnvelope', 'FlatRateEnvelope'),
        ('flatRateLegalEnvelope', 'FlatRateLegalEnvelope'),
        ('flatRatePaddedEnvelope', 'FlatRatePaddedEnvelope'),
        ('parcel', 'Parcel'),
        ('irregularParcel', 'IrregularParcel'),
        ('softPack', 'SoftPack'),
        ('smallFlatRateBox', 'SmallFlatRateBox'),
        ('mediumFlatRateBox', 'MediumFlatRateBox'),
        ('largeFlatRateBox', 'LargeFlatRateBox'),
        ('largeFlatRateBoxAPOFPO', 'LargeFlatRateBoxAPOFPO'),
        ('regionalRateBoxA', 'RegionalRateBoxA'),
        ('regionalRateBoxB', 'RegionalRateBoxB')
    )
    parcelID = models.AutoField(primary_key=True)
    parcelName = models.CharField(max_length=120, choices=PARCEL_NAME_CHOICES)# change: add predefined package names as choices
    parcelWeight = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    shipmentID = models.ForeignKey(Shipment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'parcel'

    def __str__(self):
        return self.parcelName

# Sale post_save receiver
# creates shipment record in django db

# shipment pre_save receiver
# creates easypost stuff if things aren't null



# things to store from easypost
# address ID
# 
# import easypost
# easypost.api_key = '***REMOVED***'
# on sale post_save
# check if saleStatus is payed
    # add from address
# fromAddress = easypost.Address.create(
    # company='Honeybox Boutique',
    # street1='130 Valley St.',
    # street2='',
    # city='Pasadena',
    # state='CA',
    # zip='91105',
    # phone='801-602-3439'
# )
    # store an ID for that shit
    # adr_d38080eaf6784c66b8e9971bc2b55fc7
    # get address obj
    # shipping_address_obj = instance.saleShippingAddress
    # create  to address
    # toAddress = easypost.Address.create(
        # street1=shipping_address_obj.addressLine1,
        # street2=shipping_address_obj.addressLine2,
        # city=shipping_address_obj.addressCity,
        # state=shipping_address_obj.addressState,
        # zip=shipping_address_obj.addressPostalCode,
    # )
# toAddress = easypost.Address.create(
        # street1='776 S. 500 E.',
        # city='Orem',
        # state='UT',
        # zip='84097'
    # )
    # add parcel
    # parcel = easypost.Parcel.create(
        # predefined_package='Parcel',
        # weight=10,
    # )
# parcel = easypost.Parcel.create(
    # predefined_package='Parcel',
    # weight=16,
# )  
    # create shipment
    # shipment = easypost.Shipment.create(
        # to_address=toAddress,
        # from_address=fromAddress,
        # parcel=parcel,
    # )
# shipment = easypost.Shipment.create(
        # to_address=toAddress,
        # from_address=fromAddress,
        # parcel=parcel,
    # )
    # show rates
    # for rate in shipment.rates:
        # print rate.carrier 
        # print rate.service 
        # print rate.rate 
        # print rate.id

    # buy label
    # shipment.buy(
        # rate=shipment.lowest_rate(
            # carriers=['USPS'], 
            # services=['First'],
        # )
    # ) 
# shipment.buy(
    # rate=shipment.lowest_rate(
        # carriers=['USPS'], 
        # services=['First'],
    # )
# )
    # or 

    # shipment.buy(rate={'id': '{rate_4024060b9160479c996c2bf93ac4519b}’})

    # show label
        ## Print PNG link 
        # print shipment.postage_label.label_url 
        # ## Print Tracking Code 
        # print shipment.tracking_code