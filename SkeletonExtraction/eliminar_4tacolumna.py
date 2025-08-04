"""
Código utilizado para eliminar la 4ta e innecesaria columna
captada y guardada en cada uno de los archivos CSV's
"""

import os
import pandas as pd

# Ruta base donde están las carpetas con los archivos CSV
base_ruta = r"levantar_caja_abajo"

# Listamos todas las subcarpetas dentro de la ruta base
subcarpetas = [os.path.join(base_ruta, nombre_carpeta, "camera_1", "xyz") 
               for nombre_carpeta in os.listdir(base_ruta)
               if os.path.isdir(os.path.join(base_ruta, nombre_carpeta))]

# Procesamos cada subcarpeta
for ruta in subcarpetas:
    # Listamos todos los archivos en la carpeta `xyz`
    archivos = [f for f in os.listdir(ruta) if f.endswith('.csv')]

    # Procesamos cada archivo para borrar la primera columna
    for archivo in archivos:
        archivo_ruta = os.path.join(ruta, archivo)
        
        # Comprobar si el archivo está vacío antes de leerlo
        if os.path.getsize(archivo_ruta) == 0:
            print(f"El archivo {archivo_ruta} está vacío y se omitió.")
            continue
        
        # Leer el archivo CSV
        df = pd.read_csv(archivo_ruta)
        
        # Verificar si tiene exactamente 4 columnas
        if df.shape[1] == 4:
            # Eliminar la primera columna
            df = df.iloc[:, 1:]
            
            # Guardar el archivo CSV sin la primera columna
            df.to_csv(archivo_ruta, index=False)
            print(f"Primera columna eliminada en {archivo_ruta}")
        else:
            print(f"El archivo {archivo_ruta} no tiene 4 columnas, no se modificó.")
    
    print(f"Proceso completado en {ruta}.")