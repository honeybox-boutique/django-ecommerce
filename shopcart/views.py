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
    order_obj = None
    billing_profile = None
    new_sale_obj = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')

    if new_obj or cart_items.count() == 0:# if cart was just created redirect to cart home
       redirect('shopcart:home')
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
    # add sale query that checks if this order was created
    # maybe filter on shopCartID? maybe on shopcartitems
    if billing_profile is not None:
        new_sale_obj = Sale(
                    saleBillingProfile=billing_profile,
                    saleStatus='created',
                    saleNote='default sale note',
                    saleSubTotal=cart_obj.shopCartSubTotal,
                    # saleDiscountAmount = ?
                    # saleSalesTaxAmount = ?
                    # saleShipCostAmountCharged = ?# change: default is 7.00 on models, change to calculation
                    # saleTotal=cart_obj.shopCartSubTotal# change: 
        )
        new_sale_obj.save()
        print(new_sale_obj.saleBillingProfile)
        for item in cart_items:
            # change: maybe add checking logic to make sure pricing is active, prodStockItems don't haven't been sold, etc.
            new_sale_item = SaleItems(
                            saleID=new_sale_obj,
                            prodStockID=item,
                            siBasePrice=item.productID.productBasePrice,
                            siDiscountAmount=item.productID.productDiscountAmount,
                            siSalePrice=item.productID.productSalePrice,
                            siNote=item.productID.productName
                        )
            new_sale_item.save()
    else:
        print('no billing email on profile')


    context = {
        "new_sale_obj": new_sale_obj,
        "shopcart": cart_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
    }

        # new_sale_obj = Sale(saleStatus='created', 
        # shop_cart_items = cart_obj.shopCartItems.all()
        # for item in shop_cart_items:
             # new_sale_obj.objects.add(saleItems=)
    return render(request, 'carts/checkout.html', context)