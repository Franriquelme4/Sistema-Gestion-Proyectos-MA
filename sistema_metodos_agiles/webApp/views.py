
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from usuario.models import Usuario
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


    context = {'segment': 'index','data':data,'es_usuario_nuevo':es_usuario_nuevo}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def request_page(request):
    return render(request,'home/ui-tables.html')


def usuarios(request):
    context = {}
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