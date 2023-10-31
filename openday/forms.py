from django.forms import ModelForm
from .models import *

class IscrizioniForm(ModelForm):
    class Meta:
       model = Visitatori
       fields = ['cognome','nome','email','comune','scuola']
       labels = {'comune': 'Comune di provenienza', 'scuola': 'Scuola di provenienza'}
       error_messages = {
            'cognome': {
                'required': "Campo obbligatorio.",
                'invalid': "Valore non valido.",
            },
            'nome': {
                'required': "Campo obbligatorio.",
                'invalid': "Valore non valido.",
            },
             'comune': {
                'required': "Campo obbligatorio.",
                'invalid': "Valore non valido.",
            }
        }
