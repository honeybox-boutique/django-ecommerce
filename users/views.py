from django.shortcuts import render
from django.views.generic import FormView, CreateView
from .forms import SignUpForm
# Create your views here.

def dashboard(request):
    return render(request, 'users/dashboard.html')

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url='/users/login/?next=/'