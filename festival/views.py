from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from festival.models import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import datetime

LUOGHI = [('0','Villa Reale'),('1', 'Villasanta'), ('2', 'Villa Mirabello')]

def index(request):
    context = {}
    return render(request,'festival/index.html',context)

def elenco(request):
    luoghi = dict(LUOGHI)
    questionari = Questionari.objects.all()
    elenco = [(luoghi[str(q.luogo)],q.data,q.intervistatore,q.id) for q in questionari]
    context = {'elenco':elenco}
    return render(request,'festival/elenco.html',context)

def dettaglio(request,id):
   # mostra il dettaglio di un questionario
   quest = Questionari.objects.get(id=id)
   luogo = LUOGHI[quest.luogo][1]
   risposte = Risposte.objects.filter(questionario=quest)
   context = {'questionario':quest,'risposte':risposte, 'luogo':luogo}
   return render(request,'festival/dettaglio.html',context)

@login_required
def inserimento(request):
    luogo = ""
    intervistatore = ""
    domande = Domande.objects.all()
    questions = domande[:4] # le prime 4 domande

    if request.method == 'POST':
       luogo = request.POST.get('luogo')
       data = request.POST.get('data')
       intervistatore = request.POST.get('intervistatore')
       risposta_1 = request.POST.get('risposta-1')
       risposta_2 = request.POST.get('risposta-2')
       risposta_3 = request.POST.get('risposta-3')
       risposta_4 = request.POST.get('risposta-4')
       risposte = [risposta_1,risposta_2,risposta_3,risposta_4]
       questionario = Questionari(
                 luogo = luogo,
                 data = data,
                 intervistatore = intervistatore
       )
       questionario.save()

       for i in range(4):
          risp = Risposte()
          risp.domanda_id=domande[i].id
          risp.risposta=risposte[i]
          risp.questionario_id = questionario.id
          risp.save()

    now = datetime.datetime.now()
    adesso = now.strftime("%Y-%m-%d %H:%M:%S")

    context = {'adesso': adesso, 'questions':questions, 'luoghi':LUOGHI, 'luogo':str(luogo), 'intervistatore':intervistatore}
    return render(request,'festival/inserimento.html',context)

def mioLogin(request):
   # manda alla finestra di autenticazione, per chiedere username e password
   next = request.GET['next']
   context = {'next':next,}
   return render(request,'festival/login.html',context)

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
