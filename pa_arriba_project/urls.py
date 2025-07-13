from django.contrib import admin
from django.urls import path, include
from django.conf import settings # ¡Necesario para acceder a DEBUG, STATIC_URL, etc.!
from django.conf.urls.static import static # ¡Necesario para servir archivos estáticos!
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
    # Aseguramos que Django sirve los archivos estáticos.
    # document_root puede ser STATIC_ROOT o tus STATICFILES_DIRS específicos.
    # Optamos por la carpeta de tu app 'core' donde está el logo
    urlpatterns += static(settings.STATIC_URL, document_root=Path(settings.BASE_DIR) / 'core' / 'static')

    # Opcional: También podrías añadir la línea de STATIC_ROOT por si acaso,
    # aunque la de arriba es más directa para tu caso de uso del logo en desarrollo.
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
