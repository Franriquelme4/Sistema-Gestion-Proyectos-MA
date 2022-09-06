
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
    activo = models.BooleanField(default=False)
    #rol = models.ManyToManyField(Rol)
    df_rol = models.ForeignKey('Rol',on_delete=models.CASCADE,default=2)
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nombre_usuario']
    def __str__(self):
        return self.nombre_usuario

class MiembroEquipo(models.Model):
    """Modelo de la tabla miembro, en la cual se almacenan todos los datos del cliente"""
    miembro_usuario = models.ManyToManyField(Usuario)
    miembro_rol = models.ManyToManyField(Rol)
    miembro_descripcion = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'
        ordering = ['miembro_descripcion']
    def __str__(self):
        return self.miembro_descripcion


class Cliente(models.Model):
    """Modelo de la tabla clientes, en la cual se almacenan todos los datos del cliente"""
    nombre_cliente = models.CharField(max_length=100)
    apellido_cliente = models.CharField(max_length=100)
    email_cliente = models.CharField(max_length=100)
    telefono_cliente = models.CharField(max_length=100)
    empresa_cliente = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre_cliente']
    def __str__(self):
        return self.nombre_cliente

class Proyecto(models.Model):
    """Modelo de la tabla proyectos, en la cual se almacenan todos los datos del proyecto"""
    nombre_proyecto = models.CharField(max_length=100)
    cliente_proyecto = models.ForeignKey('Cliente',on_delete=models.CASCADE,)
    fecha_ini_proyecto = models.DateField(null=True)
    fecha_fin_proyecto = models.DateField(null=True)
    descripcion_proyecto = models.CharField(max_length=100,default='')
    estado_proyecto = models.CharField(max_length=1,default='1')
    miembro_proyecto = models.ForeignKey('MiembroEquipo',on_delete=models.CASCADE,) 
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['nombre_proyecto']
    def __str__(self):
        return self.nombre_proyecto



