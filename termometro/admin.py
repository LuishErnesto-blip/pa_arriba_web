from django.contrib import admin
from .models import TermometroRespuesta

@admin.register(TermometroRespuesta)
class TermometroRespuestaAdmin(admin.ModelAdmin):
    # Columnas que verás en la lista de prospectos
    list_display = ('nombre', 'email', 'whatsapp', 'fase_final', 'fecha')
    
    # Filtros laterales para buscar rápido (por fase o tipo de negocio)
    list_filter = ('fase_final', 'tipo_negocio', 'fecha')
    
    # Barra de búsqueda para encontrar gente por nombre o correo
    search_fields = ('nombre', 'email', 'whatsapp')
    
    # Ordenar: los más nuevos primero
    ordering = ('-fecha',)
    
    # Fecha de registro (solo lectura para que nadie la altere)
    readonly_fields = ('fecha',)