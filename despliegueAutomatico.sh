# !bin/bash
dev(){
    read -p "Desea crear una nueva base de datos (y/n)?: " crearDB
    if [ $crearDB = "y" ]
    then
        # Se crea la nueva base de datos
        psql -X -U postgres password=postgres -p 5432 < ../database/init.sql
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
    crearDB=""
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
        python3 manage.py loaddata ../database/iteracion_2.json
    ;;
    "3") 
        echo "Poblando base de datos ..."
        psql -X -U postgres password=postgres -p 5432 < ../database/init.sql
    ;;
    "4") 
        echo "Poblando base de datos ..."
        psql -X -U postgres password=postgres -p 5432 < ../database/init.sql
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
    echo "Ejecutando entorno de desarrollo..."
    dev
    ;;

    
    "2") 
    psql -U postgres -W postgres -h localhost metodologias_agiles < database/iteracion_2.sql

    ;;
    "*") echo "Opcion incorrecta"
esac
# git checkout $entorno
# echo "Opcion 2 $2"
# echo "Opciones enviadas $*"
# echo -e "\n"
# echo "Recuperar valores"
# while [ -n "$1" ]
# do
# case "$1" in
# -a) echo "-a opcion utilizada";;
# -b) echo "-b opcion utilizada";;
# -c) echo "-c opcion utilizada";;
# *) echo "$1 no es una opcion"
# esac
# shift
# done
# psql -U postgres -W -h localhost metodologias_agiles < database/iteracion_2.sql
psql -X -U postgres -d metodologias_agiles password=postgres -p 5432  < ../database/iteracion_2.sql