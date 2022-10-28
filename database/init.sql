
INSERT INTO public.usuario_rol(id, nombre_rol, descripcion_rol)
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
(34,'dsp_US'            ,'Consultar User Stories'           ),
(9, 'adm_Burndown'		,'Administrar BurnDown Chart'		),
(10,'crt_Dailys'		,'Crear Dailys'						),
(11,'dsp_SprinBack'	 	,'Consultar Sprint Backlog'			),
(12,'dsp_ProductBack'	,'Consultar Product Backlog'		),
(13,'dsp_HisCambioUS'	,'Consultar Historial Cambios US'	),
(14,'upd_PrioridadUS'	,'Modificar Prioridad US'			),
(15,'crt_rol'			,'Crear Roles'						),
(16,'asg_rol'			,'Asignar Roles'					),
(17,'dlt_rol'			,'Eliminar Roles'					),
(28,'dsp_Roles'	        ,'Consultar Roles'			        ),
(18,'agr_Colaborador'	,'Agregar Colaboradores'			),
(19,'dlt_Colaborador'	,'Eliminar Colaboradores'			),
(33,'upd_Colaborador'   ,'Modificar Colaborador'            ),
(20,'upd_EstaKanban'	,'Modificar Estado Kanban'			),
(21,'asg_Proyecto'		,'Asignar Proyecto'					),
(22,'upd_PrioriNegoc'	,'Modificar Prioridad Negocio'		),
(23,'dsp_Burndown'		,'Consultar BurnDown Chart'			),
(24,'dsp_Velocity'		,'Consultar Velocity Chart'			),
(25,'dsp_ReporteEsta'	,'Consultar Reporte Estado'			),
(26,'dct_Usuario'		,'Desactivar Usuarios'				),
(27,'dsp_Colaborador'	,'Consultar Colaboradores'			),
(29,'dsp_TipoUs'	    ,'Consultar Tipo US'			    ),
(30,'ctr_TipoUs'        ,'Crear Tipo US'                    ),
(31,'upd_TipoUs'        ,'Modificar Tipo US'                ),
(32,'dlt_TipoUs'        ,'Eliminar Tipo US'                 ),
(39,'imp_TipoUs'        ,'Importar Tipo US'                 ),
(35,'dsp_Tablero'       ,'Consultar Tablero'                ),
(36,'crt_Tablero'       ,'Crear Tablero'                    ),
(37,'dlt_Tablero'       ,'Eliminar Tablero'                 ),
(38,'upd_Tablero'       ,'Modificar Tablero'                ),
(40,'upd_rol'           ,'Modificar Rol'                    ),
(41,'ini_Proyecto'      ,'Iniciar Proyecto'                 ),
(42,'upd_Proyecto'      ,'Editar Proyecto'                  ),
(44,'agr_Colaborador_Sprint','Agregar Colaborador Sprint'   ),
(45,'dsp_Colaborador_Sprint','Consultar Colaborador Sprint' ),
(46,'agr_Colaborador_US','Agregar US - Colaborador Sprint'  );


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
(25,3,9),
(26,3,10),
(23,3,11),
(21,3,12),
(29,3,13),
(30,3,14),
(14,3,15),
(32,3,16),
(33,3,17),
(13,3,18),
(37,3,19),
(36,3,20),
(31,3,21),
(34,3,22),
(27,3,23),
(38,3,24),
(28,3,25),
(39,3,26),
(15,3,27),
(16,3,28),
(17,3,29),
(18,3,30),
(19,3,31),
(20,3,32),
(22,3,33),
(24,3,34),
(35,3,35),
(40,3,36),
(41,3,37),
(42,3,38),
(43,3,39),
(44,3,40),
(45,3,41),
(46,3,42),
(47,3,44),
(48,3,45),
(49, 3, 46);




INSERT INTO public.usuario_estado
(id, descripcion)
VALUES(1, 'PENDIENTE');
INSERT INTO public.usuario_estado
(id, descripcion)
VALUES(2, 'EN PROGRESO');
INSERT INTO public.usuario_estado
(id, descripcion)
VALUES(3, 'TERMINADO');
INSERT INTO public.usuario_estado
(id, descripcion)
VALUES(4, 'CANCELADO');
INSERT INTO public.usuario_estado
(id, descripcion)
VALUES(5, 'PLANIFICACION');



INSERT INTO public.usuario_usuario
(id, nombre, apellido, email, nombre_usuario, activo, df_rol_id)
VALUES(1, 'admin', 'sistema', 'as.is2.g15@gmail.com', 'as.is2.g15', true, 1);


