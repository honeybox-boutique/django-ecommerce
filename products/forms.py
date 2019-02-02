from django import forms
from purchases.models import PurchaseItems
from .models import Product, ProductColor

class ProductSizeColorForm(forms.ModelForm):
    class Meta:
        model = PurchaseItems
        fields = ('piColor', 'piSize')