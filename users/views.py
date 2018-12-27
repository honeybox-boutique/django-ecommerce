from django.shortcuts import render
from django.views.generic import FormView, CreateView
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def dashboard(request):
    return render(request, 'users/dashboard.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/signup.html'
    success_url='/users/login/?next=/'