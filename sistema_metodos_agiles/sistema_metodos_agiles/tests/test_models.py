
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
        """
            Funcion que deja variables listas para pruebas de modelos.
        """

        self.permiso = Permiso.objects.create(descripcion_permiso = 'Permiso para prueba', nombre_permiso = 'prueba')

        self.cliente = Cliente.objects.create(nombre_cliente= 'nombre_cliente')

        self.rol = Rol.objects.create(nombre_rol='rol de prueba', descripcion_rol='rol creado para prueba')
        self.rol.save()
        self.rol.permiso.set(Permiso.objects.filter(descripcion_permiso='Permiso para prueba'))

        self.usuario = Usuario.objects.create(nombre='nombre_usuario', df_rol=self.rol)

        self.user = Usuario.objects.filter(nombre='nombre_usuario')

        self.miembro_equipo = MiembroEquipo.objects.create(descripcion='miembro equipo para prueba')
        self.miembro_equipo.miembro_usuario.set(Usuario.objects.filter(nombre='nombre_usuario'))
        self.miembro_equipo.miembro_rol.set(Rol.objects.filter(nombre_rol='rol de prueba'))
        self.miembro_equipo.save()
    

    def test_crear_proyecto(self):

        """
            Test para verificar la creacion de un proyecto
        """

        proyecto = Proyecto(
            nombre_proyecto = 'proyecto_prueba',
            cliente_proyecto = self.cliente,
            fecha_ini_proyecto = None,
            fecha_fin_proyecto = None,
            descripcion_proyecto = 'proyecto_prueba',
            estado_proyecto = '1',
            sprint_dias = 1,
            fecha_creacion = '2022-09-28'
        )
        proyecto.save()
        proyecto.miembro_proyecto.set(MiembroEquipo.objects.filter(descripcion='miembro equipo para prueba'))
        
        
        self.assertEqual(proyecto.nombre_proyecto, "proyecto_prueba")

    def test_crear_permiso(self):

        """
            Test para verificar la creacion de un permiso.
        """
        permiso = Permiso(
            descripcion_permiso = 'permiso de prueba',
            nombre_permiso = 'PermisoPrueba'
        )

        permiso.save()

    def test_crear_rol(self):
        
        """
            Test para verificar la creacion de un rol
        """

        rol = Rol(
            nombre_rol= 'rol para prueba',
            descripcion_rol = 'probando modelo rol'
        )

        rol.save()
        rol.permiso.set(Permiso.objects.filter(descripcion_permiso='permiso para prueba'))

    def test_crear_usuario(self):

        usuario = Usuario(
            nombre = 'usuario2',
            apellido = 'ApellidoPrueba',
            email = 'prueba@email.com',
            nombre_usuario = 'usuario2Prueba',
            activo = True,
        )

        usuario.save()


