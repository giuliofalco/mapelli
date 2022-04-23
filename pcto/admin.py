from django.contrib import admin
from .models import Tutor, Aziende, Contatti, Studenti, Abbinamenti

class AbbinamentiInline(admin.StackedInline):
    model = Abbinamenti
    #list_display = ['cognome','nome','classe']
    extra = 0
   
class ContattiInline(admin.StackedInline):
    model = Contatti
    fields = ['data','num_studenti','periodo_da','periodo_a','note','tutor']
    #inlines = [StudentiInline]
    extra = 0

@admin.register(Aziende)
class AziendeAdmin(admin.ModelAdmin):
    list_display = ['ragione_sociale','sede_comune','sede_provincia']
    inlines = [ContattiInline, AbbinamentiInline]

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['cognome','nome','email','classi']
