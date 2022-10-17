
import os
from django.test import TestCase
import sys

sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_metodos_agiles.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from usuario.models import CampoPersonalizado, FaseTUS, MiembroEquipo, PrioridadTUs, Proyecto, Cliente, Sprint, TipoUserStory, UserStory, Usuario, Rol, Permiso, ProyectoRol, Fase, Tablero

class TestProyecto(TestCase):
    
    def setUp(self):
        """
            Funcion que deja objetos listos para pruebas de modelos.
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

        self.prioridad_us = PrioridadTUs.objects.create(descripcion = 'Descripcion T.US de prueba', valor = 1, color= 'rojo')
        self.prioridad_us.save()

        self.campo_personalizado = CampoPersonalizado.objects.create(nombre_cp = 'nombre campo personalizado de prueba', tipoCampo_cp = 'tipo campo de prueba')
        self.campo_personalizado.save()

        self.fase_prueba = Fase.objects.create(nombre_fase = 'probando fase', cod_fase = '30')
        self.fase_prueba.save()

        self.cliente = Cliente.objects.create(
            nombre_cliente = 'cliente inicial',
            apellido_cliente = 'cliente apellido',
            email_cliente = 'cliente@inicial.com',
            telefono_cliente = '1234',
            empresa_cliente = 'empresa inicial',
        )
        self.cliente.save()

        self.proyecto = Proyecto.objects.create(
            nombre_proyecto = 'proyecto inicial',
            cliente_proyecto = Cliente.objects.get(nombre_cliente = 'cliente inicial'),
            descripcion_proyecto = 'descripcion inicial',
            estado_proyecto = '1',
            sprint_dias = 0,
            fecha_creacion = '2022-10-15',
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
            proyecto_tipo_us = Proyecto.objects.get(nombre_proyecto = 'proyecto inicial'),
            prioridad_tipo_us = PrioridadTUs.objects.get(descripcion = 'prioridadTUS inicial'),
            nombre_tipo_us = 'tipoUS inicial',
            descripcion_tipo_us = 'descripcion TUS inicial',
        )
        self.tipo_user_story.campoPer_tipo_us.set(CampoPersonalizado.objects.filter(tipoCampo_cp = 'inicial'))
        self.tipo_user_story.save()

        self.sprint = Sprint.objects.create(
            proyecto_sp = Proyecto.objects.get(nombre_proyecto = 'proyecto inicial'),
            nombre_sp = 'sprint inicial',
            duracion_sp = 5,
            fecha_creacion = '2022-10-15',
            fechaFIn_sp = '2022-10-16',
        )
        self.sprint.userStory_sp.set('')
        self.sprint.save()

        self.fase_tus = FaseTUS.objects.create(
            tipo_us_faseTUS = TipoUserStory.objects.get(nombre_tipo_us = 'tipoUS inicial'),
            fase_faseTUS = Fase.objects.get(nombre_fase = 'probando fase'),
        )
        self.fase_tus.save()

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
        self.assertEqual(permiso.descripcion_permiso, 'permiso de prueba')

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
        rol.save()
        self.assertEqual(rol.nombre_rol, 'rol para prueba')

    def test_crear_usuario(self):
        """
            Test para verificar la creacion de un usuario
        """
        usuario = Usuario(
            nombre = 'usuario2',
            apellido = 'ApellidoPrueba',
            email = 'prueba@email.com',
            nombre_usuario = 'usuario2Prueba',
            activo = True,
        )

        usuario.save()
        self.assertEqual(usuario.nombre, 'usuario2')

    def test_crear_miembro_equipo(self):
        """
            test para verificar la creacion de un miembro de equipo.
        """
        miembro = MiembroEquipo(
            descripcion = 'MiembroEquipo de prueba'
        )

        miembro.save()
        miembro.miembro_usuario.set(Usuario.objects.filter(nombre='nombre_usuario'))
        miembro.miembro_rol.set(Rol.objects.filter(nombre_rol='rol de prueba'))
        miembro.save()
        self.assertEqual(miembro.descripcion, 'MiembroEquipo de prueba')

    def test_crear_cliente(self):
        """
            Test para verificar la creacion de un nuevo cliente.
        """
        cliente = Cliente(
            nombre_cliente = 'cliente de prueba',
            apellido_cliente = 'apellido de cliente de prueba',
            email_cliente = 'clienteprueba@email.com',
            telefono_cliente = '123456',
            empresa_cliente = 'empresa de prueba',
        )
        cliente.save()
        self.assertEqual(cliente.nombre_cliente, 'cliente de prueba')

    def test_crear_proyecto_rol(self):
        """
            Test para verificar la creacion de un nuevo rol de proyecto.
        """
        proyecto_rol = ProyectoRol(
            descripcion_proyecto_rol = 'proyecto rol de prueba'
        )
        
        proyecto_rol.save()
        proyecto_rol.rol.set(Rol.objects.filter(nombre_rol='rol de prueba'))
        proyecto_rol.save()
        proyecto_rol.proyecto.set(Proyecto.objects.filter(nombre_proyecto = 'proyecto_prueba'))
        proyecto_rol.save()
        self.assertEqual(proyecto_rol.descripcion_proyecto_rol, 'proyecto rol de prueba')

    def test_tipo_user_story(self):
        """
            Test para verificar la creacion de un nuevo tipo de User Story.
        """
        tipo_user_story = TipoUserStory(
            proyecto_tipo_us = Proyecto.objects.get(nombre_proyecto = 'proyecto inicial'),
            prioridad_tipo_us = PrioridadTUs.objects.get(descripcion = 'prioridadTUS inicial'),
            nombre_tipo_us = 'nombre TUS de prueba',
            descripcion_tipo_us = 'descripcion TUS de prueba',
        )

        tipo_user_story.save()
        tipo_user_story.campoPer_tipo_us.set(CampoPersonalizado.objects.filter(nombre_cp = 'campo personalizado inicial'))
        tipo_user_story.save()
        self.assertEqual(tipo_user_story.descripcion_tipo_us, 'descripcion TUS de prueba')

    def test_user_story(self):
        """
            Test para verificar la creacion de un nuevo User Story
        """

        user_story = UserStory(
            proyecto_us = Proyecto.objects.get(descripcion_proyecto = 'descripcion inicial'),
            nombre_us = 'nombre US de prueba',
            descripcion_us = 'descripcion US de prueba',
            tiempoEstimado_us = None,
            estadoActual_us = 'TODO',
            tipo_us = TipoUserStory.objects.get(descripcion_tipo_us = 'descripcion TUS inicial'),
            asignadoUsu_us = MiembroEquipo.objects.get(descripcion = 'miembro equipo para prueba'),
        )
        
        user_story.save()
        user_story.save()
        self.assertEqual(user_story.descripcion_us, 'descripcion US de prueba')

    def test_sprint(self):
        """
            Test para verificar la creacion de un nuevo Sprint.
        """

        sprint = Sprint(
            nombre_sp = 'nombre Sprint de prueba',
            fechaFIn_sp = '2022-10-15',
            duracion_sp = 10,
        )

        sprint.save()
        sprint.userStory_sp.set(UserStory.objects.filter(nombre_us = 'nombre US de prueba'))
        sprint.save()
        self.assertEqual(sprint.nombre_sp, 'nombre Sprint de prueba')

    def test_fase(self):
        """
            Test para verificar la creacion de una fase.
        """

        fase = Fase(
            nombre_fase = 'fase prueba',
            cod_fase = '20',
        )

        fase.save()
        self.assertEqual(fase.nombre_fase, 'fase prueba')

    def test_fase_tus(self):
        """
            Test para verificar la creacion de fase por tipo de User Story.
        """

        fase_tus = FaseTUS(
            tipo_us_faseTUS = TipoUserStory.objects.get(nombre_tipo_us = 'tipoUS inicial'),
            #fase_faseTUS = Fase.objects.get(nombre_fase = 'probando fase'),
        )
        fase_tus.save()
        self.assertEqual(fase_tus.tipo_us_faseTUS, TipoUserStory.objects.get(nombre_tipo_us = 'tipoUS inicial'))

    def test_tablero(self):
        """
            Test para verificar la creacion de un nuevo tablero
        """

        tablero = Tablero(
            sprint_tablero = Sprint.objects.get(nombre_sp = 'sprint inicial'),
            tipo_us_fase = TipoUserStory.objects.get(nombre_tipo_us = 'tipoUS inicial'),
            nombre_tablero = 'tablero de prueba',
        )

        tablero.save()
        tablero.faseTUS_tablero.set(FaseTUS.objects.filter(fase_faseTUS = Fase.objects.get(nombre_fase = 'probando fase')))
        tablero.save()
        self.assertEqual(tablero.nombre_tablero, 'tablero de prueba')
    
    def test_prioridadtus(self):
        """
            Test para verificar la creacion de una nueva prioridad de los tipos de US.
        """

        prioridad_tus = PrioridadTUs(
            descripcion = 'prioridad de prueba',
            valor = 1,
            color = 'rojo',
        )
        
        prioridad_tus.save()
        self.assertEqual(prioridad_tus.descripcion, 'prioridad de prueba')
