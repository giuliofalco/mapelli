from django.contrib import admin
from .models import Tutor, Aziende, Contatti, Studenti, Abbinamenti, Storico

class AbbinamentiInline(admin.StackedInline):
    model = Abbinamenti
    #list_display = ['cognome','nome','classe']
    extra = 0
   
class ContattiInline(admin.StackedInline):
    model = Contatti
    fields = ['data','tutor','num_studenti','periodo_da','periodo_a','note']
    #inlines = [StudentiInline]
    extra = 0

@admin.register(Aziende)
class AziendeAdmin(admin.ModelAdmin):
    list_display = ['ragione_sociale','comune','provincia']
    inlines = [ContattiInline, AbbinamentiInline]

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['cognome','nome','email','classi']
    list_filter = ['cognome']

@admin.register(Storico)
class StoricoAdmin(admin.ModelAdmin):
    list_display = ['anno','ragione_sociale','classe', 'cognome','nome']
