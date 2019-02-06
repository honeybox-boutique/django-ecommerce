from django.contrib import admin


from .models import Pricing, PDiscount, CDiscount, SDiscount, SDiscountCondition

# Product pricing stuff
class PricingAdmin(admin.ModelAdmin):
    model = Pricing
admin.site.register(Pricing, PricingAdmin)

# Product discounts stuff
class PDiscountAdmin(admin.ModelAdmin):
    model = PDiscount
admin.site.register(PDiscount, PDiscountAdmin)

# Category discounts stuff
class CDiscountAdmin(admin.ModelAdmin):
    model = CDiscount
admin.site.register(CDiscount, CDiscountAdmin)

# Sale discounts stuff
class SDiscountConditionInLine(admin.StackedInline):
    model = SDiscountCondition

class SDiscountAdmin(admin.ModelAdmin):
    model = SDiscount
    inlines = [
        SDiscountConditionInLine,
    ]
admin.site.register(SDiscount, SDiscountAdmin)