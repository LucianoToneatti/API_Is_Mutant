# API_Is_Mutant

# Repositorio de Diseño de Sistemas para proyecto del Parcial

Detector de ADN Mutante
Este proyecto implementa una API REST que permite analizar secuencias de ADN para determinar si un individuo es mutante o humano. Además, incluye un servicio para consultar estadísticas sobre el total de secuencias evaluadas y los resultados de las detecciones.

Requisitos
Python 3.11 o superior
Flask
SQLAlchemy


Instrucciones para Ejecutar el Proyecto

Paso 1: Instalación de Dependencias
Instala las dependencias necesarias ejecutando el siguiente comando en tu terminal:
    pip install -r requirements.txt

Paso 2:
Inicia la aplicación ejecutando el archivo principal:
    python app.py

Paso 3:
Abre Postman y carga el archivo de colección ubicado en la carpeta collection.

Paso 4:
En Postman, selecciona la solicitud POST de las diferentes que hay y elije alguna para enviar una secuencia de ADN y verificar si pertenece a un mutante o no. Ingresa la secuencia en formato JSON en el cuerpo de la solicitud y envíala.

Tambien añadí, la posibilidad en la cual envias un ADN erroneo o vacío.

Paso 5:
Para obtener estadísticas, selecciona la solicitud GET en Postman para ver el conteo de mutantes y no mutantes almacenados en la base de datos.


Postman se ejecutara en esta URL: http://127.0.0.1:5000/

Como esta dockreizado y hosteado con render solo hace falta abrir postman y poner las siguientes url:
Para realizar POST
https://api-is-mutant.onrender.com/mutant/
Para realizar GET
https://api-is-mutant.onrender.com/stats