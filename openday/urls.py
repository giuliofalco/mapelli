from django.urls import path
from . import views

app_name="openday"

urlpatterns = [
    path('',views.index,name='index'),
    path('mioLogin',views.mioLogin,name='mioLogin'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('autentica',views.autentica,name='autentica'),
    path('iscrivi_utente/<str:sigla>',views.iscrivi_utente,name='iscrivi_utente'),
]