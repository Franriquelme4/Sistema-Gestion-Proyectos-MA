from ast import arg
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
from usuario.models import MiembroEquipo, Proyecto, Cliente, UserStory, Usuario, Rol, Permiso, PrioridadTUs, CampoPersonalizado, TipoUserStory, Fase
from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, Group

class TestViews(TestCase):

    """
        Clase para test de vistas
    """

    def setUp(self):
        
        """
            Funcion para inicializar objetos que se utilizan para pruebas de vistas
        """
        
        self.permiso = Permiso.objects.create(descripcion_permiso = 'Permiso para prueba', nombre_permiso = 'prueba')
        self.permiso.save()

        self.cliente = Cliente.objects.create(nombre_cliente= 'nombre_cliente')
        self.cliente.save()

        self.rol = Rol.objects.create(nombre_rol='rol de prueba', descripcion_rol='rol creado para prueba')
        self.rol.save()
        self.rol.permiso.set(Permiso.objects.filter(descripcion_permiso='Permiso para prueba'))
        self.rol.save()

        self.usuario = Usuario.objects.create(nombre='nombre_usuario', df_rol=self.rol)
        self.usuario.save()

        self.miembro_equipo = MiembroEquipo.objects.create(descripcion='miembro equipo para prueba')
        self.miembro_equipo.miembro_usuario.set(Usuario.objects.filter(nombre='nombre_usuario'))
        self.miembro_equipo.miembro_rol.set(Rol.objects.filter(nombre_rol='rol de prueba'))
        self.miembro_equipo.save()


        self.client = Client()
        self.client.login(username='admin2', password='admin2')
        
        self.proyecto = Proyecto(
            nombre_proyecto = 'proyecto_prueba',
            cliente_proyecto = self.cliente,
            fecha_ini_proyecto = None,
            fecha_fin_proyecto = None,
            descripcion_proyecto = 'proyecto_prueba',
            estado_proyecto = '1',
            sprint_dias = 1,
            fecha_creacion = '2022-09-28'
        )
        self.proyecto.save()
        self.proyecto.miembro_proyecto.set(MiembroEquipo.objects.filter(descripcion='miembro equipo para prueba'))
        self.proyecto.save()

        self.prioridad_tus = PrioridadTUs.objects.create(
            descripcion = 'prioridadTUS inicial',
            valor = 4,
            color = 'green',
        )    
        self.prioridad_tus.save()

        self.campo_personalizado = CampoPersonalizado.objects.create(
            nombre_cp = 'campo personalizado inicial',
            tipoCampo_cp = 'inicial',
        )
        self.campo_personalizado.save()

        self.tipo_user_story = TipoUserStory.objects.create(
            proyecto_tipo_us = Proyecto.objects.get(nombre_proyecto = 'proyecto_prueba'),
            prioridad_tipo_us = PrioridadTUs.objects.get(descripcion = 'prioridadTUS inicial'),
            nombre_tipo_us = 'tipoUS inicial',
            descripcion_tipo_us = 'descripcion TUS inicial',
        )
        self.tipo_user_story.campoPer_tipo_us.set(CampoPersonalizado.objects.filter(tipoCampo_cp = 'inicial'))
        self.tipo_user_story.save()

        self.fase_prueba = Fase.objects.create(nombre_fase = 'probando fase', cod_fase = '30')
        self.fase_prueba.save()

        self.user_story = UserStory.objects.create(
            proyecto_us = Proyecto.objects.get(nombre_proyecto = 'proyecto_prueba'),
            nombre_us = 'nombre us inicial',
            descripcion_us = 'us inicial',
            tiempoEstimado_us = None,
            estadoActual_us = None,
            duracion_us = 1,
            tipo_us = TipoUserStory.objects.get(nombre_tipo_us = 'tipoUS inicial'),
            asignadoUsu_us = MiembroEquipo.objects.get(descripcion='miembro equipo para prueba'),
        )

        self.user_story.save()

    
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
            'proyecto': self.proyecto,

        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_crear_rol_proyecto_post(self):

        """
            Prueba para verificar creacion de un rol de proyecto
        """
        
        url = reverse('crearRolProyecto', args=['1'])

        response = self.client.post(url, {
            'rol' : self.rol
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_eliminar_rol_proyecto_post(self):
        """
            Test para verificar post al eliminar rol de un proyecto.
        """

        url = reverse('eliminarRolProyecto', args=['1'])

        response = self.client.post(url, {
            'record' : self.rol
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_eliminar_rol_proyecto_get(self):
        """
            Test para verificar get al eliminar rol de un proyecto
        """

        response = self.client.get(reverse('eliminarRolProyecto', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_editar_rol_proyecto_post(self):
        """
            Test para verificar post al editar un rol de proyecto
        """

        url = reverse('editarRolProyecto', args=['1'])

        response = self.client.post(url, {
            'record' : self.rol
        }, follow=True)

        self.assertEqual(response.status_code, 200)
    
    def test_editar_rol_proyecto_get(self):
        """
            Test para verificar get al editar un rol de proyecto.
        """

        response = self.client.get(reverse('editarRolProyecto', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_eliminar_colaborador_proyecto_post(self):
        """
            Test para verificar post al eliminar un colaborador de un proyecto.
        """
        
        url = reverse('eliminarColaboradorProyecto', args=['1'])

        response = self.client.post(url, {
            'record' : self.miembro_equipo
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_eliminar_colaborador_proyecto_get(self):
        """
            Test para verificar get al eliminar un colaborador de un proyecto.
        """

        response = self.client.get(reverse('eliminarColaboradorProyecto', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_editar_colaborador_proyecto_post(self):
        """
            Test para verificar post al editar un colaborador de un proyecto.
        """

        url = reverse('editarColaboradorProyecto', args=['1'])

        response = self.client.post(url, {
            'miembro' : self.miembro_equipo,
            'proyecto' : self.proyecto,
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_editar_colaborador_proyecto_get(self):
        """
            Test para verificar get al editar un colaborador de un proyecto.
        """

        response = self.client.get(reverse('editarColaboradorProyecto', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_tipo_us_post(self):
        """
            Test para verificar post en listado de tipo de user story.
        """

        url = reverse('tipoUs', args=['1'])

        response = self.client.post(url, {
            'rolUsuario' : self.rol,
            'prioridad' : self.prioridad_tus
        }, follow=True)

        self.assertEqual(response.status_code, 200)
    
    def test_tipo_us_get(self):
        """
            Test para verificar get en listado de tipo de user story.
        """

        response = self.client.get(reverse('tipoUs', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_tipo_us_crear_post(self):
        """
            Test para verificar post al crear tipo de user story.        
        """

        url = reverse('tipoUsCrear', args=['1'])

        response = self.client.post(url, {
            'rolUsuario' : self.rol,
            'tipoUs' : self.tipo_user_story,
            'prioridad' : self.prioridad_tus
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_tipo_us_crear_get(self):
        """
            Test para verificar get al crear tipo de user story.
        """

        response = self.client.get(reverse('tipoUsCrear', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_crear_tus_proyecto_post(self):
        """
            Test para verificar post al crear tipo de user story de un proyecto.
        """

        url = reverse('crearTUSProyecto', args=['1'])

        response = self.client.post(url, {
            'tipoUs' : self.tipo_user_story,
            'fases' : self.fase_prueba
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_crear_tus_proyecto_get(self):
        """
            Test para verificar get al crear tipo de user story de un proyecto.
        """

        response = self.client.get(reverse('crearTUSProyecto', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_ver_product_backlog_post(self):
        """
            Test para verificar post al ver product backlog.
        """

        url = reverse('verProductBacklog', args=['1'])

        response = self.client.post(url, {
            'rolUsuario' : self.rol,
            'tipoUs' : self.tipo_user_story,
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_ver_product_backlog_get(self):
        """
            Test para verificar get al ver product backlog.
        """

        response = self.client.get(reverse('verProductBacklog', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_crear_us_post(self):
        """
            Test para verificar post al crear US.
        """

        url = reverse('crearUs', args=['1'])

        response = self.client.post(url, {
            'userStory' : self.user_story,
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_crear_us_get(self):
        """
            Test para verificar get al crear US.
        """

        response = self.client.get(reverse('crearUs', args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_importar_tus_proyecto_post(self):
        """
            Test para verificar post al importar tipos de US.
        """

        url = reverse('importarTusDeProyecto', args=['1'])

        response = self.client.post(url, {
            'tipoUsSelect' : self.tipo_user_story,
            'tipoUs' : self.tipo_user_story,
            'fases' : self.fase_prueba,
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_importar_tus_proyecto_get(self):
        """
            Test para verificar get al importar tipos de US.
        """

        response = self.client.get(reverse('importarTusDeProyecto', args=['1']))
        self.assertEqual(response.status_code, 302)