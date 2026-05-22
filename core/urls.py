from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('custom-sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('', views.index, name='index'),
    path('asesorias-gastronomicas/', views.asesorias_gastronomicas, name='asesorias_gastronomicas'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]