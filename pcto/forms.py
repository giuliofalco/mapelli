from datetime import date
from django import forms
from pcto.models import *

class DateInput(forms.DateInput):
    input_type='date'

class ContactForm(forms.Form):
    azienda = forms.CharField(label='Azienda (piva)', max_length=100)
    tutor   = forms.ModelChoiceField(label='Tutor', queryset=Tutor.objects.all(), empty_label=None)
    periodo_da = forms.DateField(label='Da',widget=DateInput, required=False)
    periodo_a = forms.DateField(label='A',widget=DateInput,required=False)
    num_studenti = forms.IntegerField(label='num. studenti',required=False)
    note = forms.CharField(widget=forms.Textarea,required=False)

