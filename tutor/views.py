from django.shortcuts import render
from tutor.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
import csv
from django.db import IntegrityError


# Create your views here.
def index(request):
   # return HttpResponse("<h1>Orientamento</h1>")
   return render(request,"tutor/index.html",{})

def mioLogin(request):
   # manda alla finestra di autenticazione, per chiedere username e password
   next = request.GET['next']
   context = {'next':next,}
   return render(request,'tutor/login.html',context)

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
      return render(request,'tutor/login.html',{'msg':'Autenticazione Fallita', 'next':next} )
   
def logout_view(request):
    # esegue il logout dall'utente 

    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/pcto/tutor")

def upload(request):
    return render(request,"tutor/upload.html",{})

def upload_csv_proposte(request):
   # carica il csv delle proposte
   return(HttpResponse("<h2>Dati caricati con successo</h2> <a href='/pcto/tutor'>Torna alla hoem page</a>"))

def proposte(request):
    # elenco delle proposte

   proposte = Proposte.objects.all()
   context = {'proposte':proposte}

   return render(request,"tutor/proposte.html",context)

def elenco_tutor(request):
    
   tutor = Tutor.objects.all()
   context = {'tutor':tutor}
   return render(request,"tutor/tutor.html",context)

def elenco_classi(request):
   classi = Classi.objects.all()
   context = {'classi':classi}
   return render(request,"tutor/classi.html",context)

def upload_csv_proposte(request):
    # carica dal file csv l'elenco aggiornato delle aziende

   if request.method == 'POST':
         file_csv = request.FILES['archivio'] 
         file_content = file_csv.read().decode('utf-8').splitlines()
        
         reader = csv.DictReader(file_content,delimiter=';')
        
         # aziende = Aziende.objects.all()
         #for az in aziende:
         #    az.delete()

         errori = []
         for row in reader:
               
               proposta = Proposte (
                    nome_progetto = row['nome_progetto'],
                    disciplina =row['disciplina'],
                    # max_alunni = row['max_alunni'],
                    classi_consigliate = row['classi'],
                    ente = row['ente'],
                    referente_esterno = row['referente_esterno'],
                    email_ref_esterno = row['email_ref_esterno'],
                    tel_ref_esterno = row['tel_ref_esterno'],
                    # num_ore = int(row['num_ore']),
                    data_inizio = row['data_inizio'],
                    data_fine = row['data_fine'],
               )
               try:
                  proposta.save()
               except IntegrityError as e:
                   errori.append(f"errore in {row['nome_progetto']} {e}")
               except Exception as e:
                    errori.append(f"errore sconosciuto in {row['nome_progetto']} {e}")
                    
         if errori:
                context = {'errori':errori}
                return render(request,"tutor/errori_importazione.html",context)
           
   return render(request,"tutor/errori_importazione.html",{})  # uscita senza errori

def upload_csv(request,tabella):
   # caricamento csv generico

   diz = {'Classi': Classi, 'Tutor':Tutor}

   if request.method == 'POST':

      file_csv = request.FILES['archivio'] 
      file_content = file_csv.read().decode('utf-8').splitlines()
      reader = csv.DictReader(file_content,delimiter=';')
      header_fields = reader.fieldnames
      errori = []
      for row in reader:
         record = diz[tabella](**row)
         try: 
            record.save()
         except Exception as e:
            errori.append(f"{e} in {record}")
      if errori:
         context = {'errori':errori}
         return render(request,"tutor/errori_importazione.html",context)
      
   return render(request,"tutor/errori_importazione.html",{})  # uscita senza errori

def completa_classi(request):
    # inserisce nei record classi, l'indirizzo a cui appartiene
   classi = Classi.objects.all()
   for classe in classi:
        sigla = classe.corso()
        indirizzo = Indirizzi.objects.get(sigla=sigla)
        classe.indirizzo = indirizzo
        classe.save()
   return(HttpResponse('fatto'))
