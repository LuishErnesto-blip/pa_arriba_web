import os
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from blog.models import Post
from store.models import Product
from django.views.decorators.http import require_POST

def index(request):
    products = Product.objects.all().order_by('-id')[:4]
    context = {'products': products}
    return render(request, 'core/index.html', context)

def asesorias_gastronomicas(request):
    return render(request, 'core/asesorias_gastronomicas.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def robots_txt(request):
    """
    🟢[CAMBIO] FECHA:2026-07-10|MOTIVO: robots.txt mejorado — bloquea admin/ckeditor/store, declara sitemap
    """
    base_url = getattr(settings, 'SITE_URL', 'https://pa-arriba.com').rstrip('/')
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Bloquear rutas administrativas y privadas",
        "Disallow: /admin/",
        "Disallow: /ckeditor/",
        "Disallow: /store/",
        "",
        "# Sitemap",
        f"Sitemap: {base_url}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    """
    🟢[CAMBIO] FECHA:2026-07-10|MOTIVO: sitemap.xml actualizado — agrega 3 landings SEO + mantiene blog dinámico
    """
    base_url = getattr(settings, 'SITE_URL', 'https://pa-arriba.com').rstrip('/')

    static_urls = [
        {"loc": f"{base_url}/",                        "lastmod": "2026-07-10", "changefreq": "weekly",  "priority": "1.0"},
        {"loc": f"{base_url}/asesorias-gastronomicas/", "lastmod": "2026-07-10", "changefreq": "monthly", "priority": "0.9"},
        {"loc": f"{base_url}/curso-de-costos-para-restaurantes/", "lastmod": "2026-09-05", "changefreq": "monthly", "priority": "0.9"},
        {"loc": f"{base_url}/marketing-digital-gastronomico/", "lastmod": "2026-09-06", "changefreq": "monthly", "priority": "0.9"},
        {"loc": f"{base_url}/cliente-fantasma-restaurantes/", "lastmod": "2026-09-06", "changefreq": "monthly", "priority": "0.9"},
        {"loc": f"{base_url}/metodo/",                  "lastmod": "2026-07-10", "changefreq": "monthly", "priority": "0.9"},
        {"loc": f"{base_url}/rentabilidad/",            "lastmod": "2026-07-10", "changefreq": "monthly", "priority": "0.9"},
        {"loc": f"{base_url}/sri/",                     "lastmod": "2026-07-10", "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{base_url}/oxigeno-app/",             "lastmod": "2026-07-10", "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{base_url}/diagnostico/",             "lastmod": "2026-07-10", "changefreq": "monthly", "priority": "0.6"},
        {"loc": f"{base_url}/blog/",                    "lastmod": "2026-07-10", "changefreq": "weekly",  "priority": "0.5"},
        {"loc": f"{base_url}/privacy-policy/",          "lastmod": "2026-07-10", "changefreq": "yearly",  "priority": "0.2"},
    ]

    post_urls = []
    try:
        posts = Post.objects.filter(is_published=True).order_by('-published_date')
        for p in posts:
            lastmod = p.published_date.date().isoformat() if p.published_date else datetime.utcnow().date().isoformat()
            post_urls.append({
                "loc": f"{base_url}/blog/{p.slug}/",
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.8"
            })
    except Exception:
        pass

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
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

    return HttpResponse("\n".join(lines), content_type='application/xml; charset=utf-8')

@require_POST
def diagnostico_submit(request):
    return HttpResponse('Formulario procesado correctamente.', status=200)

def sri_landing(request):
    return render(request, 'core/sri_landing.html')

def rentabilidad_landing(request):
    return render(request, 'core/rentabilidad_landing.html')

def metodo_landing(request):
    return render(request, 'core/metodo_landing.html')

def oxigeno_app_landing(request):
    return render(request, 'core/oxigeno_app_landing.html')

def curso_costos_landing(request):
    return render(request, 'core/curso_costos_landing.html')

def marketing_digital_landing(request):
    return render(request, 'core/marketing_digital_landing.html')

def cliente_fantasma_landing(request):
    return render(request, 'core/cliente_fantasma_landing.html')
