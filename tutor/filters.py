import django_filters
from django_filters import CharFilter, ModelChoiceFilter
from .models import *

class ProposteFilter(django_filters.FilterSet):
    nome_progetto = CharFilter(field_name="nome_progetto",lookup_expr="icontains")
    ente = CharFilter(field_name="ente",lookup_expr="icontains")
    indirizzo = ModelChoiceFilter(field_name='indirizzo',queryset=Indirizzi.objects.all())
    tipologia = ModelChoiceFilter(field_name='tipologia',queryset=Tipologie_proposte.objects.all())
    
    class Meta:
        model = Proposte
        fields = ['nome_progetto','indirizzo','tipologia']