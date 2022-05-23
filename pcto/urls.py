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
]
