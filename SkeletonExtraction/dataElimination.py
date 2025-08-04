"""
Con este código se eliminaron las otras 2 carpetas con información
irrelevante que fueron capturadas al momento de la grabación
"""

import os
import shutil

# Ruta base donde están las carpetas con las subcarpetas 'camera_1'
base_ruta = r"data\viene_viene_premium"

# Listamos todas las subcarpetas dentro de la ruta base
carpetas_principales = [os.path.join(base_ruta, nombre_carpeta)
                        for nombre_carpeta in os.listdir(base_ruta)
                        if os.path.isdir(os.path.join(base_ruta, nombre_carpeta))]

# Procesamos cada carpeta principal
for carpeta in carpetas_principales:
    # Ruta a la carpeta 'camera_1'
    ruta_camera_1 = os.path.join(carpeta, "camera_1")
    
    # Verificamos si existe la carpeta 'camera_1'
    if os.path.isdir(ruta_camera_1):
        # Subcarpetas dentro de 'camera_1'
        subcarpetas = [os.path.join(ruta_camera_1, subcarpeta)
                       for subcarpeta in os.listdir(ruta_camera_1)
                       if os.path.isdir(os.path.join(ruta_camera_1, subcarpeta))]

        for subcarpeta in subcarpetas:
            subcarpeta_nombre = os.path.basename(subcarpeta)
            if subcarpeta_nombre == "xyz":
                # Mover la carpeta 'xyz' al nivel de 'camera_1'
                nueva_ruta = os.path.join(carpeta, "xyz")
                shutil.move(subcarpeta, nueva_ruta)
                print(f"Movida carpeta 'xyz' de {ruta_camera_1} a {carpeta}.")
            else:
                # Eliminar las carpetas 'rgb' y 'eskeleton'
                shutil.rmtree(subcarpeta)
                print(f"Eliminada la carpeta '{subcarpeta_nombre}' en {ruta_camera_1}.")

        # Finalmente, eliminamos la carpeta 'camera_1' vacía
        os.rmdir(ruta_camera_1)
        print(f"Carpeta 'camera_1' eliminada en {carpeta}.")
    else:
        print(f"No se encontró la carpeta 'camera_1' en {carpeta}.")