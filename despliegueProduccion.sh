#!/bin/bash
docker-compose build
docker-compose exec web python3 manage.py loaddata Init.json
docker-compose up 