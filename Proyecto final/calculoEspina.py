import os
import pandas as pd

# Directorios
input_root = "data1" 
output_root = "data"

# Crear la carpeta de salida si no existe
os.makedirs(output_root, exist_ok=True)

# Recorrer todas las subcarpetas dentro de input_root
for subfolder in os.listdir(input_root):
    input_subfolder = os.path.join(input_root, subfolder)
    if os.path.isdir(input_subfolder):
        # Crear la subcarpeta correspondiente en el output
        output_subfolder = os.path.join(output_root, subfolder.replace("_Clean", "_Complete"))
        os.makedirs(output_subfolder, exist_ok=True)
        
        # Procesar los primeros 100 archivos CSV dentro de la subcarpeta
        csv_files = [f for f in os.listdir(input_subfolder) if f.endswith(".csv")][:100]
        for csv_file in csv_files:
            input_file_path = os.path.join(input_subfolder, csv_file)
            output_file_path = os.path.join(output_subfolder, csv_file)

            # Leer el archivo CSV
            df = pd.read_csv(input_file_path)

            # Verificar si la columna "espina_x" ya existe
            if "espina_x" in df.columns and "espina_y" in df.columns and "espina_z" in df.columns:
                print(f"Archivo {csv_file} ya contiene las columnas de espina. Copiando sin modificaciones...")
                # Copiar archivo directamente al output
                df.to_csv(output_file_path, index=False)
                continue

            # Verificar si las columnas necesarias existen en el archivo
            columnas_necesarias = [
                "joint11_x", "joint11_y", "joint11_z",  # Hombro Izquierdo
                "joint12_x", "joint12_y", "joint12_z",  # Hombro Derecho
                "joint23_x", "joint23_y", "joint23_z",  # Cadera Izquierda
                "joint24_x", "joint24_y", "joint24_z"   # Cadera Derecha
            ]
            if not all(col in df.columns for col in columnas_necesarias):
                print(f"Archivo {csv_file} en {subfolder} no contiene todas las columnas necesarias. Saltando...")
                continue

            # Asegurarse de que las columnas sean numéricas
            for col in columnas_necesarias:
                df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir a numérico, NaN si no se puede convertir
            
            # Reemplazar NaN por 0 (puedes ajustar esto según lo que necesites)
            df.fillna(0, inplace=True)

            # Calcular las columnas del centroide
            df["espina_x"] = (df["joint11_x"] + df["joint12_x"] + df["joint23_x"] + df["joint24_x"]) / 4
            df["espina_y"] = (df["joint11_y"] + df["joint12_y"] + df["joint23_y"] + df["joint24_y"]) / 4
            df["espina_z"] = (df["joint11_z"] + df["joint12_z"] + df["joint23_z"] + df["joint24_z"]) / 4

            # Guardar el archivo procesado en la subcarpeta de salida
            df.to_csv(output_file_path, index=False)
            print(f"Procesado y guardado: {output_file_path}")

print("Procesamiento completo.")