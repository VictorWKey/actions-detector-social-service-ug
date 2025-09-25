"""
Código utilizado para 'aplanar' los archivos csv en una solo fila
para su posterior unión en un archivo csv con dimensiones de 100 * 99
"""

import os
import pandas as pd

# Ruta base donde están las carpetas con los archivos CSV
base_ruta = r"viene_viene_premium"
# Ruta donde se guardarán los archivos reestructurados
ruta_destino = r"viene_viene_premium_Clean"  

# Prefijo para los nombres de los archivos de resumen
prefijo_resumen = "viene_viene_premium"

# Crear la ruta destino si no existe
if not os.path.exists(ruta_destino):
    os.makedirs(ruta_destino)

# Listamos todas las subcarpetas dentro de la ruta base
subcarpetas = [os.path.join(base_ruta, nombre_carpeta, "camera_1", "xyz") 
               for nombre_carpeta in os.listdir(base_ruta)
               if os.path.isdir(os.path.join(base_ruta, nombre_carpeta))]

# Procesamos cada subcarpeta
for idx, ruta in enumerate(subcarpetas, start=1):
    # Listamos todos los archivos en la carpeta `xyz`
    archivos = [f for f in os.listdir(ruta) if f.endswith('.csv')]
    
    # Lista para almacenar todas las filas reestructuradas de esta subcarpeta
    todas_las_filas = []

    # Procesamos cada archivo
    for archivo in archivos:
        archivo_ruta = os.path.join(ruta, archivo)
        
        # Comprobar si el archivo está vacío antes de leerlo
        if os.path.getsize(archivo_ruta) == 0:
            print(f"El archivo {archivo_ruta} está vacío y se omitió.")
            continue
        
        # Leer el archivo CSV sin considerar el primer renglón como encabezado
        df = pd.read_csv(archivo_ruta, header=None)
        
        # Verificar si tiene exactamente 3 columnas y 33 filas
        if df.shape[1] == 3 and df.shape[0] == 33:
            # Realizamos el reshape a un solo renglón con 99 columnas
            df_reshaped = df.values.flatten()
            
            # Verificar si el número de elementos es 99
            if df_reshaped.size == 99:
                # Generar los nuevos nombres de las columnas
                columnas = [f'joint{i // 3}_{["x", "y", "z"][i % 3]}' for i in range(99)]
                
                # Agregar esta fila al archivo resumen
                todas_las_filas.append(df_reshaped)
            else:
                print(f"El archivo {archivo_ruta} no tiene 99 elementos después del reshape, no se modificó.")
        else:
            print(f"El archivo {archivo_ruta} no tiene el formato esperado (33 filas y 3 columnas), no se modificó.")
    
    # Si se procesaron archivos, guardar el archivo de resumen para esta subcarpeta
    if todas_las_filas:
        # Crear un DataFrame con todas las filas reestructuradas
        df_resumen = pd.DataFrame(todas_las_filas, columns=columnas)
        
        # Generar la ruta del archivo de resumen con el prefijo y el índice de la subcarpeta
        archivo_resumen = os.path.join(ruta_destino, f"{prefijo_resumen}_{idx:02}.csv")
        
        # Guardar el archivo CSV con el resumen
        df_resumen.to_csv(archivo_resumen, index=False)
        print(f"Archivo de resumen guardado en {archivo_resumen}")
    else:
        print(f"No se procesaron archivos válidos en la subcarpeta {ruta}.")
    
    print(f"Proceso completado en {ruta}.")