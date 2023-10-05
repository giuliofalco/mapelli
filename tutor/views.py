from django.shortcuts import render
from pcto.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout


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