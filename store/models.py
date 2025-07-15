from django.db import models

# Modelo para representar un producto en la tienda
class Product(models.Model):
    # Campo para el nombre del producto
    # max_length define la longitud máxima del texto
    name = models.CharField(max_length=200)

    # Campo para la descripción del producto
    # blank=True permite que este campo esté vacío en la base de datos
    # null=True permite que este campo sea nulo en la base de datos
    description = models.TextField(blank=True, null=True)

    # Campo para el precio del producto
    # max_digits es el número total de dígitos permitidos (ej. 999.99)
    # decimal_places es el número de decimales (ej. .99)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Campo para la imagen del producto
    # upload_to define la subcarpeta dentro de MEDIA_ROOT donde se guardarán las imágenes
    # blank=True y null=True permiten que un producto no tenga imagen
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # Método que define cómo se representa el objeto Product como una cadena de texto
    # Esto es útil para el panel de administración de Django
    def __str__(self):
        return self.name

    # Clase Meta para opciones adicionales del modelo (opcional)
    class Meta:
        # Define el nombre plural del modelo en el panel de administración
        verbose_name_plural = "Products"
