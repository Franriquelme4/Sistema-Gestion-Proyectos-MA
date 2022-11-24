from django.http import HttpResponse
from .models import Historial, MiembroEquipo, Permiso, Proyecto, Usuario, Rol, ProyectoRol, TipoUserStory
import calendar
from datetime import date, datetime, timedelta
import datetime
import numpy as np
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO


def getUsuarioSesion(email):
    usuario = Usuario.objects.get(email=email)
    return usuario


def getIdScrumRol():
    rol = Rol.objects.get(id=3)
    return rol
#def getProyectsByUsuarioID(id):
#    proyectos = Proyecto.objects.raw(f"""
#	select up.* as proyecto,
#		uu.id as id_usuario,
#		ur.id as id_rol, ur.descripcion_rol  as descripcion_rol,
#		ur.nombre_rol  as nombre_rol 
#	from usuario_proyecto up 
#	join usuario_proyecto_miembro_proyecto upmp on upmp.proyecto_id = up.id 
#	join usuario_miembroequipo_miembro_usuario ummu on ummu.miembroequipo_id = upmp.miembroequipo_id
#	join usuario_miembroequipo_miembro_rol ummr on ummr.miembroequipo_id = upmp.miembroequipo_id 
#	join usuario_usuario uu on uu.id = ummu.usuario_id 
#	join usuario_rol ur on ur.id = ummr.rol_id 
#	where ummu.usuario_id = {id} order by up.fecha_creacion 
#   """)
#   return proyectos



def getProyectsByUsuarioID(id):
    proyectos = Proyecto.objects.raw(f"""
	select up.*,uu.id as id_usuario, 
	array_to_string(array_agg(ur.nombre_rol),', ') as roles
	from usuario_proyecto up 
	join usuario_proyecto_miembro_proyecto upmp on upmp.proyecto_id = up.id 
	join usuario_miembroequipo_miembro_usuario ummu on ummu.miembroequipo_id = upmp.miembroequipo_id
	join usuario_miembroequipo_miembro_rol ummr on ummr.miembroequipo_id = upmp.miembroequipo_id 
	join usuario_usuario uu on uu.id = ummu.usuario_id 
	join usuario_rol ur on ur.id = ummr.rol_id 
	where ummu.usuario_id = {id} group by up.id,uu.id order by up.fecha_creacion 
    """)
    return proyectos


def getProyectsByID(idProyecto, idUsuario):
    proyecto = Proyecto.objects.raw(f"""
	select up.* as proyecto,
		uu.id as id_usuario,
		ur.id as id_rol, ur.descripcion_rol  as descripcion_rol,
		ur.nombre_rol  as nombre_rol
    from usuario_proyecto up 
	join usuario_proyecto_miembro_proyecto upmp on upmp.proyecto_id = up.id 
	join usuario_miembroequipo_miembro_usuario ummu on ummu.miembroequipo_id = upmp.miembroequipo_id
	join usuario_miembroequipo_miembro_rol ummr on ummr.miembroequipo_id = upmp.miembroequipo_id 
	join usuario_usuario uu on uu.id = ummu.usuario_id 
	join usuario_rol ur on ur.id = ummr.rol_id 
	where up.id = {idProyecto} and ummu.usuario_id = {idUsuario} order by up.fecha_creacion 
    """)
    return proyecto

def getRolByID(idProyecto):
    proyecto = Proyecto.objects.raw(f"""
	select miembroequipo_id from usuario_miembroequipo_miembro_rol
	where rol.id = {idProyecto}
    """)
    return proyecto


def getProyectoRol(id):
	proyecto_rol = ProyectoRol.objects.raw(f"""select
	join usuario_rol ur on ur.id = upr.rol_id where up2.id = {id}""")

def getRolByProyectId(id):
    proyecto_rol = ProyectoRol.objects.raw(f"""select up.*, ur.descripcion_rol ,ur.nombre_rol, ur.id as id_rol from usuario_proyectorol up 
	join usuario_proyectorol_proyecto upp on upp.proyectorol_id = up.id
	join usuario_proyectorol_rol upr on upr.proyectorol_id  = up.id 
	join usuario_proyecto up2 on up2.id = upp.proyecto_id 
	join usuario_rol ur on ur.id = upr.rol_id where up2.id = {id}""")
    return proyecto_rol

def getRolByProyectIdByUsuario(id,idUsuario):
    proyecto_rol = ProyectoRol.objects.raw(f"""select up.*, ur.descripcion_rol ,ur.nombre_rol, ur.id as id_rol from usuario_proyectorol up 
	join usuario_proyectorol_proyecto upp on upp.proyectorol_id = up.id
	join usuario_proyectorol_rol upr on upr.proyectorol_id  = up.id 
	join usuario_proyecto up2 on up2.id = upp.proyecto_id 
	join usuario_rol ur on ur.id = upr.rol_id where up2.id = {id} """)
    return proyecto_rol
def getRolByproyectUsuario(id,idUsuario):
	proyectoRol = ProyectoRol.objects.raw(f"""select um.id, array_agg(distinct urp.id) as roles from usuario_miembroequipo um 
	join usuario_miembroequipo_miembro_rol ummr on um.id = ummr.miembroequipo_id 
	join usuario_miembroequipo_miembro_usuario ummu on um.id = ummu.miembroequipo_id 
	join usuario_proyecto_miembro_proyecto upmp on upmp.proyecto_id = {id}
	join usuario_rol urp on urp.id = ummr.rol_id 
	where ummu.usuario_id = {idUsuario} group by um.id""")
	return proyectoRol


def getColaboratorsByProyect(id):
    colaboradores = Usuario.objects.raw(f"""select
	uu.*,
	array_to_string(array_agg(ur.nombre_rol), ', ') as nombre_rol,
	array_to_string(array_agg(ur.descripcion_rol), ', ') as descripcion_rol,
	array_to_string(array_agg(ur.id), ', ') as id_rol
from
	usuario_usuario uu
join usuario_miembroequipo_miembro_usuario ummu on
	ummu.usuario_id = uu.id
join usuario_miembroequipo_miembro_rol ummr on
	ummr.miembroequipo_id = ummu.miembroequipo_id
join usuario_proyecto_miembro_proyecto upmp on
	upmp.miembroequipo_id = ummu.miembroequipo_id
join usuario_rol ur on
	ur.id = ummr.rol_id
join usuario_proyecto up on
	up.id = upmp.proyecto_id
where
	up.id = {id}
group by
	uu.id
		""")
    return colaboradores

def getPermisos(id_usuario,id_proyecto):
	# permisos = MiembroEquipo.objects.raw(f""" select distinct um.id,array_agg(distinct urp.permiso_id) as permisos from usuario_miembroequipo um 
	# join usuario_proyecto_miembro_proyecto upmp on upmp.proyecto_id = {id_proyecto} 
	# join usuario_miembroequipo_miembro_usuario ummu on ummu.miembroequipo_id = um.id 
	# join usuario_miembroequipo_miembro_rol ummr on ummu.miembroequipo_id = um.id
	# join usuario_rol_permiso urp on urp.rol_id = ummr.rol_id 
	# where ummu.usuario_id = {id_usuario} group by um.id """)
	print(id_usuario,id_proyecto,'permisos')
	permisos = MiembroEquipo.objects.raw(f""" select um.id, array_agg(distinct urp.permiso_id) as permisos from usuario_miembroequipo um 
	join usuario_miembroequipo_miembro_rol ummr on um.id = ummr.miembroequipo_id 
	join usuario_miembroequipo_miembro_usuario ummu on um.id = ummu.miembroequipo_id 
	join usuario_proyecto_miembro_proyecto upmp on upmp.proyecto_id = {id_proyecto} 
	join usuario_rol_permiso urp on urp.rol_id = ummr.rol_id 
	where ummu.usuario_id = {id_usuario} group by um.id""")
	permisos = permisos[0].permisos
	print(permisos,'listado de permisos')
	aux = [];
	for permiso in permisos:
		aux.append(Permiso.objects.get(id=permiso).nombre_permiso)
	# usuarioPer = Usuario.objects.get(id=id_usuario).df_rol.permiso.all()
	# # print(usuarioPer,'u')
	# aa=[]
	# for per in usuarioPer:
	# 	aa.append(per.nombre_permiso)
	# print(aa,'permisos')
	return aux

def validarPermisos(permisosVista,idUsuario,idProyecto=None):
	permisosUsuario=[]
	if idProyecto:
		permisosUsuario = getPermisos(idUsuario,idProyecto)
	else:
		usuarioPer = Usuario.objects.get(id=idUsuario).df_rol.permiso.all()

		for per in usuarioPer:
			permisosUsuario.append(per.nombre_permiso)
	permisos = {}
	for permisoVista in permisosVista:
		try:
			permisosUsuario.index(permisoVista)
			permisos[permisoVista] =  True
		except:
			permisos[permisoVista] = False

	# for permisoVista in permisosVista:
	# 	permisos[permisoVista] = rolUsuario.poseePermiso(permisoVista)
	print(permisos)
	return permisos


def getTipoUsbyProyectId(id):
	print("Llegue Id proyecto", id)
	tipoUs = TipoUserStory.objects.raw(f"""select ut.*,array_to_string(array_agg(uf.nombre_fase),', ') as fases from usuario_tipouserstory ut 
	full join usuario_tipous_proyecto utp on utp."tipoUs_id" = ut.id 
	full join usuario_fase uf on uf."tipoUs_id" = ut.id where utp.proyecto_id = {id} group by ut.id""")
	return tipoUs

def getTipoUsbyNotProyectId(id):
	print("Llegue Id proyecto", id)
	tipoUs = TipoUserStory.objects.raw(f"""select ut.*,array_to_string(array_agg(uf.nombre_fase),', ') as fases from usuario_tipouserstory ut 
	full join usuario_tipous_proyecto utp on utp."tipoUs_id" = ut.id 
	full join usuario_fase uf on uf."tipoUs_id" = ut.id where utp.proyecto_id != {id} group by ut.id""")
	return tipoUs

def calcularFechaFin(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def getTipoUsBySprint(userStory):
	tipoUsId = []
	for us in userStory:
		# print(us.us.tipo_us.id)
		tipoUsId.append(us.us.tipo_us.id)
	result = []
	tipoUs = []
	for item in tipoUsId:
		if item not in result:
			result.append(item)
			tipoUs.append(TipoUserStory.objects.get(id=item))
	print(result)
	return tipoUs

def is_busy_day(date):
  res = np.is_busday(date)
  return(res)

def busy_end_date(start_date,busy_days):
  res = 0
  contador = 0
  aux_days = busy_days
  aux_date = start_date
  while True:
    contador = contador + 1
    aux_days = busy_days - res
    td = int(aux_days)
    aux_date = aux_date + timedelta(days = td)
    res = np.busday_count(start_date.strftime('%Y-%m-%d'), aux_date.strftime('%Y-%m-%d'))
    if busy_days == res:
      break
    if res > busy_days:
      print("Error mas dias del enviado")
      break
    if contador > 99:
      print("Error break por Contador")
      break
    if res == 1:
      aux_days = aux_days + 1
  return(aux_date)

def agregarHistorial(descripcion,idProyecto):
	print("Se guarda el historial ")
	proyecto = Proyecto.objects.get(id=idProyecto)
	historial = Historial(
		descripcion = descripcion
	)
	historial.save()
	proyecto.historial.add(historial)
	return
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
