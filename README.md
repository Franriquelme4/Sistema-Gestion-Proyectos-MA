# Sistema de gestion de proyectos#
##  Descripción ##
Proyecto de Ingenieria de Software II

## Construcción ##
* ***Lenguaje*** : Python 3.10
* ***Framework*** : Django 4.1

## Requisitos ##
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Docker](https://www.docker.com/)


## Instalación Desarrollo ##
- Clonar el repositorio de [GitHub](link)
- Una vez que se clona el proyecto se ingresa al directorio sistema_metodos_agiles y se crea un entorno virtual con el siguiente comando 
```
 python3 -m venv env 
```
- Se inicia el entorno virtual con el comando 
```
source env/bin/activate 
```
- Dentro del directorio se encuentra el archivo requirements.txt -> Este archivo almacena todas las dependencias del proyecto, las cuales se instalan con el siguiente comando 
```
pip3 install -r requirements.txt 
```
## Creacion de base de datos ##
- Se debe de realizar una conexion a una base de datos en el puerto ***:5432*** utilizando el gestor de base de datos que mejor le parezca
- Se crea una base de datos llamada ***metodologias_agiles***

## Ejecución Desarrollo ##
- Estando en el directorio del proyecto, se debe de ingresar al directorio sistemas_metodos_agiles :
```
cd sistema_metodos_agiles
```
Se debe de ejecutar las migraciones
- ***makemigrations***, que se encarga de crear nuevas migraciones en función de los cambios que haya realizado en sus modelos.
```
python3 manage.py makemigrations 
```
- ***migrate*** , que se encarga de aplicar y desaplicar migraciones.
```
python3 manage.py migrate 
```
 
Para poblar la base de datos con los valores iniciales, como permisos, roles por defecto etc. se ejecuta el siguiente comando
```
python3 manage.py loaddata Init.json
```
Finalmente se ejecuta el sistema con el siguiente comando:
```
python3 manage.py runserver 
```
***Pruebas Unitarias***
- Para las pruebas unitarias se utiliza un script en la cual se engloba la ejecucion de todos los test, la cual se ejecuta con el siguiente comando
```
sh sistema_metodos_agiles/testScript.sh
```
## Instalación Produccion ##
Para el despliegue en produccion se utilizo ***docker y docker-compose*** en la cual se tienen 3 contenedores distintos
- web 
- servidor 
- base de datos 

