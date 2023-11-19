from django.urls import path
from . import views

app_name="openday"

urlpatterns = [
    path('',views.index,name='index'),
    path('mioLogin',views.mioLogin,name='mioLogin'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('autentica',views.autentica,name='autentica'),
    path('iscrivi_utente/<str:sigla>',views.iscrivi_utente,name='iscrivi_utente'),
    path('indirizzi/<str:indirizzo>',views.indirizzi,name='indirizzi'),
    path('rileva_presenze/<str:sigla>',views.rileva_presenze,name='rileva_presenze'),
    path('conferma_presenza',views.conferma_presenza,name='conferma_presenza'),
    path('gallery',views.gallery,name='gallery'),
    path('upload',views.upload,name='upload'),
    path('upload_iscrizioni/<str:evento>',views.upload_iscrizioni,name='upload_iscrizioni'),
    path('stat_iscrizioni',views.stat_iscrizioni,name='stat_iscrizioni'),
    path('conferma_presenza/<int:id>/<str:sigla>',views.conferma_presenza,name='conferma_presenza'),
    path('cancella_presenza/<int:id>/<str:sigla>',views.cancella_presenza,name='cancella_presenza'),
]