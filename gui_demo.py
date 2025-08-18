"""
Versión de demostración de la GUI que simula la cámara para pruebas
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import threading
import sys
import time
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageTk

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent / 'src'))

# Mock de los módulos RealSense para demo
class MockRealSenseCapture:
    def __init__(self, output_path="temp_data"):
        self.devices = ["Demo Camera"]  # Simular una cámara
        self.pipelines = [self]  # Simular pipeline
        self.CAPTURE_SECONDS = 10
        self.imgs2take = 300
        
    def capture_activity(self, activity_name):
        # Simular captura
        time.sleep(2)
        return "mock_capture.csv"
    
    def stop_capture(self):
        pass

class MockPreprocessor:
    def process_raw_data(self, raw_file):
        time.sleep(1)
        return "mock_processed.csv"

class MockFeatureExtractor:
    def extract_features(self, processed_file):
        time.sleep(1)
        return [0.1] * 64  # Simular 64 características

class MockClassifier:
    def __init__(self, model_path="models/activity_classifier.pkl"):
        self.model_path = model_path
        self.classes = ["Caminar", "Correr", "Saltar", "Sentarse"]
        
    def is_trained(self):
        return True
    
    def predict_activity(self, features):
        import random
        activity = random.choice(self.classes)
        probabilities = {
            "Caminar": 0.7 if activity == "Caminar" else random.uniform(0.05, 0.25),
            "Correr": 0.8 if activity == "Correr" else random.uniform(0.05, 0.25),
            "Saltar": 0.75 if activity == "Saltar" else random.uniform(0.05, 0.25),
            "Sentarse": 0.85 if activity == "Sentarse" else random.uniform(0.05, 0.25)
        }
        return activity, probabilities
    
    def train_model(self, dataset_path):
        time.sleep(3)  # Simular entrenamiento
        return 0.92  # 92% de precisión

class MockLegacyProcessor:
    def clean_capture_folders(self, base_path):
        time.sleep(1)
    
    def remove_extra_columns(self, base_path):
        time.sleep(1)
    
    def reshape_csvs_to_dataset(self, input_path, output_path, activity_prefix):
        time.sleep(2)

class MockVisualizer:
    def plot_skeleton_3d(self, csv_file, show_labels):
        time.sleep(1)
        print(f"Generando visualización 3D de {csv_file}")
    
    def plot_skeleton_animation(self, csv_file, with_spine=True):
        time.sleep(2)
        print(f"Generando animación de {csv_file}")

# Importar la GUI y reemplazar las clases
from gui_main import ActivityRecognitionGUI

# Monkey patch para demo
original_init_system = ActivityRecognitionGUI.init_system_async

def demo_init_system(self):
    """Versión de demostración que no requiere hardware real"""
    def init_worker():
        try:
            self.log_message("🔧 Inicializando sistema de demostración...")
            
            self.log_message("📹 Configurando cámara simulada...")
            self.capture_system = MockRealSenseCapture(output_path="temp_data")
            
            self.log_message("🔄 Iniciando preprocesador...")
            self.preprocessor = MockPreprocessor()
            
            self.log_message("📊 Configurando extractor de características...")
            self.feature_extractor = MockFeatureExtractor()
            
            self.log_message("🤖 Cargando clasificador...")
            self.classifier = MockClassifier(model_path="models/activity_classifier.pkl")
            
            self.log_message("🛠️ Preparando herramientas legacy...")
            self.legacy_processor = MockLegacyProcessor()
            self.visualizer = MockVisualizer()
            
            self.system_initialized = True
            self.update_status()
            
            self.log_message("✅ Sistema de demostración inicializado correctamente")
            self.log_message("ℹ️ Esta es una versión de demostración sin cámara real")
            
        except Exception as e:
            self.log_message(f"❌ Error al inicializar: {str(e)}")
            messagebox.showerror("Error de Inicialización", 
                               f"No se pudo inicializar el sistema:\n{str(e)}")
    
    threading.Thread(target=init_worker, daemon=True).start()

# Reemplazar método
ActivityRecognitionGUI.init_system_async = demo_init_system

# También necesitamos simular el video feed
def demo_video_feed_worker(self):
    """Worker simulado para video feed - Usa la misma resolución que test_camera.py"""
    try:
        while self.video_feed_active:
            # Crear una imagen de demostración con resolución exacta 640x480
            demo_image = np.zeros((480, 640, 3), dtype=np.uint8)
            demo_image[:] = (50, 50, 100)  # Fondo azul oscuro
            
            # Agregar texto de demostración
            cv2.putText(demo_image, "DEMO MODE - 640x480", (160, 200), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
            cv2.putText(demo_image, "Misma resolucion que test_camera.py", (120, 250), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
            
            # Simular detección de esqueleto con información igual a test_camera.py
            cv2.putText(demo_image, f"Modo: Color", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(demo_image, f"Poses: ON", 
                       (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(demo_image, f"Joints detectados: 33/33", 
                       (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(demo_image, f"Tasa detección: 95.5%", 
                       (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Simular joints con círculos (como en test_camera.py)
            import random
            joint_positions = [
                (320, 150), (290, 180), (350, 180),  # Cabeza y hombros
                (260, 220), (380, 220),               # Codos
                (240, 280), (400, 280),               # Muñecas
                (300, 300), (340, 300),               # Caderas
                (290, 380), (350, 380),               # Rodillas
                (285, 450), (355, 450)                # Tobillos
            ]
            
            for i, (x, y) in enumerate(joint_positions):
                # Dibujar círculos de joints
                cv2.circle(demo_image, (x, y), 3, (0, 255, 0), -1)
                cv2.circle(demo_image, (x, y), 6, (0, 255, 0), 2)
            
            # Dibujar líneas de conexión (simulando esqueleto)
            connections = [
                (0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6),  # Torso superior
                (7, 8), (7, 9), (8, 10), (9, 11), (10, 12)       # Torso inferior
            ]
            
            for start_idx, end_idx in connections:
                if start_idx < len(joint_positions) and end_idx < len(joint_positions):
                    start_pos = joint_positions[start_idx]
                    end_pos = joint_positions[end_idx]
                    cv2.line(demo_image, start_pos, end_pos, (0, 0, 255), 2)
            
            # Convertir BGR a RGB
            rgb_image = cv2.cvtColor(demo_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            photo = ImageTk.PhotoImage(pil_image)
            
            # Actualizar canvas con resolución exacta (no redimensionar)
            self.root.after(0, self.update_video_canvas, photo, 640, 480)
            
            time.sleep(0.1)  # 10 FPS para demo
            
    except Exception as e:
        if self.video_feed_active:
            self.log_message(f"⚠️ Error en video demo: {str(e)}")

# Reemplazar método de video
ActivityRecognitionGUI.video_feed_worker = demo_video_feed_worker

def main():
    """Función principal para demo"""
    print("🎮 MODO DEMOSTRACIÓN - Sistema de Reconocimiento de Actividades")
    print("=" * 60)
    print("Esta versión simula el comportamiento sin requerir cámara RealSense")
    print("=" * 60)
    
    root = tk.Tk()
    app = ActivityRecognitionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
