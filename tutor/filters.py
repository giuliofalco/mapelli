import django_filters
from django_filters import CharFilter, ModelChoiceFilter
from .models import *

class ProposteFilter(django_filters.FilterSet):
    nome_progetto = CharFilter(field_name="nome_progetto",lookup_expr="icontains",label='Proposta ')
    ente = CharFilter(field_name="ente",lookup_expr="icontains",label='Ente ')
    indirizzo = ModelChoiceFilter(field_name='indirizzo',queryset=Indirizzi.objects.all(),label='Indirizzo ')
    tipologia = ModelChoiceFilter(field_name='tipologia',queryset=Tipologie_proposte.objects.all(),label='Tipologia ')
    
    class Meta:
        model = Proposte
        fields = ['nome_progetto','indirizzo','tipologia']