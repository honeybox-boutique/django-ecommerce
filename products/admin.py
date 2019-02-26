from django.contrib import admin

# Register your models here.
from .models import Product, Category, ProductImage, CategoryImage, ProductColor, Color, Size

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

class SizeAdmin(admin.ModelAdmin):
    model = Size
admin.site.register(Size, SizeAdmin)

class ProductAdmin(admin.ModelAdmin):
    model = Product
    readonly_fields = ['productSlug', 'productBasePrice', 'productDiscountType', 'productDiscountValue', 'productDiscountAmount', 'productSalePrice']
    inlines = [
        ProdColorInline,
        # sizesinline
    ]
admin.site.register(Product, ProductAdmin)


class CatImgInline(admin.StackedInline):
    model = CategoryImage

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CatImgInline,
    ]
admin.site.register(Category, CategoryAdmin)
