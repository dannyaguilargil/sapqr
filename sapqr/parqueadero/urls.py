from django.urls import path
from . import views

urlpatterns = [
    path('', views.registro_general, name='casita'),
    path('registro/', views.registro_general, name='registro_general'),
    path('registro/<uuid:uuid>/', views.registro_qr, name='registro_qr'),
]
