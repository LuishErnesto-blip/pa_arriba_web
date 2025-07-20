from django.urls import path
from . import views

app_name = 'blog' # Define el namespace de la aplicación para evitar conflictos de nombres

urlpatterns = [
    # URL para la lista de todos los artículos del blog
    # Por ejemplo: http://127.0.0.1:8000/blog/
    path('', views.post_list, name='post_list'),

    # URL para el detalle de un artículo individual del blog
    # Por ejemplo: http://127.0.0.1:8000/blog/mi-primer-articulo/
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
