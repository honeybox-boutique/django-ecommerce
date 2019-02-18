from django.contrib import admin

from .models import BillingProfile
from addresses.models import Address
# Register your models here.
class AddressInline(admin.StackedInline):
    model = Address

class BillingProfileAdmin(admin.ModelAdmin):
    model = BillingProfile
    inlines = [
        AddressInline
    ]
admin.site.register(BillingProfile, BillingProfileAdmin)