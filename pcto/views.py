from django.shortcuts import render
from pcto.models import *
from django.templatetags.static import static
from django.core.paginator import Paginator,EmptyPage

from .filters import AziendeFilter

def index(request):
    return render(request,'index.html',{})
    
def tutor(request):
     elenco = Tutor.objects.all()
     context = {'object_list':elenco}
     return render(request,"tutor.html",context)

def aziende(request):
    elenco = Aziende.objects.all()

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
              }
    return render(request,"aziende.html",context)

def dettaglio_azienda(request,piva):
    azienda = Aziende.objects.get(partita_iva=piva)
    context = {'azienda':azienda,}
    return render(request,"dettaglio_azienda.html",context)   
