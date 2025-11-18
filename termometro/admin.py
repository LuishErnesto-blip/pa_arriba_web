from django.contrib import admin
from .models import TermometroRespuesta

@admin.register(TermometroRespuesta)
class TermometroRespuestaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "tipo_negocio", "crece", "avanza", "mejora", "reemprende", "fecha")
