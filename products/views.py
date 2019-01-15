from django.views import generic
from .models import Product
from django.shortcuts import get_object_or_404, render
# Create your views here.

class ProductList(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        if 'category' in self.kwargs:
            return Product.objects.filter(productCategories__categoryName=self.kwargs['category'])
        else:
            return Product.objects.all()

class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'products/detail.html'
    slug_url_kwarg = 'productSlug'
    slug_field = 'productSlug'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProductDetail, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context