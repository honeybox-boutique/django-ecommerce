from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from addresses.forms import AddressForm

import stripe
STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY', '***REMOVED***')
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', '***REMOVED***')
stripe.api_key = STRIPE_SECRET_KEY

from .models import BillingProfile, Card

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

    return render(request, 'billing/payment-method-form.html', {
        'address_form': address_form,
        'publish_key': STRIPE_PUB_KEY,
        'next_url': next_url,
        })



def payment_method_create_view(request):
    if request.method == 'POST' and request.is_ajax():
        form = AddressForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            print(request.POST)
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if billing_profile:
                instance.addressBillingProfile = billing_profile
                instance.addressType = 'billing'
                instance.save()


                request.session[instance.addressType + "_address_id"] = instance.id
                token = request.POST.get('token')
                if token is not None:
                    new_card_obj = Card.objects.add_new(billing_profile, token, instance)
                    return JsonResponse({'message': 'Done'})
            else:
                print('no billing profile')
                return redirect('shopcart:home')
    return HttpResponse('error', status_code=401)