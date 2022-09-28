from email.policy import default
from usuario.models import Cliente, Proyecto, Rol, TipoUserStory
from django.db import models
import pytest

def test_cliente_creation():
    cliente = Cliente(
        nombre_cliente = 'cliente1',
        apellido_cliente = 'apellido1',
        email_cliente = 'clienteusuario@cliente.com',
        telefono_cliente = '1234',
        empresa_cliente = 'empresa'
    )
    assert cliente.nombre_cliente  == 'cliente1'

@pytest.mark.django_db
def test_proyecto_creation(self):
    proyecto = Proyecto(
        nombre_proyecto = 'proyecto1',
        cliente_proyecto  = Cliente.objects.create(nombre_cliente='nombre_cliente'),
        fecha_ini_proyecto = '',
        fecha_fin_proyecto = '',
        descripcion_proyecto = 'proyecto de prueba',
        estado_proyecto = 'Pendiente',
        miembro_proyecto = 'MiembroEquipo',
        sprint_dias = 1,
        fecha_creacion = '2022-09-28'
    )
    assert proyecto.nombre_proyecto == 'proyecto1'

def test_user_story_creation():
    user_story = TipoUserStory(
        prioridad_tipo_us = 1,
        nombre_tipo_us = 'prueba',
        descripcion_tipo_us = 'user story de prueba'
    )
    assert user_story.prioridad_tipo_us == 1
