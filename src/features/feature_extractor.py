"""
Módulo para extraer características de distancias y velocidades
"""

import pandas as pd
import numpy as np
import os

class FeatureExtractor:
    def __init__(self):
        """Inicializa el extractor de características"""
        # Joints específicos para calcular distancias (respecto a la espina)
        self.target_joints = [
            'joint13',  # Codo izquierdo
            'joint14',  # Codo derecho
            'joint15',  # Muñeca izquierda
            'joint16',  # Muñeca derecha
            'joint25',  # Rodilla izquierda
            'joint26',  # Rodilla derecha
            'joint29',  # Talón izquierdo
            'joint30'   # Talón derecho
        ]
        
        # Intervalo de tiempo entre frames (asumiendo 30 FPS)
        self.time_interval = 1.0 / 30.0  # 0.033 segundos
        
    def extract_features(self, processed_file):
        """
        Extrae todas las características de un archivo procesado
        
        Args:
            processed_file: Ruta del archivo CSV procesado
            
        Returns:
            Array con las 64 características extraídas
        """
        print(f"Extrayendo características de: {processed_file}")
        
        # Leer datos procesados
        df = pd.read_csv(processed_file)
        
        # Calcular distancias
        distances_df = self._calculate_distances(df)
        
        # Calcular velocidades
        velocities_df = self._calculate_velocities(distances_df)
        
        # Extraer características estadísticas
        features = self._extract_statistical_features(distances_df, velocities_df)
        
        print(f"Extraídas {len(features)} características")
        return features
    
    def _calculate_distances(self, df):
        """
        Calcula distancias euclidianas de joints específicos hacia la espina
        
        Args:
            df: DataFrame con coordenadas de joints y espina
            
        Returns:
            DataFrame con distancias calculadas
        """
        print("Calculando distancias...")
        
        distances = []
        
        for _, row in df.iterrows():
            espina_x, espina_y, espina_z = row['espina_x'], row['espina_y'], row['espina_z']
            
            frame_distances = []
            for joint in self.target_joints:
                joint_x = row[f'{joint}_x']
                joint_y = row[f'{joint}_y'] 
                joint_z = row[f'{joint}_z']
                
                # Calcular distancia euclidiana
                distance = np.sqrt(
                    (joint_x - espina_x)**2 + 
                    (joint_y - espina_y)**2 + 
                    (joint_z - espina_z)**2
                )
                frame_distances.append(distance)
            
            distances.append(frame_distances)
        
        # Crear DataFrame con distancias
        columns = [f'Distancia_{i+1}' for i in range(len(self.target_joints))]
        distances_df = pd.DataFrame(distances, columns=columns)
        
        return distances_df
    
    def _calculate_velocities(self, distances_df):
        """
        Calcula velocidades como cambio de distancia entre frames consecutivos
        
        Args:
            distances_df: DataFrame con distancias
            
        Returns:
            DataFrame con velocidades
        """
        print("Calculando velocidades...")
        
        # Calcular diferencias entre frames consecutivos y dividir por tiempo
        velocities_df = distances_df.diff().iloc[1:] / self.time_interval
        
        # Renombrar columnas
        velocities_df.columns = [f'Velocidad_{i+1}' for i in range(len(self.target_joints))]
        
        return velocities_df
    
    def _extract_statistical_features(self, distances_df, velocities_df):
        """
        Extrae características estadísticas de distancias y velocidades
        
        Args:
            distances_df: DataFrame con distancias
            velocities_df: DataFrame con velocidades
            
        Returns:
            Lista con 64 características (8 distancias × 4 métricas + 8 velocidades × 4 métricas)
        """
        print("Extrayendo características estadísticas...")
        
        features = []
        
        # Características de distancias
        for column in distances_df.columns:
            features.extend([
                distances_df[column].mean(),    # Media
                distances_df[column].var(),     # Varianza
                distances_df[column].max(),     # Máximo
                distances_df[column].min()      # Mínimo
            ])
        
        # Características de velocidades
        for column in velocities_df.columns:
            features.extend([
                velocities_df[column].mean(),   # Media
                velocities_df[column].var(),    # Varianza
                velocities_df[column].max(),    # Máximo
                velocities_df[column].min()     # Mínimo
            ])
        
        return features
    
    def create_feature_names(self):
        """
        Crea los nombres de las características
        
        Returns:
            Lista con los nombres de las 64 características
        """
        feature_names = []
        
        # Nombres para distancias
        for i in range(len(self.target_joints)):
            for metric in ['media', 'varianza', 'maximo', 'minimo']:
                feature_names.append(f'Distancia_{metric}_{i+1}')
        
        # Nombres para velocidades
        for i in range(len(self.target_joints)):
            for metric in ['media', 'varianza', 'maximo', 'minimo']:
                feature_names.append(f'Velocidad_{metric}_{i+1}')
        
        return feature_names
