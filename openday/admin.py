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

@admin.register(Indirizzi)
class IndirizziAdmin(admin.ModelAdmin):
    list_display = ['titolo']  

@admin.register(riga_orario)
class Admin(admin.ModelAdmin):
    list_display = ['indirizzo','materia']  

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['titolo','immagine', 'descrizione']