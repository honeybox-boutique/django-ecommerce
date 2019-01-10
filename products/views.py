from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category, ProductImage

# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = 'products/list.html'

    def get_queryset(self):
        if 'category' in self.kwargs:
            return Product.objects.filter(productCategories__categoryName=self.kwargs['category'])
        else:
            return Product.objects.all()

class ProductDetail(DetailView):
    model = Product
    template_name = 'products/detail.html'
