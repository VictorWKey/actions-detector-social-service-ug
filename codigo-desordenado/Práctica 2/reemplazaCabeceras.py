import os
import pandas as pd

def reemplazar_cabeceras(carpeta_principal):
    """
    Reemplaza las cabeceras de todos los archivos CSV en una carpeta y sus subcarpetas 
    con las nuevas cabeceras especificadas.

    Args:
        carpeta_principal (str): Ruta a la carpeta principal que contiene los archivos CSV.
    """
    # Nuevas cabeceras
    nuevas_cabeceras = [
        f"joint{i}_x" for i in range(33)
    ] + [
        f"joint{i}_y" for i in range(33)
    ] + [
        f"joint{i}_z" for i in range(33)
    ]
    nuevas_cabeceras = sorted(nuevas_cabeceras, key=lambda x: (int(x.split('_')[0][5:]), x.split('_')[1]))
    
    for subcarpeta, _, archivos in os.walk(carpeta_principal):
        for archivo in archivos:
            if archivo.endswith('.csv'):
                archivo_path = os.path.join(subcarpeta, archivo)
                try:
                    # Leer el archivo CSV
                    df = pd.read_csv(archivo_path)

                    # Validar que el número de columnas coincide con las esperadas
                    if len(df.columns) != len(nuevas_cabeceras):
                        print(f"El archivo {archivo_path} tiene un número de columnas diferente al esperado ({len(df.columns)} columnas).")
                        continue

                    # Reemplazar las cabeceras
                    df.columns = nuevas_cabeceras

                    # Guardar el archivo con las nuevas cabeceras
                    df.to_csv(archivo_path, index=False)
                    print(f"Cabeceras reemplazadas en: {archivo_path}")

                except Exception as e:
                    print(f"Error al procesar el archivo {archivo_path}: {e}")

# Ruta a la carpeta principal
carpeta_principal = r'Equipo2_rawData'  # Cambia esta ruta a tu carpeta específica

# Ejecutar la función
reemplazar_cabeceras(carpeta_principal)