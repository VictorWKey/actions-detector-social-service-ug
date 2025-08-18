"""
Módulo de preprocesamiento de datos de esqueleto
"""

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import os

class DataPreprocessor:
    def __init__(self):
        """Inicializa el preprocesador de datos"""
        self.expected_frames = 100  # Número objetivo de frames
        self.expected_joints = 33   # Número de joints
        self.coords_per_joint = 3   # x, y, z por joint
        
    def process_raw_data(self, input_file):
        """
        Procesa un archivo CSV crudo aplicando todo el pipeline de limpieza
        
        Args:
            input_file: Ruta del archivo CSV crudo
            
        Returns:
            Ruta del archivo procesado
        """
        print(f"Procesando archivo: {input_file}")
        
        # Leer datos
        df = pd.read_csv(input_file)
        
        # 1. Validar formato
        expected_cols = self.expected_joints * self.coords_per_joint
        if df.shape[1] != expected_cols:
            raise ValueError(f"Archivo debe tener {expected_cols} columnas, tiene {df.shape[1]}")
        
        # 2. Limpiar datos anómalos
        df = self._clean_anomalies(df)
        
        # 3. Submuestrear a 100 frames
        df = self._subsample_data(df)
        
        # 4. Imputar valores faltantes
        df = self._impute_missing_values(df)
        
        # 5. Calcular espina (centroide)
        df = self._calculate_spine(df)
        
        # 6. Guardar datos procesados
        output_file = input_file.replace('_raw.csv', '_processed.csv')
        df.to_csv(output_file, index=False)
        
        print(f"Datos procesados guardados en: {output_file}")
        return output_file
    
    def _clean_anomalies(self, df, threshold=84):
        """
        Detecta y limpia saltos bruscos entre frames consecutivos
        
        Args:
            df: DataFrame con los datos
            threshold: Umbral para detectar saltos bruscos
            
        Returns:
            DataFrame limpio
        """
        print("Limpiando anomalías...")
        
        # Convertir a numérico y manejar errores
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Detectar saltos bruscos
        rows_to_remove = set()
        for col in df.columns:
            diffs = df[col].diff()
            anomalous_rows = diffs[diffs.abs() > threshold].index
            rows_to_remove.update(anomalous_rows.tolist())
        
        if rows_to_remove:
            print(f"Eliminando {len(rows_to_remove)} filas con anomalías")
            df = df.drop(rows_to_remove).reset_index(drop=True)
        
        return df
    
    def _subsample_data(self, df):
        """
        Reduce los datos a exactamente 100 frames mediante submuestreo
        
        Args:
            df: DataFrame con los datos
            
        Returns:
            DataFrame con 100 frames
        """
        current_frames = len(df)
        print(f"Submuestreando de {current_frames} a {self.expected_frames} frames")
        
        if current_frames <= self.expected_frames:
            # Si tenemos menos frames, duplicar algunos
            while len(df) < self.expected_frames:
                df = pd.concat([df, df.tail(1)], ignore_index=True)
        else:
            # Si tenemos más frames, seleccionar uniformemente
            indices = np.linspace(0, current_frames - 1, self.expected_frames, dtype=int)
            df = df.iloc[indices].reset_index(drop=True)
        
        return df
    
    def _impute_missing_values(self, df):
        """
        Imputa valores faltantes usando K-Nearest Neighbors
        
        Args:
            df: DataFrame con posibles valores faltantes
            
        Returns:
            DataFrame con valores imputados
        """
        print("Imputando valores faltantes...")
        
        # Verificar si hay valores nulos o ceros
        if df.isnull().sum().sum() > 0 or (df == 0).sum().sum() > 0:
            # Reemplazar ceros con NaN para imputación
            df_temp = df.replace(0, np.nan)
            
            # Aplicar KNN imputation
            imputer = KNNImputer(n_neighbors=3)
            df_imputed = pd.DataFrame(
                imputer.fit_transform(df_temp),
                columns=df.columns
            )
            
            print("Valores faltantes imputados con KNN")
            return df_imputed
        
        return df
    
    def _calculate_spine(self, df):
        """
        Calcula la coordenada de la espina como centroide de hombros y caderas
        
        Args:
            df: DataFrame con coordenadas de joints
            
        Returns:
            DataFrame con columnas de espina agregadas
        """
        print("Calculando coordenadas de espina...")
        
        # Joints para calcular la espina (hombros y caderas)
        spine_joints = {
            'joint11': 'Hombro Izquierdo',
            'joint12': 'Hombro Derecho', 
            'joint23': 'Cadera Izquierda',
            'joint24': 'Cadera Derecha'
        }
        
        # Verificar que existan las columnas necesarias
        required_cols = []
        for joint in spine_joints.keys():
            for coord in ['_x', '_y', '_z']:
                required_cols.append(joint + coord)
        
        if not all(col in df.columns for col in required_cols):
            raise ValueError("Faltan columnas necesarias para calcular la espina")
        
        # Calcular centroide
        df['espina_x'] = (df['joint11_x'] + df['joint12_x'] + 
                         df['joint23_x'] + df['joint24_x']) / 4
        df['espina_y'] = (df['joint11_y'] + df['joint12_y'] + 
                         df['joint23_y'] + df['joint24_y']) / 4
        df['espina_z'] = (df['joint11_z'] + df['joint12_z'] + 
                         df['joint23_z'] + df['joint24_z']) / 4
        
        print("Espina calculada exitosamente")
        return df
