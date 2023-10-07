from . import views
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

]