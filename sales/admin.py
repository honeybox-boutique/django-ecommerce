from django.contrib import admin

from .models import Sale, SaleItems
from pricing.models import SDiscount

class SaleItemsInline(admin.StackedInline):
    model = SaleItems

class SaleDiscountsInline(admin.StackedInline):
    model = SDiscount

class SaleAdmin(admin.ModelAdmin):
    model = Sale
    inlines = [
        SaleItemsInline
    ]
admin.site.register(Sale, SaleAdmin)
