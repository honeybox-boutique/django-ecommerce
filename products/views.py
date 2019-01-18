from django.views import generic
from django.db.models import Prefetch
from pricing.models import Product, Pricing
from purchases.models import PurchaseItems
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

# Create your views here.

class ProductList(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProductList, self).get_context_data(**kwargs)
        # where categoryName == kwarg['category']
        productListQuerySet = Product.objects.filter(productCategories__categoryName=self.kwargs['category'])
        # where pricingBasePrice is not null
        productListQuerySet = productListQuerySet.filter(pricing__pricingBasePrice__isnull=False)
        # where now() greater than pricingStartDate and now() less than pricingEndDate
        # now = timezone.now()
        productListQuerySet = productListQuerySet.filter(pricing__pricingStartDate__lte=timezone.now())
        productListQuerySet = productListQuerySet.filter(pricing__pricingEndDate__gte=timezone.now())
        context['product_list'] = productListQuerySet
        return context

class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'products/detail.html'
    slug_url_kwarg = 'productSlug'
    slug_field = 'productSlug'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProductDetail, self).get_context_data(**kwargs)
        # Get pricing table queryset filtered for current valid pricing
        pricingDateQuery = Pricing.objects.filter(pricingStartDate__lte=timezone.now())
        pricingDateQuery = pricingDateQuery.filter(pricingEndDate__gte=timezone.now())
        # Get purchaseItems queryset filtered on product ID
        purchaseItemsQuery = PurchaseItems.objects.filter(productID__productSlug=self.kwargs['productSlug']).distinct()
        # set pricingDateQuery prefetch query variable
        pricingPrefetch = Prefetch('pricing_set', queryset=pricingDateQuery)
        purchasePrefetch = Prefetch('purchaseitems_set', queryset=purchaseItemsQuery)
        # Do query for product queryset and include prefetch queryset
        productQuerySet = Product.objects.prefetch_related(pricingPrefetch, purchasePrefetch).get(productSlug__exact=self.kwargs['productSlug'])
        # Create any data and add it to the context
        context['product'] = productQuerySet
        return context