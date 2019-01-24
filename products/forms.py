from django import forms
from purchases.models import PurchaseItems
from .models import Product, ProductColor

class ProductSizeColorForm(forms.ModelForm):
    class Meta:
        model = PurchaseItems
        fields = ('piColor', 'piSize')

    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # self.fields['piSize'].queryset = PurchaseItems.objects.none()


# class ProductColorForm(forms.ModelForm):
    # class Meta:
        # model = ProductColor
        # fields = ('colorID',)

# ProductColorFormSet = forms.inlineformset_factory(Product,
                                                  # ProductColor,
                                                  # fields=('productID',))

# class TransactionItemsForm(forms.ModelForm):
    # class Meta:
        # model = Transaction
        # fields = ('transactionTypeID', 'userID', 'transactionDate',
                  # 'transactionStatus', 'transactionNote')