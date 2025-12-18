# blog/models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import strip_tags # Ya importado para meta_description
from ckeditor.fields import RichTextField # NUEVO: Importamos RichTextField

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título del Artículo")

    meta_description = models.CharField(
        max_length=160,
        blank=True,
        null=True,
        help_text="Breve descripción para los motores de búsqueda (máx. 160 caracteres)."
    )

    # MODIFICADO: Usamos RichTextField para el contenido
    content = RichTextField(blank=True, null=True, verbose_name="Contenido del Artículo")

    published_date = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Publicación")

    author = models.CharField(max_length=100, default="Pa´Arriba Equipo", verbose_name="Autor")

    slug = models.SlugField(unique=True, blank=True, null=True, max_length=200, verbose_name="Slug (URL amigable)")

    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Imagen Destacada")

    image_alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Texto alternativo para la imagen (importante para SEO y accesibilidad)."
    )

    keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Palabras clave separadas por comas para SEO."
    )

    is_published = models.BooleanField(default=False, verbose_name="Publicado")

    def save(self, *args, **kwargs):
        # Lógica para generar el slug automáticamente si no se proporciona
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            queryset = Post.objects.all().exclude(pk=self.pk)
            count = 1
            while queryset.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{count}"
                count += 1

        # Lógica para generar la meta descripción automáticamente si está vacía
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
    ESTADOS = [
        ('frio', '❄️ Frío'),
        ('caliente', '🔥 Caliente'),
        ('demo', '🎥 Demo Enviada'),
        ('seguimiento', '📞 Próximo Contacto'),
        ('cerrado', '✅ Cliente Ganado'),
    ]

    nombre_dueño = models.CharField(max_length=100, verbose_name="Nombre del Dueño")
    nombre_negocio = models.CharField(max_length=100, verbose_name="Nombre del Negocio")
    telefono = models.CharField(max_length=20, verbose_name="WhatsApp/Teléfono")
    ubicacion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Dirección o Ubicación")
    correo = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    
    que_usa_hoy = models.CharField(max_length=100, blank=True, null=True, verbose_name="¿Qué usa hoy?")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='frio', verbose_name="Estado del Prospecto")
    
    # Seguimiento y Acuerdos
    fecha_ultima_llamada = models.DateField(blank=True, null=True, verbose_name="Última Llamada")
    acuerdo_1 = models.TextField(blank=True, null=True, verbose_name="Acuerdo 1")
    fecha_acuerdo_2 = models.DateField(blank=True, null=True, verbose_name="Fecha Acuerdo 2")
    acuerdo_2 = models.TextField(blank=True, null=True, verbose_name="Acuerdo 2")
    fecha_acuerdo_3 = models.DateField(blank=True, null=True, verbose_name="Fecha Acuerdo 3")
    acuerdo_3 = models.TextField(blank=True, null=True, verbose_name="Acuerdo 3")

    notas_generales = models.TextField(blank=True, null=True, verbose_name="Notas Generales")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_negocio} - {self.nombre_dueño}"

    class Meta:
        verbose_name = "Prospecto CRM"
        verbose_name_plural = "Prospectos CRM"
        ordering = ['-fecha_registro']