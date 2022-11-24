# !bin/bash
dev(){
    export PGPASSWORD=postgres;
    crearDB=""
    read -p "Desea crear una nueva base de datos (y/n)?: " crearDB
    if [ $crearDB = "y" ]
    then
        # Se crea la nueva base de datos
        # psql -X -U postgres password=postgres -p 5432 < database/init.sql
        cat database/init.sql | psql -U postgres -p 5432 
    fi
    # psql -X -U postgres password=postgres -p 5432 < ../database/init.sql
    git checkout $tag
    git pull
    # Creando entorno virtual
    cd sistema_metodos_agiles  
    python3 -m venv env
    # Se ingresa al entorno virtual
    source env/bin/activate
    # Se instalan todos lo requerimientos
    pip3 install -r requirements.txt
    # read -p "Desea crear una nueva base de datos (y/n)?: " crearDB
    # if [ $crearDB = "y" ]
    # then
    #     # Se crea la nueva base de datos
    #     psql -X -U postgres password=postgres -p 5432 < ../database/init.sql
    # fi
    # Se aplican las migraciones
    python3 manage.py makemigrations
    python3 manage.py migrate
    echo "iteracion $iteracion"
    case $iteracion in
    "2")
        echo "Poblando base de datos ..."
        # psql -X -U postgres password=postgres -p 5432 metodologias_agiles < ../database/iteracion_2.sql
        cat ../database/init.sql | psql -X -U postgres -p 5432 -d metodologias_agiles
    ;;
    "3") 
        echo "Poblando base de datos ..."
        cat ../database/init.sql | psql -X -U postgres -p 5432 -d metodologias_agiles
    ;;
    "4") 
        echo "Poblando base de datos ..."
        cat ../database/init.sql | psql -X -U postgres -p 5432 -d metodologias_agiles
    ;;
    "5") 
        echo "Poblando base de datos ..."
        python3 manage.py loaddata Init.json
    ;;
    "6") 
        echo "Poblando base de datos ..."
        python3 manage.py loaddata Init.json
    ;;
    esac
    # python3 sistema_metodos_agiles/manage.py loaddata sistema_metodos_agiles/Init.json
    python3 manage.py runserver
}
prod(){
    # crearDB=""
    # read -p "Desea crear una nueva base de datos (y/n)?: " crearDB
    # if [ $crearDB = "y" ]
    # then
    #     # Se crea la nueva base de datos
    #     psql -X -U postgres password=postgres -p 5432 < database/init.sql
    # fi
    # psql -X -U postgres password=postgres -p 5432 < ../database/init.sql
    git checkout $tag
    git pull
    docker-compose build
    echo "iteracion $iteracion"
    case $iteracion in
    "2")
        echo "Poblando base de datos ..."
        # psql -X -U postgres password=postgres -p 5432 metodologias_agiles < ../database/iteracion_2.sql
        # python3 manage.py loaddata ../database/iteracion_2.json
    ;;
    "3") 
        echo "Poblando base de datos ..."
        # psql -X -U postgres password=postgres -p 5432 < ../database/init.sql
    ;;
    "4") 
        echo "Poblando base de datos ..."
        # psql -X -U postgres password=postgres -p 5432 < ../database/init.sql
    ;;
    "5") 
        echo "Poblando base de datos ..."
        docker-compose exec web python3 manage.py loaddata Init.json
    ;;
    "6") 
        echo "Poblando base de datos ..."
        # python3 manage.py loaddata Init.json
    ;;
    esac
    # python3 sistema_metodos_agiles/manage.py loaddata sistema_metodos_agiles/Init.json
    docker-compose up 
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
