from django.db import models
from blog.models import Prospecto


class CampanaEmail(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('enviada', 'Enviada'),
    ]
    nombre = models.CharField(max_length=200)
    asunto = models.CharField(max_length=300)
    cuerpo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    total_enviados = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Campaña Email'
        verbose_name_plural = 'Campañas Email'

    def __str__(self):
        return self.nombre


class EnvioEmail(models.Model):
    campana = models.ForeignKey(CampanaEmail, on_delete=models.CASCADE, related_name='envios')
    prospecto = models.ForeignKey(Prospecto, on_delete=models.CASCADE, related_name='envios_email')
    email_destino = models.CharField(max_length=254)
    nombre_destino = models.CharField(max_length=200)
    enviado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Envío Email'
        verbose_name_plural = 'Envíos Email'

    def __str__(self):
        return f"{self.campana.nombre} → {self.email_destino}"
