"""
Código utilizado para el cálculo y almacenamiento de las
características por cada una de las distancias y velocidades
antes obtenidas.
"""

import os
import pandas as pd

# Directorios de entrada
distancias_root = 'distancias'  # Carpeta madre con los archivos de distancias
velocidades_root = 'velocidades'  # Carpeta madre con los archivos de velocidades

# Archivo de salida
output_file = 'dataset.csv'  # Archivo final con características

# Listas para almacenar los resultados
resultados = []

# Procesar cada subcarpeta dentro de la carpeta madre de distancias
for subfolder in os.listdir(distancias_root):
    distancias_subfolder_path = os.path.join(distancias_root, subfolder)
    velocidades_subfolder_path = os.path.join(velocidades_root, subfolder)

    # Verificar que existan las subcarpetas correspondientes
    if not os.path.isdir(distancias_subfolder_path) or not os.path.isdir(velocidades_subfolder_path):
        print(f"Subcarpeta faltante: {subfolder}")
        continue

    # Procesar cada archivo dentro de la subcarpeta de distancias
    for file in os.listdir(distancias_subfolder_path):
        if not file.endswith('.csv'):
            continue  # Ignorar archivos que no sean CSV

        # Ruta completa del archivo de distancias
        distancias_file = os.path.join(distancias_subfolder_path, file)

        # Ruta completa del archivo de velocidades correspondiente
        velocidades_file = os.path.join(velocidades_subfolder_path, file.replace('_distancias', '_velocidades'))

        # Verificar si existe el archivo de velocidades correspondiente
        if not os.path.exists(velocidades_file):
            print(f"Archivo de velocidades no encontrado: {velocidades_file}")
            continue

        # Leer los archivos
        distancias_data = pd.read_csv(distancias_file)
        velocidades_data = pd.read_csv(velocidades_file)

        # Calcular características para distancias
        caracteristicas = []
        for columna in distancias_data.columns:
            caracteristicas.extend([
                distancias_data[columna].mean(),   # Media
                distancias_data[columna].var(),    # Varianza
                distancias_data[columna].max(),    # Máximo
                distancias_data[columna].min()     # Mínimo
            ])

        # Calcular características para velocidades
        for columna in velocidades_data.columns:
            caracteristicas.extend([
                velocidades_data[columna].mean(),  # Media
                velocidades_data[columna].var(),   # Varianza
                velocidades_data[columna].max(),   # Máximo
                velocidades_data[columna].min()    # Mínimo
            ])

        # Extraer la etiqueta del nombre del archivo (quitando número y sufijos)
        etiqueta = file.split('_')[0]

        # Agregar la etiqueta como última columna
        caracteristicas.append(etiqueta)

        # Agregar la fila de características al resultado
        resultados.append(caracteristicas)

# Crear un DataFrame con los resultados
columnas = [f'{tipo}_{metrica}_{i+1}' for tipo in ['Distancia', 'Velocidad'] for i in range(8) for metrica in ['media', 'varianza', 'maximo', 'minimo']]
columnas.append('Etiqueta')
resultados_df = pd.DataFrame(resultados, columns=columnas)

# Guardar el DataFrame en un archivo CSV
resultados_df.to_csv(output_file, index=False)
print(f"Características calculadas y guardadas en: {output_file}")