from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import CartRemoveItemForm, EditSaleForm, CustomerShipMethodForm, AddToCartForm
from users.forms import LoginForm, GuestForm, SignUpForm
from addresses.forms import AddressForm
from coupons.forms import SDiscountForm
from billing.models import BillingProfile
from .models import ShopCart, PurchaseItems
from users.models import Guest
from sales.models import Sale, SaleItems
from addresses.models import Address
from pricing.models import SDiscount

import stripe
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
STRIPE_PUB_KEY = settings.STRIPE_PUB_KEY
stripe.api_key = STRIPE_SECRET_KEY

def cart_home(request):
    """ Displays cart contents """
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)
    request.session['cart_count'] = cart_obj.shopCartItems.count()

    context = {
        "shopcart": cart_obj,
    }
    return render(request, 'shopcart/home.html', context)

def cart_remove_item(request):
    """ removes prodStockItem from cart """
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)
    form = CartRemoveItemForm(request.POST)

    if form.is_valid():
        prod_stock_id = form.cleaned_data.get('prod')
        prod_stock_obj = PurchaseItems.objects.get(prodStockID=prod_stock_id)
        cart_obj.shopCartItems.remove(prod_stock_obj)


    request.session['cart_count'] = cart_obj.shopCartItems.count()
    return redirect('shopcart:home')

def cart_update(request):
    """ should use product-slug, color, and size as parameters to check if:
        purchitem with matching slug, color, and size exists,
    """
    # get cart
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)
    # change: maybe? clean these parameters using form method
    if request.method == 'POST':
        cart_form = AddToCartForm(request.POST or None)
        if cart_form.is_valid():
            product_slug = cart_form.cleaned_data.get('product_slug')
            color = cart_form.cleaned_data.get('color_selection')
            size = cart_form.cleaned_data.get('size_selection')
            # quantity = request.POST.get('quantity')

            # add to cart--------------------------------------------------------------------------------

            # query for purchaseitems available
            purchase_item_query = PurchaseItems.objects.filter(
                productID__productSlug=product_slug,
                piColor__colorName=color,
                piSize=size,
                piIsAvailable=True
            )
            # exclude all pitems already in cart
            for cart_item in cart_obj.shopCartItems.all():
                purchase_item_query = purchase_item_query.exclude(pk=cart_item.pk)


            if not purchase_item_query:
                messages.warning(request, 'Not enough items in stock to add items to cart.')
                request.session['cart_count'] = cart_obj.shopCartItems.count()
                # redirect to same page with error message in context
                return redirect(request.META.get('HTTP_REFERER', 'shopcart:home'))
            else:
                messages.success(request, 'Item added to cart!')
                purchase_item_obj = purchase_item_query.first()
                cart_obj.shopCartItems.add(purchase_item_obj)
                request.session['cart_count'] = cart_obj.shopCartItems.count()
                return redirect(request.META.get('HTTP_REFERER', 'shopcart:home'))


# view that clears sale shipping or billing address on breadcrumb click
def edit_shipping(request):
    """ removes prodStockItem from cart """
    form = EditSaleForm(request.POST)

    if form.is_valid():
        sale_id = form.cleaned_data.get('sale')
        sale_obj = Sale.objects.get(saleID=sale_id)
        if sale_obj.saleStatus == 'created':
            sale_obj.saleShippingAddress = None
            sale_obj.save()
    return redirect('shopcart:checkout')

def edit_ship_method(request):
    """ removes ship method selection from sale """
    form = EditSaleForm(request.POST)

    if form.is_valid():
        sale_id = form.cleaned_data.get('sale')
        sale_obj = Sale.objects.get(saleID=sale_id)
        if sale_obj.saleStatus == 'created':
            sale_obj.customerShipMethodID = None
            sale_obj.save()
    return redirect('shopcart:checkout')


def edit_billing(request):
    """ removes billing address from sale """
    form = EditSaleForm(request.POST)

    if form.is_valid():
        sale_id = form.cleaned_data.get('sale')
        sale_obj = Sale.objects.get(saleID=sale_id)
        if sale_obj.saleStatus == 'created':
            sale_obj.saleBillingAddress = None
            sale_obj.save()
    return redirect('shopcart:checkout')

def edit_card(request):
    """ removes payment card and billing address from sale """
    form = EditSaleForm(request.POST)

    if form.is_valid():
        sale_id = form.cleaned_data.get('sale')
        sale_obj = Sale.objects.get(saleID=sale_id)
        if sale_obj.saleStatus == 'created':
            sale_obj.salePaymentCard = None
            sale_obj.saleBillingAddress = None
            sale_obj.save()
    return redirect('shopcart:checkout')

def ship_method(request):
    """ Removes shipping method from sale """
    form = CustomerShipMethodForm(request.POST)

    if form.is_valid():
        ship_method_id = form.cleaned_data.get('customerShipMethodID')
        sale_id = form.cleaned_data.get('sale')
        # get sale obj
        sale_obj = Sale.objects.get(saleStringID=sale_id)
        sale_obj.customerShipMethodID = ship_method_id
        sale_obj.save()
    return redirect('shopcart:checkout')

def checkout_home(request):
    cart_obj, cart_created = ShopCart.objects.get_or_new(request)# get cart
    cart_items = cart_obj.shopCartItems.all()
    login_form = LoginForm()
    guest_form = GuestForm()
    signup_form = SignUpForm()
    address_form = AddressForm()
    edit_form = EditSaleForm()
    #initializers
    sale_obj = None
    address_qs = None
    discount_qs = None
    card_qs = None
    coupon_form = None
    ship_method_form = None
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    if cart_created or cart_items.count() == 0:# if cart was just created redirect to cart home
        return redirect('shopcart:home')

    # first check if cart_items are available
    for item in cart_items:
        if item.piIsAvailable == False:
            messages.warning(request, 'An item in your cart has become unavailable and was removed. This does not necessarily mean we are out of stock. Please attempt to add it back to cart to verify.')
            cart_obj.shopCartItems.remove(item)
            # if sale was already created remove the item from the sale as well
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if billing_profile is not None:
                # remove item from sale
                sale_item = SaleItems.objects.filter(
                    prodStockID=item.prodStockID,
                    saleID__saleStatus='created',
                    saleID__saleBillingProfile=billing_profile
                )
                sale_item.delete()
                return redirect('shopcart:home')

    # get billing profile
    has_card = False
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        address_qs = Address.objects.filter(addressBillingProfile=billing_profile,
            addressActive=True,
        )
        # create sale
        sale_obj, sale_obj_created = Sale.objects.new_or_get(billing_profile, cart_obj)
        # initialize coupon form with sale object
        coupon_form = SDiscountForm(initial={'sobj': sale_obj.saleStringID})
        ship_method_form = CustomerShipMethodForm(initial={'sale': sale_obj.saleStringID})
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
        has_card = billing_profile.has_card
        card_qs = billing_profile.get_cards()
        

    
    if request.method == 'POST':
        '''check if sale is done'''
        is_done = sale_obj.check_done()
        if not is_done:
            pass
        elif is_done:
            did_charge, charge_msg = billing_profile.charge(sale_obj)
            if did_charge:
                # set cart status to submitted
                cart_obj.shopCartStatus = 'Submitted'
                cart_obj.save()
                sale_obj.mark_paid()

                from_email = getattr(settings, 'EMAIL_HOST_ALIAS_SUPPORT', settings.EMAIL_HOST_USER)
                # # send order confirmation email
                to_email = str(sale_obj.saleBillingProfile)
                html_message = render_to_string('emails/order-confirmation.html', {
                    'sale_obj': sale_obj,
                    })
                plain_message = strip_tags(html_message)
                subject = 'HoneyBox Boutique - Order Confirmation %s' % (sale_obj.saleStringID)
                send_mail(subject, plain_message, from_email, [to_email], auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD, html_message=html_message)

                # clear guest_email_id from session

                if 'guest_email_id' in request.session:
                    del request.session['guest_email_id']
                    if not billing_profile.user:
                        billing_profile.set_inactive()
                # clear carts session stuff
                request.session['cart_count'] = 0
                # clear items from user cart if authenticated
                is_empty = cart_obj.empty_shopcart()

                return redirect('shopcart:success')
            else:
                # add error message here
                messages.warning(request, charge_msg)
                return redirect('shopcart:checkout')

    context = {
        "cart_obj": cart_obj,
        "sale_obj": sale_obj,
        "shopcart": cart_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "signup_form": signup_form,
        "address_form": address_form,
        "coupon_form": coupon_form,
        "edit_form": edit_form,
        "ship_method_form": ship_method_form,
        "address_qs": address_qs,
        "discount_qs": discount_qs,
        "card_qs": card_qs,
        "publish_key": STRIPE_PUB_KEY,
        "has_card": has_card,
    }
    return render(request, 'shopcart/checkout.html', context)

def checkout_done_view(request):
    """ final checkout complete page, thank you for your order! """
    return render(request, 'shopcart/checkout-done.html', {})
