import email
import pytest
from django.db import models
from usuario.models import Usuario


def test_user_creation():
    user = Usuario(
        nombre = 'usuario',
        apellido = 'usuario_apellido',
        email = 'usuario@gmail.com',
        nombre_usuario = 'nickname',
        activo = False,
        df_rol = models.ForeignKey('Rol',on_delete=models.CASCADE,default=2)
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

