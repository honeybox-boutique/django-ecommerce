from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    remember_address = forms.BooleanField(required=False, initial=False, label='Remember this? (If you are not signed in with an account, this will not be remembered)')
    class Meta:
        model = Address
        fields = (
            'addressName',
            'addressLine1',
            'addressLine2',
            'addressCity',
            'addressCountry',
            'addressState',
            'addressPostalCode',
        )
        labels = {
            'addressName': 'Full Name',
            'addressLine1': 'Address',
            'addressLine2': 'Apt., Suite, Etc.',
            'addressCity': 'City',
            'addressCountry': 'Country',
            'addressState': 'State',
            'addressPostalCode': 'Zip',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["remember_address"].widget.attrs.update({'class': 'form-control', 'align': 'left',})

# class AddressFormProcessorForm(forms.Form):
    # addressName = forms.CharField()
    # addressLine1 = forms.CharField()
    # addressLine2 = forms.CharField()
    # addressCity = forms.CharField()
    # addressCountry= forms.CharField()
    # addressState = forms.CharField()
    # addressPostalCode = forms.CharField()
    # remember_address = forms.BooleanField()
    # addressType = forms.CharField()
