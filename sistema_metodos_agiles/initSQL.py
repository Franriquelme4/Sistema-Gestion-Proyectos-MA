
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_metodos_agiles.settings')
import sys
import django
django.setup()
from usuario.models import Rol,Permiso

def cargarPermiso():
    permiso = Permiso.objects.get_or_create(
        id=1,
        nombre_permiso="def",
        descripcion_permiso="Default"
    )[0]
    permiso.save()

    

def cargarDB():
    """Se carga la base de datos inicial"""
    rol = Rol.objects.get_or_create(
            id=900000,
            descripcion_rol = "Poblacion DB 2",
            nombre_rol = "Poblacion DB 2",
    )[0]
    rol.save()
    rol.permiso.add(Permiso.objects.get(id=1))



if __name__ == '__main__':
    cargarDB()
    print("La base de datos inicial se ha poblado correctamente")
