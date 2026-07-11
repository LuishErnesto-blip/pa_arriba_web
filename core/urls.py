from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('sri/', views.sri_landing, name='sri_landing'),
    path('rentabilidad/', views.rentabilidad_landing, name='rentabilidad_landing'),
    path('metodo/', views.metodo_landing, name='metodo_landing'),
    path('asesorias-gastronomicas/', views.asesorias_gastronomicas, name='asesorias_gastronomicas'),
    path('oxigeno-app/', views.oxigeno_app_landing, name='oxigeno_app_landing'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]