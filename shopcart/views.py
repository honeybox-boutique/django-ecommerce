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
    return render(request, 'carts/home.html', {"shopcart": cart_obj})

def cart_update(request):
    """ should use product-slug, color, and size as parameters to check if:
        purchitem with matching slug, color, and size exists,
        AND does NOT have a sale transaction associated with it
    """
    print(request.POST)
    # get POST parameters
    product_slug = request.POST.get('productSlug')
    color = request.POST.get('color-selection')
    size = request.POST.get('size-selection')
    quantity = request.POST.get('quantity')
    product_id = 7
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)# get cart
            # ^exclude pitems already in cart_obj
    # purchase_item_obj = PurchaseItems.objects.get(prodStockID=product_id)
    purchase_item_query = PurchaseItems.objects.filter(productID__productSlug=product_slug, piColor__colorName=color).filter(piSize=size)
    for cart_item in cart_obj.shopCartItems.all():# exclude all pitems already in cart
        purchase_item_query = purchase_item_query.exclude(pk=cart_item.pk)
    # if quantity + quantity in cart > purchase_item_query.count() return "not enough in stock to add these to cart"
    if not purchase_item_query:
        print('Not Enough')
        return redirect('shopcart:home')
    purchase_item_obj = purchase_item_query.first()
    cart_obj.shopCartItems.add(purchase_item_obj)
    return redirect('shopcart:home')