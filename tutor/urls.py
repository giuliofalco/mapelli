from . import views
from .views import *
from django.urls import path

app_name="tutor"

urlpatterns = [
      path('',views.index,name="index"),
      path('mioLogin',views.mioLogin,name='mioLogin'),
      path('logout_view',views.logout_view,name='logout_view'),
      path('autentica',views.autentica,name='autentica'),
      path('upload',views.upload,name='upload'),
      path('upload_csv_proposte',views.upload_csv_proposte,name='upload_csv_proposte'),
      path('upload_csv_studenti',views.upload_csv_studenti,name='upload_csv_studenti'),
      path('upload_csv/<str:tabella>',views.upload_csv,name='upload_csv'),
      path('proposte',views.proposte,name='proposte'),
      path('elenco_tutor',views.elenco_tutor,name='elenco_tutor'),
      path('elenco_classi',views.elenco_classi,name='elenco_classi'),
      path('elenco_studenti/<str:classe>',views.elenco_studenti,name='elenco_studenti'),
      path('completa_classi',views.completa_classi,name='completa_classi'),
      path('completa_tutor',views.completa_tutor,name='completa_tutor'),
      path('adesioni',views.adesioni,name='adesioni'),
      path('dettaglio_proposta/<int:prop>',views.dettaglio_proposta,name='dettaglio_proposta'),
      path('upload_csv_doc_coinvolti',views.upload_csv_doc_coinvolti,name='upload_csv_doc_coinvolti'),
      path('aggiungimi/<int:id>',views.aggiungimi,name='aggiungimi'),
      path('cancellami/<int:id>',views.cancellami,name='cancellami'),
      path('change_password/', ChangePasswordView.as_view(), name='change_password'),
      path('adesioni_proposta/<int:id>',views.adesioni_proposta,name='adesioni_proposta'),
      path('salva_iscrizioni',views.salva_iscrizioni,name='salva_iscrizioni'),
      path('ritira/<int:idstudente>/<int:idproposta>',views.ritira,name='ritira'),
]