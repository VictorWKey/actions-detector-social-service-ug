import os
import pandas as pd
import numpy as np

# Función para calcular la distancia euclidiana
def calcular_distancia(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

# Directorios
input_root = 'dataPractice2'  # Carpeta madre de entrada
output_root = 'distanciasPractice2'  # Carpeta madre de salida

# Asegurarse de que la carpeta de salida exista
os.makedirs(output_root, exist_ok=True)

# Definir las columnas para las distancias
joints = [
    ['joint13_x', 'joint13_y', 'joint13_z'],  # Codo izquierdo
    ['joint14_x', 'joint14_y', 'joint14_z'],  # Codo derecho
    ['joint15_x', 'joint15_y', 'joint15_z'],  # Muñeca izquierda
    ['joint16_x', 'joint16_y', 'joint16_z'],  # Muñeca derecha
    ['joint25_x', 'joint25_y', 'joint25_z'],  # Rodilla izquierda
    ['joint26_x', 'joint26_y', 'joint26_z'],  # Rodilla derecha
    ['joint29_x', 'joint29_y', 'joint29_z'],  # Talón izquierdo
    ['joint30_x', 'joint30_y', 'joint30_z']   # Talón derecho
]

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

        # Convertir columnas relevantes a numérico, manejando errores
        for col in ['espina_x', 'espina_y', 'espina_z'] + [col for joint in joints for col in joint]:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')

        resultados = []

        # Calcular las distancias para cada frame
        for _, row in data.iterrows():
            espina_x, espina_y, espina_z = row['espina_x'], row['espina_y'], row['espina_z']
            if pd.isnull([espina_x, espina_y, espina_z]).any():
                continue  # Saltar filas con valores no válidos

            distancias = []
            for joint in joints:
                joint_x, joint_y, joint_z = row[joint[0]], row[joint[1]], row[joint[2]]
                if pd.isnull([joint_x, joint_y, joint_z]).any():
                    distancias.append(np.nan)  # Si faltan datos, agregar NaN
                else:
                    distancia = calcular_distancia(espina_x, espina_y, espina_z, joint_x, joint_y, joint_z)
                    distancias.append(distancia)
            resultados.append(distancias)

        # Crear un DataFrame con los resultados (solo las 8 distancias)
        columnas = [f'Distancia_{j + 1}' for j in range(8)]
        resultados_df = pd.DataFrame(resultados, columns=columnas)

        # Guardar el archivo procesado en la carpeta de salida
        output_file = os.path.join(output_subfolder_path, archivo)
        resultados_df.to_csv(output_file, index=False)
        print(f"Archivo procesado y guardado: {output_file}")