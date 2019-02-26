from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# username
# password
# email
# first_name
# last_name
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', )

class UserAccountInfoForm(forms.ModelForm):
    
    username = forms.CharField(disabled=True, label='Username')
    email = forms.CharField(disabled=True, label='Email')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        help_texts = {
            'username': None,
            'email': None,
        } 

class GuestForm(forms.Form):
    email = forms.EmailField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
