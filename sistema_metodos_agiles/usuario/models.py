
from django.db import models

# Create your models here.

class Permiso(models.Model):
    """Los permisos se tienen previamente cargados, cada permiso se asiganan a los distintos roles"""
    descripcion = models.CharField(max_length=100,blank=False,null=False)
    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        ordering = ['descripcion']
    def __str__(self):
        return self.descripcion

class Rol(models.Model):
    """Se agrega la tabla roles para tener un control de todos los roles que tiene un determinado usuario, existen 3 roles ya creados previamente"""
    descripcion = models.CharField(max_length=100,blank=False,null=False)
    permiso = models.ManyToManyField(Permiso)
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['descripcion']
    def __str__(self):
        return self.descripcion

class Usuario(models.Model):
    """Modelo de la tabla usuarios, en la cual se almacenan todos los datos del usuario"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    nombre_usuario = models.CharField(max_length=100)
    rol = models.ManyToManyField(Rol)
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nombre_usuario']
    def __str__(self):
        return self.nombre_usuario


