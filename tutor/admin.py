from django.contrib import admin
from .models import *

@admin.register(Tipologie_proposte)
class Tipologie_proposteAdmin(admin.ModelAdmin):
    list_display = ['id','denominazione']


@admin.register(Tipologie_ente)
class Tipologie_enteAdmin(admin.ModelAdmin):
    list_display = ['id','denominazione']

@admin.register(Indirizzi)
class IndirizziAdmin(admin.ModelAdmin):
    list_display = ['id','denominazione']

@admin.register(Classi)
class ClassiAdmin(admin.ModelAdmin):
    list_display = ['id','classe', 'indirizzo', 'num_studenti']

@admin.register(Studenti)
class StudentiAdmin(admin.ModelAdmin):
    list_display = ['id','nome' , 'cognome', 'classe']

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['cognome', 'nome' ]

@admin.register(Proposte)
class ProposteAdmin(admin.ModelAdmin):
    list_display = ['ente','tipo_ente','nome_progetto','data_inizio','url']