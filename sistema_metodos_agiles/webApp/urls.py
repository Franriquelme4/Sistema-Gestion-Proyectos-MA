# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

app_name = "webApp"
urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/activar/<int:id>', views.activarUsuario, name='usuarios'),
    path('proyecto/',views.proyectos, name='proyectos'),
    path('CrearProyecto/',views.CrearProyecto, name='CrearProyecto'),
    path('GestionProyecto/',views.GestionProyecto, name='GestionProyecto'),
    path('CrearProyecto/guardar',views.crearProyectoGuardar, name='crearProyectoGuardar'),
    path('proyecto/roles/<int:id>',views.rolesProyecto, name='rolesProyecto'),
    path('proyecto/roles/crear/<int:id>',views.rolesProyectoCrear, name='rolesProyectoCrear'),
    path('proyecto/roles/guardar/<int:id>',views.crearRolProyecto, name='crearRolProyecto'),
    path('proyecto/roles/eliminar/<int:id>',views.eliminarRolProyecto, name='eliminarRolProyecto'),
    path('proyecto/roles/editar/<int:id>',views.editarRolProyecto, name='editarRolProyecto'),
    path('proyecto/colaboradores/eliminar/<int:id>',views.eliminarColaboradorProyecto, name='eliminarColaboradorProyecto'),
    path('proyecto/colaboradores/editar/<int:id>',views.editarColaboradorProyecto, name='editarColaboradorProyecto'),
    path('proyecto/<int:id>',views.verProyecto, name='verProyecto'),
    path('proyecto/colaboradores/<int:id>',views.colaboradoresProyecto, name='colaboradoresProyecto'),
    path('proyecto/colaboradores/crear/<int:id>',views.colaboradoresProyectoCrear, name='colaboradoresProyectoCrear'),
    path('proyecto/colaboradores/guardar/<int:id>',views.asignarColaboradorProyecto, name='asignarColaboradorProyecto'),
    path('proyecto/tipoUs/<int:id>',views.tipoUs, name='tipoUs'),
    path('proyecto/tipoUs/crear/<int:id>',views.tipoUsCrear, name='tipoUsCrear'),
    path('proyecto/tipoUs/importar/<int:id>',views.tipoUsImportar, name='tipoUsImportar'),
    path('proyecto/tipoUs/importar/guardar/<int:id>',views.importarTusDeProyecto, name='importarTusDeProyecto'),
    path('proyecto/tipoUs/guardar/<int:id>',views.crearTUSProyecto, name='crearTUSProyecto'),
    path('proyecto/tipoUs/importar/<int:id>',views.importarTusDeProyecto, name='importarTusDeProyecto'),
    path('proyecto/productBacklog/<int:id>',views.verProductBacklog, name='verProductBacklog'),
    path('proyecto/userStory/crear/<int:id>',views.crearUs, name='crearUs'),
    path('proyecto/userStory/guardar/<int:id>',views.crearUsGuardar, name='crearUsGuardar'),
    path('proyecto/proyecto/editar/<int:id>',views.editarProyecto, name='editarProyecto'),
    path('proyecto/proyecto/editar/guardar/<int:id>',views.editarProyectoGuardar, name='editarProyectoGuardar'),
    path('proyecto/iniciar/<int:id>',views.iniciarProyecto, name='iniciarProyecto'),
    path('proyecto/sprint/crear/<int:id>',views.sprintCrear, name='sprintCrear')
    
]
