from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    class Meta:
        fields = ("email", "password1", "password2", "first_name", "last_name")
        model = User
        labels = {
            'email': '',
            'password1': '',
            'password2': '',
            'first_name': '',
            'last_name': '',
        }
        help_texts = {
            'email': '',
            'password1': '',
            'password2': '',
            'first_name': '',
            'last_name': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
