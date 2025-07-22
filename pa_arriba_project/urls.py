"""
URL configuration for pa_arriba_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Importaciones necesarias para servir archivos estáticos y de medios en desarrollo
from django.conf import settings
from django.conf.urls.static import static
# ELIMINADO: Importaciones para el sitemap dinámico
# from django.contrib.sitemaps.views import sitemap
# from blog.sitemaps import PostSitemap # Importa la clase PostSitemap

# ELIMINADO: Definición de los sitemaps disponibles para tu proyecto
# sitemaps = {
#     'posts': PostSitemap, # 'posts' es un nombre que le das a este sitemap
# }

urlpatterns = [
    path('admin/', admin.site.urls), # Ruta para el panel de administración de Django
    path('', include('core.urls')), # Incluye las URLs de tu aplicación 'core' (probablemente la página de inicio)
    path('store/', include('store.urls')), # Incluye las URLs de tu aplicación 'store'
    path('blog/', include('blog.urls')), # Incluye las URLs de tu aplicación 'blog'
    path('ckeditor/', include('ckeditor_uploader.urls')), # URLs para el uploader de CKEditor
    # ELIMINADO: Ruta para el sitemap XML dinámico que causaba el error 500
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# ¡IMPORTANTE! Solo servir archivos estáticos y de medios en modo de desarrollo
# Estas configuraciones son cruciales para que las imágenes y otros archivos se muestren
# correctamente cuando estás desarrollando localmente. NO deben usarse en producción.
if settings.DEBUG:
    # Sirve archivos de medios (imágenes subidas por usuarios)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Sirve archivos estáticos (CSS, JS, imágenes de diseño)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
