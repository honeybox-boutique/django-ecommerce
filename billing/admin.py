from django.contrib import admin

from .models import BillingProfile, Card
from addresses.models import Address
# Register your models here.
class AddressInline(admin.StackedInline):
    model = Address
class CardInline(admin.StackedInline):
    model = Card

class BillingProfileAdmin(admin.ModelAdmin):
    model = BillingProfile
    inlines = [
        CardInline,
        AddressInline
    ]
admin.site.register(BillingProfile, BillingProfileAdmin)