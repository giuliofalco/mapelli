from django.shortcuts import render
from pcto.models import *
from django.templatetags.static import static
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .filters import AziendeFilter
from pcto.indirizzi import *
from django.urls import reverse
from .forms import *
from django.db.models import Count


def visualizza_utente(request):
    try:
       utente = 'autenticata come: ' + request.user.first_name + " " + request.user.last_name 
       return utente
    except:
       return 'anonima'

def index(request):
    try:
       utente = 'autenticata come: ' + request.user.first_name + " " + request.user.last_name 
       context = {'user': utente}
    except:
        context = {'user': 'anonima'}
    
    return render(request,'index.html',context)
    
def tutor(request):
    elenco = Tutor.objects.all()
    context = {'object_list':elenco}
    context['user'] = visualizza_utente(request)
    
    return render(request,"tutor.html",context)

@login_required
def aziende(request):
    # elenco delle aziende
    if not request.user.is_staff:
        return HttpResponse("utente non autorizzato ad accedere a questo elenco")
    elenco = Aziende.objects.all()
    numero_aziende = len(elenco)
    myfilter = AziendeFilter(request.GET,queryset=elenco)
    elenco = myfilter.qs

    pag = Paginator(elenco,20)
    totpagine = pag.num_pages
    numpag = request.GET.get('pagina',1)
    pagelist = range(int(numpag)+1,totpagine+1)
    pagelist0 = range(1,int(numpag))
    pagina = pag.page(numpag)

    context = {'object_list': pagina,           # la pagina con i dati da visualizzare
               'myfilter':myfilter,
               'totpagine': totpagine,
               'numpag' : numpag,
               'pagelist': pagelist, 
               'pagelist0': pagelist0,
               'numero_aziende' : numero_aziende
              }
    context['user'] = visualizza_utente(request)
    return render(request,"aziende.html",context)

def dettaglio_azienda(request,piva):
    # mostra i dati dell'aziende e dei contatti associati
    azienda = Aziende.objects.get(partita_iva=piva)
    contatti = azienda.contatti_set.all()
    #stagisti = azienda.stagisti.all()
    abbinamenti = Abbinamenti.objects.filter(azienda=azienda)
    tutor = Tutor.objects.all()
    
    contatto = request.GET.get('contatto','')
    note = request.GET.get('note','')
    tutoremail = request.GET.get('tutor','')
    if contatto:
        obj = Contatti.objects.get(id=contatto)
        obj.note = note
        nuovo_tutor = Tutor.objects.get(email=tutoremail)
        obj.tutor = nuovo_tutor
        obj.save()

    if contatti:
        posti = contatti[0].num_studenti - len(abbinamenti)
    else:
        posti = 0

    studenti = Studenti.objects.all()

    context = {'azienda':azienda, 'contatti': contatti, 'abbinamenti':abbinamenti, 
               'posti':posti, 'tutor':tutor, 'studenti':studenti}
    context['user'] = visualizza_utente(request)
    form = ContactForm(initial={'azienda':azienda.partita_iva, 'num_studenti': 0})
    context['form'] = form
    return render(request,"dettaglio_azienda.html",context) 

def mioLogin(request):
   # manda alla finestra di autenticazione, per chiedere username e password
   next = request.GET['next']
   context = {'next':next,}
   return render(request,'login.html',context)

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
      return render(request,'login.html',{'msg':'Autenticazione Fallita', 'next':next} )

def contatti(request):
    # elenco dei contatti in ordine decrescente di data
    contatti = Contatti.objects.all()
    righe = []
    for item in contatti:
        azienda = item.azienda
        stagisti = azienda.stagisti
        disponibili = item.num_studenti - stagisti.count()
        righe.append((item,disponibili))
    context = {'contatti': righe}

    return render(request,"contatti.html",context)
    
@login_required
def studenti(request,corso):
    # visualizza gli studenti del corso suddivisi per classi
    
    studenti = Studenti.objects.all()        # elenco di tutti gli studenti
    abbinamenti = Abbinamenti.objects.all()  # elenco di tutti gli abbinamenti
    studenti_corso = [item for item in studenti if item.corso()==corso]
    classi = [item.classe for item in studenti_corso] # la classe di ciascun studente
    classi = set(classi)  # tolgo i doppioni
    classi = list(classi) # lista con le classi
    classi.sort()         # in ordine alfabetico
    report = [[classe,[studente for studente in studenti if studente.classe == classe]] for classe in classi]
    # dopo che ho raggruppato l'elenco studenti per classe, 
    # verifico per ognuno se lo studente compare nella lista degli abbinamenti
    # sostituisco lo studente con una lista: al primo posto lo studente al secondo l'azienda
    for classe in report:
        for i in range(len(classe[1])):
            abbinati = abbinamenti.filter(studente=classe[1][i])
            if abbinati:
                classe[1][i] = [classe[1][i],abbinati[0].azienda]
            else:
                classe[1][i] = [classe[1][i],""]
   
    context = {'corso':sigle[corso],'report':report, 'classi' : classi}
    context['user'] = visualizza_utente(request)
    return render(request,"studenti.html",context)

def elenco_abbinamenti(request):
    abbinamenti = Abbinamenti.objects.all()
    context = {'abbinamenti' : abbinamenti}
    return render(request,"abbinamenti.html",context)

def inserisci (request):
    # aggiunge un abbinamento
    piva = request.POST.get("azienda")
    azienda = Aziende.objects.get(partita_iva=piva)
    idstud = request.POST.get("studente")
    studente = Studenti.objects.get(id=idstud)
    periodo_da = request.POST.get("periodo_da")
    periodo_a = request.POST.get("periodo_a")
    abbinamento = Abbinamenti()
    abbinamento.studente = studente
    abbinamento.azienda = azienda
    abbinamento.periodo_da = periodo_da
    abbinamento.periodo_a = periodo_a
    abbinamento.save()
    return HttpResponseRedirect('aziende/' + azienda.partita_iva)

def cancella (request):
    # cancella un abbinamento
    idabbinamento = request.GET.get('id')
    record = Abbinamenti.objects.get(id=idabbinamento)
    record.delete()
    piva = request.GET.get('piva')
    return HttpResponseRedirect('aziende/'+piva)

def add_contatto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            piva = form.cleaned_data['azienda']
            tutor= form.cleaned_data['tutor']
            num_studenti = form.cleaned_data['num_studenti']
            periodo_da= form.cleaned_data['periodo_da']
            periodo_a= form.cleaned_data['periodo_a']
            note = form.cleaned_data['note']
            azienda = Aziende.objects.get(partita_iva = piva)
            contatto = Contatti()
            contatto.azienda = azienda
            contatto.tutor = tutor
            contatto.num_studenti = num_studenti
            contatto.periodo_da = periodo_da
            contatto.periodo_a = periodo_a
            contatto.note = note
            contatto.save()
    return HttpResponseRedirect('aziende/'+piva)

def statistica(request):
    anno = Storico.objects.values('anno').annotate(Count('anno')).order_by('anno')
    aziende = Storico.objects.values('ragione_sociale','sede_provincia').annotate(Count('ragione_sociale')).order_by('-ragione_sociale__count','ragione_sociale')
    labels = []
    data = []
    for year in anno:
        labels.append(year['anno'])
        data.append(year['anno__count'])
    context = {'anno':anno, 'aziende':aziende, 'labels':labels, 'data':data }
    return render(request,"statistica.html",context)

def dettaglio_stat(request,azienda):
    dist = Storico.objects.filter(ragione_sociale=azienda).values('anno').annotate(Count('anno')).order_by('anno')
    labels = []
    data = []
    for d in dist:
        labels.append(d['anno'])
        data.append(d['anno__count'])
    context = {'azienda': azienda,'dist': dist, 'labels':labels, 'data':data}
    return render(request,"abbinamenti_azienda.html",context)

import csv
from django.db import IntegrityError
def upload_csv_aziende(request):
    # carica dal file csv l'elenco aggiornato delle aziende

    if request.method == 'POST':
        file_csv = request.FILES['archivio'] 
        file_content = file_csv.read().decode('utf-8').splitlines()
        
        reader = csv.DictReader(file_content,delimiter=';')
        
        aziende = Aziende.objects.all()
        for az in aziende:
            az.delete()

        errori = []
        for row in reader:
               
                azienda = Aziende(
                    partita_iva = row['PARTITA_IVA'],
                    ragione_sociale =row['RAGIONE_SOCIALE'],
                    indirizzo = row['INDIRIZZO'],
                    comune = row['COMUNE'],
                    provincia = row['PROVINCIA'],
                    cap = row['CAP'],
                    stato = row['STATO'],
                    codice_ateco = row['CODICE_ATECO'],
                   
                )
                try:
                   azienda.save()
                except IntegrityError as e:
                   errori.append(f"errore in {row['RAGIONE_SOCIALE']} {e}")
                except Exception as e:
                    errori.append(f"errore sconosciuto in {row['RAGIONE_SOCIALE']} {e}")
                    


        if errori:
                context = {'errori':errori}
                return render(request,"errori_importazione.html",context)
           
        
    return render(request,"errori_importazione.html",{})  

def upload(request):
    # carica il template per l'uload
    return render(request,"upload.html") 