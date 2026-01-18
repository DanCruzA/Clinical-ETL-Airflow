# 🧪 Automated Clinical Lab ETL Pipeline (Airflow + Docker)

## 📋 Descripción del Proyecto
Este proyecto consiste en un **Pipeline de Ingeniería de Datos End-to-End** que automatiza la ingesta, limpieza y carga de resultados de laboratorio clínico masivos.

Se construyó una arquitectura contenerizada utilizando **Docker**, donde **Apache Airflow** orquesta el flujo de datos (DAGs), procesando archivos crudos con **Pandas** y cargándolos en un Data Warehouse en **PostgreSQL**.

## 🏗️ Arquitectura de la Solución

```mermaid
graph LR
    A[Generador de Datos<br>Script Python] -->|CSV Raw| B(Sistema de Archivos)
    B --> C{Apache Airflow<br>Orquestador}
    C -->|Extract & Transform<br>Pandas| D[Limpieza de Datos]
    D -->|Load| E[(PostgreSQL<br>Data Warehouse)]

. Fuente: Datos simulados de laboratorio (5,000 registros con ruido/errores intencionales).

. Transformación: Normalización de valores negativos, imputación de nulos y tipado de datos.

. Infraestructura: Despliegue mediante docker-compose con servicios aislados.

## 🛠️ Tecnologías Utilizadas

. Docker & Docker Compose: Para la infraestructura como código (IaC).

. Apache Airflow 2.9: Para la orquestación y calendarización de tareas.

. Python 3.10 (Pandas/SQLAlchemy): Motor de procesamiento ETL.

. PostgreSQL 16: Base de datos destino.

. Linux (Pop!_OS): Entorno de desarrollo.

## 🔧 Desafíos Técnicos y Soluciones (Troubleshooting)
Durante la implementación de este pipeline en un entorno Linux estricto, se superaron los siguientes retos técnicos:

1. Gestión de Dependencias en Contenedores (Custom Image)
Problema: La imagen base de Airflow no incluye librerías de ciencia de datos (pandas, sqlalchemy), causando fallos en la ejecución de tareas (ModuleNotFoundError). Solución: En lugar de instalar librerías manualmente en tiempo de ejecución, se implementó una imagen personalizada mediante un Dockerfile para garantizar la reproducibilidad.

Código implementado (Dockerfile):

FROM apache/airflow:2.9.1
# Instalación de dependencias al construir la imagen
RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary

2. Conflictos de Permisos en Volúmenes (Linux)
Problema: Al mapear volúmenes locales (./logs, ./data) al contenedor, Airflow (UID 50000) no tenía permisos de escritura sobre las carpetas del host (usuario local), generando errores PermissionError: [Errno 13]. Solución: Se aplicó una apertura de permisos recursiva en el entorno de desarrollo para permitir que el contenedor escribiera los logs de ejecución.

Comando de solución:

sudo chmod -R 777 dags data logs

## 🚀 Cómo ejecutar este proyecto

Clonar el repositorio:

git clone [https://github.com/DanCruzA/Clinical-ETL-Airflow.git](https://github.com/DanCruzA/Clinical-ETL-Airflow.git)
cd Clinical-ETL-Airflow

Generar la Data Simulada:

python3 generar_data.py

Desplegar la Infraestructura:

# El flag --build es importante para crear la imagen con Pandas
docker-compose up --build -d

Acceder a Airflow:

. URL: http://localhost:8085

. Credenciales: admin / admin

. Activar el DAG etl_laboratorio_clinico.

## 📊 Verificación de Datos
Una vez ejecutado el pipeline, se puede verificar la carga en el Data Warehouse:

-- Verificar corrección de valores negativos y conteo total
SELECT count(*) FROM fact_resultados_lab;
-- Resultado esperado: 5000