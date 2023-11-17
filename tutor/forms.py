from django.forms import ModelForm
from .models import *

class AttivitaForm(ModelForm):
    class Meta:
       model = Attivita_tutor
       fields = ['data','titolo','tipologia', 'target', 'durata', 'descrizione']
       # labels = {}
       error_messages = {
            'titolo': {
                'required': "Campo obbligatorio.",
                'invalid': "Valore non valido.",
            },
            'durata': {
                'required': "Campo obbligatorio.",
                'invalid': "Valore non valido.",
            }
        }
