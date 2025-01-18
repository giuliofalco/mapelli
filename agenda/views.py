from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date, datetime, timedelta
import calendar
from .models import DayEntry
from .forms import DayEntryForm
from .filters import *
from calendar import monthrange
import os
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse
from collections import OrderedDict


WEEKDAY = ('Lunedì','Martedì','Mercoledì','Giovedì','Venerdì','Sabato','Domenica')

MESI = ('Gennaio', 'Febbraio', 'Marzo','Aprile',
        'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre',
        'Ottobre', 'Novembre', 'Dicembre')
        

#@login_required
def calendar_view(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
   
    month = int(request.GET.get('month', today.month))
   
    # Gestisci i limiti dei mesi
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    days_in_month = monthrange(year, month)[1]
    month_name = calendar.month_name[month]
    first_weekday = date(year, month, 1).weekday()
    last_weekday = date(year, month, days_in_month).weekday()
    days = []
    for day in range(1, days_in_month + 1):
        giorno = {
        "day": day,
        "date": date(year, month, day),
        "is_today": today.year == year and today.month == month and today.day == day,
        }
        print(year, month, day)
        try:
            record_giorno = DayEntry.objects.get(date=date(year,month,day))
            cookie = request.COOKIES.get(date(year,month,day).strftime("%Y-%m-%d"))
            updated =   record_giorno.updated_at.strftime("%Y-%m-%d")
            if record_giorno.vuoto():
                dot = False
            else:
                dot = cookie != updated 
        except DayEntry.DoesNotExist:
            dot = False
        
        giorno['dot'] = dot
        
        days.append(giorno)
   
    # Celle vuote all'inizio e alla fine
    empty_start = list(range(first_weekday))  # Celle vuote prima del primo giorno
    empty_end = list(range(6 - last_weekday))  # Celle vuote dopo l'ultimo giorno
    context = {
        'days': days,
        'year': year,
        'month': month,
        'month_name': month_name,
        'mese': MESI[month-1],
        'first_weekday': first_weekday,  # Giorno della settimana del primo giorno
        'last_weekday': last_weekday,    # Giorno della settimana dell'ultimo giorno
        'empty_start': empty_start,
        'empty_end': empty_end,
    }
    return render(request, 'agenda/calendar_view.html', context)

def day_editor(request, year, month, day):
    entry_date = date(year, month, day)
    prev_date = entry_date - timedelta(days=1)
    next_date = entry_date + timedelta(days=1)
    day_entry, created = DayEntry.objects.get_or_create(date=entry_date)
    weekday = WEEKDAY[entry_date.weekday()]

    if request.method == 'POST':
        form = DayEntryForm(request.POST, instance=day_entry)
        if form.is_valid():
            form.save()
            return redirect('calendar_view')
    else:
        form = DayEntryForm(instance=day_entry)
        context = {'form': form, 'entry_date': entry_date, 'mese':MESI[month-1],
                   'prev_day': prev_date.day, 'next_day':next_date.day, 
                   'prev_month':prev_date.month, 'next_month':next_date.month,
                   'prev_year': prev_date.year,'next_year': next_date.year, 
                   'weekday' : weekday, 
        }
        response = render(request, 'agenda/day_editor.html', context )
        response.set_cookie(
           key=day_entry.date.strftime('%Y-%m-%d'),
           value=day_entry.updated_at.strftime('%Y-%m-%d'),
           max_age=60 * 60 * 24 * 365  # Cookie valido per 1 anno
        )
    
        return response


@xframe_options_exempt
def serve_pdf(request, filename):
    # view di test per poter incorporare un file pdf in un iframe
    filepath = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
    response = FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    response['X-Frame-Options'] = 'SAMEORIGIN'
    response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
    return response


def monthly_report(request):
    # view per il report di backup dei dati raggrupapti per mese
    # Ottieni tutti i record con almeno un campo non vuoto

    entries = DayEntry.objects.filter(
        Q(assenze__isnull=False, assenze__gt='') |
        Q(eventi__isnull=False, eventi__gt='') |
        Q(uscite__isnull=False, uscite__gt='') |
        Q(note__isnull=False, note__gt='')
    )
  
    # Organizza i dati per mese
    data_by_month = {}
    for entry in entries:
        # Ottieni il mese e l'anno come stringa leggibile (es. "Gennaio 2025")
        month = entry.date.strftime('%B %Y').capitalize()
        if month not in data_by_month:
            data_by_month[month] = []
        # Aggiungi il record al mese corrispondente
        data_by_month[month].append({
            'date': entry.date.strftime('%d-%m-%Y'),
            'assenze': entry.assenze,
            'eventi': entry.eventi,
            'uscite': entry.uscite,
            'note': entry.note,
        })
    
    parola = ''
    if request.method == 'POST':             # richiama il filtro
        parola = request.POST.get('q','')
        data_by_month = filtra_dizionario(data_by_month,parola)

     # Ordina i mesi in ordine decrescente
    sorted_months = sorted(data_by_month.keys(), key=lambda month: datetime.strptime(month, "%B %Y"), reverse=True)
     # Crea un nuovo dizionario con i mesi ordinati
    data_by_month = {month: data_by_month[month] for month in sorted_months}
    # Ordina i giorni all'interno di ogni mese
    for month in data_by_month:
        data_by_month[month].sort(key=lambda x: x['date'],reverse=True)
    # Passa i dati al template
    return render(request, 'agenda/monthly_report.html', {'data_by_month': data_by_month, 'parola':parola})
