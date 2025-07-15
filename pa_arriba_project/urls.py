from django.contrib import admin
from django.urls import path, include
from django.conf import settings # ¡Necesario para acceder a DEBUG, STATIC_URL, etc.!
from django.conf.urls.static import static 
from pathlib import Path # Necesario para BASE_DIR con Path
from django.views.generic.base import RedirectView # NUEVO: Importar RedirectView para el favicon

urlpatterns = [
    # NUEVO: URL para el favicon
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'core/logo_pa_arriba_fav_icon.png', permanent=True)),
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # O la ruta a tu app principal 'core'
]

# ¡IMPORTANTE! Solo servir archivos estáticos en modo de desarrollo
if settings.DEBUG:
    # Sirve los archivos de medios (ej. imágenes subidas por usuarios)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Sirve los archivos estáticos (CSS, JS, imágenes de tu diseño)
    # STATIC_ROOT es la ubicación donde collectstatic copia todos los archivos estáticos.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
