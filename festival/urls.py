from . import views
from django.urls import path

app_name="festival"

urlpatterns = [
      path('',views.index,name="index"),
      path('elenco',views.elenco,name="elenco"),
      path('inserimento',views.inserimento,name="inserimento"),
      path('dettaglio/<int:id>',views.dettaglio,name="dettaglio"),
      path('report',views.report,name="report"),
      path('download',views.download,name='download'),
]