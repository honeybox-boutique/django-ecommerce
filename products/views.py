from django.views import generic
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils import timezone
from pricing.models import Product, Pricing, PDiscount
from purchases.models import PurchaseItems
from products.models import ProductImage
from shopcart.models import ShopCart
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
        at least one product pricing is active
        """
        # Call the base implementation first to get the context
        context = super(ProductList, self).get_context_data(**kwargs)
        # filter products based on category kwarg
        product_list_query = Product.objects.filter(productCategories__categoryName=self.kwargs['category'])
        # filter products out with inactive pricings
        product_list_query = product_list_query.filter(pricing__pricingIsActive=True)
        context['product_list'] = product_list_query
        return context

class ProductDetail(generic.DetailView):
    """ Product generic detailview """
    model = Product
    template_name = 'products/detail.html'
    slug_url_kwarg = 'productSlug'
    slug_field = 'productSlug'

    def get_context_data(self, *args, **kwargs):
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
        context = super(ProductDetail, self).get_context_data(*args, **kwargs)
        # test query for pricing manager
        pricing_test = PDiscount.largestActive.get_largest_active(self)
        # Get pricing table queryset filtered for current valid pricing
        pricingDateQuery = Pricing.objects.filter(pricingIsActive=True)
        # Get colorset for product
        product_color_query = Product.objects.filter(productSlug__exact=self.kwargs['productSlug'], productcolor__productimage__isnull=False)
        # Get purchaseItems queryset filtered on product ID
        purchaseItemsQuery = PurchaseItems.objects.filter(productID__productSlug=self.kwargs['productSlug']).distinct('piColor')
        # set pricingDateQuery prefetch query variable
        pricingPrefetch = Prefetch('pricing_set', queryset=pricingDateQuery)
        purchasePrefetch = Prefetch('purchaseitems_set', queryset=purchaseItemsQuery)
        # Do query for product queryset and include prefetch queryset
        productQuerySet = Product.objects.prefetch_related(pricingPrefetch, purchasePrefetch).get(productSlug__exact=self.kwargs['productSlug'])
        # get or add cart
        cart_obj, new_obj = ShopCart.objects.get_or_new(self.request)
        # Create any data and add it to the context
        context['shopcart'] = cart_obj
        context['product1'] = product_color_query
        context['product'] = productQuerySet
        return context

def load_sizes(request):
    """ This method will populate the available purchaseitem sizes based on color selection """
    productColorID = request.GET.get('productColorID')
    productSlug = request.GET.get('productSlug')
    sizes = PurchaseItems.objects.filter(piColor__colorName__exact=productColorID, productID__productSlug__iexact=productSlug).distinct('piSize').values('piSize')
    # data = [{'piSize': size.piSize} for size in size_list]
    images = ProductImage.objects.filter(productColorID__colorID__colorName__iexact=productColorID, productColorID__productID__productSlug__iexact=productSlug)# .values('productImagePath')
    # return render(request, 'products/size_dropdown_list_options.html', {'sizes': sizes, 'images': images})
    return render(request, 'products/size_dropdown_list_options.html', {'sizes': sizes, 'images': images})