from django import forms
from sales.models import Sale

class CustomerShipMethodForm(forms.ModelForm):
    sale = forms.CharField(widget=forms.HiddenInput(), required=True)
    class Meta:
        model = Sale
        fields = ('customerShipMethodID',)
        labels = {
            'customerShipMethodID': 'Shipping Method'
        }
        # change: widget to radio button

class CartRemoveItemForm(forms.Form):
    prod = forms.CharField(widget=forms.HiddenInput(), required=True)

class EditSaleForm(forms.Form):
    sale = forms.CharField(widget=forms.HiddenInput(), required=True)

class AddToCartForm(forms.Form):
    product_slug = forms.CharField()
    color_selection = forms.CharField()
    size_selection = forms.CharField()