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
    path('proyectos/',views.proyectos, name='proyectos'),
    path('CrearProyecto/',views.CrearProyecto, name='CrearProyecto'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    path('test/',views.request_page , name='test'),
]
