from django.urls import path
from . import views

app_name="pcto"

urlpatterns = [
      path('',views.index,name="index"),
      path('tutor/',views.tutor,name="tutor"),
      path('aziende/',views.aziende,name="aziende"),
      path('aziende/<str:piva>',views.dettaglio_azienda,name="dettaglio_aziende"),
      path('mioLogin',views.mioLogin,name="mioLogin"),
      path('autentica',views.autentica,name="autentica"),
      path('contatti/',views.contatti,name='contatti'),
      path('studenti/<str:corso>',views.studenti,name='studenti'),
      path('elenco_abbinamenti',views.elenco_abbinamenti,name='elenco_abbinamenti'),
      path('inserisci',views.inserisci,name="inserisci"),
      path('cancella',views.cancella,name="cancella"),
      path('add_contatto',views.add_contatto,name="add_contatto"),
      path('statistica',views.statistica,name="statistica"),
      path('dettaglio_stat/<str:azienda>',views.dettaglio_stat,name="dettaglio_stat"),
      # path('importa/<str:model>',views.importa,name="importa"),

]
