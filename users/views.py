from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, CreateView, ListView, DetailView
from django.forms import inlineformset_factory, modelformset_factory
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile, Card
from billing.forms import CardForm, BaseCardFormSet
from sales.models import Sale
from .forms import SignUpForm, GuestForm, UserAccountInfoForm
from django.contrib.auth import authenticate, login, logout, mixins, views
from django.utils.http import is_safe_url
from django.contrib.auth import views as auth_views

from .models import Guest
# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
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
    if not request.user.is_authenticated:
        return redirect('users:login')
    user_obj = request.user
    billing_profile = user_obj.billingprofile
    address_qs = Address.objects.filter(addressBillingProfile=billing_profile,
        addressActive=True,
    )
    # Make formset for Addresses
    AddressFormSet = inlineformset_factory(BillingProfile, Address, form=AddressForm, extra=1, can_delete=True)
    if request.method == 'POST':
        # move this to template as include
        formset = AddressFormSet(request.POST or None, instance=billing_profile)
        # form = NewAddressForm(request.POST or None, instance=billing_profile)
        if formset.is_valid() :
            for form in formset:
                if form.is_valid():
                    # check if form was filled out
                    if form.cleaned_data.get('addressLine1'):
                        if form.cleaned_data.get('DELETE') and form.instance.pk:
                            form.instance.addressActive = False
                            form.instance.save()
                        else:
                            # get cleaned_data and save to user
                            instance = form.save(commit=False)
                            if not instance.addressType:
                                instance.addressType = 'shipping'
                            instance.save()
            
        return redirect('users:dashboard_addresses')
    else:
        formset = AddressFormSet(queryset=address_qs, instance=billing_profile)

    context = {
        'formset': formset,
        'address_qs': address_qs,
    }
    return render(request, 'users/dashboard_addresses.html', context)

def dashboard_payment_methods(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    # stripe stuff
    from django.conf import settings
    import stripe
    STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
    STRIPE_PUB_KEY = settings.STRIPE_PUB_KEY
    stripe.api_key = STRIPE_SECRET_KEY

    #next url stuff
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    
    #get user and billingprofile
    user_obj = request.user
    billing_profile = user_obj.billingprofile
    # get active cards associated with billing profile
    card_qs = Card.objects.filter(
        billingProfile=billing_profile,
        cardActive=True,
    )
    # Make formset for Addresses
    CardFormSet = inlineformset_factory(BillingProfile, Card, form=CardForm, formset=BaseCardFormSet, extra=0, can_delete=True)
    if request.method == 'POST':
        # move this to template as include
        formset = CardFormSet(request.POST or None, instance=billing_profile)
        # form = NewAddressForm(request.POST or None, instance=billing_profile)
        if formset.is_valid() :
            for form in formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.cardActive = False
                        form.instance.save()
            
        return redirect('users:dashboard_payment_methods')
    else:
        formset = CardFormSet(instance=billing_profile, queryset=card_qs)
        address_form = AddressForm(instance=billing_profile)

    context = {
        'formset': formset,
        'address_qs': card_qs,
        'address_form': address_form,
        'publish_key': STRIPE_PUB_KEY,
        'next_url': next_url,
    }
    return render(request, 'users/dashboard_payment_methods.html', context)
class DashboardCardListView(mixins.LoginRequiredMixin, ListView):
    model = Card
    template_name = 'users/dashboard_payment_methods.html'

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # user_obj = self.request.user
        # billing_profile = user_obj.billingprofile
        # sale_qs = Sale.objects.filter(saleBillingProfile=billing_profile).exclude(saleStatus='created')
        # # address_qs = Address.objects.filter(addressBillingProfile=billing_profile)
        # context['sale_list'] = sale_qs
        # return context

class DashboardOrderListView(mixins.LoginRequiredMixin, ListView):
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

class DashboardOrderDetailView(mixins.LoginRequiredMixin, DetailView):
    model = Sale
    context_object_name = 'sale'
    template_name = 'users/dashboard_order_detail.html'

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # # # address_qs = Address.objects.filter(addressBillingProfile=billing_profile)
        # # context['sale_list'] = sale_qs
        # return context

def dashboard_orders(request):
    return render(request, 'users/dashboard_orders.html')

class PasswordResetView(auth_views.PasswordResetView):

    def get_success_url(self):
        return reverse('users:password_reset_done')

class CustomLoginView(views.LoginView):

    def form_valid(self, form):
        """ Override to clear guest_session_id """
        valid = super(CustomLoginView, self).form_valid(form)
        # delete session thing
        if 'guest_email_id' in self.request.session:
            del self.request.session['guest_email_id']

        return valid

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
        # send_promos = form.cleaned_data.get("send_promos")
        new_guest_email = Guest.objects.create(
            guestEmail=email,
            # guestSendPromos=send_promos,
        )
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(next_post, request.get_host()):
            return redirect(next_post)
        else:
            redirect('users/signup')
    return redirect('users/signup')
