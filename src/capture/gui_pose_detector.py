"""
Detector de poses mejorado usando MediaPipe - Compatible con test_camera.py
"""

import cv2
import numpy as np
import mediapipe as mp

class GUIPoseDetector:
    """Detector de poses optimizado para la GUI - Idéntico a test_camera.py"""
    
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Diccionario de nombres de joints en español
        self.joint_names = {
            0: "Nariz", 1: "Ojo Izq. Int", 2: "Ojo Izq", 3: "Ojo Izq. Ext",
            4: "Ojo Der. Int", 5: "Ojo Der", 6: "Ojo Der. Ext",
            7: "Oreja Izq", 8: "Oreja Der", 9: "Boca Izq", 10: "Boca Der",
            11: "Hombro Izq", 12: "Hombro Der", 13: "Codo Izq",
            14: "Codo Der", 15: "Muñeca Izq", 16: "Muñeca Der",
            17: "Meñique Izq", 18: "Meñique Der", 19: "Índice Izq", 20: "Índice Der",
            21: "Pulgar Izq", 22: "Pulgar Der", 23: "Cadera Izq", 24: "Cadera Der",
            25: "Rodilla Izq", 26: "Rodilla Der", 27: "Tobillo Izq", 28: "Tobillo Der",
            29: "Talón Izq", 30: "Talón Der", 31: "Pie Izq", 32: "Pie Der"
        }
    
    def detect_pose(self, image):
        """Detecta poses en la imagen - Idéntico a test_camera.py"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        return results
    
    def draw_landmarks(self, image, results, show_names=False):
        """Dibuja los landmarks detectados - Idéntico a test_camera.py"""
        if results.pose_landmarks:
            # Dibujar conexiones del esqueleto
            self.mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
            
            # Opcionalmente mostrar nombres de joints
            if show_names:
                h, w, c = image.shape
                for idx, landmark in enumerate(results.pose_landmarks.landmark):
                    if idx in [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 29, 30]:  # Joints importantes
                        x = int(landmark.x * w)
                        y = int(landmark.y * h)
                        cv2.putText(image, self.joint_names[idx], (x-20, y-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1)
    
    def get_joint_coordinates(self, results, depth_frame=None):
        """Extrae coordenadas 3D de los joints detectados - Idéntico a test_camera.py"""
        joints_3d = []
        if results.pose_landmarks:
            h, w = 480, 640  # Resolución de la cámara
            
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                
                # Obtener coordenada Z del sensor de profundidad si está disponible
                z = 0
                if depth_frame and 0 <= x < w and 0 <= y < h:
                    z = depth_frame.get_distance(x, y)
                
                joints_3d.append({
                    'id': idx,
                    'name': self.joint_names[idx],
                    'x': x, 'y': y, 'z': z,
                    'confidence': landmark.visibility
                })
        
        return joints_3d
    
    def count_detected_joints(self, results):
        """Cuenta cuántos joints fueron detectados"""
        if results.pose_landmarks:
            return len(results.pose_landmarks.landmark)
        return 0
