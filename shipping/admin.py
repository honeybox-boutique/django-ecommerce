from django.contrib import admin

from sales.models import CustomerShipMethod
from .models import Shipment, Parcel, Warehouse

class CustomerShipMethodAdmin(admin.ModelAdmin):
    model = CustomerShipMethod
admin.site.register(CustomerShipMethod, CustomerShipMethodAdmin)

class ParcelInLine(admin.StackedInline):
    model = Parcel

class ShipmentAdmin(admin.ModelAdmin):
    model = Shipment
    inlines = [
        ParcelInLine,
    ]
    readonly_fields = (
        'saleID',
        'shipmentEasyPostID',
        'shipmentCost',
        'shipmentTrackingNumber',
        'shipmentLabelURL',
    )
admin.site.register(Shipment, ShipmentAdmin)

admin.site.register(Warehouse)
