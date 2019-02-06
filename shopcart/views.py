from django.shortcuts import render, redirect

from users.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from coupons.forms import SDiscountForm
from billing.models import BillingProfile
from .models import ShopCart, PurchaseItems
from users.models import Guest
from sales.models import Sale, SaleItems
from addresses.models import Address
from pricing.models import SDiscount

def cart_home(request):
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)
    request.session['cart_count'] = cart_obj.shopCartItems.count()
    return render(request, 'shopcart/home.html', {"shopcart": cart_obj})

def cart_update(request):
    """ should use product-slug, color, and size as parameters to check if:
        purchitem with matching slug, color, and size exists,
        AND does NOT have a sale transaction associated with it
    """
    # get cart
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)
    # change: maybe? clean these parameters using form method
    # get POST parameters
    product_slug = request.POST.get('productSlug')
    color = request.POST.get('color-selection')
    size = request.POST.get('size-selection')
    quantity = request.POST.get('quantity')


    # query for purchaseitems available
    purchase_item_query = PurchaseItems.objects.filter(
                                productID__productSlug=product_slug,
                                piColor__colorName=color,
                                piSize=size,
                                piIsAvailable=True# change: change once you are done
                            )
    # exclude all pitems already in cart
    for cart_item in cart_obj.shopCartItems.all():
        purchase_item_query = purchase_item_query.exclude(pk=cart_item.pk)

    # change: add quantity logic here
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
    cart_obj, cart_created = ShopCart.objects.get_or_new(request)# get cart
    cart_items = cart_obj.shopCartItems.all()
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    #initializers
    sale_obj = None
    address_qs = None
    discount_qs = None
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    if cart_created or cart_items.count() == 0:# if cart was just created redirect to cart home
        return redirect('shopcart:home')

    # get billing profile
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(addressBillingProfile=billing_profile)
        # create sale
        sale_obj, sale_obj_created = Sale.objects.new_or_get(billing_profile, cart_obj)
        # initialize coupon form with sale object
        coupon_form = SDiscountForm(initial={'sobj': sale_obj.saleStringID})
        # get discount qs
        discount_qs = SDiscount.objects.filter(sale=sale_obj)
        if shipping_address_id:
            sale_obj.saleShippingAddress = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            sale_obj.saleBillingAddress = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            sale_obj.save()
        

    
    if request.method == 'POST':
        '''check if sale is done'''
        is_done = sale_obj.check_done()
        if not is_done:
            print('something is not done')
        elif is_done:
            print('clearing stuff becuase isdone')
            # set cart status to submitted
            cart_obj.shopCartStatus = 'Submitted'
            cart_obj.save()
            sale_obj.mark_paid()
            request.session['cart_count'] = 0
            # clear items from user cart if authenticated
            if request.user.is_authenticated:
                # remove items from cart
                is_empty = cart_obj.empty_shopcart()
                print(is_empty)

            return redirect('shopcart:success')

    context = {
        "cart_obj": cart_obj,
        "sale_obj": sale_obj,
        "shopcart": cart_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "coupon_form": coupon_form,
        "address_qs": address_qs,
        "discount_qs": discount_qs,
    }
    return render(request, 'shopcart/checkout.html', context)

def checkout_done_view(request):
    """ final checkout complete page, thank you for your order! """
    return render(request, 'shopcart/checkout-done.html', {})
