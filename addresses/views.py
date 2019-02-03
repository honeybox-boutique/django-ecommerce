from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

# Create your views here.
from .forms import AddressForm
from billing.models import BillingProfile

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form,
    }
    next_post = request.POST['next']
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)

        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('addressType')
            print(address_type)
            instance.addressBillingProfile = billing_profile
            instance.addressType = address_type
            instance.save()


            request.session[address_type + "_address_id"] = instance.id
            # print(address_type + '_address_id')
            billing_address_id = request.session.get('billing_address_id', None)
            shipping_address_id = request.session.get('shipping_address_id', None)

        else:
            print('address error of some kind')
            return redirect('shopcart:checkout')
        if is_safe_url(next_post, request.get_host()):
            return redirect(next_post)
        else:
            redirect('shopcart:checkout')
    return redirect('shopcart:checkout')