from django.contrib import admin

from .models import Shipment, Parcel, Warehouse

class ParcelInLine(admin.StackedInline):
    model = Parcel

class ShipmentAdmin(admin.ModelAdmin):
    model = Shipment
    inlines = [
        ParcelInLine,
    ]
admin.site.register(Shipment, ShipmentAdmin)

admin.site.register(Warehouse)