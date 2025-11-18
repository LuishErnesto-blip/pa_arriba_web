from django.db import models

class TermometroRespuesta(models.Model):
    # Datos del emprendedor
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=30)
    tipo_negocio = models.CharField(max_length=60)

    # Respuestas del wizard (asumiremos que son valores numéricos convertibles)
    crece = models.CharField(max_length=60)
    avanza = models.CharField(max_length=60)
    mejora = models.CharField(max_length=60)
    reemprende = models.CharField(max_length=60)

    # RESULTADO DEL DIAGNÓSTICO (NUEVOS CAMPOS)
    puntaje_caos = models.IntegerField(default=0, help_text="Puntuación total del diagnóstico (Max. 16).")
    fase_final = models.CharField(max_length=15, default='RE-EMPRENDE', help_text="Fase de la marca (CRECE, AVANZA, MEJORA, RE-EMPRENDE).")

    # Auditoría
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.fase_final}] {self.nombre} ({self.email}) - {self.fecha:%Y-%m-%d}"