from django.shortcuts import render, redirect

from users.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from .models import ShopCart, PurchaseItems
from users.models import Guest
from sales.models import Sale, SaleItems

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
    cart_items = cart_obj.shopCartItems.all()
    user = request.user
    sale_obj = None
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')

    if new_obj or cart_items.count() == 0:# if cart was just created redirect to cart home
        return redirect('shopcart:home')
    else:# cart is not new, begin checkout
        pass
    
    if user.is_authenticated:
        print('authenticated, getting profile')
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, billingEmail=user.email)
        print(billing_profile.id)
    elif guest_email_id is not None:
        guest_obj = Guest.objects.get(id=guest_email_id)
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(billingEmail=guest_obj.guestEmail)
        print(billing_profile.id)
    else:
        # change: do we need error raise here?
        pass

    if billing_profile is not None:
        sale_obj, sale_obj_created = Sale.objects.new_or_get(billing_profile, cart_items)

        # set cart status to submitted
        cart_obj.shopCartStatus = 'Submitted'
        cart_obj.save()
    else:
        print('no billing email on profile')


    context = {
        "sale_obj": sale_obj,
        "shopcart": cart_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
    }

    return render(request, 'carts/checkout.html', context)