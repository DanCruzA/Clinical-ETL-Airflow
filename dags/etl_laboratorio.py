from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import os

# Conexión al Postgres DW (Nombre del servicio en docker-compose: p3_postgres_dw)
DB_CONN = 'postgresql+psycopg2://data_engineer:password123@p3_postgres_dw/dw_clinica'
INPUT_FILE = '/opt/airflow/data/laboratorio_raw.csv'

def run_etl():
    print("--- INICIO ETL ---")
    
    # 1. EXTRACT
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"No existe: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    print(f"Extraídos: {len(df)} registros")
    
    # 2. TRANSFORM
    df['resultado_valor'] = df['resultado_valor'].abs() # Corregir negativos
    df['tecnico_responsable'] = df['tecnico_responsable'].fillna('Sin Asignar') # Llenar nulos
    df['fecha_proceso'] = datetime.now()
    
    # 3. LOAD
    engine = create_engine(DB_CONN)
    df.to_sql('fact_resultados_lab', engine, if_exists='replace', index=False)
    print("--- CARGA EXITOSA ---")

default_args = {
    'owner': 'DataEngineer',
    'start_date': datetime(2024, 1, 1),
    'retries': 0
}

with DAG('etl_laboratorio_clinico', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    
    task_etl = PythonOperator(
        task_id='ejecutar_etl_completo',
        python_callable=run_etl
    )