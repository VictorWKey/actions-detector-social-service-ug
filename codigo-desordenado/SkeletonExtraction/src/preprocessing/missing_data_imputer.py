"""
Código utilizado para imputar valores (joints) faltantes
o no detectados por la cámara en el momento de la grabación
"""

import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

# Ruta base donde están las carpetas con los archivos CSV
base_ruta = r"levantar_caja_abajo"

# Listamos todas las subcarpetas dentro de la ruta base
subcarpetas = [os.path.join(base_ruta, nombre_carpeta, "camera_1", "xyz") 
               for nombre_carpeta in os.listdir(base_ruta)
               if os.path.isdir(os.path.join(base_ruta, nombre_carpeta))]

# Procesamos cada subcarpeta
for ruta in subcarpetas:
    # Listamos todos los archivos en la carpeta `xyz`
    archivos = sorted([f for f in os.listdir(ruta) if f.endswith('.csv')])

    # Procesamos cada archivo CSV
    for archivo in archivos:
        archivo_ruta = os.path.join(ruta, archivo)
        
        # Leer el archivo CSV sin encabezados
        df = pd.read_csv(archivo_ruta, header=None)

        # Verificar si todos los valores son numéricos
        if not df.stack().map(np.isreal).all():
            print(f"Archivo {archivo_ruta} contiene valores no numéricos. Verifica y corrige manualmente.")
            continue

        # Verificar si el archivo tiene menos de 33 filas
        if df.shape[0] < 33:
            print(f"El archivo {archivo_ruta} tiene {df.shape[0]} filas, completando con los k vecinos más cercanos.")
            
            # Aplicar interpolación con los k vecinos más cercanos (en este caso, k=3)
            imputer = KNNImputer(n_neighbors=3)
            df_imputed = pd.DataFrame(imputer.fit_transform(df))
            
            # Llenamos hasta llegar a 33 filas duplicando la última fila con los valores imputados
            while df_imputed.shape[0] < 33:
                df_imputed = pd.concat([df_imputed, df_imputed.tail(1)], ignore_index=True)
            
            # Guardar el archivo con los datos completados
            df_imputed.to_csv(archivo_ruta, index=False, header=False)
            print(f"Archivo {archivo} completado con vecinos más cercanos y guardado.")
        else:
            print(f"El archivo {archivo} tiene {df.shape[0]} filas, no se requieren cambios.")