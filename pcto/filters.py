import django_filters
from django_filters import CharFilter
from .models import *

class AziendeFilter(django_filters.FilterSet):
    ragione_sociale = CharFilter(field_name="ragione_sociale",lookup_expr="icontains")
    sede_comune = CharFilter(field_name="sede_comune",lookup_expr="icontains")
    sede_provincia = CharFilter(field_name="sede_provincia",lookup_expr="icontains")
    settore = CharFilter(field_name="settore",lookup_expr="icontains")
    class Meta:
        model = Aziende
        fields = []
    