from django.shortcuts import render
from pcto.models import *
from django.templatetags.static import static
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .filters import AziendeFilter
from pcto.indirizzi import *


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
    context = {'contatti':contatti}
    return render(request,"contatti.html",context)

def studenti(request,corso):
    # visualizza gli studenti del corso suddivisi per classi
    
    studenti = Studenti.objects.all()
    studenti_corso = [item for item in studenti if item.corso()==corso]
    classi = [item.classe for item in studenti_corso]
    classi = set(classi) # tolgo i doppioni
    classi = list(classi)
    classi.sort()
    report = [[classe,[studente for studente in studenti if studente.classe == classe]] for classe in classi]
    context = {'corso':sigle[corso],'report':report, 'classi' : classi}
    return render(request,"studenti.html",context)


  
