from django.forms import ModelForm
from .models import *

class IscrizioniForm(ModelForm):
    class Meta:
       model = Visitatori
       fields = ['cognome','nome','email','comune','scuola']
       labels = {'comune': 'Comune di provenienza', 'scuola': 'Scuola di provenienza'}
