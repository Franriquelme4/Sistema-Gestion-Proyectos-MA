from django.test import TestCase
from django.urls.base import reverse

from .models import Rol, Usuario
# Create your tests here.
class ProyectoViewTest(TestCase):
    def test_future_questions(self):
        """
        Se revisa la existencia de la ruta 
        """
        rol = Rol.objects.create(
            nombre_rol = 'admin',
            descripcion_rol ='admin'
        )
        usuario = Usuario.objects.create(
            nombre = 'Admin',
            apellido = 'Admin',
            email = 'Admin',
            nombre_usuario = 'Admin',
            df_rol = rol
        )
        url = reverse("webApp:index",usuario)
        response =  self.client.get(url)
        self.assertEqual(response.status_code,404)