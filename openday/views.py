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
from .filters import IscrittiFilter

# HOME PAGE
def index(request):
   novita = News.objects.all()
   eventi = Eventi.objects.order_by('luogo')
   indirizzi = Indirizzi.objects.all()
   context = {'novita':novita, 'eventi':eventi, 'indirizzi':indirizzi}
   return render(request,"openday/index.html",context)

# AUTENTICAZIONE
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
      return render(request,'/openday/login.html',{'msg':'Autenticazione Fallita', 'next':next} )
   
def logout_view(request):
    # esegue il logout dall'utente 

    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/orienta/openday")

def iscrivi_utente(request,sigla):
   # memorizza l'iscrizione dell'utente ad un evento

   # if sigla in ('LZ','LS'):
   #   return HttpResponse("<h2>Spiacenti, non è più possibile iscriversi a questo evento.</h2> <a href=/orienta/openday>Home</a>")

   evento = Eventi.objects.get(sigla=sigla)
   if evento.attivo == False: 
      return HttpResponse("<h2>Spiacenti, non è più possibile iscriversi a questo evento.</h2> <a href=/orienta/openday>Home</a>")
     
   if request.method == 'POST':                # se la form restituisce i risultati da salvare
         form = IscrizioniForm(request.POST)
         if form.is_valid():                   # se è valida sava i dati e passa alla conferma
            cognome = request.POST.get('cognome')
            nome = request.POST.get('nome')
            comune = request.POST.get('comune')
            scuola = request.POST.get('scuola')
            visitatore, created = Visitatori.objects.get_or_create(cognome=cognome,nome=nome,comune=comune,scuola=scuola)
            iscrizione = Iscrizioni(evento=evento,visitatore=visitatore)
            iscrizione.save()  # Salva l'iscrizione nel database
            return render(request,f"openday/conferma_iscrizione.html",{'evento':evento})  # Reindirizza a una pagina di conferma o a un'altra vista
   else:                                       # se la form è chiamata per visualizzare e inserire i dati
      form = IscrizioniForm()                  # prepara la form vuota

   context = {'form':form,'evento':evento}     # in ogni caso metti la form vuota oppure con i messaggi di errore
   return render(request, 'openday/iscrizione.html', context)

def indirizzi(request,indirizzo):
    # mostra la pagina descrittiva dell'indirizzo
   eventi = Eventi.objects.filter(attivo=True) # tutti gli eventi attivi per le voci di menu
   indirizzi = Indirizzi.objects.all()         # tutti gli indirizzi per le voci di menu     
   pagina = Indirizzi.objects.get(titolo=indirizzo) # l'indirizzo da mostrare
   righe_orario = riga_orario.objects.filter(indirizzo = pagina) 
   context = {'pagina':pagina, 'righe_orario':righe_orario, 'indirizzi':indirizzi, 'eventi':eventi}
   return render(request,"openday/indirizzo.html",context)

def conferma_presenza(id):
   # conferma la presenza identificata da id 
   try:
      id = int(id)
      adesione = Iscrizioni.objects.get(id=id)
      adesione.presente = True
      adesione.save()
   except:
      print("errore nel salvataggio")
   return

def rileva_presenze(request,sigla):
   # elenca gli iscritti per rilevre le presenze
   evento = Eventi.objects.get(sigla=sigla)
   titolo = evento.titolo
   data   = evento.data
   iscritti = Iscrizioni.objects.filter(evento=evento).order_by('visitatore__cognome')
   presenze = len(iscritti.filter(presente=True))
   myfilter = IscrittiFilter(request.GET,queryset=iscritti)
   iscritti = myfilter.qs
   context = {'iscritti':iscritti, 'titolo':titolo, 'data':data, 'myfilter':myfilter, 'presenze': presenze}
   if request.method == 'POST':
      for id in request.POST:
         if id != "csrfmiddlewaretoken":
            conferma_presenza(id)
   
   return render(request,"openday/presenze.html",context)

def gallery(request):
   # mostra la gallery di immagini e video
   eventi = Eventi.objects.all() # tutti gli eventi attivi per le voci di menu
   indirizzi = Indirizzi.objects.all()         # tutti gli indirizzi per le voci di menu  
   immagini = Gallery.objects.all()
   context = {'immagini':immagini,'eventi':eventi,'indirizzi':indirizzi}
   return render(request,"openday/gallery.html",context)
   
def upload(request):
    # carica il template per l'upload
    return render(request,"openday/upload.html")

import csv
def upload_iscrizioni(request,evento):
   # carica da file csv le nuove iscrizioni senza duplicare le esistenti
  
   if request.method == 'POST':

      try:  
         event = Eventi.objects.get(sigla=evento)
      except:
         return HttpResponse('sigla di evento non esistente o duplicato') 

      file_csv = request.FILES['archivio'] 
      file_content = file_csv.read().decode('utf-8').splitlines()
      reader = csv.DictReader(file_content)
        
      for row in reader:
                
               utente, created = Visitatori.objects.get_or_create(cognome=row['Nome e Cognome'], email = row['Nome utente'])
               # Creazione di una nuova istanza del modello Iscrizioni
               try :
                  Iscrizioni.objects.get(visitatore=utente,evento=event)
               except:
                  iscrizione = Iscrizioni(
                                 visitatore = utente,
                                 evento = event
                              ) 
                  iscrizione.save()
        
   return HttpResponse("<h3>Caricamento completato <a href='/orienta/openday/'>Home</a>")  

def stat_iscrizioni(request):
   # alimenta il file con le statistiche riguardanti le presenze agli eventi
   statistica = []
   eventi = Eventi.objects.all().order_by('luogo')
   for ev in eventi:
      iscrizioni = Iscrizioni.objects.filter(evento = ev)
      iscritti = len(iscrizioni)
      presenze = iscrizioni.filter(presente=True).count()
      #perc = presenze/iscritti * 100
      try:
         perc = int(presenze / iscritti * 10000) / 100


      except:
         perc = 0
      visitatori = [iscr.visitatore for iscr in iscrizioni] # elenco dei visitatori
      comuni = {} # conteggio deo visitatori per comune di provenienza
      for v in visitatori:
         if v.comune in comuni:
            comuni[v.comune] += 1
         else:
            comuni[v.comune] = 1
      stat_comune = comuni.items()
      stat_comune = sorted(stat_comune, key=lambda x: x[1], reverse=True)
      statistica.append([ev.titolo,[iscritti,presenze,perc,stat_comune]])
   context = {'statistica': statistica, 'eventi':eventi}
   return render(request,"openday/statistica.html",context)
   