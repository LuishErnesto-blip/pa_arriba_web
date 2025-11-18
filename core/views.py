import os
import logging
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from blog.models import Post
from store.models import Product  # <--- ¡IMPORTANTE! Traemos el modelo de Productos
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

# Página principal (landing page)
def index(request):
    # 1. Cargar Blog
    latest_posts = []
    try:
        latest_posts = Post.objects.filter(is_published=True).order_by('-published_date')[:3]
    except Exception as e:
        logger.error(f"Error al cargar los últimos posts del blog en la vista index: {e}")

    # 2. Cargar Tienda (ESTO FALTABA)
    products = []
    try:
        # Intentamos traer los productos. Usamos .all() para asegurar que traiga algo.
        # Si tienes un campo 'is_active', podrías usar .filter(is_active=True)
        products = Product.objects.all().order_by('-id')[:4] 
    except Exception as e:
        logger.error(f"Error al cargar productos en la vista index: {e}")

    # 3. Empaquetar todo para la plantilla
    context = {
        'latest_posts': latest_posts,
        'products': products  # <--- Aquí enviamos los productos a la mesa
    }
    return render(request, 'core/index.html', context)

# Política de privacidad
def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

# robots.txt con dominio forzado
def robots_txt(request):
    """
    Sirve robots.txt apuntando al sitemap en tu dominio personalizado.
    """
    base_url = getattr(settings, 'SITE_URL', 'https://pa-arriba.com').rstrip('/')
    content = f"User-agent: *\nAllow: /\n\nSitemap: {base_url}/sitemap.xml"
    return HttpResponse(content, content_type="text/plain")

# sitemap.xml dinámico con dominio forzado
def sitemap_xml(request):
    """
    Genera sitemap.xml dinámico usando el dominio configurado y tus posts publicados.
    """
    host = request.get_host()
    if 'onrender.com' in host:
        base_url = 'https://pa-arriba.com'
    else:
        base_url = f'https://{host}'

    static_urls = [
        {"loc": f"{base_url}/", "lastmod": "2025-07-22", "changefreq": "daily", "priority": "1.0"},
        {"loc": f"{base_url}/blog/", "lastmod": "2025-07-22", "changefreq": "daily", "priority": "0.8"},
        {"loc": f"{base_url}/store/", "lastmod": "2025-07-22", "changefreq": "weekly", "priority": "0.7"},
        {"loc": f"{base_url}/privacy-policy/", "lastmod": "2025-07-22", "changefreq": "monthly", "priority": "0.5"},
    ]

    # URLs de posts publicados
    post_urls = []
    try:
        posts = Post.objects.filter(is_published=True).order_by('-published_date')
        for p in posts:
            lastmod = (p.published_date.date().isoformat()
                       if hasattr(p, 'published_date') and p.published_date
                       else datetime.utcnow().date().isoformat())
            post_urls.append({
                "loc": f"{base_url}/blog/{p.slug}/",
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.9",
            })
    except Exception as e:
        logger.error(f"Error al generar URLs de posts en sitemap: {e}")

    # Construcción del XML
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!-- PA-ARRIBA SITEMAP V1 -->',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for entry in static_urls + post_urls:
        lines.extend([
            '  <url>',
            f'    <loc>{entry["loc"]}</loc>',
            f'    <lastmod>{entry["lastmod"]}</lastmod>',
            f'    <changefreq>{entry["changefreq"]}</changefreq>',
            f'    <priority>{entry["priority"]}</priority>',
            '  </url>'
        ])
    lines.append('</urlset>')
    xml_content = "\n".join(lines)

    return HttpResponse(xml_content, content_type='application/xml')

@require_POST
def diagnostico_submit(request):
    """
    Placeholder para recibir el POST del formulario del termómetro.
    Integra aquí tu lógica si es necesario, aunque ya la manejas en termometro/views.py.
    """
    return HttpResponse('Formulario procesado correctamente.', status=200)