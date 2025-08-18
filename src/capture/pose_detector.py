"""
Detector de poses usando MediaPipe para la captura de coordenadas 3D
"""

import cv2
import numpy as np
import mediapipe as mp

class PoseDetector:
    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=True, trackCon=0.5):
        """
        Inicializa el detector de poses usando MediaPipe
        
        Args:
            mode: Si True, trata cada imagen como independiente
            upBody: Si True, detecta solo la parte superior del cuerpo
            smooth: Si True, suaviza las coordenadas entre frames
            detectionCon: Confianza mínima para detección
            trackCon: Confianza mínima para tracking
        """
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            self.mode, 
            self.upBody, 
            self.smooth, 
            self.detectionCon, 
            self.trackCon
        )

    def findPose(self, img, draw=True):
        """
        Detecta poses en una imagen
        
        Args:
            img: Imagen de entrada
            draw: Si True, dibuja las poses en la imagen
            
        Returns:
            Tupla con (imagen_con_poses, esqueleto_en_fondo_negro)
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        blackBG = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        self.results = self.pose.process(imgRGB)
        
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(
                    img, 
                    self.results.pose_landmarks, 
                    self.mpPose.POSE_CONNECTIONS
                )
                self.mpDraw.draw_landmarks(
                    blackBG, 
                    self.results.pose_landmarks, 
                    self.mpPose.POSE_CONNECTIONS
                )

        return img, blackBG

    def getPosition(self, img, draw=True):
        """
        Extrae las posiciones de los joints detectados
        
        Args:
            img: Imagen de entrada
            draw: Si True, dibuja círculos en los joints
            
        Returns:
            Lista de [id, x, y] para cada joint detectado
        """
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList
