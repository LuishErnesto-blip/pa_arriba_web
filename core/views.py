# Importa la función render de Django para renderizar plantillas HTML
from django.shortcuts import render

# Define la vista para la página principal (landing page)
def index(request):
    # Renderiza la plantilla 'core/index.html' cuando se accede a la URL principal
    return render(request, 'core/index.html')

# NUEVO: Define la vista para la página de política de privacidad
def privacy_policy(request):
    # Renderiza la plantilla 'core/privacy_policy.html' cuando se accede a la URL de política de privacidad
    return render(request, 'core/privacy_policy.html')
