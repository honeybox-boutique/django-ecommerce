from django import forms
from purchases.models import PurchaseItems

class ProductSizeColorForm(forms.ModelForm):
    class Meta:
        model = PurchaseItems
        fields = ('piColor', 'piSize')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['piSize'].queryset = PurchaseItems.objects.none()


class CartRemoveItemForm(forms.Form):
    prod = forms.CharField(widget=forms.HiddenInput(), required=True)

class EditSaleForm(forms.Form):
    sale = forms.CharField(widget=forms.HiddenInput(), required=True)