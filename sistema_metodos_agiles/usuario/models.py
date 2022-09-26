from django.db import models
import datetime
# Create your models here.

class Permiso(models.Model):
    """Los permisos se tienen previamente cargados, cada permiso se asiganan a los distintos roles"""
    descripcion_permiso = models.CharField(max_length=100,blank=False,null=False)
    nombre_permiso = models.CharField(max_length=15,blank=False,null=False)
    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        ordering = ['descripcion_permiso']
    def __str__(self):
        return self.descripcion_permiso

class Rol(models.Model):
    """Se agrega la tabla roles para tener un control de todos los roles que tiene un determinado usuario, existen 3 roles ya creados previamente"""
    nombre_rol = models.CharField(max_length=50,blank=False,null=False)
    descripcion_rol = models.CharField(max_length=100,blank=False,null=False)
    permiso = models.ManyToManyField(Permiso)
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['descripcion_rol']
    def __str__(self):
        return self.descripcion_rol
    def getPermisos(self):
        return self.permiso.all()
    def poseePermiso(self,codigo):
        permiso = self.permiso.filter(nombre_permiso=codigo)
        return permiso.count() > 0


class Usuario(models.Model):
    """Modelo de la tabla usuarios, en la cual se almacenan todos los datos del usuario"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    nombre_usuario = models.CharField(max_length=100)
    activo = models.BooleanField(default=False)
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
    descripcion = models.CharField(max_length=100,default='')
    class Meta:
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'
    def __str__(self):
        return self.descripcion


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
    miembro_proyecto = models.ManyToManyField('MiembroEquipo')
    sprint_dias = models.IntegerField(default=0)
    fecha_creacion = models.DateField(default=datetime.date.today)
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['nombre_proyecto']
    def __str__(self):
        return self.nombre_proyecto

class ProyectoRol(models.Model):
    """Se almacenan los roles por proyecto"""
    rol = models.ManyToManyField('Rol')
    proyecto = models.ManyToManyField('Proyecto')
    descripcion_proyecto_rol = models.CharField(max_length=100,default='')
    class Meta:
        verbose_name = 'ProyectoRol'
        verbose_name_plural = 'ProyectoRoles'
        
class TipoUserStory(models.Model):
    """Modelo de la tabla tipo de user story, en la cual se almacenan todos los datos de los tipos de user story"""
    prioridad_tipo_us = models.IntegerField()
    nombre_tipo_us = models.CharField(max_length=50,null=False)
    descripcion_tipo_us = models.CharField(max_length=100,null=False)
    class Meta:
        verbose_name = 'Tipo User Story'
        verbose_name_plural = 'Tipos de User Story'
        ordering = ['nombre_tipo_us']
    def __str__(self):
        return self.nombre_tipo_us

class UserStory(models.Model):
    """Modelo de la tabla user story, en la cual se almacenan todos los datos de los user story"""
    nombre_us = models.CharField(max_length=50,null=False)
    descripcion_us = models.CharField(max_length=50,null=False)
    duracion_us = models.IntegerField()
    tipo_us = models.ForeignKey('TipoUserStory',on_delete=models.CASCADE)
    fechaIni_us = models.DateField(default=datetime.date.today)
    class Meta:
        verbose_name = 'User Story'
        verbose_name_plural = 'User Stories'
        ordering = ['nombre_us']
    def __str__(self):
        return self.nombre_us

class Sprint(models.Model):
    """Modelo de la tabla sprint, en la cual se almacenan todos los datos del sprint"""
    nombre_sp = models.CharField(max_length=50,null=False)
    fechaIni_sp = models.DateField(default=datetime.date.today)
    fechaFIn_sp = models.DateField()
    duracion_sp = models.IntegerField(null=False)
    userStory_sp = models.ForeignKey('UserStory',on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'
        ordering = ['nombre_sp']
    def __str__(self):
        return self.nombre_sp