from .models import Proyecto, Usuario,Rol



def getUsuarioSesion(email):
    usuario = Usuario.objects.get(email=email)
    return usuario

def getIdScrumRol():
    rol = Rol.objects.get(descripcion = "Scrum")
    return rol

def getProyectsByUsuarioID(id):
    proyectos = Proyecto.objects.raw(f"""
	select up.* as proyecto,
		uu.id as id_usuario,
		ur.id as id_rol, ur.descripcion  as descripcion_rol 
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
		ur.id as id_rol, ur.descripcion  as descripcion_rol 
    from usuario_proyecto up 
	join usuario_proyecto_miembro_proyecto upmp on upmp.proyecto_id = up.id 
	join usuario_miembroequipo_miembro_usuario ummu on ummu.miembroequipo_id = upmp.miembroequipo_id
	join usuario_miembroequipo_miembro_rol ummr on ummr.miembroequipo_id = upmp.miembroequipo_id 
	join usuario_usuario uu on uu.id = ummu.usuario_id 
	join usuario_rol ur on ur.id = ummr.rol_id 
	where up.id = {idProyecto} and ummu.usuario_id = {idUsuario} order by up.fecha_creacion 
    """)
    return proyecto
