"""
Módulo para capturar datos 3D usando cámaras Intel RealSense
"""

import os
import threading
import time
import cv2
import pyrealsense2 as rs
import numpy as np
import pandas as pd
from datetime import datetime
from .pose_detector import PoseDetector

class RealSenseCapture:
    def __init__(self, 
                 frame_rate=30, 
                 capture_seconds=10, 
                 resolution=(640, 480),
                 output_path="temp_data"):
        """
        Inicializa el capturador de RealSense
        
        Args:
            frame_rate: FPS de captura
            capture_seconds: Duración de captura en segundos
            resolution: Resolución de captura (ancho, alto)
            output_path: Carpeta donde guardar los datos
        """
        self.FRAME_RATE = frame_rate
        self.CAPTURE_SECONDS = capture_seconds
        self.RESOLUTION = resolution
        self.OUTPUT_PATH = output_path
        self.imgs2take = frame_rate * capture_seconds
        self.capture = False
        
        # Inicializar el detector de poses
        self.detector = PoseDetector()
        self.object_to_track = range(0, 33)  # 33 joints de MediaPipe
        
        # Configurar pipelines de RealSense
        self.context = rs.context()
        self.devices = self.context.devices
        self.pipelines = []
        
        if len(self.devices) == 0:
            raise Exception("No se encontró ningún dispositivo RealSense conectado.")
            
        self._setup_pipelines()

    def _setup_pipelines(self):
        """Configura los pipelines para todas las cámaras conectadas"""
        for i, device in enumerate(self.devices):
            pipeline = rs.pipeline()
            config = rs.config()

            # Usar el dispositivo específico por serial
            serial = device.get_info(rs.camera_info.serial_number)
            config.enable_device(serial)

            # Habilitar streams
            config.enable_stream(
                rs.stream.color, 
                self.RESOLUTION[0], 
                self.RESOLUTION[1], 
                rs.format.bgr8, 
                self.FRAME_RATE
            )
            config.enable_stream(
                rs.stream.depth, 
                self.RESOLUTION[0], 
                self.RESOLUTION[1], 
                rs.format.z16, 
                self.FRAME_RATE
            )

            # Iniciar pipeline
            pipeline.start(config)
            self.pipelines.append(pipeline)
            print(f"Cámara {i + 1} conectada, serial: {serial}")

    def capture_activity(self, activity_name="unknown"):
        """
        Captura una actividad completa y guarda los datos
        
        Args:
            activity_name: Nombre de la actividad a capturar
            
        Returns:
            Ruta donde se guardaron los datos
        """
        print(f"Iniciando captura de '{activity_name}' por {self.CAPTURE_SECONDS} segundos...")
        
        # Crear timestamp para la sesión
        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        session_path = os.path.join(self.OUTPUT_PATH, f"{activity_name}_{timestamp}")
        
        # Preparar datos para captura
        self.capture = True
        captured_data = []
        
        try:
            # Usar solo la primera cámara para simplicidad
            pipeline = self.pipelines[0]
            imgsCount = 0
            
            while imgsCount < self.imgs2take and self.capture:
                frames = pipeline.wait_for_frames()
                frame_depth = frames.get_depth_frame()
                frame_color = frames.get_color_frame()

                if not frame_color:
                    continue

                image_color = np.asanyarray(frame_color.get_data())
                pose, skeleton = self.detector.findPose(image_color)
                lmList = self.detector.getPosition(pose)

                # Procesar joints para obtener coordenadas 3D
                frame_data = []
                if len(lmList) != 0:
                    for obj in self.object_to_track:
                        if obj < len(lmList):
                            _, x, y = lmList[obj]
                            
                            # Validar coordenadas
                            if (x < 0 or x >= self.RESOLUTION[0] or 
                                y < 0 or y >= self.RESOLUTION[1]):
                                frame_data.extend([0, 0, 0])
                                continue
                                
                            # Obtener coordenada Z del sensor de profundidad
                            z = frame_depth.get_distance(x, y)
                            if z <= 0:
                                frame_data.extend([0, 0, 0])
                                continue
                                
                            frame_data.extend([x, y, z])
                        else:
                            frame_data.extend([0, 0, 0])
                else:
                    # Si no se detectaron poses, llenar con ceros
                    frame_data = [0] * 99  # 33 joints × 3 coordenadas

                captured_data.append(frame_data)
                imgsCount += 1
                
                # Mostrar progreso
                if imgsCount % 30 == 0:  # Cada segundo
                    print(f"Capturados {imgsCount}/{self.imgs2take} frames...")

            # Guardar datos capturados
            return self._save_captured_data(captured_data, session_path, activity_name)
            
        except Exception as e:
            print(f"Error durante la captura: {e}")
            return None
        finally:
            self.capture = False

    def _save_captured_data(self, data, session_path, activity_name):
        """
        Guarda los datos capturados en formato CSV
        
        Args:
            data: Lista de frames con coordenadas
            session_path: Ruta de la sesión
            activity_name: Nombre de la actividad
            
        Returns:
            Ruta del archivo guardado
        """
        os.makedirs(session_path, exist_ok=True)
        
        # Crear nombres de columnas
        columns = []
        for i in range(33):
            columns.extend([f'joint{i}_x', f'joint{i}_y', f'joint{i}_z'])
        
        # Crear DataFrame y guardar
        df = pd.DataFrame(data, columns=columns)
        output_file = os.path.join(session_path, f"{activity_name}_raw.csv")
        df.to_csv(output_file, index=False)
        
        print(f"Datos guardados en: {output_file}")
        return output_file

    def stop_capture(self):
        """Detiene la captura y libera recursos"""
        self.capture = False
        for pipeline in self.pipelines:
            pipeline.stop()
        print("Captura detenida y recursos liberados.")
