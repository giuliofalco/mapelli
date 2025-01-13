from django import forms
from .models import *

class DayEntryForm(forms.ModelForm):
    class Meta:
        model = DayEntry
        fields = ['assenze', 'eventi','uscite','note']
        widgets = {
            'assenze': forms.Textarea(attrs={'rows': 28, 'cols': 10}),
            'eventi': forms.Textarea(attrs={'rows': 28, 'cols': 10}),
            'uscite': forms.Textarea(attrs={'rows': 28, 'cols': 10}),
            'note': forms.Textarea(attrs={'rows': 28, 'cols': 10}),
        }
