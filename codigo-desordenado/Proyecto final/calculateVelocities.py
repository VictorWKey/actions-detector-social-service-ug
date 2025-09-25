import os
import pandas as pd

# Directorios
input_root = 'distancias'  # Carpeta madre con los archivos de distancias
output_root = 'velocidades'  # Carpeta madre para los archivos de velocidades

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

    # Procesar los archivos dentro de la subcarpeta actual
    for file in os.listdir(input_subfolder_path):
        input_file = os.path.join(input_subfolder_path, file)
        if not input_file.endswith('.csv'):
            continue  # Ignorar archivos que no sean CSV

        # Leer los datos
        data = pd.read_csv(input_file)

        # Calcular las velocidades como diferencia entre filas consecutivas / 0.1
        velocidades = data.diff().iloc[1:] / 0.1  # Ignorar la primera fila (NaN tras diff)

        # Guardar el archivo procesado en la carpeta de salida con el mismo nombre
        output_file = os.path.join(output_subfolder_path, file)
        velocidades.to_csv(output_file, index=False)
        print(f"Archivo de salida guardado: {output_file}")