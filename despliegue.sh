# !bin/bash
dev(){
    export PGPASSWORD=postgres;
    crearDB=""
    read -p "Desea crear una nueva base de datos (y/n)?: " crearDB
    if [ $crearDB = "y" ]
    then
        # Se crea la nueva base de datos
        cat database/init.sql | psql -U postgres -p 5432 
    fi
    git checkout $tag
    git pull
    # Creando entorno virtual
    cd sistema_metodos_agiles  
    python3 -m venv env
    # Se ingresa al entorno virtual
    source env/bin/activate
    # Se instalan todos lo requerimientos
    pip3 install -r requirements.txt
    # Se aplican las migraciones
    python3 manage.py makemigrations
    python3 manage.py migrate
    if [ $crearDB = "y" ]
    then
        echo "Poblando base de datos ..."
        case $iteracion in
        "2")
            cat ../database/init.sql | psql -X -U postgres -p 5432 -d metodologias_agiles
        ;;
        "3") 
            cat ../database/init.sql | psql -X -U postgres -p 5432 -d metodologias_agiles
        ;;
        "4") 
            cat ../database/init.sql | psql -X -U postgres -p 5432 -d metodologias_agiles
        ;;
        "5") 
            python3 manage.py loaddata Init.json
        ;;
        "6") 
            python3 manage.py loaddata Init.json
        ;;
        esac
    fi
    python3 manage.py runserver
}
prod(){
    # Se elimina todos los contenedores 
    docker-compose down --rmi all -v --remove-orphans
    git checkout $tag
    git pull
    docker-compose up --build
    echo "Poblando base de datos ..."
    case $iteracion in
    "2")
        docker-compose  exec -T db psql -U postgres -d metodologias_agiles < database/init.sql
    ;;
    "3") 
        docker-compose  exec -T db psql -U postgres -d metodologias_agiles < database/init.sql
    ;;
    "4") 
        docker-compose  exec -T db psql -U postgres -d metodologias_agiles < database/init.sql
    ;;
    "5") 
        docker-compose exec web python manage.py loaddata Init.json
    ;;
    "6") 
        docker-compose exec web python3 manage.py loaddata Init.json
    ;;
    esac
}
echo "--------------------------------------------------------------------------"
echo "===================== Sistema de Gestion de Proyecto ====================="
echo "========================= Despliegue automatico =========================="
echo "--------------------------------------------------------------------------"
tag=""
iteracion=""
echo "Seleccionar la iteracion a la cual desea acceder "
echo "1) Iteracion 1 --> tag=v0.0.1"
echo "2) Iteracion 2 --> tag=Iteracion_2"
echo "3) Iteracion 3 --> tag=iteracion_3"
echo "4) Iteracion 4 --> tag=iteracion_4.1"
echo "5) Iteracion 5 --> tag=iteracion_5"
echo "6) Iteracion 6 --> tag=iteracion_6"
read -p "Ingresar una iteracion: " iteracion
case $iteracion in
    "1") tag="v0.0.1";;
    "2") tag="Iteracion_2";;
    "3") tag="iteracion_3";;
    "4") tag="iteracion_4.1";;
    "5") tag="iteracion_5";;
    "6") tag="iteracion_6";;
    "*") echo "Opcion incorrecta"
esac
echo "Seleccionar en entorno en el que quiere iniciar el proyecto"
echo "1) Desarrollo"
echo "2) Produccion"
read -p "Ingresar una opcion: " entorno
case $entorno in
    "1") 
    echo "Ejecutando entorno de desarrollo ..."
    dev
    ;;
    "2") 
    echo "Ejecutando entorno de produccion ..."
    prod
    ;;
    "*") echo "Opcion incorrecta"
esac
