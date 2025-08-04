"""
Código utilizado para realizar un submuestreo y quedarnos
con 100 de 300 frames capturados para quitar información
irrelevante
"""

import os

# Ruta base donde están las carpetas con los archivos CSV
base_ruta = r"viene_viene_premium"

# Listamos todas las subcarpetas dentro de la ruta base
subcarpetas = [os.path.join(base_ruta, nombre_carpeta, "camera_1", "xyz") 
               for nombre_carpeta in os.listdir(base_ruta)
               if os.path.isdir(os.path.join(base_ruta, nombre_carpeta))]

# Procesamos cada subcarpeta
for ruta in subcarpetas:
    # Listamos todos los archivos en la carpeta `xyz`
    archivos = sorted([f for f in os.listdir(ruta) if f.endswith('.csv')])

    # Verificamos la cantidad de archivos
    num_archivos = len(archivos)

    if num_archivos == 300:
        # Mantenemos solo uno de cada tres archivos
        for i, archivo in enumerate(archivos):
            if i % 3 != 0:
                # Eliminamos el archivo si no es uno de cada tres
                os.remove(os.path.join(ruta, archivo))
        print(f"Proceso completado en {ruta}. Ahora solo tienes 100 archivos.")
    elif num_archivos == 100:
        print(f"No es necesario realizar cambios en {ruta}, ya tienes 100 archivos.")
    else:
        print(f"Cantidad de archivos inesperada en {ruta}: {num_archivos}.")