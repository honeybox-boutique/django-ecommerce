from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import stripe
stripe.api_key = "***REMOVED***"
STRIPE_PUB_KEY = '***REMOVED***'

# Create your views here.
def payment_method_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'billing/payment-method.html', {'publish_key': STRIPE_PUB_KEY})



def payment_method_create_view(request):
    if request.method == 'POST' and request.is_ajax():
        print(request.POST)
        return JsonResponse({'message': 'Done'})
    return HttpResponse('error', status_code=401)