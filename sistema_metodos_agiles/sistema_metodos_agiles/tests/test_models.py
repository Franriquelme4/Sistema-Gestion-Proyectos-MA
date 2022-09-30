
import os
from django.test import TestCase
import sys

sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_metodos_agiles.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from usuario.models import MiembroEquipo, Proyecto, Cliente, Usuario, Rol, Permiso

class TestProyecto(TestCase):
    
    def setUp(self):
        self.permiso = Permiso.objects.filter(id=4)
        

        self.cliente = Cliente.objects.create(nombre_cliente= 'nombre_cliente')
        self.cliente.save()

        self.rol = Rol(id=1)
        self.rol.permiso.set(self.permiso)
        self.rol.save()

        self.usuario = Usuario.objects.create(id=40, nombre='nombre_usuario', df_rol=self.rol)
        self.usuario.save()

        self.user = Usuario.objects.filter(id=40)

        self.miembro_equipo = MiembroEquipo.objects.create(id=1)
        self.miembro_equipo.miembro_usuario.set(Usuario.objects.filter(id=40))
        self.miembro_equipo.miembro_rol.set(Rol.objects.filter(id=1))
        self.miembro_equipo.save()
    

    def test_crear_proyecto(self):

        """
            Test para verificar la creacion de un proyecto
        """

        proyecto = Proyecto(
            id = 1,
            nombre_proyecto = 'proyecto_prueba',
            cliente_proyecto = self.cliente,
            fecha_ini_proyecto = None,
            fecha_fin_proyecto = None,
            descripcion_proyecto = 'proyecto_prueba',
            estado_proyecto = '1',
            sprint_dias = 1,
            fecha_creacion = '2022-09-28'
        )
        proyecto.miembro_proyecto.set(MiembroEquipo.objects.filter(id=1))
        proyecto.save()
        
        self.assertEqual(proyecto.nombre_proyecto, "proyecto_prueba")

    def test_crear_permiso(self):

        """
            Test para verificar la creacion de un permiso
        """
        permiso = Permiso(
            id = 20,
            descripcion_permiso = 'permiso de prueba',
            nombre_permiso = 'PermisoPrueba'
        )

        permiso.save()

    