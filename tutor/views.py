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
from .filters import ProposteFilter
from .forms import AttivitaForm


# Create your views here.
def index(request):
   # return HttpResponse("<h1>Orientamento</h1>")
   news = News.objects.all()
   return render(request,"tutor/index.html",{'news':news})

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
    return HttpResponseRedirect("/orienta/tutor")

class ChangePasswordView(PasswordChangeView):
    # consente all'utente  di cambiarsi la password

    template_name = 'tutor/change_password.html'
    success_url = "/orienta/tutor"

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
    
@login_required
def upload(request):
    return render(request,"tutor/upload.html",{})

@login_required
def upload_csv_proposte(request):
   # carica il csv delle proposte
   return(HttpResponse("<h2>Dati caricati con successo</h2> <a href='/orienta/tutor'>Torna alla hoem page</a>"))

def proposte(request):
    # elenco delle proposte

   proposte = Proposte.objects.filter(attivo=True)
   myfilter = ProposteFilter(request.GET,queryset=proposte)
   proposte = myfilter.qs
   context = {'proposte':proposte, 'myfilter':myfilter}

   return render(request,"tutor/proposte.html",context)

@login_required
def elenco_tutor(request):
   # Elenco dei Tutor
    
   tutor = Tutor.objects.all()
   context = {'tutor':tutor}
   return render(request,"tutor/tutor.html",context)

@login_required
def elenco_attivita_tutor(request,idtutor):
   # mostra l'elenco attività  o diario di bordo dei tutor
   utente = str(request.user)
   if utente not in ('annamaria','dirigente'):
      try:
         tutor = Tutor.objects.get(cognome=utente)
      except:
         return HttpResponse('Utente non autorizzato')
      if tutor.id != idtutor:
         return HttpResponse('Non è consentito visualizzare attività di altri tutor')
   tutor = Tutor.objects.get(id=idtutor)
   elenco = Attivita_tutor.objects.filter(tutor=tutor)
   form = AttivitaForm()
   context = {'elenco':elenco, 'tutor':tutor, 'form':form}
   return render(request,"tutor/elenco_attivita_tutor.html",context)

@login_required
def salva_attivita_tutor(request):
   # salva una nuova attivita inserita dal tutor e ritorna a elenco attivita tutor
   if request.method == 'POST':
      form = AttivitaForm(request.POST)
      tutor = Tutor.objects.get(id=request.POST.get('tutor'))
      elenco = Attivita_tutor.objects.filter(tutor=tutor)
      if form.is_valid:
         attivita = Attivita_tutor()
         attivita.tutor = tutor
         attivita.tipologia = Tipologia_attivita.objects.get(id=request.POST.get('tipologia'))
         attivita.target = Target_attivita.objects.get(id = request.POST.get('target'))
         attivita.titolo = request.POST.get('titolo')
         attivita.durata = request.POST.get('durata')
         attivita.descrizione = request.POST.get('descrizione')
         attivita.save()
         form = AttivitaForm()
      context = {'elenco':elenco, 'tutor':tutor, 'form':form}
      return render(request,"tutor/elenco_attivita_tutor.html",context)
   else:
      return HttpResponse('errore, method diverso da POST in salva_attivita_tutor')

@login_required
def dettaglio_attivita_tutor(request,idattivita):
   # apre la form per modificare o cancellare  una attivita tutor
   if request.method == 'POST':
      form = AttivitaForm(request.POST)
      if form.is_valid:
         tutorid = request.POST.get('tutor')
         attivita = Attivita_tutor.objects.get(id=idattivita)
         attivita.tipologia = Tipologia_attivita.objects.get(id=request.POST.get('tipologia'))
         attivita.target = Target_attivita.objects.get(id = request.POST.get('target'))
         attivita.data = request.POST.get('data')
         attivita.titolo = request.POST.get('titolo')
         attivita.durata = request.POST.get('durata')
         attivita.descrizione = request.POST.get('descrizione')
         attivita.save()
         return HttpResponseRedirect(f"/orienta/tutor/elenco_attivita_tutor/{tutorid}")
   else:
      attivita = Attivita_tutor.objects.get(id=idattivita)
      form = AttivitaForm(instance=attivita)
   context = {'attivita':attivita, 'form':form}
   return render(request,"tutor/dettaglio_attivita_tutor.html",context)

def cancella_attivita(request,id):
   # cancella l'attività identificata dalla chiave id
   attivita = Attivita_tutor.objects.get(id=id)
   tutorid = attivita.tutor.id
   attivita.delete()
   return HttpResponseRedirect(f"/orienta/tutor/elenco_attivita_tutor/{tutorid}")
   

@login_required
def elenco_classi(request):
   # Elenco delle classi

   classi = Classi.objects.all().order_by('classe')
   indirizzi = Indirizzi.objects.all()
   dati = [[corso.denominazione,classi.filter(indirizzo = corso)] for corso in indirizzi]
   context = {'dati':dati}
   return render(request,"tutor/classi.html",context)

@login_required
def elenco_studenti(request,classe):
   # elenco degli studenti di una specifica classe

   objclass = Classi.objects.get(classe=classe)
   studenti = Studenti.objects.filter(classe=objclass)
   context = {'classe':classe, 'studenti':studenti}
   return render(request,"tutor/studenti.html",context)

@login_required
def dettaglio_proposta(request,prop):
    # pagina con il dettaglio delle proposte e la possibilità di adesione

    LUOGHI = {0:'A Scuola', 1 : 'Esterno', 2 : 'Da definire'}
    utente = str(request.user)
    proposta = Proposte.objects.get(id=prop) 
    referenti_interni =  proposta.referenti_interni.all()
    iscritti = proposta.iscrizioni.all()
    context = {'proposta':proposta, 'referenti_interni': referenti_interni, 'iscritti':iscritti, 
               'utente':utente, 'luogo' : LUOGHI[proposta.luogo]}
    return render(request,"tutor/dettaglio_proposta.html",context)

@login_required
def aggiungimi(request,id):
   # Aggiunge tra i referenti interni l'utente connesso alla proposta con pk = id
   utente = str(request.user)
   try:
       tutor = Tutor.objects.get(cognome=utente)
   except:
      return HttpResponse('Utente non autorizzato')
   proposta = Proposte.objects.get(id=id)
   try:
      proposta.referenti_interni.add(tutor)
      proposta.save()
   except:
      pass
   return HttpResponseRedirect(f"/orienta/tutor/dettaglio_proposta/{id}")

@login_required
def cancellami(request,id):
   # rimuove il tutor dai referenti interni
   utente = str(request.user)
   try:
      tutor = Tutor.objects.get(cognome=utente)
      proposta = Proposte.objects.get(id=id)
      if tutor in proposta.referenti_interni.all():
         proposta.referenti_interni.remove(tutor)
      proposta.save()
   except:
      pass
   return HttpResponseRedirect(f"/orienta/tutor/dettaglio_proposta/{id}")

@login_required
def ritira(request,idstudente,idproposta):
   # ritira lo studente dall'adesione alla proposta
   proposta = Proposte.objects.get(id=idproposta)
   studente = Studenti.objects.get(id=idstudente)
   proposta.iscrizioni.remove(studente)
   proposta.save()
   return HttpResponseRedirect(f"/orienta/tutor/dettaglio_proposta/{idproposta}")

@login_required
def adesioni_proposta(request,id):
   # va alla pagina con gli studenti del tutor da assegnare alla proposta pk = id
   utente = str(request.user)
   try:
      tutor = Tutor.objects.get(cognome=utente)
   except:
      return HttpResponse("L'utente non è autorizzato ad eseguire l'operazione")
   studenti = Studenti.objects.filter(tutor=tutor)
   proposta = Proposte.objects.get(id=id)
   iscrizioni = proposta.iscrizioni.all()
   iscrivibili = []
   for studente in studenti:
      if studente not in iscrizioni:
         iscrivibili.append(studente)
   classi = []                   # elenco delle classi
   for s in iscrivibili:
      if s.classe not in classi:
         classi.append(s.classe)      
   target = [[classe,[std for std in iscrivibili if std.classe==classe]] for classe in classi]   
   # raggruppamento per classi degli studenti iscrivibili 

   context = {'idproposta':id, 'target' : target, 'tutor':tutor}
   return render(request,"tutor/adesioni_proposta.html",context)

@login_required
def salva_iscrizioni(request):
   # salva le iscrizioni degli studenti selezionati nella proposta
   if request.method == "POST":
      idproposta = request.POST.get('idproposta')
      proposta = Proposte.objects.get(id=idproposta)
      for idstudent in request.POST: 
         if idstudent != "csrfmiddlewaretoken" and idstudent != "idproposta":
            studente = Studenti.objects.get(id=int(idstudent))
            proposta.iscrizioni.add(studente)
      proposta.save()  
      return HttpResponseRedirect(f"/orienta/tutor/dettaglio_proposta/{idproposta}")
   return HttpResponseRedirect("/orienta/tutor")

@login_required   
def adesioni(request):
   # elenca le proposte con almeno un referente interno o una adesione
   # elementi della lista [proposta,referentinumerod i adesioni]
   proposte = Proposte.objects.filter(attivo=True)
   selezione = [prop for prop in proposte if len(prop.referenti_interni.all())>0 or len(prop.iscrizioni.all())>0]
   context = {'selezione':selezione}
   return render(request,"tutor/elenco_adesioni.html",context)
      

###################################
### UPLOAD - DOWNLOAD - ARCHIVI ###
###################################

@login_required
def upload_csv_proposte(request):
    # carica dal file csv l'elenco aggiornato delle aziende

   if request.method == 'POST':
         file_csv = request.FILES['archivio'] 
         file_content = file_csv.read().decode('utf-8').splitlines()
        
         reader = csv.DictReader(file_content,delimiter=';')

         errori = []
         for row in reader:
        
            try:
               proposta = Proposte (
                    id = row['id'],
                    nome_progetto = row['nome_progetto'],
                    descrizione = row['descrizione'],
                    disciplina =row['disciplina'],
                    # max_alunni = row['max_alunni'],
                    # classi_consigliate = row['classi'],
                    ente = row['ente'],
                    referente_esterno = row['referente_esterno'],
                    email_ref_esterno = row['email_ref_esterno'],
                    tel_ref_esterno = row['tel_ref_esterno'],
                    # num_ore = int(row['num_ore']),
                    data_inizio = row['data_inizio'],
                    data_fine = row['data_fine'],
               )
            except:
               print('errore')
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

@login_required
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

@login_required
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
      
@login_required
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

@login_required
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

@login_required
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

@login_required 
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