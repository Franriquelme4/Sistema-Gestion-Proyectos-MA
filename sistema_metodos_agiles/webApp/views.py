

from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from usuario.utils import getUsuarioSesion,getIdScrumRol,getProyectsByUsuarioID,getProyectsByID
from usuario.models import Usuario,Cliente,Proyecto,MiembroEquipo
from django.template import loader
from django import template
# Create your views here.
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
    print(data.username)
    if not usuario:
        es_usuario_nuevo = True
        nuevo_usuario = Usuario(
            nombre = data.first_name,
            apellido = data.last_name,
            email = data.email,
            nombre_usuario = data.username
        )
        nuevo_usuario.save()
        userSession = nuevo_usuario
    else:
        userSession = usuario[0]
    proyectos = getProyectsByUsuarioID(userSession.id)
    
    context = {'segment': 'index','userSession':userSession,'proyectos':proyectos}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



def request_page(request):
    return render(request,'home/ui-tables.html')


def usuarios(request):
    userSession = getUsuarioSesion(request.user.email)
    usuarios = Usuario.objects.all()
    context = {'usuarios':usuarios,'segment': 'usuarios','userSession':userSession}
    html_template = loader.get_template('home/usuarios.html')
    return HttpResponse(html_template.render(context, request))

def proyectos(request):
    userSession = getUsuarioSesion(request.user.email)
    proyectos = Proyecto.objects.all()
    context = {'userSession':userSession,'proyectos':proyectos}
    html_template = loader.get_template('home/proyectos.html')
    return HttpResponse(html_template.render(context, request))

def CrearProyecto(request):
    usuarios = Usuario.objects.all()
    userSession = getUsuarioSesion(request.user.email)
    context = {'usuarios':usuarios,'segment': 'crearProyecto','userSession':userSession}
    html_template = loader.get_template('home/CrearProyecto.html')
    return HttpResponse(html_template.render(context, request))

def activarUsuario(request,id):
    usuario = Usuario.objects.get(id=id)
    usuario.activo = True
    usuario.save()
    return redirect('/')

def crearProyectoGuardar(request):
    print(request.POST['nombreProyecto'])
    variables = request.POST
    if request.method == 'POST':
        cliente = Cliente(
           nombre_cliente = variables['nombreCliente'] ,
           apellido_cliente =variables['apellidoCliente'] ,
           email_cliente = variables['emailCliente'],
           telefono_cliente = variables['telefonoCliente'],
           empresa_cliente = variables['empresaCliente']
        )
        cliente.save()
        miembro = MiembroEquipo(
           descripcion = ''
        )
        miembro.save()
        miembro.miembro_rol.add(getIdScrumRol())
        miembro.miembro_usuario.add(Usuario.objects.get(id=variables['scrumMaster']))
        proyecto = Proyecto(
           nombre_proyecto = variables['nombreProyecto'],
           cliente_proyecto = cliente,
           fecha_ini_proyecto = variables['fechaInicio'],
           fecha_fin_proyecto = variables['fechaFin'],
           descripcion_proyecto = variables['descripcion'],
           sprint_dias = variables['sprintDias']
        )
        proyecto.save()
        proyecto.miembro_proyecto.add(miembro)
    return redirect('/')

def verProyecto(request,id):
    userSession = getUsuarioSesion(request.user.email)
    print(id,userSession.id)
    proyecto = getProyectsByID(id,userSession.id)
    print(proyecto)
    context= {'userSession':userSession,'proyecto':proyecto[0],'segment': 'verProyecto'}
    html_template = loader.get_template('home/vistaProyectos.html')
    return HttpResponse(html_template.render(context,request))

def rolesProyecto(request):
    context={}
    html_template = loader.get_template('home/rolesProyecto.html')
    return HttpResponse(html_template.render(context,request))
