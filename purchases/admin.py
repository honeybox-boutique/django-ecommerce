from django.contrib import admin

from .forms import PurchaseItemsForm, PurchaseItemsFormSet, PurchaseForm
from .models import Vendor, Purchase, PurchaseItems

admin.site.register(PurchaseItems)

class VendorAdmin(admin.ModelAdmin):
    inlines = [
    ]
admin.site.register(Vendor, VendorAdmin)

class PurchaseItemsInline(admin.StackedInline):
    model = PurchaseItems
    form = PurchaseItemsForm
    formset = PurchaseItemsFormSet

class PurchaseAdmin(admin.ModelAdmin):
    form = PurchaseForm
    inlines = [
        PurchaseItemsInline,
    ]
admin.site.register(Purchase, PurchaseAdmin)
