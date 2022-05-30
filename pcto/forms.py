from django import forms
from pcto.models import *

class ContactForm(forms.Form):
    azienda = forms.CharField(label='Azienda (piva)', max_length=100, widget=forms.HiddenInput())
    tutor   = forms.ModelChoiceField(label='Tutor', queryset=Tutor.objects.all(), empty_label=None)
    periodo_da = forms.DateField(label='Da')
    periodo_a = forms.DateField(label='A')
    num_studenti = forms.IntegerField(label='num. studenti')
    note = forms.CharField(widget=forms.Textarea)

