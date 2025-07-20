# Importa la función render de Django para renderizar plantillas HTML
from django.shortcuts import render
# Importamos el modelo Post de la aplicación blog para obtener los artículos
from blog.models import Post # NUEVO: Importamos el modelo Post

# Define la vista para la página principal (landing page)
def index(request):
    """
    Vista para la página principal que ahora también carga los últimos posts del blog.
    """
    # Obtener los 3 artículos de blog más recientes y publicados
    # Asegúrate de que el campo 'is_published' y 'published_date' existan en tu modelo Post
    latest_posts = Post.objects.filter(is_published=True).order_by('-published_date')[:3]

    # Crea un diccionario de contexto para pasar datos a la plantilla
    context = {
        'latest_posts': latest_posts # NUEVO: Pasamos los últimos posts a la plantilla
    }
    # Renderiza la plantilla 'core/index.html' con el contexto
    return render(request, 'core/index.html', context)

# Define la vista para la página de política de privacidad
def privacy_policy(request):
    """
    Vista para la página de política de privacidad.
    """
    # Renderiza la plantilla 'core/privacy_policy.html' cuando se accede a la URL de política de privacidad
    return render(request, 'core/privacy_policy.html')

