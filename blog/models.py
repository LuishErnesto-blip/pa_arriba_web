# blog/models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import strip_tags
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título del Artículo")
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    content = RichTextField(blank=True, null=True, verbose_name="Contenido del Artículo")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Publicación")
    author = models.CharField(max_length=100, default="Pa´Arriba Equipo", verbose_name="Autor")
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=200)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    image_alt_text = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=False, verbose_name="Publicado")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            queryset = Post.objects.all().exclude(pk=self.pk)
            count = 1
            while queryset.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{count}"
                count += 1
        if not self.meta_description and self.content:
            cleaned_content = strip_tags(self.content)
            self.meta_description = cleaned_content[:160]
            last_space = self.meta_description.rfind(' ')
            if last_space != -1 and len(cleaned_content) > 160:
                self.meta_description = self.meta_description[:last_space] + '...'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Artículo de Blog"
        verbose_name_plural = "Artículos de Blog"


class Prospecto(models.Model):
    ETAPAS = [
        ('e0', 'E0 — Sin contactar'),
        ('e1', 'E1 — Mensaje enviado, sin respuesta'),
        ('e2', 'E2 — Conversación activa'),
        ('e3', 'E3 — Demo agendada'),
        ('e4', 'E4 — Negociación'),
        ('congelador', 'Congelador — Reactivar en 30 días'),
        ('alianza', 'Alianza — Canal diferente'),
        ('perdido', 'Perdido — Sin respuesta'),
        ('cerrado', 'Cerrado — Cliente ganado'),
    ]

    DOLORES = [
        ('costos_ojo', '#1 No controla costos — trabaja al ojo'),
        ('mermas', '#2 Mermas y fugas de dinero'),
        ('inventario', '#3 Sin control de inventario'),
        ('facturacion', '#4 Facturación manual'),
        ('otro', 'Otro'),
    ]

    CANALES = [
        ('meta_ad1', 'Meta Ads — Ad 1 Carrusel Mermas'),
        ('meta_ad2', 'Meta Ads — Ad 2'),
        ('meta_ad3', 'Meta Ads — Ad 3'),
        ('meta_ad4', 'Meta Ads — Ad 4 Reel Fugas'),
        ('referido', 'Referido'),
        ('organico', 'Orgánico'),
        ('otro', 'Otro'),
    ]

    # Datos básicos
    nombre_dueño = models.CharField(max_length=100, verbose_name="Nombre del Dueño")
    nombre_negocio = models.CharField(max_length=100, verbose_name="Nombre del Negocio")
    telefono = models.CharField(max_length=20, verbose_name="WhatsApp/Teléfono")
    correo = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    ubicacion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ciudad / Ubicación")

    # Clasificación
    etapa = models.CharField(max_length=20, choices=ETAPAS, default='e0', verbose_name="Etapa")
    dolor_principal = models.CharField(max_length=20, choices=DOLORES, blank=True, null=True, verbose_name="Dolor Principal")
    canal_entrada = models.CharField(max_length=20, choices=CANALES, blank=True, null=True, verbose_name="Canal de Entrada")
    que_usa_hoy = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Qué usa hoy?")

    # Seguimiento
    ultimo_mensaje_enviado = models.TextField(blank=True, null=True, verbose_name="Último mensaje enviado")
    ultima_respuesta = models.TextField(blank=True, null=True, verbose_name="Última respuesta recibida")
    proxima_accion = models.TextField(blank=True, null=True, verbose_name="Próxima acción")
    fecha_proxima_accion = models.DateField(blank=True, null=True, verbose_name="Fecha próxima acción")

    # Acuerdos
    fecha_ultima_llamada = models.DateField(blank=True, null=True, verbose_name="Última Llamada")
    acuerdo_1 = models.TextField(blank=True, null=True, verbose_name="Acuerdo 1")
    acuerdo_2 = models.TextField(blank=True, null=True, verbose_name="Acuerdo 2")
    acuerdo_3 = models.TextField(blank=True, null=True, verbose_name="Acuerdo 3")
    notas_generales = models.TextField(blank=True, null=True, verbose_name="Notas Generales")

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_negocio} — {self.nombre_dueño} [{self.get_etapa_display()}]"

    class Meta:
        verbose_name = "Prospecto CRM"
        verbose_name_plural = "Prospectos CRM"
        ordering = ['-fecha_actualizacion']
