from django.urls import path
from . import views

app_name="OffPcto"

urlpatterns = [
      path('',views.index,name="index"),
      path('tutor/',views.tutor,name="tutor"),
      path('aziende/',views.aziende,name="aziende"),
      path('aziende/<str:piva>',views.dettaglio_azienda,name="dettaglio_aziende"),
]
