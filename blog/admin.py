from django.contrib import admin
from .models import Post, Prospecto
from import_export.admin import ImportExportModelAdmin
from ckeditor.widgets import CKEditorWidget

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content', 'keywords')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {'fields': ('title', 'meta_description', 'slug', 'author', 'published_date', 'is_published')}),
        ('Contenido', {'fields': ('content', 'image', 'image_alt_text', 'keywords')}),
    )
    actions = ['make_published', 'make_draft']
    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = "Marcar como publicados"
    def make_draft(self, request, queryset):
        queryset.update(is_published=False)
    make_draft.short_description = "Marcar como borrador"

admin.site.register(Post, PostAdmin)

@admin.register(Prospecto)
class ProspectoAdmin(ImportExportModelAdmin):
    list_display = ('nombre_negocio', 'nombre_dueño', 'telefono', 'etapa', 'dolor_principal', 'canal_entrada', 'fecha_proxima_accion')
    list_filter = ('etapa', 'dolor_principal', 'canal_entrada')
    search_fields = ('nombre_negocio', 'nombre_dueño', 'telefono')
    list_editable = ('etapa',)
    fieldsets = (
        ('Datos Básicos', {'fields': ('nombre_dueño', 'nombre_negocio', 'telefono', 'correo', 'ubicacion')}),
        ('Clasificación', {'fields': ('etapa', 'dolor_principal', 'canal_entrada', 'que_usa_hoy')}),
        ('Seguimiento', {'fields': ('ultimo_mensaje_enviado', 'ultima_respuesta', 'proxima_accion', 'fecha_proxima_accion', 'fecha_ultima_llamada')}),
        ('Acuerdos y Notas', {'fields': ('acuerdo_1', 'acuerdo_2', 'acuerdo_3', 'notas_generales')}),
    )
