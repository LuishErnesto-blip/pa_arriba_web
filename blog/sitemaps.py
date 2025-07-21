from django.contrib.sitemaps import Sitemap
from .models import Post # Importa tu modelo Post de la aplicación blog

class PostSitemap(Sitemap):
    # Frecuencia con la que se espera que cambie el contenido de los posts.
    # 'daily', 'weekly', 'monthly', 'yearly', 'always', 'hourly', 'never'.
    changefreq = "daily"

    # Prioridad de esta URL en relación con otras URLs de tu sitio (0.0 a 1.0).
    # Los posts del blog suelen tener una prioridad alta.
    priority = 0.9

    def items(self):
        # Retorna todos los objetos Post que están publicados.
        # Esto asegura que solo los posts visibles aparezcan en el sitemap.
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        # Retorna la fecha de la última modificación del objeto.
        # Esto ayuda a los motores de búsqueda a saber cuándo rastrear de nuevo.
        return obj.published_date # Asume que tienes un campo 'published_date' en tu modelo Post
