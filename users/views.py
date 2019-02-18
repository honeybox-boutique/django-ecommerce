from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, CreateView, ListView
from django.forms import modelformset_factory, inlineformset_factory
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from sales.models import Sale
from .forms import SignUpForm, GuestForm, UserAccountInfoForm
from django.contrib.auth import authenticate, login, logout
from django.utils.http import is_safe_url
from django.contrib.auth import views as auth_views

from .models import Guest
# Create your views here.

def dashboard(request):
    user_obj = request.user
    data = {
        'username': user_obj.username,
        'first_name': user_obj.first_name,
        'last_name': user_obj.last_name,
        'email': user_obj.email,
    }
    if request.method == 'POST':
        form = UserAccountInfoForm(request.POST, instance=user_obj or None)
        if form.is_valid():
            # get cleaned_data and save to user
            # username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            # user_obj.username = username
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            print('changed some stuff')
            user_obj.save()
    else:
        form = UserAccountInfoForm(initial=data)

    context = {
        'form': form,
    }
    return render(request, 'users/dashboard.html', context)

class DashboardAddressListView(ListView):
    model = Address
    template_name = 'users/dashboard_address.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.request.user
        billing_profile = user_obj.billingprofile
        address_qs = Address.objects.filter(addressBillingProfile=billing_profile)
        context['address_list'] = address_qs
        return context

def dashboard_addresses(request):
    user_obj = request.user
    billing_profile = user_obj.billingprofile
    address_qs = Address.objects.filter(addressBillingProfile=billing_profile)
    next_post = None  
    # form = AddressForm()
    AddressFormSet = inlineformset_factory(BillingProfile, Address, form=AddressForm, extra=0)
    if request.method == 'POST':
        # move this to template as include
        formset = AddressFormSet(request.POST, instance=billing_profile or None)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        # get cleaned_data and save to user
                        instance = form.save(commit=False)
                        # address_line_1 = formset.cleaned_data.get('addressLine1')
                        # address_line_2 = formset.cleaned_data.get('addressLine2')
                        # address_city = formset.cleaned_data.get('addressCity')
                        # address_country = formset.cleaned_data.get('addressCountry')
                        # address_state = formset.cleaned_data.get('addressState')
                        # address_postal_code = formset.cleaned_data.get('addressPostalCode')
                        # address_type = formset.cleaned_data.get('addressType')
                        print(instance.addressLine2)
                        # instance.addressType = address_type
                        print('changed some stuff')
                        instance.save()
    else:
        print('making formset')
        formset = AddressFormSet(instance=billing_profile)
        # form = AddressForm(initial=data)

    context = {
        'formset': formset,
        'address_qs': address_qs,
    }
    return render(request, 'users/dashboard_addresses.html', context)

def dashboard_payment_methods(request):
    return render(request, 'users/dashboard_payment_methods.html')

class DashboardOrderListView(ListView):
    model = Sale
    template_name = 'users/dashboard_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.request.user
        billing_profile = user_obj.billingprofile
        sale_qs = Sale.objects.filter(saleBillingProfile=billing_profile).exclude(saleStatus='created')
        # address_qs = Address.objects.filter(addressBillingProfile=billing_profile)
        context['sale_list'] = sale_qs
        return context

def dashboard_orders(request):
    return render(request, 'users/dashboard_orders.html')

class PasswordResetView(auth_views.PasswordResetView):

    def get_success_url(self):
        return reverse('users:password_reset_done')

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_arg = self.kwargs.get('next')
        if is_safe_url(next_arg, self.request.get_host()):
            context['next'] = next_arg
        else:
            context['next'] = '/'
        return context

    def get_success_url(self):
        next_get = self.kwargs.get('next')
        next_post = self.request.POST['next']
        if is_safe_url(next_post, self.request.get_host()):
            success_url = next_post
        elif is_safe_url(next_get, self.request.get_host()):
            success_url = next_get
        else:
            success_url = '/'
        return success_url


    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        if new_user is not None:
            login(self.request, new_user)
        return valid

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form,
    }
    next_post = request.POST['next']
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = Guest.objects.create(guestEmail=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(next_post, request.get_host()):
            return redirect(next_post)
        else:
            redirect('users/signup')
    return redirect('users/signup')
