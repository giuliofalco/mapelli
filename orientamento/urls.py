from . import views
from django.urls import path

app_name="orientamento"

urlpatterns = [
      path('',views.index,name="index"),
      path('mioLogin',views.mioLogin,name='mioLogin'),
      path('logout_view',views.logout_view,name='logout_view'),
      path('autentica',views.autentica,name='autentica'),
]