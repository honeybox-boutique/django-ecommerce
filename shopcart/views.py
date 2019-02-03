from django.shortcuts import render, redirect

from users.forms import LoginForm, GuestForm
from .models import ShopCart, PurchaseItems
from billing.models import BillingProfile
from users.models import Guest
# from django.contrib.messages.views import SuccessMessageMixin
# 
# class ShopCartUpdateView(SuccessMessageMixin, UpdateView):
#     ...
#     success_message = 'List successfully saved!!!!'

def cart_home(request):
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)
    request.session['cart_count'] = cart_obj.shopCartItems.count()
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
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)# get cart
    purchase_item_query = PurchaseItems.objects.filter(productID__productSlug=product_slug, piColor__colorName=color).filter(piSize=size)
    for cart_item in cart_obj.shopCartItems.all():# exclude all pitems already in cart
        purchase_item_query = purchase_item_query.exclude(pk=cart_item.pk)
    # if quantity + quantity in cart > purchase_item_query.count() return "not enough in stock to add these to cart"
    if not purchase_item_query:
        print('Not Enough')
        request.session['cart_count'] = cart_obj.shopCartItems.count()
        return redirect('shopcart:home')
    purchase_item_obj = purchase_item_query.first()
    cart_obj.shopCartItems.add(purchase_item_obj)
    request.session['cart_count'] = cart_obj.shopCartItems.count()
    return redirect('shopcart:home')

def checkout_home(request):
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)# get cart
    user = request.user
    order_obj = None
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')

    if new_obj or cart_obj.shopCartItems.count() == 0:# if cart was just created redirect to cart home
       redirect('shopcart:home')
    else:# cart is not new, begin checkout
        pass
    
    if user.is_authenticated:
        billing_profile = BillingProfile.objects.get_or_create(user=user, billingEmail=user.email)
    elif guest_email_id is not None:
        guest_obj = Guest.objects.get(id=guest_email_id)
        billing_profile = BillingProfile.objects.get_or_create(billingEmail=guest_obj.guestEmail)
    else:
        # change: do we need error raise here?
        pass
    
    context = {
        "shopcart": cart_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
    }

    # saleStatus = models.CharField(max_length=120, default='created', choices=SALE_STATUS_CHOICES) # purchaseDate = models.DateTimeField('date purchased')
    # saleSubTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# Amount should be sum(saleitemprice - p-cDiscount)
    # saleDiscountAmount = ? # change: determine if value appropriate: only sale-level discount amount, doesn't include p or c discount
    # saleSalesTaxAmount = ? # change: add logic for sales tax calculation
    # saleShipCostAmountCharged = models.DecimalField(default=7.00, max_digits=12, decimal_places=2)# change: integrate shipping API
    # saleTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: generate total from other fields
        # new_sale_obj = Sale(saleStatus='created', 
        # shop_cart_items = cart_obj.shopCartItems.all()
        # for item in shop_cart_items:
             # new_sale_obj.objects.add(saleItems=)
    return render(request, 'carts/checkout.html', context)