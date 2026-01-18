import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Configuración
NUM_REGISTROS = 5000
ARCHIVO_SALIDA = 'data/laboratorio_raw.csv'

# Crear carpeta data si no existe
os.makedirs('data', exist_ok=True)

tipos_examen = ['Hemoglobina', 'Glucosa', 'Colesterol', 'Triglicéridos', 'Creatinina']
sedes = ['Surco', 'San Borja', 'Miraflores', 'Lima Centro']

print("Generando datos...")
data = []
for i in range(1, NUM_REGISTROS + 1):
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    fecha = start + timedelta(days=random.randint(0, (end - start).days))
    
    valor = round(random.uniform(70, 200), 2)
    # 5% de error (negativos)
    if random.random() < 0.05: valor = valor * -1 
    
    registro = {
        'id_examen': i,
        'id_paciente': random.randint(100, 500),
        'fecha_toma': fecha.strftime('%Y-%m-%d'),
        'tipo_examen': random.choice(tipos_examen),
        'resultado_valor': valor,
        'sede': random.choice(sedes),
        'tecnico_responsable': np.nan if random.random() < 0.05 else f"Tecnico_{random.randint(1,10)}"
    }
    data.append(registro)

pd.DataFrame(data).to_csv(ARCHIVO_SALIDA, index=False)
print(f"✅ Archivo creado: {ARCHIVO_SALIDA}")