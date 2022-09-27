INSERT INTO usuario_rol(id, nombre_rol, descripcion_rol)
VALUES 
(1,'Administrador','Rol para administrar el sistema'),
(2,'Observador','Rol por default para todos los usuarios'),
(3,'Scrum Master','Rol para gestionar proyecto');

INSERT INTO usuario_permiso(id, nombre_permiso, descripcion_permiso)
VALUES 
(1, 'def'				,'Default'							),
(2, 'crt_Sprint'		,'Crear Sprint'						),
(3, 'asg_Sprint'		,'Asignar Sprint'					),
(4, 'crt_Proyecto'		,'Crear Proyecto'					),
(5, 'act_Usuario'		,'Activar Usuarios'					),
(6, 'crt_US'			,'Crear User Stories'				),
(7, 'upd_US'			,'Modificar User Stories'			),
(8, 'dlt_US'			,'Eliminar User Stories'			),
(9, 'adm_Burndown'		,'Administrar BurnDown Chart'		),
(10,'crt_Dailys'		,'Crear Dailys'						),
(11,'dsp_SprinBack'	 	,'Consultar Sprint Backlog'			),
(12,'dsp_ProductBack'	,'Consultar Product Backlog'		),
(13,'dsp_HisCambioUS'	,'Consultar Historial Cambios US'	),
(14,'upd_PrioridadUS'	,'Modificar Prioridad US'			),
(15,'crt_rol'			,'Crear Roles'						),
(16,'asg_rol'			,'Asignar Roles'					),
(17,'dlt_rol'			,'Eliminar Roles'					),
(18,'agr_Colaborador'	,'Agregar Colaboradores'			),
(19,'dlt_Colaborador'	,'Eliminar Colaboradores'			),
(20,'upd_EstaKannban'	,'Modificar Estado Kanban'			),
(21,'asg_Proyecto'		,'Asignar Proyecto'					),
(22,'upd_PrioriNegoc'	,'Modificar Prioridad Negocio'		),
(23,'dsp_Burndown'		,'Consultar BurnDown Chart'			),
(24,'dsp_Velocity'		,'Consultar Velocity Chart'			),
(25,'dsp_ReporteEsta'	,'Consultar Reporte Estado'			),
(26,'dct_Usuario'		,'Desactivar Usuarios'				),
(27,'dsp_Colaborador'	,'Consultar Colaboradores'			),
(28,'dsp_Roles'	        ,'Consultar Roles'			        ),
(29,'dsp_TipoUs'	    ,'Consultar Tipo US'			    );


INSERT INTO public.usuario_permiso
(id, descripcion_permiso, nombre_permiso)
VALUES(30, 'Crear Tipo de US', 'ctr_TipoUs');
INSERT INTO public.usuario_permiso
(id, descripcion_permiso, nombre_permiso)
VALUES(31, 'Modificar Tipo de US', 'upd_TipoUs');
INSERT INTO public.usuario_permiso
(id, descripcion_permiso, nombre_permiso)
VALUES(32, 'Eliminar Tipo de Us', 'dlt_TipoUs');


INSERT INTO usuario_rol_permiso(id, rol_id, permiso_id)
VALUES 
(1,2,1),
(2,1,1),
(3,1,4),
(4,1,5),
(5,1,21),
(6,1,26),
(7,3,1),
(8,3,2),
(9,3,3),
(10,3,6),
(11,3,7),
(12,3,8),
(13,3,18),
(14,3,15),
(15,3,27),
(16,3,28),
(17,3,29),
(18,3,30),
(19,3,31),
(20,3,32),
(21,3,12);

INSERT INTO public.usuario_prioridadtus
(id, descripcion, valor)
VALUES(1, 'Alta', 1);
INSERT INTO public.usuario_prioridadtus
(id, descripcion, valor)
VALUES(2, 'Media', 2);
INSERT INTO public.usuario_prioridadtus
(id, descripcion, valor)
VALUES(3, 'Baja', 3);



