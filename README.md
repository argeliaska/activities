# API REST Actividades de propiedades para TH
TH DRF CRUD practice test 

Esta API contiene los servicios REST necesarios para agendar, listar, reagendar y cancelar actividades 
para una propiedad

Esta API se desarrolló en base a los requerimientos proporcionados por TH utilizando el framework Django
y Django Rest Framework usando Postgresql como base de datos

---

### En este proyecto solo utilice la rama **main**

---

## Instalación de paquetes para el proyecto

Pasos de instalación de paquetes, framework y servidor.

1. Crear el directorio donde va a estar el proyecto y dentro un entorno virtual de Python.
2. Con el entorno activo, instalar django v. 1.11.29 con **pip install Django==1.11.29**
3. Luego instalar DRF con **pip djangorestframework==3.8.2**
4. Después el driver de postgresql **pip install psycopg2==2.8.6**
5. Listo ya tienes todo el entorno listo para poder ejecutar el proyecto.

---

## Ejecución del proyecto

Desde el directorio que contiene el proyecto y el entorno virtual de python: 

1. Abrir una ventana de command o shell. 
2. Activar el entorno virtual **source venv/bin/activate** **env\Script\activate** 
3. Iniciar el servidor: **python manage.py runserver localhost:8001**
4. Podrás ver el API en el navegador **http://localhost:8001/api/v1/**
5. Podrás ver el listado de actividades en **http://localhost:8001/api/v1/activities**
