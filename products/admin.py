from django.contrib import admin

# Register your models here.
from .models import Product, Category, ProductImage, CategoryImage

class ProdImgInline(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProdImgInline,
    ] 
admin.site.register(Product, ProductAdmin)


class CatImgInline(admin.StackedInline):
    model = CategoryImage

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CatImgInline,
    ] 
admin.site.register(Category, CategoryAdmin)