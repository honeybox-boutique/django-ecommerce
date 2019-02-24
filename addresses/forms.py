from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'addressLine1',
            'addressLine2',
            'addressCity',
            'addressCountry',
            'addressState',
            'addressPostalCode',
        )
        labels = {
            'addressLine1': 'Address',
            'addressLine2': 'Apt., Suite, Etc.',
            'addressCity': 'City',
            'addressCountry': 'Country',
            'addressState': 'State',
            'addressPostalCode': 'Zip',
        }