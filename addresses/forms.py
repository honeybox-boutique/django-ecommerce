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