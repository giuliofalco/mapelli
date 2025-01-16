from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('edit/<int:year>/<int:month>/<int:day>/', views.day_editor, name='day_editor'),
    path('pdfs/<str:filename>', views.serve_pdf, name='serve_pdf'),
    path('monthly_report/', views.monthly_report, name='monthly_report'),
]