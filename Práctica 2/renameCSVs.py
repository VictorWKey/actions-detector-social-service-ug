import os

def renombrar_csvs(carpeta, nuevo_nombre_de_archivo, indice):
    """
    Renombra todos los archivos CSV en una carpeta siguiendo un patrón de nombres.

    Args:
        carpeta (str): Ruta de la carpeta que contiene los archivos CSV.
        nuevo_nombre_de_archivo (str): Base del nuevo nombre de los archivos.
        indice (int): Número inicial para numerar los archivos.
    """
    try:
        # Asegurarse de que la carpeta existe
        if not os.path.exists(carpeta):
            print(f"La carpeta '{carpeta}' no existe.")
            return

        # Obtener todos los archivos CSV en la carpeta
        archivos_csv = [f for f in os.listdir(carpeta) if f.endswith('.csv')]
        
        if not archivos_csv:
            print(f"No se encontraron archivos CSV en la carpeta '{carpeta}'.")
            return

        # Ordenar los archivos para que el renombrado sea consistente
        archivos_csv.sort()

        # Renombrar los archivos
        for i, archivo in enumerate(archivos_csv, start=indice):
            # Nuevo nombre del archivo
            nuevo_nombre = f"{nuevo_nombre_de_archivo}_{i:02d}.csv"
            ruta_actual = os.path.join(carpeta, archivo)
            nueva_ruta = os.path.join(carpeta, nuevo_nombre)

            # Renombrar archivo
            os.rename(ruta_actual, nueva_ruta)
            print(f"Renombrado: '{archivo}' -> '{nuevo_nombre}'")

        print("Renombrado completado.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Ejemplo de uso:
carpeta = r"velocidades\viene"  # Ruta a la carpeta con los archivos CSV
nuevo_nombre_de_archivo = "viene"  # Base del nuevo nombre
indice = 1  # Número inicial para los archivos renombrados

renombrar_csvs(carpeta, nuevo_nombre_de_archivo, indice)