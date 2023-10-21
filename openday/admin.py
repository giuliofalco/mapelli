from django.contrib import admin
from .models import *

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['titolo','autore','data']


@admin.register(Eventi)
class EventiAdmin(admin.ModelAdmin):
    list_display = ['titolo','data','sigla','luogo','attivo']

@admin.register(Visitatori)
class VisitatoriAdmin(admin.ModelAdmin):
    list_display = ['cognome','nome','email','ruolo']

@admin.register(Iscrizioni)
class IscrizioniAdmin(admin.ModelAdmin):
    list_display = ['visitatore','evento','presente']