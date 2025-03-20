#!/bin/bash

# Esperar a que Airflow esté listo
sleep 10

# Crear usuario administrador en Airflow
airflow users create \
    --username admin2 \
    --firstname Nicolas \
    --lastname Rojo \
    --role Admin \
    --email yo@ex.com \
    --password admin
