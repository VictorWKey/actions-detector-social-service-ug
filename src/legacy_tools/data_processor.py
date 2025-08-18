"""
Herramientas para procesar datos legacy y limpiar estructuras de carpetas antiguas
"""

import os
import shutil
import pandas as pd

class LegacyDataProcessor:
    def __init__(self):
        """Inicializa el procesador de datos legacy"""
        pass
    
    def clean_capture_folders(self, base_path):
        """
        Limpia estructura de carpetas de capturas antiguas, manteniendo solo xyz
        Equivalente a dataElimination.py
        
        Args:
            base_path: Ruta base donde están las carpetas con subcarpetas 'camera_1'
        """
        print(f"Limpiando estructura de carpetas en: {base_path}")
        
        if not os.path.exists(base_path):
            print(f"Ruta no encontrada: {base_path}")
            return False
        
        # Listar todas las subcarpetas
        carpetas_principales = [
            os.path.join(base_path, nombre_carpeta)
            for nombre_carpeta in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, nombre_carpeta))
        ]
        
        folders_processed = 0
        
        for carpeta in carpetas_principales:
            ruta_camera_1 = os.path.join(carpeta, "camera_1")
            
            if os.path.isdir(ruta_camera_1):
                # Subcarpetas dentro de 'camera_1'
                subcarpetas = [
                    os.path.join(ruta_camera_1, subcarpeta)
                    for subcarpeta in os.listdir(ruta_camera_1)
                    if os.path.isdir(os.path.join(ruta_camera_1, subcarpeta))
                ]
                
                for subcarpeta in subcarpetas:
                    subcarpeta_nombre = os.path.basename(subcarpeta)
                    if subcarpeta_nombre == "xyz":
                        # Mover la carpeta 'xyz' al nivel de 'camera_1'
                        nueva_ruta = os.path.join(carpeta, "xyz")
                        if not os.path.exists(nueva_ruta):
                            shutil.move(subcarpeta, nueva_ruta)
                            print(f"Movida carpeta 'xyz' de {ruta_camera_1} a {carpeta}")
                    else:
                        # Eliminar las carpetas 'rgb' y 'skeleton'
                        shutil.rmtree(subcarpeta)
                        print(f"Eliminada carpeta '{subcarpeta_nombre}' en {ruta_camera_1}")
                
                # Eliminar la carpeta 'camera_1' vacía
                try:
                    os.rmdir(ruta_camera_1)
                    print(f"Carpeta 'camera_1' eliminada en {carpeta}")
                    folders_processed += 1
                except OSError:
                    print(f"No se pudo eliminar 'camera_1' en {carpeta} (puede no estar vacía)")
            else:
                print(f"No se encontró carpeta 'camera_1' en {carpeta}")
        
        print(f"Procesamiento completado. {folders_processed} carpetas procesadas.")
        return True
    
    def remove_extra_columns(self, base_path):
        """
        Elimina columnas innecesarias de archivos CSV (generalmente la primera columna)
        Equivalente a eliminar_4tacolumna.py
        
        Args:
            base_path: Ruta base donde están las carpetas con archivos CSV
        """
        print(f"Eliminando columnas extra en: {base_path}")
        
        if not os.path.exists(base_path):
            print(f"Ruta no encontrada: {base_path}")
            return False
        
        # Encontrar subcarpetas con archivos CSV
        subcarpetas = []
        for root, dirs, files in os.walk(base_path):
            if any(f.endswith('.csv') for f in files):
                subcarpetas.append(root)
        
        files_processed = 0
        
        for ruta in subcarpetas:
            archivos = [f for f in os.listdir(ruta) if f.endswith('.csv')]
            
            for archivo in archivos:
                archivo_ruta = os.path.join(ruta, archivo)
                
                # Comprobar si el archivo está vacío
                if os.path.getsize(archivo_ruta) == 0:
                    print(f"Archivo vacío omitido: {archivo}")
                    continue
                
                try:
                    # Leer el archivo CSV
                    df = pd.read_csv(archivo_ruta)
                    
                    # Verificar si tiene exactamente 4 columnas (caso común)
                    if df.shape[1] == 4:
                        # Eliminar la primera columna
                        df = df.iloc[:, 1:]
                        df.to_csv(archivo_ruta, index=False)
                        print(f"Primera columna eliminada en: {archivo}")
                        files_processed += 1
                    elif df.shape[1] == 3:
                        print(f"Archivo ya tiene formato correcto: {archivo}")
                    else:
                        print(f"Formato inesperado ({df.shape[1]} columnas): {archivo}")
                        
                except Exception as e:
                    print(f"Error procesando {archivo}: {e}")
        
        print(f"Procesamiento completado. {files_processed} archivos modificados.")
        return True
    
    def reshape_csvs_to_dataset(self, input_path, output_path, activity_prefix):
        """
        Convierte archivos CSV de formato 33x3 a 1x99 y los combina en un dataset
        Equivalente a reshapeCSVs.py
        
        Args:
            input_path: Ruta donde están los archivos CSV individuales
            output_path: Ruta donde guardar los archivos reestructurados
            activity_prefix: Prefijo para nombrar los archivos de salida
        """
        print(f"Reestructurando CSVs de {input_path} a {output_path}")
        
        if not os.path.exists(input_path):
            print(f"Ruta de entrada no encontrada: {input_path}")
            return False
        
        # Crear directorio de salida
        os.makedirs(output_path, exist_ok=True)
        
        # Encontrar subcarpetas con archivos CSV
        subcarpetas = []
        for item in os.listdir(input_path):
            item_path = os.path.join(input_path, item)
            if os.path.isdir(item_path):
                # Buscar archivos CSV en la subcarpeta o en xyz dentro de ella
                csv_path = item_path
                xyz_path = os.path.join(item_path, "xyz")
                if os.path.exists(xyz_path):
                    csv_path = xyz_path
                
                if any(f.endswith('.csv') for f in os.listdir(csv_path)):
                    subcarpetas.append(csv_path)
        
        datasets_created = 0
        
        for idx, ruta in enumerate(subcarpetas, start=1):
            archivos = [f for f in os.listdir(ruta) if f.endswith('.csv')]
            todas_las_filas = []
            
            for archivo in archivos:
                archivo_ruta = os.path.join(ruta, archivo)
                
                # Comprobar si el archivo está vacío
                if os.path.getsize(archivo_ruta) == 0:
                    print(f"Archivo vacío omitido: {archivo}")
                    continue
                
                try:
                    # Leer el archivo CSV
                    df = pd.read_csv(archivo_ruta, header=None)
                    
                    # Verificar formato esperado (33 filas, 3 columnas)
                    if df.shape[1] == 3 and df.shape[0] == 33:
                        # Realizar reshape a una fila con 99 columnas
                        df_reshaped = df.values.flatten()
                        
                        if df_reshaped.size == 99:
                            todas_las_filas.append(df_reshaped)
                        else:
                            print(f"Tamaño incorrecto después del reshape: {archivo}")
                    else:
                        print(f"Formato incorrecto ({df.shape[0]}x{df.shape[1]}): {archivo}")
                        
                except Exception as e:
                    print(f"Error procesando {archivo}: {e}")
            
            # Guardar dataset si se procesaron archivos
            if todas_las_filas:
                # Generar nombres de columnas
                columnas = [f'joint{i // 3}_{["x", "y", "z"][i % 3]}' for i in range(99)]
                
                # Crear DataFrame
                df_resumen = pd.DataFrame(todas_las_filas, columns=columnas)
                
                # Guardar archivo
                archivo_salida = os.path.join(output_path, f"{activity_prefix}_{idx:02}.csv")
                df_resumen.to_csv(archivo_salida, index=False)
                print(f"Dataset creado: {archivo_salida} ({len(todas_las_filas)} filas)")
                datasets_created += 1
            else:
                print(f"No se procesaron archivos válidos en: {ruta}")
        
        print(f"Reestructuración completada. {datasets_created} datasets creados.")
        return True
