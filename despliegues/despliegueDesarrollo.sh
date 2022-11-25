#!/bin/bash
source sistema_metodos_agiles/env/bin/activate
python3 sistema_metodos_agiles/manage.py makemigrations
python3 sistema_metodos_agiles/manage.py migrate
python3 sistema_metodos_agiles/manage.py loaddata sistema_metodos_agiles/Init.json
python3 sistema_metodos_agiles/manage.py runserver