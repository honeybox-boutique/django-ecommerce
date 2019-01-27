from django import forms
from purchases.models import PurchaseItems

class ProductSizeColorForm(forms.ModelForm):
    class Meta:
        model = PurchaseItems
        fields = ('piColor', 'piSize')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['piSize'].queryset = PurchaseItems.objects.none()