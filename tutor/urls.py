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
      path('upload_csv_tutor',views.upload_csv_tutor,name='upload_csv_tutor'),
      path('proposte',views.proposte,name='proposte'),
      path('elenco_tutor',views.elenco_tutor,name='elenco_tutor'),

]