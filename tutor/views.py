from django.shortcuts import render
from tutor.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
import csv
from django.db import IntegrityError
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages


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

class ChangePasswordView(PasswordChangeView):
    # consente all'utente  di cambiarsi la password

    template_name = 'tutor/change_password.html'
    success_url = "/pcto/tutor"

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

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
   classi = Classi.objects.all().order_by('classe')
   indirizzi = Indirizzi.objects.all()
   dati = [[corso.denominazione,classi.filter(indirizzo = corso)] for corso in indirizzi]
   context = {'dati':dati}
   return render(request,"tutor/classi.html",context)

def elenco_studenti(request,classe):
   # elenco degli studenti di una specifia classe

   objclass = Classi.objects.get(classe=classe)
   studenti = Studenti.objects.filter(classe=objclass)
   context = {'classe':classe, 'studenti':studenti}
   return render(request,"tutor/studenti.html",context)

def adesioni(request):
    return HttpResponse('Funzionalità non ancora implementata')

def dettaglio_proposta(request,prop):
    # pagina con il dettaglio delle proposte e la popssibilità di adesione
    
    proposta = Proposte.objects.get(id=prop) 
    referenti_interni =  proposta.referenti_interni.all()
    context = {'proposta':proposta, 'referenti_interni': referenti_interni}
    return render(request,"tutor/dettaglio_proposta.html",context)

@login_required
def aggiungimi(request,id):
   # Aggiunge tra i referenti interni l'utente connesso alla proposta con pk = id
   utente = str(request.user)
   tutor = Tutor.objects.get(cognome=utente)
   proposta = Proposte.objects.get(id=id)
   proposta.referenti_interni.add(tutor)
   proposta.save()
   return HttpResponseRedirect(f"/pcto/tutor/dettaglio_proposta/{id}")

@login_required
def cancellami(request,id):
   # rimuove il tutor dai referenti interni
   utente = str(request.user)
   tutor = Tutor.objects.get(cognome=utente)
   proposta = Proposte.objects.get(id=id)
   if tutor in proposta.referenti_interni.all():
      proposta.referenti_interni.remove(tutor)
   proposta.save()
   return HttpResponseRedirect(f"/pcto/tutor/dettaglio_proposta/{id}")

###################################
### UPLOAD - DOWNLOAD - ARCHIVI ###
###################################

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

def upload_csv_doc_coinvolti(request):
   # Carica dal filel csv i docenti tutor assegnati alle classi
   # Le classi devono essere giù state caricate con la procedura generica valida per classi e tutor

   if request.method == 'POST':
      file_csv = request.FILES['archivio'] 
      file_content = file_csv.read().decode('utf-8').splitlines()
      errori = []
      reader = csv.DictReader(file_content,delimiter=';')
      for row in reader:
         classe = row['classe']
         try:
            objclasse = Classi.objects.get(classe=classe)
            objclasse.docenti_coinvolti = row['docenti_coinvolti']
            objclasse.save()
         except:
            errori.append(f"errore in {classe}")
      
      context = {'errori':errori}
      return render(request,"tutor/errori_importazione.html",context)
      

def upload_csv_studenti(request):

   if request.method == 'POST':
      file_csv = request.FILES['archivio'] 
      file_content = file_csv.read().decode('utf-8').splitlines()
      errori = []
     
      reader = csv.DictReader(file_content,delimiter=';')

      for row in reader:
        
         classe = row['classe']
         try:
            oggetto_classe = Classi.objects.get(classe=classe)
            studente = Studenti (
               cognome = row['cognome'],
               nome = row['nome'],
               classe = oggetto_classe
            )
            studente.save()
         except Exception as e:
            errori.append(f"errore in {classe} {e}")
        
      if errori:
         context = {'errori':errori}
         return render(request,"tutor/errori_importazione.html",context)
      
   return render(request,"tutor/errori_importazione.html",{})

### UTILITY UTILITA'
   
def completa_classi(request):
    # inserisce nei record classi, l'indirizzo a cui appartiene
   classi = Classi.objects.all()
   for classe in classi:
        sigla = classe.corso()
        indirizzo = Indirizzi.objects.get(sigla=sigla)
        classe.indirizzo = indirizzo
        classe.save()
   return(HttpResponse('Done'))

def intera_classe(classe):
    # restituisce True, se l'intera classe è stata assegnata ad un solo tutor
   doc = classe.docenti_coinvolti
   lista = doc.split()
   return len(lista) == 1

def studenti_tutor():
   # prepara i dati alla view completa_tutor. Lista con (cognome tutor,lista di studenti)

   classi = Classi.objects.all()
   # tutti i tutor che hanno assegnato una intera classe, con il tutor e la classe (anche ripetuti)
   tutor = [[classe.docenti_coinvolti,classe] for classe in classi if intera_classe(classe) ]
   # ad ogni tutor associo gli studentii dell'intera classe
   diz = {}
   for t in tutor:
      studenti = Studenti.objects.filter(classe=t[1])
      if t[0] in diz:
         diz[t[0]] += (list(studenti))
      else:
         diz[t[0]] = list(studenti) 
   lista = diz.items()
   lista = sorted(lista,key = lambda x: x[0])                             
   return lista
  
def completa_tutor(request):
   # inserisce a ciascuno studente il tutor assegnato, se l'intera classe è assegnata al tutor
   assegnamenti = studenti_tutor()
   errori = []
   if request.GET: # se viene richiamata dal template
      # assegno il tutor agli studenti
      for ass in assegnamenti:
         try:
            tutor = Tutor.objects.get(cognome=ass[0].strip())
         except Exception as e:
            errori.append(f"assegnamento: {ass[0]}: {e}")
         for stud in ass[1]:
               studente = Studenti.objects.get(id=stud.id)
               studente.tutor = tutor
               try:
                  studente.save()
               except Exception as e:
                  errori.append(f"in salvataggio studente {studente} : {e} ")
      if errori:
         context = {'errori':errori}
         return render(request,"tutor/errori_importazione.html",context)
      else:       
         return render(request,"tutor/errori_importazione.html",{})
   else:           # richiama il template
      context = {'assegnamenti': assegnamenti}        
      return render(request,"tutor/lista_tutor.html",context)