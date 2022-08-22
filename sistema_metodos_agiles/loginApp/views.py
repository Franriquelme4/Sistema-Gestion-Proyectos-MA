
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required

from usuario.models import Usuario
# Create your views here.

def login(request):
    """
    Metodo de redireccion del login para poder ingresar mediante sso
    """
    return render(request,'login.html')

@login_required
def home(request):
    """
    Este metodo se utiliza para hacer la validacion del usuario, si consiste en un usuario ya registrado anteriormente 
    se muestra en pantalla la informacion del mismo y si corresponde a un nuevo usuario almacena en la base de datos 
    y retorna un mensaje
    """
    data = request.user
    usuario = Usuario.objects.filter(email = data.email)
    es_usuario_nuevo = False
    if not usuario:
        es_usuario_nuevo = True
        nuevo_usuario = Usuario(
            nombre = data.first_name,
            apellido = data.last_name,
            email = data.email,
            nombre_usuario = data.username
        )
        nuevo_usuario.save()
    else:
        es_usuario_nuevo = False
        data = usuario[0]
    
    return render(request,'home.html',{'data':data,'es_usuario_nuevo':es_usuario_nuevo})
