from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from django.views.generic import UpdateView
# Create your views here.
from .forms import AddressForm
from billing.models import BillingProfile
from addresses.models import Address


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)# change: check if you're using this
    context = {
        "form": form,
    }
    next_post = request.POST.get('next')
    if form.is_valid():
        instance = form.save(commit=False)

        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('addressType')
            remember_address = form.cleaned_data.get('remember_address')
            print(address_type)
            print(remember_address)
            instance.addressBillingProfile = billing_profile
            instance.addressType = address_type
            instance.addressActive = remember_address
            instance.save()


            request.session[address_type + "_address_id"] = instance.id

        else:
            print('address error of some kind')
            return redirect('shopcart:checkout')
        if is_safe_url(next_post, request.get_host()):
            return redirect(next_post)
        else:
            redirect('shopcart:checkout')
    return redirect('shopcart:checkout')

def checkout_address_reuse_view(request):
    form = AddressForm(request.POST or None)
    next_post = request.POST['next']
    if request.method == 'POST':
        print(request.POST)
        address = request.POST.get('address', None)
        address_type = request.POST.get('addressType')
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if address is not None:
            qs = Address.objects.filter(id=address, addressBillingProfile=billing_profile)
            if qs.exists():
                request.session[address_type + "_address_id"] = address
            if is_safe_url(next_post, request.get_host()):
                return redirect(next_post)
    return redirect('shopcart:checkout')