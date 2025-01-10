from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from datetime import date, datetime, timedelta
import calendar
from .models import DayEntry
from .forms import DayEntryForm
from calendar import monthrange

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
    days = [

        {
            "day": day,
            "date": date(year, month, day),
            "is_today": today.year == year and today.month == month and today.day == day
        }
        for day in range(1, days_in_month + 1)
    ]
    # Celle vuote all'inizio e alla fine
    empty_start = list(range(first_weekday))  # Celle vuote prima del primo giorno
    empty_end = list(range(6 - last_weekday))  # Celle vuote dopo l'ultimo giorno
    context = {
        'days': days,
        'year': year,
        'month': month,
        'month_name': month_name,
        'first_weekday': first_weekday,  # Giorno della settimana del primo giorno
        'last_weekday': last_weekday,    # Giorno della settimana dell'ultimo giorno
        'empty_start': empty_start,
        'empty_end': empty_end,
    }
    return render(request, 'agenda/calendar_view.html', context)

def day_editor(request, year, month, day):
    entry_date = date(year, month, day)
    day_entry, created = DayEntry.objects.get_or_create(date=entry_date)

    if request.method == 'POST':
        form = DayEntryForm(request.POST, instance=day_entry)
        if form.is_valid():
            form.save()
            return redirect('calendar_view')
    else:
        form = DayEntryForm(instance=day_entry)

    return render(request, 'agenda/day_editor.html', {'form': form, 'entry_date': entry_date})
