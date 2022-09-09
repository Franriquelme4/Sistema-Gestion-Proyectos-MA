import email
import pytest
from usuario.models import Usuario


def test_user_creation():
    user = Usuario(
        nombre = 'usuario',
        apellido = 'usuario_apellido',
        email = 'usuario@gmail.com',
        telefono = '123456',
        nombre_usuario = 'nickname',
        roles = 'observador'
    )
    assert user.nombre == 'usuario'


def test_observador_creation():
    user = Usuario(
        nombre = 'Victor',
        apellido = 'Irala',
        email = 'correo@gmail.com',
        telefono = '1234',
        nombre_usuario = 'vict',
        roles = ''
    )
    assert user.roles == 'observador'
    