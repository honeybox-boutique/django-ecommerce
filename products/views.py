from django.views import generic
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils import timezone
from pricing.models import Product, Pricing, PDiscount
from purchases.models import PurchaseItems
from products.models import ProductImage, CategoryImage
from shopcart.models import ShopCart


class ProductList(generic.ListView):
    model = Product
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        return Product.objects.filter(pricing__pricingIsActive=True)

class CategoryList(generic.ListView):
    model = Product
    template_name = 'products/list.html'

    def get_context_data(self, *args, **kwargs):
        """ queries database for products using the criteria below and adds it to context:

        product categoryName = key word argument 'category'
        at least one product pricing is active
        """
        # Call the base implementation first to get the context
        context = super(CategoryList, self).get_context_data(**kwargs)

        if 'category' in self.kwargs:
            category_arg = self.kwargs['category']
            context['category'] = category_arg
            query = CategoryImage.objects.filter(categoryID__categoryName=self.kwargs['category'])
            context['category_image_obj'] = query.first()

        product_list_query = Product.objects.filter(
            productCategories__categoryName=self.kwargs['category'],
            pricing__pricingIsActive=True
        )
        # filter products out with inactive pricings
        context['product_list'] = product_list_query
        return context

    # def get_queryset(self, *args, **kwargs):
        # context = super(CategoryList, self).get_context_data(**kwargs)
        # context['category_image_obj'] = query.first()
        # return query

class ProductDetail(generic.DetailView):
    """ Product generic detailview """
    model = Product
    template_name = 'products/detail.html'
    slug_url_kwarg = 'productSlug'
    slug_field = 'productSlug'

    def get_context_data(self, *args, **kwargs):
        """ queries database for a product using the criteria below and adds it to context:
        """
        # Call the base implementation first to get the context
        context = super(ProductDetail, self).get_context_data(*args, **kwargs)

        # change: change these disaster queries and remove template logics
        # Get colorset for product
        product_color_query = Product.objects.filter(productSlug__exact=self.kwargs['productSlug'],
                                        productcolor__productimage__isnull=False
                                    )

        # check if pitems associated with product id available == 0
        # if 0 add out_of_stock message

        # get or add cart
        cart_obj, new_obj = ShopCart.objects.get_or_new(self.request)

        # add to context
        context['shopcart'] = cart_obj
        context['product1'] = product_color_query
        # context['product'] = productQuerySet
        return context

def load_sizes(request):
    """ This method will populate the available purchaseitem sizes based on color selection """
    product_color = request.GET.get('productColorID')
    product_slug = request.GET.get('productSlug')

    # change: fix these queries
    sizes = PurchaseItems.objects.filter(piColor__colorName__exact=product_color,
                                    productID__productSlug__iexact=product_slug,
                                ).distinct('piSize').values('piSize')

    images = ProductImage.objects.filter(productColorID__colorID__colorName__iexact=product_color,
                                productColorID__productID__productSlug__iexact=product_slug
                            )# .values('productImagePath')

    return render(request, 'products/size_dropdown_list_options.html', {'sizes': sizes, 'images': images})