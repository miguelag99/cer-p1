# cer-p1

# Repositorio de la aplicación web de Computación en Red

Configuración inicial (requiere pip3):

    git clone https://github.com/miguelag99/cer-p1.git
    cd cer-p1
    sh install_webapp.sh

Una vez instalado todo lo necesario se debe lanzar el servicio de la base de datos:


    systemctl start elasticsearch.service 


Por último, para ejecutar la lógica y la capa de presentación:

    sh launch_web_app.sh