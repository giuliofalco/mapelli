from django.contrib import admin
from .models import *

class RisposteInline(admin.StackedInline):
    model = Risposte
    fields = ['domanda','risposta']
    extra = 0

@admin.register(Questionari)
class QuestionariAdmin(admin.ModelAdmin):
    list_display = ['luogo','data','intervistatore']
    inlines = [RisposteInline]

@admin.register(Domande)
class QuestionariAdmin(admin.ModelAdmin):
    list_display = ['numero','testo']
