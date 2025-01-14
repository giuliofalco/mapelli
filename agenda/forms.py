from django import forms
from .models import *

from ckeditor.widgets import CKEditorWidget
class DayEntryForm(forms.ModelForm):
    class Meta:
        model = DayEntry
        fields = ['assenze', 'eventi','uscite','note']
        widgets = {
            'assenze': CKEditorWidget(),
            'eventi': CKEditorWidget(),
            'uscite': CKEditorWidget(),
            'note':CKEditorWidget(),
        }
