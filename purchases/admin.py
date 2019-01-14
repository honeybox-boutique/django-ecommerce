from django.contrib import admin
from .forms import PurchaseItemsForm, PurchaseItemsFormSet, TransactionItemsForm 
from .models import Vendor, Transaction, PurchaseItems, TransactionType
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    inlines = [
    ]
admin.site.register(Vendor, VendorAdmin)

class PurchaseItemsInline(admin.StackedInline):
    model = PurchaseItems
    form = PurchaseItemsForm
    formset = PurchaseItemsFormSet

class TransactionAdmin(admin.ModelAdmin):
    form = TransactionItemsForm
    inlines = [
        PurchaseItemsInline,
    ]
admin.site.register(Transaction, TransactionAdmin)

class TransactionTypeAdmin(admin.ModelAdmin):
    inlines = [
    ]
admin.site.register(TransactionType, TransactionTypeAdmin)