# Importa las funciones necesarias de Django
from django.shortcuts import render
from django.http import HttpResponse # Importa HttpResponse para servir contenido de texto

# Importamos el modelo Post de la aplicación blog para obtener los artículos
from blog.models import Post

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
        'latest_posts': latest_posts # Pasamos los últimos posts a la plantilla
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

def robots_txt(request):
    """
    Vista para servir el contenido del archivo robots.txt directamente.
    Esto asegura que el archivo sea accesible en la raíz del dominio para los motores de búsqueda.
    """
    # El contenido de robots.txt se define aquí directamente.
    # Incluye la directiva Sitemap apuntando a la URL de tu sitemap.
    return HttpResponse("User-agent: *\nAllow: /\n\nSitemap: https://pa-arriba-landing.onrender.com/sitemap.xml", content_type="text/plain")
