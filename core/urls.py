# Importa la función path de Django para definir URLs
from django.urls import path
# Importa las vistas de tu aplicación actual (core)
from . import views
app_name = 'core' # NUEVO: Define el namespace de la aplicación 'core'
# Define los patrones de URL para tu aplicación core
urlpatterns = [
    # URL para la página principal (landing page) de tu aplicación
    # Cuando alguien accede a la raíz de tu app (ej: www.tudominio.com/), se llama a la vista 'index'
    path('', views.index, name='index'), 
    # NUEVO: URL para la página de política de privacidad
    # Cuando alguien accede a www.tudominio.com/privacy-policy/, se llama a la vista 'privacy_policy'
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'), 
]
