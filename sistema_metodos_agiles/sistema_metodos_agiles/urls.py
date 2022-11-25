"""sistema_metodos_agiles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from webApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('social-auth/',include('social_django.urls'),name='social'),
    path('',include('webApp.urls')),
    path('CrearProyecto/',views.CrearProyecto, name='CrearProyecto'),
    path('proyecto/',views.proyectos, name='proyectos'),
    path('usuarios/activar/<int:id>', views.activarUsuario, name='usuarios'),
    path('proyecto/roles/<int:id>',views.rolesProyecto, name='rolesProyecto'),
    path('proyecto/roles/guardar/<int:id>',views.crearRolProyecto, name='crearRolProyecto'),
    path('proyecto/colaboradores/guardar/<int:id>',views.asignarColaboradorProyecto, name='asignarColaboradorProyecto'),
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
    path('proyecto/tipoUs/guardar/<int:id>',views.crearTUSProyecto, name='crearTUSProyecto'),
    path('proyecto/tipoUs/importar/<int:id>',views.importarTusDeProyecto, name='importarTusDeProyecto'),
    path('proyecto/productBacklog/<int:id>',views.verProductBacklog, name='verProductBacklog'),
    path('proyecto/userStory/guardar/<int:id>',views.crearUs, name='crearUs'),
    path('proyecto/productBacklog/<int:id>',views.verProductBacklog, name='verProductBacklog'),
    path('proyecto/userStory/crear/<int:id>',views.crearUs, name='crearUs'),
    path('proyecto/userStory/guardar/<int:id>',views.crearUsGuardar, name='crearUsGuardar'),
    path('proyecto/proyecto/editar/<int:id>',views.editarProyecto, name='editarProyecto'),
    path('proyecto/proyecto/editar/guardar/<int:id>',views.editarProyectoGuardar, name='editarProyectoGuardar'),
    path('proyecto/iniciar/<int:id>',views.iniciarProyecto, name='iniciarProyecto'),
    path('proyecto/sprint/<int:id>',views.sprintProyecto, name='sprintProyecto'),
    path('proyecto/sprint/crear/<int:id>',views.sprintCrear, name='sprintCrear'),
    path('proyecto/sprint/guardar/<int:id>',views.sprintCrearGuardar, name='sprintCrearGuardar'),
    path('proyecto/sprint/colaborador/<int:idProyecto>/<int:idSprint>',views.sprintColaboradorAgregar, name='sprintColaboradorAgregar'),
    path('proyecto/sprint/colaborador/guardar/<int:id>',views.sprintColaboradorAgregarGuardar, name='sprintColaboradorAgregarGuardar'),
    path('proyecto/sprint/us/<int:idProyecto>/<int:idSprint>',views.sprintUsAgregar, name='sprintUsAgregar'),
    path('proyecto/sprint/us/guardar/<int:id>',views.sprintUsAgregarGuardar, name='sprintUsAgregarGuardar'),
    path('proyecto/sprint/backlog/<int:idProyecto>/<int:idSprint>',views.sprintBacklog, name='sprintBacklog'),
    path('proyecto/sprint/tablero/<int:idProyecto>/<int:idSprint>/<int:idTipoUs>',views.sprintTablero, name='sprintTablero'),
    path('proyecto/sprint/tablero/<int:idProyecto>/<int:idSprint>',views.sprintTablero, name='sprintTablero2'),
    path('proyecto/sprint/tablero/actualizar/<int:idProyecto>/<int:idSprint>',views.sprintTableroActualizarEstado, name='sprintTableroActualizarEstado'),
    path('proyecto/sprint/get/comentarios', views.getComentarios, name = "ajax_comentarios"),
    path('proyecto/userStory/detalles/<int:idProyecto>/<int:idUs>',views.verDetallesUs, name='verDetallesUs'),
    path('proyecto/sprint/iniciar/<int:idProyecto>/<int:idSprint>', views.iniciarSprint, name="iniciarSprint"),
    path('proyecto/sprint/velocitychart/<int:idProyecto>',views.visualizarVelocity, name='visualizarVelocity'),
    path('proyecto/historial/<int:id>',views.verHistorialProyecto, name='verHistorialProyecto'),
    path('proyecto/finalizar', views.cerrarProyecto, name="cerrarProyecto"),
    path('proyecto/sprint/burndownchart2/<int:idProyecto>/<int:idSprint>',views.visualizarBurndown2, name='visualizarBurndown2'),
]
