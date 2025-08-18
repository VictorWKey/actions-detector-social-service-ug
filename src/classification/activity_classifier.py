"""
Módulo de clasificación de actividades
"""

import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

class ActivityClassifier:
    def __init__(self, model_path="models/activity_classifier.pkl"):
        """
        Inicializa el clasificador de actividades
        
        Args:
            model_path: Ruta donde guardar/cargar el modelo entrenado
        """
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.classes = None
        
        # Crear directorio de modelos si no existe
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Intentar cargar modelo existente
        self._load_model()
    
    def train_model(self, dataset_path):
        """
        Entrena el modelo usando un dataset existente
        
        Args:
            dataset_path: Ruta del archivo CSV con el dataset
        """
        print(f"Entrenando modelo con dataset: {dataset_path}")
        
        # Cargar dataset
        df = pd.read_csv(dataset_path)
        
        # Separar características y etiquetas
        X = df.iloc[:, :-1].values  # Todas las columnas excepto la última
        y = df.iloc[:, -1].values   # Última columna (etiquetas)
        
        # Guardar clases únicas
        self.classes = np.unique(y)
        print(f"Clases detectadas: {self.classes}")
        
        # Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Normalizar características
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Entrenar modelo Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluar modelo
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Precisión del modelo: {accuracy:.3f}")
        print("\nReporte de clasificación:")
        print(classification_report(y_test, y_pred))
        
        # Guardar modelo entrenado
        self._save_model()
        
        return accuracy
    
    def predict_activity(self, features):
        """
        Predice la actividad basada en las características extraídas
        
        Args:
            features: Array con 64 características
            
        Returns:
            Tupla con (actividad_predicha, probabilidades)
        """
        if self.model is None:
            raise ValueError("Modelo no entrenado. Entrena primero o carga un modelo.")
        
        # Convertir a array 2D para el scaler
        features_array = np.array(features).reshape(1, -1)
        
        # Normalizar características
        features_scaled = self.scaler.transform(features_array)
        
        # Predecir
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Crear diccionario de probabilidades por clase
        prob_dict = dict(zip(self.classes, probabilities))
        
        return prediction, prob_dict
    
    def _save_model(self):
        """Guarda el modelo entrenado, scaler y clases"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'classes': self.classes
        }
        
        joblib.dump(model_data, self.model_path)
        print(f"Modelo guardado en: {self.model_path}")
    
    def _load_model(self):
        """Carga un modelo previamente entrenado"""
        if os.path.exists(self.model_path):
            try:
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.classes = model_data['classes']
                print(f"Modelo cargado desde: {self.model_path}")
                print(f"Clases disponibles: {self.classes}")
            except Exception as e:
                print(f"Error al cargar modelo: {e}")
                self.model = None
    
    def is_trained(self):
        """Verifica si el modelo está entrenado"""
        return self.model is not None
    
    def get_feature_importance(self):
        """
        Obtiene la importancia de las características
        
        Returns:
            Array con la importancia de cada característica
        """
        if self.model is None:
            raise ValueError("Modelo no entrenado.")
        
        return self.model.feature_importances_
