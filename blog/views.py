from django.shortcuts import render, get_object_or_404
from .models import Post # MODIFICADO: Importamos tu modelo 'Post'

def post_list(request):
    """
    Vista para mostrar una lista de todos los artículos del blog publicados.
    """
    # MODIFICADO: Usamos 'Post' y filtramos por 'is_published' y ordenamos por 'published_date'
    blogs = Post.objects.filter(is_published=True).order_by('-published_date')

    context = {
        'blogs': blogs
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    """
    Vista para mostrar un artículo individual del blog.
    Utiliza get_object_or_404 para devolver un 404 si el artículo no existe.
    """
    # MODIFICADO: Usamos 'Post' y filtramos por 'is_published'
    post = get_object_or_404(Post, slug=slug, is_published=True)

    context = {
        'post': post
    }
    return render(request, 'blog/detalle_post.html', context)

