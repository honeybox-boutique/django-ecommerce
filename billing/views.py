from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

import stripe
stripe.api_key = "***REMOVED***"
STRIPE_PUB_KEY = '***REMOVED***'

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

    return render(request, 'billing/payment-method.html', {
        'publish_key': STRIPE_PUB_KEY,
        'next_url': next_url,
        })



def payment_method_create_view(request):
    if request.method == 'POST' and request.is_ajax():
        print(request.POST)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        print(billing_profile.billingToken)
        if not billing_profile:
            print('no billing profile')
            return redirect('shopcart:home')
        token = request.POST.get('token')
        if token is not None:
            customer = stripe.Customer.retrieve(billing_profile.billingToken)
            card_respone = customer.sources.create(source=token)
            new_card_obj = Card.objects.add_new(billing_profile, card_respone)
            print(new_card_obj)
            return JsonResponse({'message': 'Done'})
    return HttpResponse('error', status_code=401)