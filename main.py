"""
Sistema principal de reconocimiento de actividades humanas
Integra captura, preprocesamiento, extracción de características y clasificación
"""

import os
import sys
import time
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.capture import RealSenseCapture
from src.preprocessing import DataPreprocessor
from src.features import FeatureExtractor
from src.classification import ActivityClassifier
from src.legacy_tools import LegacyDataProcessor, SkeletonVisualizer

class ActivityRecognitionSystem:
    def __init__(self, 
                 model_path="models/activity_classifier.pkl",
                 temp_data_path="temp_data"):
        """
        Inicializa el sistema de reconocimiento de actividades
        
        Args:
            model_path: Ruta del modelo de clasificación
            temp_data_path: Carpeta temporal para datos de captura
        """
        print("🔧 Inicializando Sistema de Reconocimiento de Actividades...")
        
        self.model_path = model_path
        self.temp_data_path = temp_data_path
        
        # Crear directorios necesarios
        os.makedirs(temp_data_path, exist_ok=True)
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        try:
            # Inicializar componentes
            self.capture_system = RealSenseCapture(output_path=temp_data_path)
            self.preprocessor = DataPreprocessor()
            self.feature_extractor = FeatureExtractor()
            self.classifier = ActivityClassifier(model_path=model_path)
            self.legacy_processor = LegacyDataProcessor()
            self.visualizer = SkeletonVisualizer()
            
            print("✅ Sistema inicializado correctamente")
            
            # Verificar si hay modelo entrenado
            if self.classifier.is_trained():
                print(f"📊 Modelo cargado: {self.classifier.classes}")
            else:
                print("⚠️  No hay modelo entrenado. Usa 'entrenar' para entrenar un modelo.")
                
        except Exception as e:
            print(f"❌ Error al inicializar el sistema: {e}")
            raise
    
    def detect_activity(self):
        """
        Ejecuta el flujo completo de detección de actividad
        
        Returns:
            Tupla con (actividad_predicha, probabilidades)
        """
        print("\n🎯 INICIANDO DETECCIÓN DE ACTIVIDAD")
        print("=" * 50)
        
        try:
            # 1. Capturar actividad
            print("📹 Fase 1: Capturando actividad...")
            raw_file = self.capture_system.capture_activity("unknown_activity")
            if not raw_file:
                raise Exception("Error en la captura de datos")
            print(f"✅ Datos capturados en: {raw_file}")
            
            # 2. Preprocesar datos
            print("\n🔄 Fase 2: Preprocesando datos...")
            processed_file = self.preprocessor.process_raw_data(raw_file)
            print(f"✅ Datos procesados en: {processed_file}")
            
            # 3. Extraer características
            print("\n📊 Fase 3: Extrayendo características...")
            features = self.feature_extractor.extract_features(processed_file)
            print(f"✅ Extraídas {len(features)} características")
            
            # 4. Clasificar actividad
            print("\n🔍 Fase 4: Clasificando actividad...")
            if not self.classifier.is_trained():
                raise Exception("No hay modelo entrenado. Entrena primero un modelo.")
            
            predicted_activity, probabilities = self.classifier.predict_activity(features)
            
            # Mostrar resultados
            print("\n🎉 RESULTADOS:")
            print("=" * 30)
            print(f"🏷️  Actividad detectada: {predicted_activity}")
            print(f"🎯 Confianza: {max(probabilities.values()):.2%}")
            print("\n📈 Probabilidades por clase:")
            for activity, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
                print(f"   {activity}: {prob:.2%}")
            
            # Limpiar archivos temporales
            self._cleanup_temp_files([raw_file, processed_file])
            
            return predicted_activity, probabilities
            
        except Exception as e:
            print(f"❌ Error durante la detección: {e}")
            return None, None
    
    def train_model(self, dataset_path):
        """
        Entrena el modelo con un dataset existente
        
        Args:
            dataset_path: Ruta del archivo CSV con el dataset
        """
        print(f"\n🎓 ENTRENANDO MODELO")
        print("=" * 30)
        
        if not os.path.exists(dataset_path):
            print(f"❌ Dataset no encontrado: {dataset_path}")
            return False
        
        try:
            accuracy = self.classifier.train_model(dataset_path)
            print(f"✅ Modelo entrenado exitosamente con precisión: {accuracy:.2%}")
            return True
        except Exception as e:
            print(f"❌ Error durante el entrenamiento: {e}")
            return False
    
    def _cleanup_temp_files(self, files):
        """Limpia archivos temporales"""
        for file_path in files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"⚠️  No se pudo eliminar {file_path}: {e}")
    
    def process_legacy_data(self):
        """
        Menú para procesar datos legacy
        """
        print("\n� HERRAMIENTAS PARA DATOS LEGACY")
        print("=" * 35)
        print("1. Limpiar estructura de carpetas (dataElimination)")
        print("2. Eliminar columnas extra (eliminar_4tacolumna)")
        print("3. Convertir CSVs a dataset (reshapeCSVs)")
        print("4. Volver al menú principal")
        
        while True:
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "1":
                base_path = input("📁 Ruta base de las carpetas a limpiar: ").strip()
                self.legacy_processor.clean_capture_folders(base_path)
                break
                
            elif opcion == "2":
                base_path = input("📁 Ruta base de los archivos CSV: ").strip()
                self.legacy_processor.remove_extra_columns(base_path)
                break
                
            elif opcion == "3":
                input_path = input("📁 Ruta de archivos CSV individuales: ").strip()
                output_path = input("📁 Ruta de salida para datasets: ").strip()
                activity_prefix = input("🏷️  Prefijo para nombres de archivo: ").strip()
                self.legacy_processor.reshape_csvs_to_dataset(input_path, output_path, activity_prefix)
                break
                
            elif opcion == "4":
                break
                
            else:
                print("❓ Opción no válida. Intenta de nuevo.")
    
    def visualize_data(self):
        """
        Menú para visualización de datos
        """
        print("\n📊 HERRAMIENTAS DE VISUALIZACIÓN")
        print("=" * 32)
        print("1. Visualizar esqueleto 3D (un frame)")
        print("2. Crear animación de esqueleto")
        print("3. Volver al menú principal")
        
        while True:
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "1":
                csv_file = input("📄 Ruta del archivo CSV: ").strip()
                show_labels = input("🏷️  Mostrar nombres de joints? (s/n): ").strip().lower() == 's'
                self.visualizer.plot_skeleton_3d(csv_file, show_labels)
                break
                
            elif opcion == "2":
                csv_file = input("📄 Ruta del archivo CSV: ").strip()
                with_spine = input("🌟 Incluir espina? (s/n): ").strip().lower() == 's'
                self.visualizer.plot_skeleton_animation(csv_file, with_spine=with_spine)
                break
                
            elif opcion == "3":
                break
                
            else:
                print("❓ Opción no válida. Intenta de nuevo.")

    def get_system_status(self):
        """Muestra el estado del sistema"""
        print("\n📊 ESTADO DEL SISTEMA")
        print("=" * 25)
        print(f"🎥 Cámaras conectadas: {len(self.capture_system.devices)}")
        print(f"🤖 Modelo entrenado: {'✅ Sí' if self.classifier.is_trained() else '❌ No'}")
        if self.classifier.is_trained():
            print(f"🏷️  Clases disponibles: {', '.join(self.classifier.classes)}")
        print(f"🔧 Herramientas legacy: ✅ Disponibles")
        print(f"📊 Visualización: ✅ Disponible")

def main():
    """Función principal del sistema"""
    print("🚀 SISTEMA DE RECONOCIMIENTO DE ACTIVIDADES HUMANAS")
    print("=" * 55)
    
    # Inicializar sistema
    try:
        system = ActivityRecognitionSystem()
    except Exception as e:
        print(f"❌ Error al inicializar el sistema: {e}")
        return
    
    # Menú interactivo
    while True:
        print("\n🎮 MENÚ DE OPCIONES:")
        print("1. 'detectar' - Detectar actividad")
        print("2. 'entrenar' - Entrenar modelo")
        print("3. 'estado' - Ver estado del sistema")
        print("4. 'legacy' - Procesar datos legacy")
        print("5. 'visualizar' - Herramientas de visualización")
        print("6. 'salir' - Salir del programa")
        
        comando = input("\n👉 Ingresa tu comando: ").strip().lower()
        
        if comando == "detectar":
            result = system.detect_activity()
            if result[0] is None:
                print("⚠️  La detección falló. Inténtalo de nuevo.")
                
        elif comando == "entrenar":
            dataset_path = input("📁 Ruta del dataset (ej: Proyecto final/dataset.csv): ").strip()
            system.train_model(dataset_path)
            
        elif comando == "estado":
            system.get_system_status()
            
        elif comando == "legacy":
            system.process_legacy_data()
            
        elif comando == "visualizar":
            system.visualize_data()
            
        elif comando == "salir":
            print("👋 ¡Hasta luego!")
            break
            
        else:
            print("❓ Comando no reconocido. Intenta de nuevo.")

if __name__ == "__main__":
    main()
