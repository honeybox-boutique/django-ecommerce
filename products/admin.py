from django.contrib import admin

# Register your models here.
from .models import Product, Category, ProductImage, CategoryImage, ProductColor, Color

class ProdColorInline(admin.StackedInline):
    model = ProductColor

class ProductImageInline(admin.StackedInline):
    model = ProductImage

class ProductColorAdmin(admin.ModelAdmin):
    model = ProductColor
    inlines = [
        ProductImageInline
    ]
admin.site.register(ProductColor, ProductColorAdmin)

class ColorAdmin(admin.ModelAdmin):
    model = Color
    inlines = [
        ProdColorInline,
    ]
admin.site.register(Color, ColorAdmin)


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['productSlug', 'productBasePrice', 'productDiscountAmount', 'productSalePrice']
    inlines = [
        ProdColorInline,
    ]
admin.site.register(Product, ProductAdmin)


class CatImgInline(admin.StackedInline):
    model = CategoryImage

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CatImgInline,
    ]
admin.site.register(Category, CategoryAdmin)
