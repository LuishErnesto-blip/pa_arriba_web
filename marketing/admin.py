from django.contrib import admin
from django.core.mail import get_connection, EmailMessage
from django.utils import timezone
from django.contrib import messages
from .models import CampanaEmail, EnvioEmail


class EnvioEmailInline(admin.TabularInline):
    model = EnvioEmail
    extra = 0
    readonly_fields = ("email_destino", "nombre_destino", "enviado", "fecha_envio", "error")
    can_delete = False

def enviar_campana(modeladmin, request, queryset):
    from blog.models import Prospecto
    etapa_filtro = request.POST.get("etapa_filtro", "")
    dolor_filtro = request.POST.get("dolor_filtro", "")
    prospectos = Prospecto.objects.exclude(correo__isnull=True).exclude(correo__exact="")
    if etapa_filtro:
        prospectos = prospectos.filter(etapa=etapa_filtro)
    if dolor_filtro:
        prospectos = prospectos.filter(dolor_principal__icontains=dolor_filtro)
    connection = get_connection(
        backend="django.core.mail.backends.smtp.EmailBackend",
        host="mail.privateemail.com",
        port=587,
        username="contacto@pa-arriba.com",
        password="Appdiana2.",
        use_tls=True,
        fail_silently=False,
    )
    for campana in queryset:
        if campana.estado == "enviada":
            modeladmin.message_user(
                request,
                f"La campana {campana.nombre} ya fue enviada. Se omite.",
                level=messages.WARNING
            )
            continue
        enviados = 0
        for prospecto in prospectos:
            nombre_dest = prospecto.nombre_negocio if prospecto.nombre_negocio else ""
            envio, created = EnvioEmail.objects.get_or_create(
                campana=campana,
                prospecto=prospecto,
                defaults={
                    "email_destino": prospecto.correo,
                    "nombre_destino": nombre_dest,
                }
            )
            if envio.enviado:
                continue
            try:
                email = EmailMessage(
                    subject=campana.asunto,
                    body=campana.cuerpo,
                    from_email="Oxigeno App <contacto@pa-arriba.com>",
                    to=[prospecto.correo],
                    connection=connection,
                )
                email.content_subtype = "html"
                email.send()
                envio.enviado = True
                envio.fecha_envio = timezone.now()
                envio.save()
                enviados += 1
            except Exception as e:
                envio.error = str(e)
                envio.save()
        campana.total_enviados += enviados
        campana.fecha_envio = timezone.now()
        campana.estado = "enviada"
        campana.save()
        modeladmin.message_user(
            request,
            f"Campana {campana.nombre}: {enviados} emails enviados.",
            level=messages.SUCCESS
        )


enviar_campana.short_description = "Seleccionar leads y enviar campana"


@admin.register(CampanaEmail)
class CampanaEmailAdmin(admin.ModelAdmin):
    list_display = ("nombre", "asunto", "estado", "total_enviados", "fecha_envio")
    list_filter = ("estado",)
    search_fields = ("nombre", "asunto")
    actions = [enviar_campana]
    inlines = [EnvioEmailInline]


@admin.register(EnvioEmail)
class EnvioEmailAdmin(admin.ModelAdmin):
    list_display = ("campana", "email_destino", "nombre_destino", "enviado", "fecha_envio")
    list_filter = ("enviado", "campana")
    search_fields = ("email_destino", "nombre_destino")
    readonly_fields = ("campana", "prospecto", "email_destino", "nombre_destino", "enviado", "fecha_envio", "error")
