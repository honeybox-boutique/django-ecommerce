from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    cardBrand = forms.CharField(disabled=True, label='Brand')
    cardLast4 = forms.CharField(disabled=True, label='Last 4 #')

    class Meta:
        model = Card
        fields = (
            'cardBrand',
            'cardLast4',
        )

class BaseCardFormSet(forms.models.BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseCardFormSet, self).add_fields(form, index)
        form.fields['DELETE'].label = 'Are you sure?'

class CardIDForm(forms.ModelForm):
    cID = forms.CharField()
    class Meta:
        model = Card
        fields = (
            'cardBrand',
        )