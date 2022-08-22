from django.db import models

# Create your models here.
class Usuario(models.Model):
    """Modelo de la tabla usuarios, en la cual se almacenan todos los datos del usuario"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    nombre_usuario = models.CharField(max_length=100)
    roles = models.CharField(max_length=100,default="observador")
    def __str__(self):
        return self.nombre_usuario
    