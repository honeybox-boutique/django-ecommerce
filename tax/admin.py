from django.contrib import admin

from .models import Jurisdiction, TaxRate


class TaxRateInline(admin.StackedInline):
    model = TaxRate

class JurisdictionAdmin(admin.ModelAdmin):
    model = Jurisdiction
    inlines = [
        TaxRateInline,
    ]
admin.site.register(Jurisdiction, JurisdictionAdmin)
