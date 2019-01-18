from django import forms
from .models import PurchaseItems, Transaction

class PurchaseItemsForm(forms.ModelForm):
    class Meta:
        model = PurchaseItems
        fields = ('productID', 'vendorID', 'piPrice', 'piColor', 'piSize', 'piCondition', 'piNotes')

PurchaseItemsFormSet = forms.inlineformset_factory(Transaction,
                                                   PurchaseItems,
                                                   fields=('productID', 'vendorID', 'piPrice',
                                                           'piColor', 'piCondition', 'piNotes'))

class TransactionItemsForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('transactionTypeID', 'userID', 'transactionDate',
                  'transactionStatus', 'transactionNote')
