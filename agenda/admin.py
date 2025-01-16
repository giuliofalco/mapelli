from django.contrib import admin
from .models import *
from .forms import *

  
@admin.register(DayEntry)
class DayEntryAdmin(admin.ModelAdmin):
    list_display = ['date','updated_at']
    readonly_fields = ['updated_at']  # Rendi il campo visibile ma non modificabile
    form = DayEntryForm

    class Media:
        css = {
            'all': ('admin/css/custom.css',)  # Percorso relativo al file statico
        }