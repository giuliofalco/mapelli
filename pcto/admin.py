from django.contrib import admin
from .models import Tutor, Aziende, Contatti

class ContattiInline(admin.StackedInline):
    model = Contatti
    fields = ['data','num_studenti','periodo_da','periodo_a','note','tutor']
    extra = 0

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['cognome','nome','email','classi']

@admin.register(Aziende)
class AziendeAdmin(admin.ModelAdmin):
    list_display = ['ragione_sociale','sede_comune','sede_provincia']
    inlines = [ContattiInline]
