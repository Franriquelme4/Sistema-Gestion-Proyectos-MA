from email.policy import default
from usuario.models import Cliente, Proyecto, Rol
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

def test_proyecto_creation():
    proyecto = Proyecto(
        nombre_proyecto = 'proyecto1',
        cliente_proyecto = '',
        fecha_ini_proyecto = Cliente.cliente,
        fecha_fin_proyecto = '',
        descripcion_proyecto = 'proyecto de prueba',
        estado_proyecto = 'Pendiente',
        miembro_proyecto = 'MiembroEquipo',
        sprint_dias = 1,
        fecha_creacion = ''
    )
    assert proyecto.nombre_proyecto == 'proyecto1'