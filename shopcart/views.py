from django.shortcuts import render, redirect

from .models import ShopCart, PurchaseItems
# Create your views here.
# from django.contrib.messages.views import SuccessMessageMixin
# 
# class ShopCartUpdateView(SuccessMessageMixin, UpdateView):
#     ...
#     success_message = 'List successfully saved!!!!'

def cart_home(request):
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)
    return render(request, 'carts/home.html', {})

def cart_update(request):
    """ should use product-slug, color, and size as parameters to check if:
        purchitem with matching slug, color, and size exists,
        AND does NOT have a sale transaction associated with it
    """
    product_id = 7
    purchase_item_obj = PurchaseItems.objects.get(prodStockID=product_id)
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)
    cart_obj.shopCartItems.add(purchase_item_obj)
    return redirect('shopcart:home')