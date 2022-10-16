

import datetime
import json
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from usuario.utils import validarPermisos,busy_end_date,getUsuarioSesion,getTipoUsBySprint,getIdScrumRol,getProyectsByUsuarioID,getProyectsByID,getRolByProyectId,getColaboratorsByProyect,calcularFechaFin,getTipoUsbyProyectId,getTipoUsbyNotProyectId,getPermisos
from usuario.models import Usuario,FaseTUS,TipoUs_Proyecto,SprintUserStory,SprintColaborador,Sprint,Cliente,Proyecto,MiembroEquipo,Permiso,Rol,ProyectoRol,TipoUserStory,PrioridadTUs,UserStory,Fase,Estado
from django.template import loader
from django.db.models import Q
from datetime import datetime

# Create your views here.
def login(request):
    """
    Metodo de redireccion del login para poder ingresar mediante sso
    """
    return render(request,'accounts/login.html')

@login_required(login_url="/login/")
def index(request):
    """
    Luego de loguease se lleva a la vista principal la cual tiene
    distintas opciones dependiendo el rol que tenga 
    """
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
    request.session['userSesion'] = "userSession"
    proyectos = getProyectsByUsuarioID(userSession.id)
    total_proyectos = Proyecto.objects.count()
    total_usuarios = Usuario.objects.count()
    context = {
        'segment': 'index',
        'userSession':userSession,
        'proyectos':proyectos,
        'total_proyectos':total_proyectos,
        'total_usuarios':total_usuarios
        }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



def usuarios(request):
    """
    Se lista los usuarios actuales del sistema, este metodo se utiliza en el usuario admin
    """
    userSession = getUsuarioSesion(request.user.email)
    usuarios = Usuario.objects.all()
    rolUsuario = Rol.objects.get(id=userSession.df_rol.id)
    permisosProyecto = ['act_Usuario','dct_Usuario']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id)
    context = { 'usuarios':usuarios,
                'segment': 'usuarios',
                'userSession':userSession,
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos}
    html_template = loader.get_template('home/usuarios.html')
    return HttpResponse(html_template.render(context, request))
@login_required(login_url="/login/")
def proyectos(request):
    """
    Se lista los proyectos actuales del sistema, este metodo se utiliza en el usuario admin
    """
    userSession = getUsuarioSesion(request.user.email)
    rolUsuario = Rol.objects.get(id=userSession.df_rol.id)
    proyectos = Proyecto.objects.all()
    permisosProyecto = ['crt_Proyecto','asg_Proyecto']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id)
    context = { 'userSession':userSession,
                'proyectos':proyectos,
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos}
    html_template = loader.get_template('home/proyectos.html')
    return HttpResponse(html_template.render(context, request))

def GestionProyecto(request):
    usuarios = Usuario.objects.all()
    userSession = getUsuarioSesion(request.user.email)
    context = {'usuarios':usuarios,'segment': 'GestionProyecto','userSession':userSession}
    html_template = loader.get_template('home/GestionProyecto.html')
    return HttpResponse(html_template.render(context, request))

def GestionProyectoAgregar(request):
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
           descripcion_proyecto = variables['descripcion'],
           sprint_dias = variables['sprintDias']
        )
        proyecto.save()
        proyecto.miembro_proyecto.add(miembro)
    return redirect('/')
@login_required(login_url="/login/")
def CrearProyecto(request):
    """
    Redirige a la vista de creacion de proyectos, consiste en un formulario
    """
    usuarios = Usuario.objects.all()
    userSession = getUsuarioSesion(request.user.email)
    rolUsuario = Rol.objects.get(id=userSession.df_rol.id)
    print(rolUsuario.permiso.all())
    context = { 'usuarios':usuarios,
                'segment': 'crearProyecto',
                'userSession':userSession,
                'rolUsuario':rolUsuario
                }
    html_template = loader.get_template('home/CrearProyecto.html')
    return HttpResponse(html_template.render(context, request))

def activarUsuario(request,id):
    """
    Cuando un usuario nuevo se loguea en el sistema queda en estado pendiente hasta que el admin le de acceso
    """
    usuario = Usuario.objects.get(id=id)
    usuario.activo = True
    usuario.save()
    return redirect('/')

def crearProyectoGuardar(request):
    """
    Metodo en el se crea el proyecto, realizando todos los inserts requeridos
    """
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
           fecha_ini_proyecto = None,
           fecha_fin_proyecto = None,
           duracion = variables['duracion'],
           estado = Estado.objects.get(descripcion="PENDIENTE"),
           descripcion_proyecto = variables['descripcion'],
           sprint_dias = variables['sprintDias']
        )
        proyecto.save()
        proyecto.miembro_proyecto.add(miembro)
    return redirect('/')
@login_required(login_url="/login/")
def verProyecto(request,id):
    """
    Cuando un usuario ingresa a un proyecto en el cual fue asignado se visualizan 
    todos los datos de la misma 
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(getPermisos(userSession.id,id),'Permisos')
    permisosProyecto = ['dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'verProyecto',
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos
                }
    html_template = loader.get_template('home/vistaProyectos.html')
    return HttpResponse(html_template.render(context,request))
@login_required(login_url="/login/")
def rolesProyecto(request,id):
    """
    Se lista todos los roles especificos de cada proyecto
    """
    userSession = getUsuarioSesion(request.user.email)
    rolesProyecto = getRolByProyectId(id)
    permisos = Permiso.objects.all()
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(request.session['userSesion'])
    permisosProyecto = ['crt_rol','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'rolesProyecto',
                'permisos':permisos,
                'rolesProyecto':rolesProyecto,
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos
                }
    html_template = loader.get_template('home/rolesProyecto.html')
    return HttpResponse(html_template.render(context,request))

@login_required(login_url="/login/")
def rolesProyectoCrear(request,id):
    """
    Se lista todos los roles especificos de cada proyecto
    """
    userSession = getUsuarioSesion(request.user.email)
    rolesProyecto = getRolByProyectId(id)
    permisos = Permiso.objects.all()
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(request.session['userSesion'])
    permisosProyecto = ['crt_rol','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'rolesProyecto',
                'permisos':permisos,
                'rolesProyecto':rolesProyecto,
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos
                }
    html_template = loader.get_template('home/rolesProyectoCrear.html')
    return HttpResponse(html_template.render(context,request))

def crearRolProyecto(request,id):
    """Se crea un nuevo rol con todos los permisos asociados"""
    variables = request.POST
    if request.method == 'POST':
        rol = Rol(
            descripcion_rol = variables.get('descripcion',False),
            nombre_rol = variables.get('nombre_rol',False),
        )
        rol.save()
        for permiso in variables.getlist('permisos',False):
            print(permiso)
            rol.permiso.add(Permiso.objects.get(id=permiso))
        proyecto_rol = ProyectoRol(
            descripcion_proyecto_rol=''
        )
        proyecto_rol.save()
        proyecto_rol.rol.add(rol)
        proyecto_rol.proyecto.add(Proyecto.objects.get(id=id))
    return redirect(f'/proyecto/roles/{id}')



def eliminarRolProyecto(request,id):
    """Se elimina el rol asociado al id"""
    variables = request.POST
    record = Rol.objects.filter(id = variables.get('idRol',False))
    record.delete()

    """validarEliminacion = getRolByID(id)
    print(validarEliminacion)
    if(validarEliminacion==None):
        print("no es")
    else:
        rol = Rol(
            descripcion_rol = variables.get('descripcion',False),
            nombre_rol = variables.get('nombre_rol',False),
        )
        rol.delete()
    
    rol = Rol(
            descripcion_rol = variables.get('descripcion',False),
            nombre_rol = variables.get('nombre_rol',False),
        )
    rol.delete()
    if request.method == 'POST':
        rol = Rol(
            descripcion_rol = variables.get('descripcion',False),
            nombre_rol = variables.get('nombre_rol',False),
        )
        rol.delete()
        for permiso in variables.getlist('permisos',False):
            print(permiso)
            rol.permiso.remove(Permiso.objects.get(id=permiso))
        proyecto_rol = ProyectoRol(
            descripcion_proyecto_rol=''
        )
        rol.objects.filter(id=id).delete()
        proyecto_rol.objects.filter(id=id).delete()
        #$proyecto_rol.delete()
        proyecto_rol.rol.remove(rol)
        proyecto_rol.proyecto.remove(Proyecto.objects.get(id=id))"""
    return redirect(f'/proyecto/roles/1')


def editarRolProyecto(request,idd):
    """Se elimina el rol asociado al id"""
    print("Entra en la funcion")
    variables = request.POST
    validarEliminacion = getRolByID(id)
    print(validarEliminacion)
    record = Rol.objects.filter(id = idd).first()
    

    return redirect(f'/proyecto/{id}')

def colaboradoresProyecto(request,id):
    """
    Se lista todos colaboradores del proyecto
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(getPermisos(userSession.id,id),'Permisos')
    rolesProyecto = getRolByProyectId(id)
    colaboradores = getColaboratorsByProyect(id)
    usuarios = Usuario.objects.filter(~Q(id=userSession.id)).filter(~Q(df_rol=1))
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context={
        'colaboradores':colaboradores,
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'usuarios':usuarios,
        'validacionPermisos':validacionPermisos
        }
    html_template = loader.get_template('home/colaboradoresProyecto.html')
    return HttpResponse(html_template.render(context,request))
@login_required(login_url="/login/")

def colaboradoresProyectoCrear(request,id):
    """
    Se lista todos colaboradores del proyecto
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(rolUsuario.permiso.all())
    rolesProyecto = getRolByProyectId(id)
    colaboradores = getColaboratorsByProyect(id)
    usuarios = Usuario.objects.filter(~Q(id=userSession.id)).filter(~Q(df_rol=1))
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context={
        'colaboradores':colaboradores,
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'usuarios':usuarios,
        'validacionPermisos':validacionPermisos
        }
    html_template = loader.get_template('home/colaboradoresProyectoCrear.html')
    return HttpResponse(html_template.render(context,request)) 

def asignarColaboradorProyecto(request,id):
    """Se almacena el nuevo rol con el colaborador al proyecto"""
    variables = request.POST
    roles = variables.getlist('rol',False)
    if request.method == 'POST':
        miembro = MiembroEquipo(
           descripcion = ''
        )
        miembro.save()
        for rol in variables.getlist('rol',False):
            miembro.miembro_rol.add(Rol.objects.get(id=rol))
        miembro.miembro_usuario.add(Usuario.objects.get(id=variables.get('usuario',False)))
        proyecto = Proyecto.objects.get(id=id)
        proyecto.miembro_proyecto.add(miembro)
    return redirect(f'/proyecto/colaboradores/{id}')

def eliminarColaboradorProyecto(request,id):
    variables = request.POST
    record = MiembroEquipo.miembro_usuario.objects.filter(id = variables.get('idRol',False))
    record.delete()
    return redirect(f'/proyecto/{id}')

def editarColaboradorProyecto(request,id):
    """Se eliminan los colaboradores de un proyecto especifico"""
    variables = request.POST
    if request.method == 'POST':
        miembro = MiembroEquipo(
           descripcion = ''
        )
        miembro.save()
        miembro.miembro_rol.add(Rol.objects.get(id=variables.get('rol',False)))
        miembro.miembro_usuario.add(Usuario.objects.get(id=variables.get('usuario',False)))
        proyecto = Proyecto.objects.get(id=id)
        proyecto.miembro_proyecto.add(miembro)
    return redirect(f'/proyecto/{id}')

def tipoUs(request,id):
    """Se listan todos los tipos de US"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    tipoUs = getTipoUsbyProyectId(id)
    prioridad = PrioridadTUs.objects.all()
    rolesProyecto = getRolByProyectId(id)
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','ctr_TipoUs','imp_TipoUs','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context={
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'validacionPermisos':validacionPermisos,
        'prueba':rolesProyecto,
        'tipoUs':"tipoUs",
        'prioridades':"prioridad",
        }
    html_template = loader.get_template('home/tipoUS.html')
    return HttpResponse(html_template.render(context,request))
def tipoUsCrear(request,id):
    """Se listan todos los tipos de US"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    prioridad = PrioridadTUs.objects.all()
    print(tipoUs)
    rolesProyecto = getRolByProyectId(id)
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','ctr_TipoUs','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context={
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'validacionPermisos':validacionPermisos,
        'prueba':rolesProyecto,
        'prioridades':prioridad
        }
    html_template = loader.get_template('home/tipoUSCrear.html')
    return HttpResponse(html_template.render(context,request))


def crearTUSProyecto(request,id):
    """Se almacena en base de datos el nuevo tipo de US"""
    variables = request.POST
    if request.method == 'POST':
        jsonFase=json.loads(variables.get('jsonFase',False))
        tipoUs = TipoUserStory(
            nombre_tipo_us = variables.get('nombre',False),
            descripcion_tipo_us= variables.get('descripcion',False),
        )
        tipoUs.save()
        print(jsonFase)
        for faseJson in jsonFase:
            Fase.objects.create(
                nombre_fase=faseJson['nombre'],
                orden_fase=faseJson['orden'],
                tipoUs=tipoUs
            )
        TipoUs_Proyecto.objects.create(
            proyecto=Proyecto.objects.get(id=id),
            tipoUs=tipoUs
        )
    return redirect(f'/proyecto/tipoUs/{id}')

def tipoUsImportar(request,id):
    """Se listan todos los tipos de US"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    prioridad = PrioridadTUs.objects.all()
    tipoUs = getTipoUsbyProyectId(id)
    todostipoUs = getTipoUsbyNotProyectId(id)
    print(tipoUs)
    rolesProyecto = getRolByProyectId(id)
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','ctr_TipoUs','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context={
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'validacionPermisos':validacionPermisos,
        'prueba':rolesProyecto,
        'todostipoUs':todostipoUs,
        'prioridades':prioridad
        }
    html_template = loader.get_template('home/tipoUSImportar.html')
    return HttpResponse(html_template.render(context,request))
def importarTusDeProyecto(request,id):
    variables = request.POST
    if request.method == 'POST':
        tipoUs = TipoUserStory.objects.get(id=variables.get('idTipoUs',False))
        proyecto = Proyecto.objects.get(id=id)
        TipoUs_Proyecto.objects.create(proyecto=proyecto,tipoUs=tipoUs)
    return redirect(f'/proyecto/tipoUs/{id}')
def verProductBacklog(request,id):
    """Se visualiza todos los US"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    rolesProyecto = getRolByProyectId(id)
    # tipoUs = TipoUserStory.objects.filter(proyecto_tipo_us = id)
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','crt_US','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    userStorys = UserStory.objects.filter(proyecto_us = id)
    context={
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'validacionPermisos':validacionPermisos,
        'tipoUs':tipoUs,
        'prueba':rolesProyecto,
        'userStorys':userStorys
        }
    html_template = loader.get_template('home/productBacklog.html')
    return HttpResponse(html_template.render(context,request))

def crearUs(request,id):
    """Se listan todos los tipos de US"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    prioridad = PrioridadTUs.objects.all()
    tipoUs = TipoUs_Proyecto.objects.filter(proyecto = id)
    print(tipoUs)
    rolesProyecto = getRolByProyectId(id)
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','ctr_TipoUs','crt_US','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context={
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'validacionPermisos':validacionPermisos,
        'prueba':rolesProyecto,
        'prioridades':prioridad,
        'tipoUs':tipoUs,
        }
    html_template = loader.get_template('home/usCrear.html')
    return HttpResponse(html_template.render(context,request))

def crearUsGuardar(request,id):
    """Se agregan los nuevos Us"""
    variables = request.POST
    if request.method == 'POST':
        userStory = UserStory(
            proyecto_us = Proyecto.objects.get(id=id),
            nombre_us = variables.get('nombre',False),
            descripcion_us= variables.get('descripcion',False),
            tiempoEstimado_us = variables.get('tiempo',False),
            tipo_us= TipoUserStory.objects.get(id=variables.get('tipoUs',False)),
            prioridad_negocio=variables.get('prioridad',False)
        )
        userStory.save()
    return redirect(f'/proyecto/{id}')

def editarProyecto(request,id):
    """
    Cuando un usuario ingresa a un proyecto en el cual fue asignado se visualizan 
    todos los datos de la misma 
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(getPermisos(userSession.id,id),'Permisos')
    permisosProyecto = ['dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'verProyecto',
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos
                }
    html_template = loader.get_template('home/editarProyecto.html')
    return HttpResponse(html_template.render(context,request))

def editarProyectoGuardar(request,id):
    """
    Metodo en el se crea el proyecto, realizando todos los inserts requeridos
    """
    print(request.POST['nombreProyecto'])
    variables = request.POST
    if request.method == 'POST':
        Cliente.objects.filter(id=variables['idCliente']).update(
            nombre_cliente = variables['nombreCliente'] ,
            apellido_cliente =variables['apellidoCliente'] ,
            email_cliente = variables['emailCliente'],
            telefono_cliente = variables['telefonoCliente'],
            empresa_cliente = variables['empresaCliente']
        )
        Proyecto.objects.filter(id=id).update(
           nombre_proyecto = variables['nombreProyecto'],
           duracion = variables['duracion'],
           descripcion_proyecto = variables['descripcion'],
           sprint_dias = variables['sprintDias']
        )
    return redirect(f'/proyecto/{id}')

def iniciarProyecto(request,id):
    proyectoActual = Proyecto.objects.get(id=id)
    Proyecto.objects.filter(id=id).update(
            fecha_ini_proyecto = datetime.today(),
            fecha_fin_proyecto = calcularFechaFin(datetime.today(),proyectoActual.duracion),
           estado = Estado.objects.get(descripcion="EN PROGRESO"), 
    )
    return redirect(f'/proyecto/{id}')

def sprintProyecto(request,id):
    """Se visualiza todos los US"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    rolesProyecto = getRolByProyectId(id)
    sprint = Sprint.objects.filter(proyecto_sp=id)
    print(sprint,'sprint')
    # tipoUs = TipoUserStory.objects.filter(proyecto_tipo_us = id)
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','crt_US','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    userStorys = UserStory.objects.filter(proyecto_us = id)
    context={
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'validacionPermisos':validacionPermisos,
        'tipoUs':tipoUs,
        'prueba':rolesProyecto,
        'userStorys':userStorys,
        'sprint':sprint
        }
    html_template = loader.get_template('home/sprint.html')
    return HttpResponse(html_template.render(context,request))

def sprintCrear(request,id):
    """
    Cuando un usuario ingresa a un proyecto en el cual fue asignado se visualizan 
    todos los datos de la misma 
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    userStorys = UserStory.objects.filter(proyecto_us = id)
    colaboradores = getColaboratorsByProyect(id)
    permisosProyecto = ['dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,id)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'verProyecto',
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos,
                'userStorys':userStorys,
                'colaboradores':colaboradores
                }
    html_template = loader.get_template('home/sprintCrear.html')
    return HttpResponse(html_template.render(context,request))

def sprintCrearGuardar(request,id):
    """Se guardan los datos iniciales del sprint"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    variables = request.POST
    #print(variables.get('fecha_inicio',False),proyecto.sprint_dias)
    #print(str(busy_end_date(datetime. strptime(variables.get('fecha_inicio',False),'%Y-%m-%d'),proyecto.sprint_dias)))
    if request.method == 'POST':
         Sprint.objects.create(
             descripcion_sp = variables.get('descripcion',False),
             nombre_sp = variables.get('nombre',False),
             fechaIni_sp = variables.get('fecha_inicio',False),
             fechaFIn_sp = busy_end_date(datetime. strptime(variables.get('fecha_inicio',False),'%Y-%m-%d'),proyecto.sprint_dias),
             proyecto_sp = Proyecto.objects.get(id=id),
             estado = Estado.objects.get(descripcion="PENDIENTE"),
         )
    return redirect(f'/proyecto/sprint/{id}')

def sprintColaboradorAgregar(request,idProyecto,idSprint):
    """
    Cuando un usuario ingresa a un proyecto en el cual fue asignado se visualizan 
    todos los datos de la misma 
    """
    aux = Sprint.objects.get(id=idSprint).colaborador_sp.all()
    for i in aux:
        print(i.colaborador,'col')
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(idProyecto,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    colaboradores = getColaboratorsByProyect(idProyecto)
    permisosProyecto = ['dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,idProyecto)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'verProyecto',
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos,
                'colaboradores':colaboradores,
                'sprint':Sprint.objects.get(id=idSprint)
                }
    html_template = loader.get_template('home/sprintAgregarColaborador.html')
    return HttpResponse(html_template.render(context,request))


def sprintColaboradorAgregarGuardar(request,id):
    """Se almacenan los colaboradores del Sprint"""
    variables = request.POST
    if request.method == 'POST':
        jsonColaborador=json.loads(variables.get('jsonColaborador',False))
        sprint = Sprint.objects.get(id=variables.get('idSprint',False))
        print(jsonColaborador)
        for colJson in jsonColaborador:
            spColaborador = SprintColaborador.objects.create(
                colaborador=Usuario.objects.get(id=colJson['colaborador']),
                horas=colJson['horas'],
            )
            sprint.colaborador_sp.add(spColaborador)
    return redirect(f'/proyecto/sprint/{id}')

def sprintUsAgregar(request,idProyecto,idSprint):
    """
    Cuando un usuario ingresa a un proyecto en el cual fue asignado se visualizan 
    todos los datos de la misma 
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(idProyecto,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    aux = Sprint.objects.get(id=idSprint).userStory_sp.all()
    for i in aux:
        print(i.us,'col')
    userStorys = UserStory.objects.filter(proyecto_us = idProyecto,disponible=True)
    colaboradores = Sprint.objects.get(id=idSprint).colaborador_sp.all()
    permisosProyecto = ['dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,idProyecto)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'verProyecto',
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos,
                'colaboradores':colaboradores,
                'sprint':Sprint.objects.get(id=idSprint),
                'userStorys':userStorys
                }
    html_template = loader.get_template('home/sprintAgregarUs.html')
    return HttpResponse(html_template.render(context,request))

def sprintUsAgregarGuardar(request,id):
    """Se almacenan los colaboradores del Sprint"""
    variables = request.POST
    if request.method == 'POST':
        jsonUs=json.loads(variables.get('jsonUs',False))
        sprint = Sprint.objects.get(id=variables.get('idSprint',False))
        print(jsonUs)
        for colJson in jsonUs:
            spUs = SprintUserStory.objects.create(
                colaborador=Usuario.objects.get(id=colJson['colaborador']),
                us=UserStory.objects.get(id = colJson['us']),
            )
            TipoUsEditar=UserStory.objects.get(id = colJson['us']).tipo_us
            UserStory.objects.filter(id = colJson['us']).update(disponible=False,fase=Fase.objects.get(tipoUs=TipoUsEditar,orden_fase=1))
            sprint.userStory_sp.add(spUs)
    return redirect(f'/proyecto/sprint/{id}')
def sprintBacklog(request,idProyecto,idSprint):
    """
    Cuando un usuario ingresa a un proyecto en el cual fue asignado se visualizan 
    todos los datos de la misma 
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(idProyecto,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    userStorys = Sprint.objects.get(id=idSprint).userStory_sp.all()
    permisosProyecto = ['dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,idProyecto)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'verProyecto',
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos,
                'sprint':Sprint.objects.get(id=idSprint),
                'userStorys':userStorys
                }
    html_template = loader.get_template('home/sprintBackLog.html')
    return HttpResponse(html_template.render(context,request))
def sprintTablero(request,idProyecto,idSprint,idTipoUs=None):
    """
    Cuando un usuario ingresa a un proyecto en el cual fue asignado se visualizan 
    todos los datos de la misma 
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(idProyecto,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    userStorys = Sprint.objects.get(id=idSprint).userStory_sp.all()
    tipoUs = getTipoUsBySprint(userStorys)
    tipoUsTablero = ''
    if idTipoUs or idTipoUs == 0:
        if idTipoUs == 0:
            tipoUsTablero = tipoUs[0]
        else:
            tipoUsTablero = TipoUserStory.objects.get(id=idTipoUs)
    else:
        variables = request.POST
        if request.method == 'POST':
            idTp=json.loads(variables.get('tipoUsId',False))
            tipoUsTablero = TipoUserStory.objects.get(id=idTp)
    fases = Fase.objects.filter(tipoUs=tipoUsTablero)
    permisosProyecto = ['dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','dsp_SprinBack']
    validacionPermisos = validarPermisos(permisosProyecto,userSession.id,idProyecto)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'verProyecto',
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos,
                'sprint':Sprint.objects.get(id=idSprint),
                'userStorys':userStorys,
                'tipoUs':tipoUs,
                'tipoUsTablero':tipoUsTablero,
                'fases':fases
                }
    html_template = loader.get_template('home/sprintTablero.html')
    return HttpResponse(html_template.render(context,request))

def pruebaAjax(request):
    print('llegue')
    return redirect(f'/proyecto/sprint/2')

def sprintTableroActualizarEstado(request,idProyecto,idSprint):
    variables = request.POST
    if request.method == 'POST':
        idUserStory = variables.get('userStory',False)
        idNuevaFase = variables.get('nuevaFase',False)
        idTipoUs = variables.get('tipoUsId',False)
        UserStory.objects.filter(id=idUserStory).update(
            fase = Fase.objects.get(id=idNuevaFase)
        )
    return redirect(f'/proyecto/sprint/tablero/{idProyecto}/{idSprint}/{idTipoUs}')