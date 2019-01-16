from django.contrib import admin
from .models import Pricing
# Register your models here.

class PricingAdmin(admin.ModelAdmin):
    model = Pricing
admin.site.register(Pricing, PricingAdmin)