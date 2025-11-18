from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# --- IMPORTACIÓN CLAVE PARA SEO ---
# Traemos las funciones que creaste en core/views.py para que Google las vea
from core.views import robots_txt, sitemap_xml 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('store/', include('store.urls')),
    path('blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Ruta Estratégica para el Test de Caos
    path('diagnostico/', include('termometro.urls')),

    # --- RUTAS SEO PARA GOOGLE ---
    # Esto permite que funcionen tusitio.com/robots.txt y tusitio.com/sitemap.xml
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)