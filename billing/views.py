from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from addresses.forms import AddressForm
from .forms import CardIDForm

from .models import BillingProfile, Card
from sales.models import Sale
from shopcart.models import ShopCart

import stripe
STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY', '***REMOVED***')
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', '***REMOVED***')
stripe.api_key = STRIPE_SECRET_KEY


# Create your views here.
def payment_method_view(request):
    if request.user.is_authenticated:
        billing_profile = request.user.billingprofile
        customer_id = billing_profile.billingToken
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        print('no billing profile')
        return redirect('shopcart:home')
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    address_form = AddressForm()

    return render(request, 'billing/existing-payment-method-form.html', {
        'address_form': address_form,
        'publish_key': STRIPE_PUB_KEY,
        'next_url': next_url,
        })



def payment_method_create_view(request):
    cart_obj, new_obj = ShopCart.objects.get_or_new(request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    # get sale_obj
    sale_obj, sale_obj_created = Sale.objects.new_or_get(billing_profile, cart_obj)
    if request.method == 'POST' and request.is_ajax():
        form = AddressForm(request.POST or None)
        print(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if billing_profile:
                instance.addressBillingProfile = billing_profile
                instance.addressType = 'billing'
                instance.save()


                request.session[instance.addressType + "_address_id"] = instance.id
                token = request.POST.get('token')
                if token:
                    print('new card')
                    new_card_obj = Card.objects.add_new(billing_profile, token, instance)
                    sale_obj.salePaymentCard = new_card_obj
                    sale_obj.save()
                    return JsonResponse({'message': 'Done'})


    elif request.method == 'POST':
        form = CardIDForm(request.POST or None)
        print(request.POST)
        if form.is_valid():
            card = form.cleaned_data['cID']
            print(card)
            if card:
                print('existing card')
                # get card_obj
                # change: add try thing for error handling?
                card_obj = Card.objects.get(
                    id=card,
                    billingProfile=billing_profile
                )
                # add card to sale
                sale_obj.salePaymentCard = card_obj
                # save sale
                sale_obj.save()
                return redirect('shopcart:checkout')
            else:
                print('unable to find card')
                return redirect('shopcart:home')
        else:
            print(form.errors)
    return HttpResponse('error', status_code=401)
