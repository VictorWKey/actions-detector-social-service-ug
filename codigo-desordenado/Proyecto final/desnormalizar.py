import os
import pandas as pd

# Directorios
input_root = 'Equipo2_rawData'  # Carpeta madre de entrada con archivos normalizados
output_root = 'Equipo2_cleanData'  # Carpeta madre de salida para los archivos desnormalizados

# Dimensiones de la imagen
image_width = 640  # Ancho de la imagen original
image_height = 480  # Alto de la imagen original

# Asegurarse de que la carpeta de salida exista
os.makedirs(output_root, exist_ok=True)

# Procesar cada subcarpeta en la carpeta madre
for subfolder in os.listdir(input_root):
    input_subfolder_path = os.path.join(input_root, subfolder)
    if not os.path.isdir(input_subfolder_path):
        continue  # Ignorar archivos si los hubiera

    # Crear la subcarpeta correspondiente en el directorio de salida
    output_subfolder_path = os.path.join(output_root, subfolder)
    os.makedirs(output_subfolder_path, exist_ok=True)

    # Procesar todos los archivos CSV dentro de la subcarpeta actual
    for archivo in os.listdir(input_subfolder_path):
        if not archivo.endswith('.csv'):
            continue

        input_file = os.path.join(input_subfolder_path, archivo)

        # Leer los datos
        data = pd.read_csv(input_file)

        # Desnormalizar las columnas x e y
        for column in data.columns:
            if "_x" in column:
                data[column] = data[column] * image_width
            elif "_y" in column:
                data[column] = data[column] * image_height

        # Guardar el archivo desnormalizado en la carpeta de salida
        output_file = os.path.join(output_subfolder_path, archivo)
        data.to_csv(output_file, index=False)
        print(f"Archivo desnormalizado y guardado: {output_file}")