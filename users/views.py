from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, CreateView
from .forms import SignUpForm, GuestForm
from django.contrib.auth import authenticate, login, logout
from django.utils.http import is_safe_url
from django.contrib.auth import views as auth_views

from .models import Guest
# Create your views here.

def dashboard(request):
    return render(request, 'users/dashboard.html')

def dashboard_addresses(request):
    return render(request, 'users/dashboard_addresses.html')

def dashboard_payment_methods(request):
    return render(request, 'users/dashboard_payment_methods.html')

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
        print(self.kwargs.get('next'))
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
