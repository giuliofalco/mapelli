import django_filters
from django_filters import CharFilter, ModelChoiceFilter
from .models import *
from django import forms

class EnteSelectWidget(forms.Select):
    def __init__(self, *args, **kwargs):
        super(EnteSelectWidget, self).__init__(*args, **kwargs)
        # Recupera le voci distinte dal campo 'ente' del modello
        ente_choices = Proposte.objects.values_list('ente', flat=True).distinct().order_by('ente')
        # Crea le opzioni per il widget
        self.choices = [(value, value) for value in ente_choices]

class ProposteFilter(django_filters.FilterSet):
    nome_progetto = CharFilter(field_name="nome_progetto",lookup_expr="icontains",label='Proposta ')
    ente = CharFilter(field_name="ente",lookup_expr="icontains",label='Ente ',widget=EnteSelectWidget)
  
    indirizzo = ModelChoiceFilter(field_name='indirizzo',queryset=Indirizzi.objects.all(),label='Indirizzo ')
    tipologia = ModelChoiceFilter(field_name='tipologia',queryset=Tipologie_proposte.objects.all(),label='Tipologia ')
    
    class Meta:
        model = Proposte
        fields = ['nome_progetto','indirizzo','tipologia','ente']