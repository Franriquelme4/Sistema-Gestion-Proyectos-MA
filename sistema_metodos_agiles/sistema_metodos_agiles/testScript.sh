#!/bin/bash

echo Prueba sobre Views

python3 -m unittest ./tests/test_views.py

echo Prueba sobre Models

python3 -m unittest ./tests/test_models.py