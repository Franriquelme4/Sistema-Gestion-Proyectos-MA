import os
import sys
from urllib import response

from django.forms import PasswordInput
sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_metodos_agiles.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from django.urls import reverse, resolve
from webApp import views, urls
from webApp.templates import *
from usuario.models import MiembroEquipo, Proyecto, Cliente, Usuario, Rol, Permiso
from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, Group

class TestViews(TestCase):

    """
        Clase para test de vistas
    """

    def setUp(self):

        self.admin = User.objects.create_user(username='admin', email='admin@mail.com', password="admin")
        self.admin.is_staff = True
        admin_group = Group.objects.create(name='Administrador')
        
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


        self.client = Client()
        self.client.login(username='admin2', password='admin2')
        
        self.proyecto = Proyecto(
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
        self.proyecto.miembro_proyecto.set(MiembroEquipo.objects.filter(id=1))
        self.proyecto.save()

    
    def test_crear_proyecto_get(self):

        """
            Prueba para verificar GET al crear un proyecto
        """

        response = self.client.get(reverse('CrearProyecto'))
        self.assertEqual(response.status_code, 302)
        #self.assertTemplateUsed(response, 'home/CrearProyecto.html')
    
    
    def test_crear_proyecto_post(self):

        """
            Prueba para verificar POST al crear proyecto
        """
        url = reverse('CrearProyecto')
        response = self.client.post(url, data={
            'usuarios' : Usuario.objects.all(),
            'rolUsuario' : self.rol}, follow=True)

        self.assertEqual(response.status_code, 200)
    
    def test_ver_proyecto_get(self):

        """
            Prueba para verificar GET al ver un proyecto
        """

        response = self.client.get(reverse('proyectos'))
        self.assertEqual(response.status_code, 302)
        #self.assertTemplateUsed(response, '/login/?next=/proyecto/')

    def test_roles_proyecto_post(self):

        """
            Prueba para verificar POST al listar roles de proyecto
        """

        url = reverse('rolesProyecto', args=['1'])
        response = self.client.post(url, data={

        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_crear_rol_proyecto_post(self):

        """
            Prueba para verificar POST al crear un rol proyecto
        """

        url = reverse('crearRolProyecto', args=['1'])
        response = self.client.post(url, data={

        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_asignar_colaborador_proyecto_get(self):

        """
            Prueba para verificar GET al asignar colaborador a un proyecto
        """
        
        response = self.client.get(reverse('asignarColaboradorProyecto', args=['1']))

        self.assertEqual(response.status_code, 302)

    def test_asignar_colaborador_proyecto_post(self):
        
        """
            Prueba para verificar POST al asignar un colaborador a un proyecto
        """

        url = reverse('asignarColaboradorProyecto', args=['1'])
        response = self.client.post(url, data={
            'miembro': self.miembro_equipo,
            'proyecto': self.proyecto

        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_crear_rol_proyecto(self):

        """
            Prueba para verificar creacion de un rol de proyecto
        """
        
        url = reverse('crearRolProyecto', args=['1'])

        response = self.client.post(url, {
            'rol' : self.rol
        }, follow=True)

        self.assertEqual(response.status_code, 200)
