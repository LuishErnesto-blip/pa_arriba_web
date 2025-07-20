# blog/admin.py
from django.contrib import admin
from .models import Post # Importamos el modelo Post
from ckeditor.widgets import CKEditorWidget # Importamos CKEditorWidget si lo necesitamos para el admin

# Clase para personalizar cómo se muestra y se comporta el modelo Post en el admin
class PostAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de Posts en el admin
    list_display = ('title', 'author', 'published_date', 'is_published')

    # Campos por los que se puede filtrar la lista de Posts
    list_filter = ('published_date', 'author')

    # Campos por los que se puede buscar en la lista de Posts
    search_fields = ('title', 'content', 'keywords')

    # Campos que se autocompletan al escribir (útil para relaciones, aquí no aplica directamente)
    # raw_id_fields = ('author',) # Si 'author' fuera un ForeignKey a User

    # Campos que se rellenan automáticamente (ej. slug a partir del título)
    prepopulated_fields = {'slug': ('title',)}

    # Campos que se muestran en el formulario de edición/creación
    fieldsets = (
        (None, {
            'fields': ('title', 'meta_description', 'slug', 'author', 'published_date', 'is_published'),
        }),
        ('Contenido del Artículo', {
            'fields': ('content', 'image', 'image_alt_text', 'keywords'),
            'description': 'Aquí puedes redactar el contenido de tu blog y gestionar la imagen destacada.'
        }),
    )

      # NUEVO: Añadimos la clase Media para incluir CSS y JS personalizados
    class Media:
        css = {
            'all': ('blog/admin.css',) # Ruta a nuestro archivo CSS personalizado
        }

    # Añadimos un campo booleano para controlar si el post está publicado o es un borrador
    actions = ['make_published', 'make_draft']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = "Marcar posts seleccionados como publicados"

    def make_draft(self, request, queryset):
        queryset.update(is_published=False)
    make_draft.short_description = "Marcar posts seleccionados como borrador"

# Registramos el modelo Post con nuestra clase PostAdmin personalizada
admin.site.register(Post, PostAdmin)