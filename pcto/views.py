from django.shortcuts import render
from pcto.models import *
from django.templatetags.static import static
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .filters import AziendeFilter

def index(request):
    return render(request,'index.html',{})
    
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
    azienda = Aziende.objects.get(partita_iva=piva)
    contatti = azienda.contatti_set.all()
    context = {'azienda':azienda, 'contatti': contatti}
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
  
