from django.shortcuts import render
from pcto.models import *
from django.templatetags.static import static
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .filters import AziendeFilter
from pcto.indirizzi import *

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
    if contatto:
        obj = Contatti.objects.get(id=contatto)
        obj.note = note
        obj.save()

    if contatti:
        posti = contatti[0].num_studenti - len(abbinamenti)
    else:
        posti = 0
        
    context = {'azienda':azienda, 'contatti': contatti, 'abbinamenti':abbinamenti, 
               'posti':posti, 'tutor':tutor}
    context['user'] = visualizza_utente(request)
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


  
