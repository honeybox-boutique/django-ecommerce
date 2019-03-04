from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from addresses.forms import AddressForm
from .forms import CardIDForm

from .models import BillingProfile, Card
from addresses.models import Address
from sales.models import Sale
from shopcart.models import ShopCart

import stripe
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
STRIPE_PUB_KEY = settings.STRIPE_PUB_KEY
stripe.api_key = STRIPE_SECRET_KEY


# Create your views here.
def payment_method_view(request):
    if request.user.is_authenticated:
        billing_profile = request.user.billingprofile
        customer_id = billing_profile.billingToken
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
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
        if form.is_valid():
            instance = form.save(commit=False)
            remember = form.cleaned_data.get('remember_address')
            if billing_profile:
                instance.addressBillingProfile = billing_profile
                instance.addressType = 'billing'
                instance.save()


                request.session[instance.addressType + "_address_id"] = instance.id
                token = request.POST.get('token')
                if token:
                    new_card_obj, new_card_error = Card.objects.add_new(billing_profile, token, instance, remember)
                    if new_card_obj:
                        sale_obj.salePaymentCard = new_card_obj
                        sale_obj.saleBillingAddress = instance
                        sale_obj.save()
                        return JsonResponse({'message': 'Success! Your card was added.'})
                    else:
                        print('deleted address')
                        form.instance.delete()
                        del request.session['billing_address_id']
                        return JsonResponse({'message': str(new_card_error)})



    elif request.method == 'POST':
        form = CardIDForm(request.POST or None)
        if form.is_valid():
            card = form.cleaned_data['cID']
            if card:
                # get card_obj
                # change: add try thing for error handling?
                card_obj = Card.objects.get(
                    id=card,
                    billingProfile=billing_profile,
                    cardActive=True,
                )
                # add card to sale
                sale_obj.salePaymentCard = card_obj
                # add corresponding address to sale
                billing_address_qs = Address.objects.filter(
                    addressBillingProfile=billing_profile,
                    addressLine1=card_obj.cardAddressLine1,
                    addressLine2=card_obj.cardAddressLine2,
                    addressCity=card_obj.cardCity,
                    addressState=card_obj.cardState,
                    addressPostalCode=card_obj.cardPostalCode,
                    addressName=card_obj.cardName,
                )
                if billing_address_qs.count() == 1:
                    print('found address')
                    # add address to sale
                    sale_obj.saleBillingAddress = billing_address_qs.first()
                    # save sale
                    sale_obj.save()
                else:
                    print('no matching address')
                return redirect('shopcart:checkout')
            else:
                return redirect('shopcart:home')
        else:
            pass
    return HttpResponse('error', status_code=401)
