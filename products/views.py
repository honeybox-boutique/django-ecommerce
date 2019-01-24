from django.views import generic
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils import timezone
from pricing.models import Product, Pricing
from purchases.models import PurchaseItems
# import django_filters
# Create your views here.

# class ProductFilter(django_filters.FilterSet):
    # class Meta:
        # model = Product
        # fields = {
            # 'product__pricing__pricingStartDate': ['exact', 'contains'],
            # 'last_login': ['exact', 'year__gt'],
        # }
class ProductList(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        """ queries database for products using the criteria below and adds it to context:

        product categoryName = key word argument 'category'
        product pricing basePrice is not null - this may not be needed
        product pricing StartDate <= timenow
        product pricing EndDate <= timenow
        """
        # Call the base implementation first to get the context
        context = super(ProductList, self).get_context_data(**kwargs)
        # where categoryName == kwarg['category']
        product_list_query = Product.objects.filter(productCategories__categoryName=self.kwargs['category'])
        # where pricingBasePrice is not null
        product_list_query = product_list_query.filter(pricing__pricingBasePrice__isnull=False)
        # where now() greater than pricingStartDate and now() less than pricingEndDate
        product_list_query = product_list_query.filter(pricing__pricingStartDate__lte=timezone.now(), pricing__pricingEndDate__gte=timezone.now())
        context['product_list'] = product_list_query
        return context

class ProductDetail(generic.DetailView):
    """ Product generic detailview """
    model = Product
    template_name = 'products/detail.html'
    slug_url_kwarg = 'productSlug'
    slug_field = 'productSlug'

    def get_context_data(self, **kwargs):
        """ queries database for a product using the criteria below and adds it to context:



        prefetches pricing queryset:
            product pricing StartDate before now
            product pricing EndDate after now
            
        prefetches purchaseitems queryset:
            product slug = kwarg
            distinct on color

        gets queryset:
            productslug = kwarg
        """
        # Call the base implementation first to get the context
        context = super(ProductDetail, self).get_context_data(**kwargs)
        # Get pricing table queryset filtered for current valid pricing
        pricingDateQuery = Pricing.objects.filter(pricingStartDate__lte=timezone.now(), pricingEndDate__gte=timezone.now())
        # Get colorset for product
        product_color_query = Product.objects.filter(productSlug__exact=self.kwargs['productSlug'], productcolor__productColorID__isnull=False)
        # Get purchaseItems queryset filtered on product ID
        purchaseItemsQuery = PurchaseItems.objects.filter(productID__productSlug=self.kwargs['productSlug']).distinct('piColor')
        # set pricingDateQuery prefetch query variable
        pricingPrefetch = Prefetch('pricing_set', queryset=pricingDateQuery)
        purchasePrefetch = Prefetch('purchaseitems_set', queryset=purchaseItemsQuery)
        # Do query for product queryset and include prefetch queryset
        productQuerySet = Product.objects.prefetch_related(pricingPrefetch, purchasePrefetch).get(productSlug__exact=self.kwargs['productSlug'])
        # Create any data and add it to the context
        context['product1'] = product_color_query
        context['product'] = productQuerySet
        return context

def load_sizes(request):
    """ This method will populate the available purchaseitem sizes based on color selection """
    productColorName = request.GET.get('productColorName')
    sizes = PurchaseItems.objects.filter(piColor__iexact=productColorName).distinct('piSize')
    return render(request, 'products/size_dropdown_list_options.html', {'sizes': sizes})