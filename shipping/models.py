from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.utils import timezone

from sales.models import Sale
from addresses.models import Address


import easypost
easypost.api_key = settings.EASYPOST_SECRET_KEY


class Warehouse(models.Model):
    warehouseID = models.AutoField(primary_key=True)
    warehouseName = models.CharField(max_length=120)
    warehouseAddress = models.ForeignKey(Address, on_delete=models.PROTECT)

    class Meta:
        db_table = 'warehouse'

    def __str__(self):
        return self.warehouseName

class Shipment(models.Model):
    FROM_ADDRESS_CHOICES = (
        ('home', 'House in Pasadena'),
    )
    SHIPMENT_STATUS_CHOICES = (
        ('in progress', 'Being Prepared'),
        ('printed', 'Printed'),
        ('shipped', 'Shipped'),
    )
    CARRIER_OPTIONS = (
        ('USPS', 'USPS'),
    )
    RATE_OPTIONS = (
        ('Priority', 'Priority'),
        ('ParcelSelect', 'Parcel Select'),
        ('First', 'First Class'),
        ('Express', 'Express'),
    )
    shipmentID = models.AutoField(primary_key=True)
    shipmentDateRequested = models.DateTimeField('shipment date created')
    shipmentDateLabelPrinted = models.DateTimeField('shipment date label printed', blank=True, null=True)
    shipmentNote = models.CharField(max_length=120, default='Default Shipment Note')
    warehouseID = models.ForeignKey(Warehouse, on_delete=models.PROTECT, blank=True, null=True)
    shipmentToAddress = models.ForeignKey(Address, related_name='shipmentToAddress', null=True, blank=True, on_delete=models.PROTECT)
    # shipmentToAddress = models.ForeignKey(Address, on_delete=models.PROTECT)
    shipmentLabelIsBought = models.BooleanField(default=False)

    # maybe add shipmentStatus to clarify IsBought
    shipmentStatus = models.CharField(max_length=120, default='in progress', choices=SHIPMENT_STATUS_CHOICES)
    
    saleID = models.ForeignKey(Sale, on_delete=models.CASCADE)

    shipmentCarrier = models.CharField(max_length=120, choices=CARRIER_OPTIONS)
    shipmentRate = models.CharField(max_length=120, choices=RATE_OPTIONS)
    # easypost providedstuff
    shipmentEasyPostID = models.CharField(max_length=120, blank=True, null=True)
    shipmentCost = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipmentTrackingNumber = models.CharField(max_length=120, blank=True, null=True)
    shipmentTrackingURL = models.URLField(verbose_name='tracking url', blank=True, null=True)
    shipmentLabelURL = models.URLField(blank=True, null=True)

    shipmentReturnEasyPostID = models.CharField(max_length=120, blank=True, null=True)
    shipmentReturnLabelCost = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipmentReturnTrackingNumber = models.CharField(max_length=120, blank=True, null=True)
    shipmentReturnLabelURL = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'shipment'

    def __str__(self):
        return str(self.saleID)

    def save(self, *args, **kwargs):
        # if shipmentStatus is shipped
        if self.shipmentStatus == 'shipped':
            # set saleStatus to shipped
            self.saleID.saleStatus = 'shipped'
            # do shipment email

        # if shipmentStatus is in progress
        if self.warehouseID and self.shipmentToAddress and self.shipmentStatus == 'in progress':
            # check parcel is good
            if self.parcel_set.count() > 0:
                # now call create easy_post stuff
                for parcel in self.parcel_set.all():
                    if parcel.parcelName and parcel.parcelWeight > 0:
                        self.shipmentEasyPostID, self.shipmentCost, self.shipmentTrackingNumber, self.shipmentTrackingURL, self.shipmentLabelURL, self.shipmentReturnEasyPostID, self.shipmentReturnLabelCost, self.shipmentReturnTrackingNumber, self.shipmentReturnLabelURL = self.create_easypost()
                        if self.shipmentTrackingNumber and self.shipmentLabelURL:
                            # if tracking num and label are gotten set status to printed
                            self.shipmentStatus = 'printed'
                            self.shipmentDateLabelPrinted = timezone.now()
                            # send shipping email
                            sent_ship_email = self.send_shipping_email()

        super(Shipment, self).save(*args, **kwargs)

    def send_shipping_email(self):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        # change: add error handling here. currently this is always false
        sent = False
        # get sale obj
        sale_obj = self.saleID
        # # send order confirmation email
        from_email = settings.EMAIL_HOST_ALIAS_SUPPORT
        to_email = str(sale_obj.saleBillingProfile)
        html_message = render_to_string('emails/shipping-information.html', {
            'sale_obj': sale_obj,
            })
        plain_message = strip_tags(html_message)
        subject = 'HoneyBox Boutique - Order Shipped! - %s' % (sale_obj.saleStringID)
        send_mail(subject, plain_message, from_email, [to_email], auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD, html_message=html_message)
        return sent
    
    def create_easypost(self):
        from_address = self.get_from_address()
        to_address = self.get_to_address()
        parcel = self.get_parcel()
        
        shipment_cost = None
        shipment_track_num = None
        shipment_track_url = None
        shipment_label_url = None
        return_shipment_cost = None
        return_easy_shipment_id = None
        return_shipment_track_num = None
        return_shipment_label_url = None

        
        # if marked bought
        if self.shipmentLabelIsBought and self.shipmentEasyPostID:
            easy_shipment_id, shipment_cost, shipment_track_num, shipment_track_url, shipment_label_url = self.buy_shipment(from_address, to_address, parcel)
            # get current EasypostID
            return_shipment_id = self.shipmentEasyPostID
            return_easy_shipment_id, return_shipment_cost, return_shipment_track_num, return_shipment_label_url = self.buy_return_shipment(return_shipment_id)

        # if not marked for buying
        else:
            easy_shipment_id, shipment_cost = self.create_shipment(from_address, to_address, parcel)
            if easy_shipment_id:
                # get current EasypostID
                return_easy_shipment_id, return_shipment_cost = self.create_return_shipment(easy_shipment_id)
            else:
                pass

        return easy_shipment_id, shipment_cost, shipment_track_num, shipment_track_url, shipment_label_url, return_easy_shipment_id, return_shipment_cost, return_shipment_track_num, return_shipment_label_url
        
            
    def buy_shipment(self, from_address, to_address, parcel):
        # call buy_shipment
        easy_shipment_id = None
        shipment_cost = None
        shipment_track_num = None
        shipment_track_url = None
        shipment_label_url = None
        shipment = easypost.Shipment.create(
            to_address=to_address,
            from_address=from_address,
            parcel=parcel,
        )
        # show rates
        for rate in shipment.rates:
            if rate.carrier == self.shipmentCarrier and rate.service == self.shipmentRate:
                shipment_cost = rate.rate
                easy_shipment_id = shipment.id

                shipment.buy(rate={'id': rate.id})
                shipment_label_url = shipment.postage_label.label_url
                ## Print Tracking Code
                shipment_track_num = shipment.tracking_code
                shipment_track_url = shipment.tracker.public_url
        return easy_shipment_id, shipment_cost, shipment_track_num, shipment_track_url, shipment_label_url

    def create_shipment(self, from_address, to_address, parcel):
        # create_shipment
        
        easy_shipment_id = None
        shipment_cost = None
        shipment = easypost.Shipment.create(
            to_address=to_address,
            from_address=from_address,
            parcel=parcel,
        )
        # show rates
        for rate in shipment.rates:
            if rate.carrier == self.shipmentCarrier and rate.service == self.shipmentRate:
                shipment_cost = rate.rate
                easy_shipment_id = shipment.id
                # call create_return_shipment
                return easy_shipment_id, shipment_cost

        return easy_shipment_id, shipment_cost


    def create_return_shipment(self, shipment):
        return_easy_shipment_id = None
        # get passed shipmentid and get shipment
        shipment = easypost.Shipment.retrieve(shipment)
        return_shipment = easypost.Shipment.create(
            to_address=shipment.from_address,
            from_address=shipment.to_address,
            parcel=shipment.parcel,
            is_return=True,
        )
        
        # show rates
        for rate in return_shipment.rates:
            if rate.carrier == self.shipmentCarrier and rate.service == self.shipmentRate:
                return_shipment_cost = rate.rate
                return_easy_shipment_id = return_shipment.id
                # call create_return_shipment
        return return_easy_shipment_id, return_shipment_cost


    def buy_return_shipment(self, shipment):
        return_easy_shipment_id = None
        return_shipment_cost = None
        return_shipment_label_url = None
        return_shipment_track_num = None
        # get passed shipmentid and get shipment
        shipment = easypost.Shipment.retrieve(shipment)
        return_shipment = easypost.Shipment.create(
            to_address=shipment.from_address,
            from_address=shipment.to_address,
            parcel=shipment.parcel,
            is_return=True,
        )
        
        # show rates
        for rate in return_shipment.rates:
            if rate.carrier == self.shipmentCarrier and rate.service == self.shipmentRate:
                return_shipment_cost = rate.rate
                return_easy_shipment_id = return_shipment.id

                return_shipment.buy(rate={'id': rate.id})
                return_shipment_label_url = return_shipment.postage_label.label_url
                ## Print Tracking Code
                return_shipment_track_num = return_shipment.tracking_code
                # call create_return_shipment
        return return_easy_shipment_id, return_shipment_cost, return_shipment_track_num, return_shipment_label_url

    def get_from_address(self):
        # get warehouse address obj
        warehouse_address_obj = self.warehouseID.warehouseAddress
        # create address
        from_address = easypost.Address.create(
            company='Honeybox Boutique',
            street1=warehouse_address_obj.addressLine1,
            street2=warehouse_address_obj.addressLine2,
            city=warehouse_address_obj.addressCity,
            state=warehouse_address_obj.addressState,
            zip=warehouse_address_obj.addressPostalCode,
        )
        return from_address

    def get_to_address(self):
        # create  to address
        shipping_address_obj = self.saleID.saleShippingAddress
        to_address = easypost.Address.create(
            street1=shipping_address_obj.addressLine1,
            street2=shipping_address_obj.addressLine2,
            city=shipping_address_obj.addressCity,
            state=shipping_address_obj.addressState,
            zip=shipping_address_obj.addressPostalCode,
            name=shipping_address_obj.addressName,
        )
        return to_address

    def get_parcel(self):
        # get parcel_set
        parcel = self.parcel_set.first()
        # for parcel in parcels:
            # create parcel
        parcel = easypost.Parcel.create(
            predefined_package=parcel.parcelName,
            weight=parcel.parcelWeight,
        )
        return parcel

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
def post_save_create_shipment(sender, instance, *args, **kwargs):
    if instance.saleStatus == 'payed':
        # create shipment
        Shipment.objects.create(
            shipmentDateRequested=timezone.now(),# change: add timezone import
            shipmentToAddress=instance.saleShippingAddress,
            saleID=instance,
        )

post_save.connect(post_save_create_shipment, sender=Sale)
