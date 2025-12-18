# blog/admin.py
from django.contrib import admin
from .models import Post, Prospecto # Importamos ambos modelos
from import_export.admin import ImportExportModelAdmin # Nueva herramienta para Excel/PDF
from ckeditor.widgets import CKEditorWidget

# --- SECCIÓN DE BLOG ---
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content', 'keywords')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'meta_description', 'slug', 'author', 'published_date', 'is_published'),
        }),
        ('Contenido del Artículo', {
            'fields': ('content', 'image', 'image_alt_text', 'keywords'),
            'description': 'Aquí puedes redactar el contenido de tu blog y gestionar la imagen destacada.'
        }),
    )

    class Media:
        css = {
            'all': ('blog/admin.css',)
        }

    actions = ['make_published', 'make_draft']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = "Marcar posts seleccionados como publicados"

    def make_draft(self, request, queryset):
        queryset.update(is_published=False)
    make_draft.short_description = "Marcar posts seleccionados como borrador"

admin.site.register(Post, PostAdmin)

# --- SECCIÓN DE CRM (Con Exportación activada) ---
@admin.register(Prospecto)
class ProspectoAdmin(ImportExportModelAdmin): # Aquí activamos la magia del Excel
    list_display = ('nombre_negocio', 'nombre_dueño', 'estado', 'fecha_registro')
    list_filter = ('estado', 'fecha_registro')
    search_fields = ('nombre_negocio', 'nombre_dueño', 'telefono')
    list_editable = ('estado',)