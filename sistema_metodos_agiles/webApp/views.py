

from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from usuario.models import Usuario
from django.template import loader
from django import template
# Create your views here.
userSession = ''
def login(request):
    """
    Metodo de redireccion del login para poder ingresar mediante sso
    """
    return render(request,'accounts/login.html')


@login_required(login_url="/login/")
def index(request):
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
        userSession = usuario[0]

    context = {'segment': 'index','userSession':userSession,'es_usuario_nuevo':es_usuario_nuevo}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



def request_page(request):
    return render(request,'home/ui-tables.html')


def usuarios(request):
    usuarios = Usuario.objects.all()
    context = {'usuarios':usuarios,'segment': 'usuarios'}
    html_template = loader.get_template('home/usuarios.html')
    return HttpResponse(html_template.render(context, request))

def proyectos(request):
    context = {}
    html_template = loader.get_template('home/proyectos.html')
    return HttpResponse(html_template.render(context, request))

def CrearProyecto(request):
    context = {}
    html_template = loader.get_template('home/CrearProyecto.html')
    return HttpResponse(html_template.render(context, request))