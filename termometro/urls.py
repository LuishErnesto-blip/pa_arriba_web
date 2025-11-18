from django.urls import path
from . import views

# Opcional pero recomendado: define el namespace de la aplicación
app_name = 'termometro' 

urlpatterns = [
    # 1. URL para la Landing Page (la que muestra el formulario)
    # Nota: Si tu URL principal es '/diagnostico/', el patrón en urls.py debe ser 'diagnostico/'
    # Si la ruta en el urls principal ya es path('diagnostico/', include('termometro.urls')), 
    # entonces aquí solo necesitas '' o 'landing/'
    # Asumo que la ruta principal tiene: path('diagnostico/', include('termometro.urls'))
    path('', views.termometro_landing, name='diagnostico'), # Cambiamos el nombre a 'diagnostico' para que coincida con lo que tu template de la landing necesita para crear el enlace de vuelta a la pagina.

    # 2. URL para el envío del formulario (la ruta que estaba faltando)
    path('enviar/', views.diagnostico_submit, name='diagnostico_submit'),
]