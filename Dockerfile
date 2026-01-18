# Usamos la imagen oficial de Airflow
FROM apache/airflow:2.9.1

# Instalamos Pandas y SQL apenas se construye la imagen
RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary