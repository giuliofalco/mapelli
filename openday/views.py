from openday.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.db import IntegrityError
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from .forms import IscrizioniForm

# Create your views here.
def index(request):
   novita = News.objects.all()
   eventi = Eventi.objects.filter(attivo=True)
   indirizzi = Indirizzi.objects.all()
   context = {'novita':novita, 'eventi':eventi, 'indirizzi':indirizzi}
   return render(request,"openday/index.html",context)

def mioLogin(request):
   # manda alla finestra di autenticazione, per chiedere username e password
   next = request.GET['next']
   context = {'next':next,}
   return render(request,'openday/login.html',context)

def autentica(request):
   # riceve dalla finestra di autenticazione e controlla per effettuare il login
   utente  = request.POST.get('utente') 
   password = request.POST.get('password')
   next = request.POST.get('next')
   user = authenticate(request, username=utente, password=password)
 
   if user is not None:
      login(request, user)
      return HttpResponseRedirect(next)
   else:
      return render(request,'openday/login.html',{'msg':'Autenticazione Fallita', 'next':next} )
   
def logout_view(request):
    # esegue il logout dall'utente 

    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/orienta/openday")

def iscrivi_utente(request,sigla):
   evento = Eventi.objects.get(sigla=sigla)
   context = {'evento':evento}
   form = IscrizioniForm()
   if request.method == 'POST':
         form = IscrizioniForm(request.POST)
         if form.is_valid():
            cognome = request.POST.get('cognome')
            nome = request.POST.get('nome')
            comune = request.POST.get('comune')
            scuola = request.POST.get('scuola')
            visitatore, created = Visitatori.objects.get_or_create(cognome=cognome,nome=nome,comune=comune,scuola=scuola)
            iscrizione = Iscrizioni(evento=evento,visitatore=visitatore)
            iscrizione.save()  # Salva l'iscrizione nel database
         form = IscrizioniForm()
         return render(request,f"openday/conferma_iscrizione.html",context)  # Reindirizza a una pagina di conferma o a un'altra vista
   else:
         context = {'form': form, 'evento':evento}
         return render(request, 'openday/iscrizione.html', context)

def indirizzi(request,indirizzo):
    # mostra la pagina descrittiva dell'indirizzo
   pagina = Indirizzi.objects.get(titolo=indirizzo)
   return render(request,"openday/indirizzo.html",{'pagina':pagina})

def rileva_presenze(request,sigla):
   evento = Eventi.objects.get(sigla=sigla)
   iscritti = Iscrizioni.objects.filter(evento=evento)
   context = {'iscritti':iscritti}
   return render(request,"openday/presenze.html",context)
   