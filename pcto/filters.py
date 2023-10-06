import django_filters
from django_filters import CharFilter
from .models import *

class AziendeFilter(django_filters.FilterSet):
    ragione_sociale = CharFilter(field_name="ragione_sociale",lookup_expr="icontains")
    comune = CharFilter(field_name="comune",lookup_expr="icontains")
    provincia = CharFilter(field_name="provincia",lookup_expr="icontains")
    codice_ateco = CharFilter(field_name="codice_ateco",lookup_expr="icontains")
    class Meta:
        model = Aziende
        fields = []
    