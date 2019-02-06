from django import forms

from pricing.models import SDiscount

class SDiscountForm(forms.ModelForm):
    sobj = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = SDiscount
        fields = (
            'sDiscountCouponCode',
        )