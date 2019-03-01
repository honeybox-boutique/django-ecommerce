from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    # send_promos = forms.BooleanField(required=False, initial=True, label='Send me emails about new HoneyBox Boutique Products')
    class Meta:
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")
        model = User
        labels = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
            'first_name': '',
            'last_name': '',
        }
        help_texts = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
            'first_name': '',
            'last_name': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username*'})
        self.fields["email"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email*'})
        self.fields["first_name"].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields["last_name"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields["password1"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password*'})
        self.fields["password2"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Reenter Password*'})
        self.fields["email"].help_text = None
        self.fields["first_name"].help_text = None
        self.fields["last_name"].help_text = None
        # self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None
class UserAccountInfoForm(forms.ModelForm):
    
    username = forms.CharField(disabled=True, label='Username')
    email = forms.CharField(disabled=True, label='Email')
    # send_promos = forms.BooleanField(required=False, initial=True, label='Send me emails about new HoneyBox Boutique Products')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        help_texts = {
            'username': None,
            'email': None,
        } 

class GuestForm(forms.Form):
    email = forms.EmailField(label='')
    # send_promos = forms.BooleanField(required=False, initial=True, label='Sign me up for HoneyBox Boutique emails (you can unsubscribe at any time).')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email*'})
        # self.fields["send_promos"].widget.attrs.update({'class': 'form-control', 'align': 'left',})

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
