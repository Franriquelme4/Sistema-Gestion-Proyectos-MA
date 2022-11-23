# !bin/bash
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
    git checkout $tag
    git pull
    source sistema_metodos_agiles/env/bin/activate
    pip3 install -r requirements.txt
    python3 sistema_metodos_agiles/manage.py makemigrations
    python3 sistema_metodos_agiles/manage.py migrate
    python3 sistema_metodos_agiles/manage.py loaddata sistema_metodos_agiles/Init.json
    python3 sistema_metodos_agiles/manage.py runserver
    ;;
    "2") echo "Prod"
    echo "Prod"
    echo "Prod"
    echo "Prod"
    echo "Prod"
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
