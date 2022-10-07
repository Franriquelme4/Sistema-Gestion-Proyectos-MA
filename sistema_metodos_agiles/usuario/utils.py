from .models import Proyecto, Usuario,Rol,ProyectoRol



def getUsuarioSesion(email):
    usuario = Usuario.objects.get(email=email)
    return usuario

def getIdScrumRol():
    rol = Rol.objects.get(id = 3)
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
	where ummu.usuario_id = {id} order by up.fecha_creacion 
   """)
   return proyectos

def getProyectsByID(idProyecto,idUsuario):
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

def getRolByProyectId(id):
	proyecto_rol = ProyectoRol.objects.raw(f"""select up.*, ur.descripcion_rol ,ur.nombre_rol, ur.id as id_rol from usuario_proyectorol up 
	join usuario_proyectorol_proyecto upp on upp.proyectorol_id = up.id
	join usuario_proyectorol_rol upr on upr.proyectorol_id  = up.id 
	join usuario_proyecto up2 on up2.id = upp.proyecto_id 
	join usuario_rol ur on ur.id = upr.rol_id where up2.id = {id}""")
	return proyecto_rol
def getColaboratorsByProyect(id):
	colaboradores = Usuario.objects.raw(f"""
		select uu.*, ur.id as id_rol, ur.nombre_rol as nombre_rol,ur.descripcion_rol as descripcion_rol from usuario_usuario uu 
		join usuario_miembroequipo_miembro_usuario ummu on ummu.usuario_id = uu.id 
		join usuario_miembroequipo_miembro_rol ummr on ummr.miembroequipo_id = ummu.miembroequipo_id 
		join usuario_proyecto_miembro_proyecto upmp on upmp.miembroequipo_id = ummu.miembroequipo_id 
		join usuario_rol ur on ur.id = ummr.rol_id 
		join usuario_proyecto up on up.id = upmp.proyecto_id where up.id = {id}
		""")
	return colaboradores

def validarPermisos(permisosVista,rolUsuario):
	permisos = {}
	for permisoVista in permisosVista:
		permisos[permisoVista] = rolUsuario.poseePermiso(permisoVista)
	return permisos
