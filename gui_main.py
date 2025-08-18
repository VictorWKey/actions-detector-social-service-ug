"""
Interfaz gráfica moderna para el Sistema de Reconocimiento de Actividades Humanas
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

from src.capture import RealSenseCapture
from src.preprocessing import DataPreprocessor
from src.features import FeatureExtractor
from src.classification import ActivityClassifier
from src.legacy_tools import LegacyDataProcessor, SkeletonVisualizer
from src.capture.gui_pose_detector import GUIPoseDetector

class ActivityRecognitionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Sistema de Reconocimiento de Actividades Humanas")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.system_initialized = False
        self.is_detecting = False
        self.is_training = False
        self.camera_running = False
        self.video_feed_active = False
        self.countdown_active = False
        
        # Detector específico para GUI (igual a test_camera.py)
        self.gui_pose_detector = None
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Inicializar sistema en hilo separado
        self.init_system_async()
        
        # Configurar cierre de aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones principales
        style.configure('Main.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       foreground='white',
                       background='#0078d4',
                       borderwidth=0,
                       relief='flat',
                       padding=(20, 10))
        
        style.map('Main.TButton',
                 background=[('active', '#106ebe'),
                           ('pressed', '#005a9e')])
        
        # Estilo para botones secundarios
        style.configure('Secondary.TButton',
                       font=('Segoe UI', 10),
                       foreground='#323130',
                       background='#f3f2f1',
                       borderwidth=1,
                       relief='solid',
                       padding=(15, 8))
        
        style.map('Secondary.TButton',
                 background=[('active', '#edebe9'),
                           ('pressed', '#e1dfdd')])
        
        # Estilo para frames
        style.configure('Card.TFrame',
                       background='#ffffff',
                       relief='solid',
                       borderwidth=1)
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Card.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(20, 30))
        
        title_label = tk.Label(title_frame,
                              text="🚀 Sistema de Reconocimiento de Actividades",
                              font=('Segoe UI', 18, 'bold'),
                              fg='#323130',
                              bg='#ffffff')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Detecta y clasifica actividades humanas en tiempo real",
                                 font=('Segoe UI', 11),
                                 fg='#605e5c',
                                 bg='#ffffff')
        subtitle_label.pack(pady=(5, 0))
        
        # Frame para el estado del sistema
        self.status_frame = ttk.Frame(main_frame, style='Card.TFrame')
        self.status_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        self.create_status_panel()
        
        # Notebook para organizar funcionalidades
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Pestaña principal - Detección
        self.detection_frame = ttk.Frame(notebook)
        notebook.add(self.detection_frame, text="🎯 Detección de Actividades")
        self.create_detection_panel()
        
        # Pestaña de entrenamiento
        self.training_frame = ttk.Frame(notebook)
        notebook.add(self.training_frame, text="🎓 Entrenamiento")
        self.create_training_panel()
        
        # Pestaña de herramientas
        self.tools_frame = ttk.Frame(notebook)
        notebook.add(self.tools_frame, text="🛠️ Herramientas")
        self.create_tools_panel()
        
        # Pestaña de visualización
        self.visualization_frame = ttk.Frame(notebook)
        notebook.add(self.visualization_frame, text="📊 Visualización")
        self.create_visualization_panel()
        
        # Console de salida
        self.create_console()
    
    def create_status_panel(self):
        """Crea el panel de estado del sistema"""
        status_label = tk.Label(self.status_frame,
                               text="📊 Estado del Sistema",
                               font=('Segoe UI', 12, 'bold'),
                               fg='#323130',
                               bg='#ffffff')
        status_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        # Grid para indicadores
        indicators_frame = ttk.Frame(self.status_frame)
        indicators_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        # Indicador de inicialización
        self.init_status = tk.Label(indicators_frame,
                                   text="🔄 Inicializando sistema...",
                                   font=('Segoe UI', 10),
                                   fg='#d13438',
                                   bg='#ffffff')
        self.init_status.grid(row=0, column=0, sticky='w', pady=2)
        
        # Indicador de cámaras
        self.camera_status = tk.Label(indicators_frame,
                                     text="📷 Cámaras: Verificando...",
                                     font=('Segoe UI', 10),
                                     fg='#d13438',
                                     bg='#ffffff')
        self.camera_status.grid(row=0, column=1, sticky='w', padx=(20, 0), pady=2)
        
        # Indicador de modelo
        self.model_status = tk.Label(indicators_frame,
                                    text="🤖 Modelo: No entrenado",
                                    font=('Segoe UI', 10),
                                    fg='#d13438',
                                    bg='#ffffff')
        self.model_status.grid(row=1, column=0, sticky='w', pady=2)
        
        # Indicador de clases
        self.classes_status = tk.Label(indicators_frame,
                                      text="🏷️ Clases: --",
                                      font=('Segoe UI', 10),
                                      fg='#605e5c',
                                      bg='#ffffff')
        self.classes_status.grid(row=1, column=1, sticky='w', padx=(20, 0), pady=2)
    
    def create_detection_panel(self):
        """Crea el panel de detección de actividades"""
        # Título
        title = tk.Label(self.detection_frame,
                        text="🎯 Detectar Actividad en Tiempo Real",
                        font=('Segoe UI', 14, 'bold'),
                        fg='#323130')
        title.pack(pady=(20, 10))
        
        # Frame principal para video y controles
        main_detection_frame = ttk.Frame(self.detection_frame)
        main_detection_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Frame izquierdo para video
        video_frame = ttk.LabelFrame(main_detection_frame, text="📹 Vista en Vivo de la Cámara")
        video_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Canvas para mostrar el video
        self.video_canvas = tk.Canvas(video_frame, 
                                     width=640, 
                                     height=480, 
                                     bg='#2b2b2b')
        self.video_canvas.pack(padx=10, pady=10)
        
        # Mostrar placeholder inicial
        self.show_camera_placeholder()
        
        # Label para mostrar estado del video
        self.video_status = tk.Label(video_frame,
                                    text="📷 Cámara desconectada",
                                    font=('Segoe UI', 10),
                                    fg='#d13438')
        self.video_status.pack(pady=(0, 10))
        
        # Controles de video
        video_controls = ttk.Frame(video_frame)
        video_controls.pack(pady=(0, 10))
        
        self.start_camera_btn = ttk.Button(video_controls,
                                          text="🎥 Iniciar Cámara",
                                          command=self.toggle_camera)
        self.start_camera_btn.pack(side='left', padx=5)
        
        # Frame derecho para controles y resultados
        controls_frame = ttk.Frame(main_detection_frame)
        controls_frame.pack(side='right', fill='y', padx=(10, 0))
        
        # Instrucciones
        instructions_frame = ttk.LabelFrame(controls_frame, text="📋 Instrucciones")
        instructions_frame.pack(fill='x', pady=(0, 10))
        
        instructions = tk.Label(instructions_frame,
                               text="1. Inicia la cámara para ver el esqueleto\n"
                                    "2. Posiciónate frente a la cámara\n"
                                    "3. Presiona 'Detectar' (tendrás 3 segundos)\n"
                                    "4. Realiza la actividad por 10 segundos",
                               font=('Segoe UI', 9),
                               fg='#605e5c',
                               justify='left')
        instructions.pack(padx=10, pady=10)
        
        # Botón principal de detección
        self.detect_button = ttk.Button(controls_frame,
                                       text="🚀 INICIAR DETECCIÓN",
                                       style='Main.TButton',
                                       command=self.start_detection)
        self.detect_button.pack(pady=10, fill='x')
        
        # Label para countdown
        self.countdown_label = tk.Label(controls_frame,
                                       text="",
                                       font=('Segoe UI', 24, 'bold'),
                                       fg='#d13438')
        self.countdown_label.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(controls_frame,
                                          variable=self.progress_var,
                                          maximum=100,
                                          length=300)
        self.progress_bar.pack(pady=10, fill='x')
        
        # Área de resultados
        results_frame = ttk.LabelFrame(controls_frame, text="📈 Resultados de Detección")
        results_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     height=12,
                                                     width=40,
                                                     font=('Consolas', 9),
                                                     bg='#f8f8f8')
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_training_panel(self):
        """Crea el panel de entrenamiento"""
        # Título
        title = tk.Label(self.training_frame,
                        text="🎓 Entrenar Modelo de Clasificación",
                        font=('Segoe UI', 14, 'bold'),
                        fg='#323130')
        title.pack(pady=(20, 10))
        
        # Frame para selección de dataset
        dataset_frame = ttk.LabelFrame(self.training_frame, text="📁 Seleccionar Dataset")
        dataset_frame.pack(fill='x', padx=20, pady=20)
        
        self.dataset_path_var = tk.StringVar()
        dataset_entry = ttk.Entry(dataset_frame,
                                 textvariable=self.dataset_path_var,
                                 font=('Segoe UI', 10),
                                 width=50)
        dataset_entry.pack(side='left', padx=10, pady=10, fill='x', expand=True)
        
        browse_button = ttk.Button(dataset_frame,
                                  text="📂 Buscar",
                                  command=self.browse_dataset)
        browse_button.pack(side='right', padx=10, pady=10)
        
        # Botón de entrenamiento
        self.train_button = ttk.Button(self.training_frame,
                                      text="🚀 ENTRENAR MODELO",
                                      style='Main.TButton',
                                      command=self.start_training)
        self.train_button.pack(pady=20)
        
        # Progress bar para entrenamiento
        self.train_progress_var = tk.DoubleVar()
        self.train_progress_bar = ttk.Progressbar(self.training_frame,
                                                variable=self.train_progress_var,
                                                maximum=100,
                                                length=400)
        self.train_progress_bar.pack(pady=10)
        
        # Área de resultados de entrenamiento
        train_results_frame = ttk.LabelFrame(self.training_frame, text="📊 Resultados de Entrenamiento")
        train_results_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.train_results_text = scrolledtext.ScrolledText(train_results_frame,
                                                           height=10,
                                                           font=('Consolas', 10),
                                                           bg='#f8f8f8')
        self.train_results_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_tools_panel(self):
        """Crea el panel de herramientas legacy"""
        # Título
        title = tk.Label(self.tools_frame,
                        text="🛠️ Herramientas para Datos Legacy",
                        font=('Segoe UI', 14, 'bold'),
                        fg='#323130')
        title.pack(pady=(20, 10))
        
        # Grid de botones de herramientas
        tools_grid = ttk.Frame(self.tools_frame)
        tools_grid.pack(expand=True, pady=20)
        
        # Herramientas de procesamiento
        ttk.Button(tools_grid,
                  text="🧹 Limpiar Estructura de Carpetas",
                  style='Secondary.TButton',
                  command=self.clean_folders).grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        ttk.Button(tools_grid,
                  text="✂️ Eliminar Columnas Extra",
                  style='Secondary.TButton',
                  command=self.remove_columns).grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        ttk.Button(tools_grid,
                  text="🔄 Convertir CSVs a Dataset",
                  style='Secondary.TButton',
                  command=self.reshape_csvs).grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        
        # Configurar columnas para que se expandan uniformemente
        tools_grid.columnconfigure(0, weight=1)
        tools_grid.columnconfigure(1, weight=1)
    
    def create_visualization_panel(self):
        """Crea el panel de visualización"""
        # Título
        title = tk.Label(self.visualization_frame,
                        text="📊 Herramientas de Visualización",
                        font=('Segoe UI', 14, 'bold'),
                        fg='#323130')
        title.pack(pady=(20, 10))
        
        # Grid de botones de visualización
        viz_grid = ttk.Frame(self.visualization_frame)
        viz_grid.pack(expand=True, pady=20)
        
        ttk.Button(viz_grid,
                  text="🦴 Visualizar Esqueleto 3D",
                  style='Secondary.TButton',
                  command=self.visualize_skeleton_3d).grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        ttk.Button(viz_grid,
                  text="🎬 Crear Animación de Esqueleto",
                  style='Secondary.TButton',
                  command=self.create_skeleton_animation).grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        # Configurar columnas
        viz_grid.columnconfigure(0, weight=1)
        viz_grid.columnconfigure(1, weight=1)
    
    def create_console(self):
        """Crea la consola de salida"""
        console_frame = ttk.LabelFrame(self.root, text="📟 Console de Sistema")
        console_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.console = scrolledtext.ScrolledText(console_frame,
                                               height=8,
                                               font=('Consolas', 9),
                                               bg='#1e1e1e',
                                               fg='#d4d4d4',
                                               insertbackground='white')
        self.console.pack(fill='both', padx=10, pady=10)
        
        # Agregar mensaje inicial
        self.log_message("🚀 Sistema de Reconocimiento de Actividades iniciado")
        self.log_message("📋 Inicializando componentes...")
    
    def log_message(self, message):
        """Agrega un mensaje a la consola"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.console.insert(tk.END, formatted_message)
        self.console.see(tk.END)
        self.root.update_idletasks()
    
    def init_system_async(self):
        """Inicializa el sistema en un hilo separado"""
        def init_worker():
            try:
                self.log_message("🔧 Inicializando componentes del sistema...")
                
                # Inicializar detector de poses para GUI primero
                self.log_message("🤖 Configurando detector de poses para GUI...")
                self.gui_pose_detector = GUIPoseDetector()
                
                # Inicializar componentes uno por uno
                self.log_message("📹 Configurando cámaras RealSense...")
                self.capture_system = RealSenseCapture(output_path="temp_data")
                
                self.log_message("🔄 Iniciando preprocesador...")
                self.preprocessor = DataPreprocessor()
                
                self.log_message("📊 Configurando extractor de características...")
                self.feature_extractor = FeatureExtractor()
                
                self.log_message("🤖 Cargando clasificador...")
                self.classifier = ActivityClassifier(model_path="models/activity_classifier.pkl")
                
                self.log_message("🛠️ Preparando herramientas legacy...")
                self.legacy_processor = LegacyDataProcessor()
                self.visualizer = SkeletonVisualizer()
                
                # Actualizar estado
                self.system_initialized = True
                self.update_status()
                
                self.log_message("✅ Sistema inicializado correctamente")
                
                # Iniciar automáticamente la cámara
                self.root.after(1000, self.auto_start_camera)  # Esperar 1 segundo y luego iniciar
                
            except Exception as e:
                self.log_message(f"❌ Error al inicializar: {str(e)}")
                messagebox.showerror("Error de Inicialización", 
                                   f"No se pudo inicializar el sistema:\n{str(e)}")
        
        threading.Thread(target=init_worker, daemon=True).start()
    
    def update_status(self):
        """Actualiza los indicadores de estado"""
        if self.system_initialized:
            self.init_status.config(text="✅ Sistema inicializado", fg='#107c10')
            
            # Estado de cámaras
            if hasattr(self, 'capture_system'):
                cam_count = len(self.capture_system.devices)
                if cam_count > 0:
                    self.camera_status.config(text=f"📷 Cámaras: {cam_count} conectadas", fg='#107c10')
                else:
                    self.camera_status.config(text="📷 Cámaras: No conectadas", fg='#d13438')
            
            # Estado del modelo
            if hasattr(self, 'classifier') and self.classifier.is_trained():
                self.model_status.config(text="🤖 Modelo: Entrenado", fg='#107c10')
                if self.classifier.classes is not None:
                    classes_text = ", ".join(self.classifier.classes)
                    self.classes_status.config(text=f"🏷️ Clases: {classes_text}")
            else:
                self.model_status.config(text="🤖 Modelo: No entrenado", fg='#d13438')
    
    def toggle_camera(self):
        """Inicia o detiene la cámara en vivo"""
        if not self.system_initialized:
            messagebox.showwarning("Sistema no listo", 
                                 "El sistema aún se está inicializando. Espera un momento.")
            return
        
        if not self.camera_running:
            self.start_camera_feed()
        else:
            self.stop_camera_feed()
    
    def start_camera_feed(self):
        """Inicia la transmisión en vivo de la cámara"""
        try:
            self.camera_running = True
            self.video_feed_active = True
            self.start_camera_btn.config(text="🛑 Detener Cámara")
            self.video_status.config(text="📹 Cámara activa - Detectando esqueleto", fg='#107c10')
            self.log_message("📹 Iniciando transmisión en vivo de la cámara...")
            
            # Iniciar hilo para el video feed
            threading.Thread(target=self.video_feed_worker, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"❌ Error iniciando cámara: {str(e)}")
            messagebox.showerror("Error de Cámara", f"No se pudo iniciar la cámara:\n{str(e)}")
            self.camera_running = False
    
    def stop_camera_feed(self):
        """Detiene la transmisión en vivo de la cámara"""
        self.camera_running = False
        self.video_feed_active = False
        self.start_camera_btn.config(text="🎥 Iniciar Cámara")
        self.video_status.config(text="📷 Cámara desconectada", fg='#d13438')
        self.video_canvas.delete("all")
        self.video_canvas.create_text(320, 240, 
                                     text="📷 Cámara desconectada",
                                     fill='white',
                                     font=('Segoe UI', 14))
        self.log_message("📷 Transmisión de cámara detenida")
    
    def auto_start_camera(self):
        """Inicia automáticamente la cámara cuando el sistema está listo"""
        try:
            if hasattr(self, 'capture_system') and len(self.capture_system.devices) > 0:
                self.log_message("🎥 Iniciando cámara automáticamente...")
                self.video_status.config(text="📹 Iniciando cámara...", fg='#d13438')
                self.start_camera_feed()
            else:
                self.log_message("⚠️ No se pudo iniciar la cámara automáticamente - No hay dispositivos")
                self.video_status.config(text="❌ No hay cámaras conectadas", fg='#d13438')
                self.video_canvas.delete("all")
                self.video_canvas.create_text(320, 200, 
                                             text="❌ No se detectaron cámaras",
                                             fill='#ff6b6b',
                                             font=('Segoe UI', 16, 'bold'))
                self.video_canvas.create_text(320, 240, 
                                             text="Verifica que la cámara RealSense esté conectada",
                                             fill='#cccccc',
                                             font=('Segoe UI', 10))
        except Exception as e:
            self.log_message(f"⚠️ Error al iniciar cámara automáticamente: {str(e)}")
            self.video_status.config(text="❌ Error en cámara", fg='#d13438')
    
    def video_feed_worker(self):
        """Worker thread para la transmisión de video en vivo - Idéntico a test_camera.py"""
        try:
            # Usar la primera cámara/pipeline
            if not hasattr(self, 'capture_system') or len(self.capture_system.pipelines) == 0:
                self.log_message("❌ No hay cámaras disponibles")
                self.stop_camera_feed()
                return
            
            pipeline = self.capture_system.pipelines[0]
            frame_count = 0
            joints_detected = 0
            
            while self.video_feed_active:
                try:
                    # EXACTAMENTE igual a test_camera.py
                    frames = pipeline.wait_for_frames()
                    
                    # Obtener frame de color y profundidad
                    color_frame = frames.get_color_frame()
                    depth_frame = frames.get_depth_frame()
                    
                    if not color_frame or not depth_frame:
                        continue
                    
                    frame_count += 1
                    
                    # Convertir a arrays de numpy
                    color_image = np.asanyarray(color_frame.get_data())
                    depth_image = np.asanyarray(depth_frame.get_data())
                    
                    # Detectar poses usando el detector GUI (igual a test_camera.py)
                    pose_results = None
                    joints_3d = []
                    if self.gui_pose_detector:
                        pose_results = self.gui_pose_detector.detect_pose(color_image)
                        joints_3d = self.gui_pose_detector.get_joint_coordinates(pose_results, depth_frame)
                        if joints_3d:
                            joints_detected += 1

                    # Preparar imagen para mostrar (igual a test_camera.py)
                    display_image = color_image.copy()

                    # Dibujar poses si están habilitadas (igual a test_camera.py)
                    if pose_results and self.gui_pose_detector:
                        self.gui_pose_detector.draw_landmarks(display_image, pose_results, False)

                    # Agregar información de estado (igual a test_camera.py)
                    cv2.putText(display_image, f"Modo: Color", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(display_image, f"Poses: ON", 
                               (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(display_image, f"Joints detectados: {len(joints_3d)}/33", 
                               (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    if frame_count > 0:
                        detection_rate = (joints_detected / frame_count) * 100
                        cv2.putText(display_image, f"Tasa detección: {detection_rate:.1f}%", 
                                   (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    # Mostrar joints importantes detectados (igual a test_camera.py)
                    if joints_3d:
                        important_joints = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 29, 30]
                        y_offset = 130
                        for joint in joints_3d:
                            if joint['id'] in important_joints and joint['confidence'] > 0.5:
                                text = f"{joint['name']}: ({joint['x']}, {joint['y']}, {joint['z']:.2f}m)"
                                cv2.putText(display_image, text, (10, y_offset), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
                                y_offset += 20
                                if y_offset > 400:  # Limitar para que no se salga de la pantalla
                                    break
                    
                    # Mostrar controles
                    cv2.putText(display_image, "Vista en vivo - GUI Activa", 
                               (10, display_image.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    
                    # La imagen ya está en el tamaño correcto (640x480)
                    # No necesitamos redimensionar porque ya tiene la resolución exacta
                    height, width = display_image.shape[:2]
                    
                    # Convertir BGR a RGB para Tkinter
                    rgb_image = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
                    
                    # Convertir a PIL Image y luego a PhotoImage
                    pil_image = Image.fromarray(rgb_image)
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Actualizar canvas en el hilo principal con el tamaño real
                    self.root.after(0, self.update_video_canvas, photo, width, height)
                    
                    # Controlar FPS exactamente igual a test_camera.py
                    time.sleep(1/30)  # 30 FPS
                    
                except Exception as e:
                    if self.video_feed_active:  # Solo mostrar error si aún deberíamos estar activos
                        self.log_message(f"⚠️ Error en frame de video: {str(e)}")
                        time.sleep(0.1)  # Esperar un poco antes de reintentar
                    
        except Exception as e:
            self.log_message(f"❌ Error en transmisión de video: {str(e)}")
        finally:
            if self.camera_running:
                self.root.after(0, self.stop_camera_feed)
    
    def update_video_canvas(self, photo, width, height):
        """Actualiza el canvas con el nuevo frame - Mantiene resolución original"""
        if not self.video_feed_active:
            return
            
        self.video_canvas.delete("all")
        
        # No centrar, usar toda la resolución disponible (640x480)
        # Esto mantiene exactamente el mismo campo de visión que test_camera.py
        self.video_canvas.create_image(0, 0, anchor='nw', image=photo)
        
        # Mantener referencia para evitar garbage collection
        self.video_canvas.image = photo
    
    def show_camera_placeholder(self):
        """Muestra un placeholder cuando la cámara no está activa"""
        self.video_canvas.delete("all")
        self.video_canvas.create_text(320, 200, 
                                     text="🎥 Cámara Iniciando...",
                                     fill='white',
                                     font=('Segoe UI', 16, 'bold'))
        self.video_canvas.create_text(320, 240, 
                                     text="Por favor espera...",
                                     fill='#cccccc',
                                     font=('Segoe UI', 12))
        self.video_canvas.create_text(320, 280, 
                                     text="La cámara se iniciará automáticamente",
                                     fill='#999999',
                                     font=('Segoe UI', 10))
    
    def start_detection(self):
        """Inicia la detección de actividad con countdown"""
        if not self.system_initialized:
            messagebox.showwarning("Sistema no listo", 
                                 "El sistema aún se está inicializando. Espera un momento.")
            return
        
        if self.is_detecting:
            return
        
        if not self.classifier.is_trained():
            messagebox.showwarning("Modelo no entrenado", 
                                 "Primero debes entrenar un modelo en la pestaña de Entrenamiento.")
            return
        
        # Iniciar countdown
        self.start_countdown()
    
    def start_countdown(self):
        """Inicia el countdown de 3 segundos"""
        self.countdown_active = True
        self.detect_button.config(state='disabled')
        self.log_message("⏰ Iniciando countdown - Posiciónate frente a la cámara")
        
        def countdown_worker():
            try:
                for i in range(3, 0, -1):
                    if not self.countdown_active:
                        return
                    
                    # Actualizar label de countdown
                    self.root.after(0, lambda num=i: self.countdown_label.config(
                        text=f"⏰ {num}",
                        fg='#d13438' if num > 1 else '#107c10'
                    ))
                    
                    self.log_message(f"⏰ Countdown: {i}")
                    time.sleep(1)
                
                if self.countdown_active:
                    # Limpiar countdown y comenzar detección
                    self.root.after(0, lambda: self.countdown_label.config(text="🎬 ¡GRABANDO!"))
                    self.root.after(0, self.execute_detection)
                    
            except Exception as e:
                self.log_message(f"❌ Error en countdown: {str(e)}")
                self.root.after(0, self.reset_detection_ui)
        
        threading.Thread(target=countdown_worker, daemon=True).start()
    
    def execute_detection(self):
        """Ejecuta la detección real después del countdown"""
        def detection_worker():
            try:
                self.is_detecting = True
                self.progress_var.set(0)
                
                self.log_message("🎯 ¡Iniciando detección de actividad!")
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "🎯 DETECCIÓN EN PROGRESO\n")
                self.results_text.insert(tk.END, "=" * 50 + "\n\n")
                
                # Capturar actividad con callback de progreso
                self.log_message("📹 Capturando datos de la cámara...")
                raw_file = self.capture_activity_with_progress()
                
                if raw_file:
                    self.root.after(0, lambda: self.countdown_label.config(text="🔄 Procesando..."))
                    
                    self.log_message("🔄 Preprocesando datos...")
                    processed_file = self.preprocessor.process_raw_data(raw_file)
                    
                    self.log_message("📊 Extrayendo características...")
                    features = self.feature_extractor.extract_features(processed_file)
                    
                    self.log_message("🔍 Clasificando actividad...")
                    predicted_activity, probabilities = self.classifier.predict_activity(features)
                    
                    # Mostrar resultados
                    self.results_text.delete(1.0, tk.END)
                    self.results_text.insert(tk.END, "🎉 RESULTADOS DE DETECCIÓN\n")
                    self.results_text.insert(tk.END, "=" * 50 + "\n\n")
                    self.results_text.insert(tk.END, f"🏷️ Actividad detectada: {predicted_activity}\n")
                    self.results_text.insert(tk.END, f"🎯 Confianza: {max(probabilities.values()):.2%}\n\n")
                    self.results_text.insert(tk.END, "📈 Probabilidades por clase:\n")
                    
                    for activity, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
                        self.results_text.insert(tk.END, f"   {activity}: {prob:.2%}\n")
                    
                    self.log_message(f"✅ Actividad detectada: {predicted_activity} ({max(probabilities.values()):.2%})")
                    
                    # Limpiar archivos temporales
                    try:
                        if os.path.exists(raw_file):
                            os.remove(raw_file)
                        if os.path.exists(processed_file):
                            os.remove(processed_file)
                    except:
                        pass
                else:
                    self.log_message("❌ Error en la captura de datos")
                    self.results_text.delete(1.0, tk.END)
                    self.results_text.insert(tk.END, "❌ Error en la captura de datos\n")
                
            except Exception as e:
                self.log_message(f"❌ Error durante la detección: {str(e)}")
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"❌ Error durante la detección:\n{str(e)}")
                messagebox.showerror("Error de Detección", f"Error durante la detección:\n{str(e)}")
            finally:
                self.root.after(0, self.reset_detection_ui)
        
        threading.Thread(target=detection_worker, daemon=True).start()
    
    def capture_activity_with_progress(self):
        """Captura actividad con actualizaciones de progreso"""
        try:
            # Usar el método de captura existente pero con progreso
            return self.capture_system.capture_activity("unknown_activity")
        except Exception as e:
            self.log_message(f"❌ Error en captura: {str(e)}")
            return None
    
    def reset_detection_ui(self):
        """Resetea la interfaz después de la detección"""
        self.is_detecting = False
        self.countdown_active = False
        self.detect_button.config(state='normal')
        self.countdown_label.config(text="")
        self.progress_var.set(0)
    
    def old_start_detection(self):
        if not self.system_initialized:
            messagebox.showwarning("Sistema no listo", 
                                 "El sistema aún se está inicializando. Espera un momento.")
            return
        
        if self.is_detecting:
            return
        
        if not self.classifier.is_trained():
            messagebox.showwarning("Modelo no entrenado", 
                                 "Primero debes entrenar un modelo en la pestaña de Entrenamiento.")
            return
        
        def detection_worker():
            try:
                self.is_detecting = True
                self.detect_button.config(text="🔄 DETECTANDO...", state='disabled')
                self.progress_var.set(0)
                
                self.log_message("🎯 Iniciando detección de actividad...")
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "🎯 DETECCIÓN EN PROGRESO\n")
                self.results_text.insert(tk.END, "=" * 50 + "\n\n")
                
                # Simular progreso durante la captura
                for i in range(10):
                    time.sleep(1)
                    progress = (i + 1) * 10
                    self.progress_var.set(progress)
                    self.results_text.insert(tk.END, f"📹 Capturando... {progress}%\n")
                    self.results_text.see(tk.END)
                
                # Ejecutar detección real
                self.log_message("📹 Capturando datos de la cámara...")
                raw_file = self.capture_system.capture_activity("unknown_activity")
                
                if raw_file:
                    self.log_message("🔄 Preprocesando datos...")
                    processed_file = self.preprocessor.process_raw_data(raw_file)
                    
                    self.log_message("📊 Extrayendo características...")
                    features = self.feature_extractor.extract_features(processed_file)
                    
                    self.log_message("🔍 Clasificando actividad...")
                    predicted_activity, probabilities = self.classifier.predict_activity(features)
                    
                    # Mostrar resultados
                    self.results_text.delete(1.0, tk.END)
                    self.results_text.insert(tk.END, "🎉 RESULTADOS DE DETECCIÓN\n")
                    self.results_text.insert(tk.END, "=" * 50 + "\n\n")
                    self.results_text.insert(tk.END, f"🏷️ Actividad detectada: {predicted_activity}\n")
                    self.results_text.insert(tk.END, f"🎯 Confianza: {max(probabilities.values()):.2%}\n\n")
                    self.results_text.insert(tk.END, "📈 Probabilidades por clase:\n")
                    
                    for activity, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
                        self.results_text.insert(tk.END, f"   {activity}: {prob:.2%}\n")
                    
                    self.log_message(f"✅ Actividad detectada: {predicted_activity} ({max(probabilities.values()):.2%})")
                    
                    # Limpiar archivos temporales
                    try:
                        if os.path.exists(raw_file):
                            os.remove(raw_file)
                        if os.path.exists(processed_file):
                            os.remove(processed_file)
                    except:
                        pass
                else:
                    self.log_message("❌ Error en la captura de datos")
                    self.results_text.delete(1.0, tk.END)
                    self.results_text.insert(tk.END, "❌ Error en la captura de datos\n")
                
            except Exception as e:
                self.log_message(f"❌ Error durante la detección: {str(e)}")
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"❌ Error durante la detección:\n{str(e)}")
                messagebox.showerror("Error de Detección", f"Error durante la detección:\n{str(e)}")
            finally:
                self.is_detecting = False
                self.detect_button.config(text="🚀 INICIAR DETECCIÓN", state='normal')
                self.progress_var.set(0)
        
        threading.Thread(target=detection_worker, daemon=True).start()
    
    def browse_dataset(self):
        """Abre el diálogo para seleccionar el dataset"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de dataset",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.dataset_path_var.set(filename)
    
    def start_training(self):
        """Inicia el entrenamiento del modelo"""
        if not self.system_initialized:
            messagebox.showwarning("Sistema no listo", 
                                 "El sistema aún se está inicializando. Espera un momento.")
            return
        
        dataset_path = self.dataset_path_var.get().strip()
        if not dataset_path or not os.path.exists(dataset_path):
            messagebox.showwarning("Dataset no válido", 
                                 "Por favor selecciona un archivo de dataset válido.")
            return
        
        if self.is_training:
            return
        
        def training_worker():
            try:
                self.is_training = True
                self.train_button.config(text="🔄 ENTRENANDO...", state='disabled')
                self.train_progress_var.set(25)
                
                self.log_message(f"🎓 Iniciando entrenamiento con dataset: {dataset_path}")
                self.train_results_text.delete(1.0, tk.END)
                self.train_results_text.insert(tk.END, "🎓 ENTRENAMIENTO EN PROGRESO\n")
                self.train_results_text.insert(tk.END, "=" * 50 + "\n\n")
                
                self.train_progress_var.set(50)
                accuracy = self.classifier.train_model(dataset_path)
                self.train_progress_var.set(100)
                
                # Mostrar resultados
                self.train_results_text.insert(tk.END, f"✅ Modelo entrenado exitosamente\n")
                self.train_results_text.insert(tk.END, f"📊 Precisión: {accuracy:.2%}\n")
                self.train_results_text.insert(tk.END, f"🏷️ Clases detectadas: {', '.join(self.classifier.classes)}\n")
                
                self.log_message(f"✅ Entrenamiento completado - Precisión: {accuracy:.2%}")
                self.update_status()
                
                messagebox.showinfo("Entrenamiento Completado", 
                                  f"Modelo entrenado exitosamente\nPrecisión: {accuracy:.2%}")
                
            except Exception as e:
                self.log_message(f"❌ Error durante el entrenamiento: {str(e)}")
                self.train_results_text.insert(tk.END, f"❌ Error durante el entrenamiento:\n{str(e)}")
                messagebox.showerror("Error de Entrenamiento", f"Error durante el entrenamiento:\n{str(e)}")
            finally:
                self.is_training = False
                self.train_button.config(text="🚀 ENTRENAR MODELO", state='normal')
                self.train_progress_var.set(0)
        
        threading.Thread(target=training_worker, daemon=True).start()
    
    # Métodos para herramientas legacy
    def clean_folders(self):
        """Limpia estructura de carpetas"""
        base_path = filedialog.askdirectory(title="Seleccionar carpeta base para limpiar")
        if base_path:
            try:
                self.legacy_processor.clean_capture_folders(base_path)
                self.log_message(f"✅ Carpetas limpiadas en: {base_path}")
                messagebox.showinfo("Éxito", "Estructura de carpetas limpiada exitosamente")
            except Exception as e:
                self.log_message(f"❌ Error limpiando carpetas: {str(e)}")
                messagebox.showerror("Error", f"Error limpiando carpetas:\n{str(e)}")
    
    def remove_columns(self):
        """Elimina columnas extra de CSVs"""
        base_path = filedialog.askdirectory(title="Seleccionar carpeta con archivos CSV")
        if base_path:
            try:
                self.legacy_processor.remove_extra_columns(base_path)
                self.log_message(f"✅ Columnas extra eliminadas en: {base_path}")
                messagebox.showinfo("Éxito", "Columnas extra eliminadas exitosamente")
            except Exception as e:
                self.log_message(f"❌ Error eliminando columnas: {str(e)}")
                messagebox.showerror("Error", f"Error eliminando columnas:\n{str(e)}")
    
    def reshape_csvs(self):
        """Convierte CSVs a dataset"""
        input_path = filedialog.askdirectory(title="Seleccionar carpeta con CSVs individuales")
        if not input_path:
            return
        
        output_path = filedialog.askdirectory(title="Seleccionar carpeta de salida para datasets")
        if not output_path:
            return
        
        activity_prefix = tk.simpledialog.askstring("Prefijo", 
                                                   "Ingresa el prefijo para nombres de archivo:")
        if activity_prefix:
            try:
                self.legacy_processor.reshape_csvs_to_dataset(input_path, output_path, activity_prefix)
                self.log_message(f"✅ CSVs convertidos a dataset - Salida: {output_path}")
                messagebox.showinfo("Éxito", "CSVs convertidos a dataset exitosamente")
            except Exception as e:
                self.log_message(f"❌ Error convirtiendo CSVs: {str(e)}")
                messagebox.showerror("Error", f"Error convirtiendo CSVs:\n{str(e)}")
    
    def visualize_skeleton_3d(self):
        """Visualiza esqueleto 3D"""
        csv_file = filedialog.askopenfilename(title="Seleccionar archivo CSV",
                                            filetypes=[("CSV files", "*.csv")])
        if csv_file:
            show_labels = messagebox.askyesno("Etiquetas", "¿Mostrar nombres de joints?")
            try:
                self.visualizer.plot_skeleton_3d(csv_file, show_labels)
                self.log_message(f"✅ Visualización 3D generada para: {csv_file}")
            except Exception as e:
                self.log_message(f"❌ Error en visualización 3D: {str(e)}")
                messagebox.showerror("Error", f"Error en visualización 3D:\n{str(e)}")
    
    def create_skeleton_animation(self):
        """Crea animación de esqueleto"""
        csv_file = filedialog.askopenfilename(title="Seleccionar archivo CSV",
                                            filetypes=[("CSV files", "*.csv")])
        if csv_file:
            with_spine = messagebox.askyesno("Espina", "¿Incluir espina dorsal?")
            try:
                self.visualizer.plot_skeleton_animation(csv_file, with_spine=with_spine)
                self.log_message(f"✅ Animación generada para: {csv_file}")
            except Exception as e:
                self.log_message(f"❌ Error en animación: {str(e)}")
                messagebox.showerror("Error", f"Error en animación:\n{str(e)}")
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        try:
            # Detener cámara si está activa
            if self.camera_running:
                self.stop_camera_feed()
            
            # Detener sistema si está inicializado
            if hasattr(self, 'capture_system'):
                try:
                    self.capture_system.stop_capture()
                except:
                    pass
            
            self.log_message("👋 Cerrando aplicación...")
            self.root.destroy()
            
        except Exception as e:
            print(f"Error al cerrar: {e}")
            self.root.destroy()

def main():
    """Función principal"""
    root = tk.Tk()
    app = ActivityRecognitionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
