from django.contrib import admin

from .models import Sale, SaleItems

class SaleItemsInline(admin.StackedInline):
    model = SaleItems

class SaleAdmin(admin.ModelAdmin):
    model = Sale
    inlines = [
        SaleItemsInline
    ]
admin.site.register(Sale, SaleAdmin)
