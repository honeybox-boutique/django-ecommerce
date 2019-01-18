from django.contrib import admin
from .models import Pricing, PDiscount
# Register your models here.

class PricingAdmin(admin.ModelAdmin):
    model = Pricing
admin.site.register(Pricing, PricingAdmin)

class PDiscountAdmin(admin.ModelAdmin):
    model = PDiscount
admin.site.register(PDiscount, PDiscountAdmin)
