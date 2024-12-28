import django_filters
from django_filters import CharFilter
from .models import *
from django.db.models.functions import Lower

class AziendeFilter(django_filters.FilterSet):
    ragione_sociale = CharFilter(field_name="ragione_sociale",lookup_expr="icontains")
    comune = CharFilter(field_name="comune",lookup_expr="icontains")
    provincia = CharFilter(field_name="provincia",lookup_expr="icontains")
    codice_ateco = CharFilter(field_name="codice_ateco",lookup_expr="icontains")
    class Meta:
        model = Aziende
        fields = []


class AziendeViewFilter(django_filters.FilterSet):
    ragione_sociale = django_filters.CharFilter(
        lookup_expr='icontains', 
        field_name='ragione_sociale',
        label='Ragione Sociale'
    )
    comune = django_filters.ChoiceFilter(
        label='Comune',
        choices=[(comune['comune'], comune['comune']) for comune in 
                 Aziende.objects
                 .values('comune')  # Seleziona solo i valori distinti
                 .distinct()
                 .order_by('comune')],  # Ordina in modo alfabetico ignorando il case
    )
    provincia = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Aziende
        fields = ['ragione_sociale','comune']  # Qui puoi aggiungere altri campi da filtrare se necessario

    