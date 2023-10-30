import django_filters
from django_filters import CharFilter
from .models import *

class IscrittiFilter(django_filters.FilterSet):
    cognome = CharFilter(field_name="visitatore__cognome",lookup_expr="icontains", label="Nome e Cognome")
    class Meta:
        model = Iscrizioni
        fields = []
    