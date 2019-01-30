from django import forms
from .models import PurchaseItems, Purchase

class PurchaseItemsForm(forms.ModelForm):
    class Meta:
        model = PurchaseItems
        fields = ('productID', 'vendorID', 'piPrice', 'piColor', 'piSize', 'piCondition', 'piNotes')

PurchaseItemsFormSet = forms.inlineformset_factory(Purchase,
                                                   PurchaseItems,
                                                   fields=('productID', 'vendorID', 'piPrice',
                                                           'piColor', 'piCondition', 'piNotes'))

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('userID', 'purchaseDate',
                  'purchaseStatus', 'purchaseNote')
