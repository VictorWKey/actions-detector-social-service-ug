"""
Development interface for data processing and model training
"""

import sys
import os
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFrame, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

# Add capture module to path
capture_path = os.path.join(os.path.dirname(__file__), '../../capture')
sys.path.insert(0, capture_path)
from camera_widget import CameraCapture


class DevInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.camera_capture = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Interfaz de Desarrollo - Captura de Datos")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Camera display area
        self.camera_label = QLabel("Cámara no iniciada")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.camera_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Iniciar Cámara")
        self.start_button.clicked.connect(self.start_camera)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Detener Cámara")
        self.stop_button.clicked.connect(self.stop_camera)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)
        
        # Action selection section
        action_layout = QHBoxLayout()
        action_label = QLabel("Acción a capturar:")
        action_layout.addWidget(action_label)
        
        self.action_combo = QComboBox()
        self.action_combo.addItems(["aplaudir", "saludar", "vieneviene", "dibujar circulo", "sentadilla"])
        self.action_combo.setCurrentText("aplaudir")
        action_layout.addWidget(self.action_combo)
        
        layout.addLayout(action_layout)
        
        # Capture section
        capture_layout = QHBoxLayout()
        
        self.capture_button = QPushButton("Capturar 5 Segundos (con countdown)")
        self.capture_button.clicked.connect(self.start_capture)
        self.capture_button.setEnabled(False)
        capture_layout.addWidget(self.capture_button)
        
        # Status label
        self.status_label = QLabel("Estado: Cámara detenida")
        capture_layout.addWidget(self.status_label)
        
        layout.addLayout(capture_layout)
        self.setLayout(layout)
    
    def start_camera(self):
        """Start camera capture"""
        try:
            self.camera_capture = CameraCapture()
            
            # Connect signals
            self.camera_capture.frame_ready.connect(self.update_frame)
            self.camera_capture.countdown_update.connect(self.on_countdown_update)
            self.camera_capture.capture_started.connect(self.on_capture_started)
            self.camera_capture.capture_progress.connect(self.on_capture_progress)
            self.camera_capture.capture_finished.connect(self.on_capture_finished)
            
            self.camera_capture.start()
            
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.capture_button.setEnabled(True)
            self.camera_label.setText("Iniciando cámara...")
            self.status_label.setText("Estado: Cámara iniciada")
        except Exception as e:
            self.camera_label.setText(f"Error: {e}")
            self.status_label.setText(f"Estado: Error - {e}")
    
    def stop_camera(self):
        """Stop camera capture"""
        if self.camera_capture:
            self.camera_capture.stop()
            self.camera_capture = None
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.capture_button.setEnabled(False)
        self.camera_label.setText("Cámara detenida")
        self.status_label.setText("Estado: Cámara detenida")
    
    def update_frame(self, frame):
        """Update camera display with new frame"""
        try:
            # Convert numpy array to QImage
            height, width, channels = frame.shape
            bytes_per_line = channels * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            
            # Convert to QPixmap and display
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.camera_label.setPixmap(scaled_pixmap)
        except Exception as e:
            print(f"Error updating frame: {e}")
    
    def start_capture(self):
        """Start 5-second data capture with countdown"""
        if self.camera_capture:
            # Get selected action
            action_name = self.action_combo.currentText()
            self.camera_capture.start_capture_with_countdown(action_name)
            self.capture_button.setEnabled(False)
    
    def on_countdown_update(self, seconds):
        """Handle countdown update signal"""
        if seconds > 0:
            self.status_label.setText(f"Estado: Iniciando captura en {seconds} segundos...")
        else:
            self.status_label.setText("Estado: ¡CAPTURANDO!")
    
    def on_capture_started(self):
        """Handle capture started signal"""
        self.status_label.setText("Estado: Capturando datos...")
    
    def on_capture_progress(self, current_frame, total_frames):
        """Handle capture progress signal"""
        progress = (current_frame / total_frames) * 100
        self.status_label.setText(f"Estado: Capturando... {progress:.1f}% ({current_frame}/{total_frames})")
    
    def on_capture_finished(self, save_path):
        """Handle capture finished signal"""
        self.status_label.setText(f"Estado: Captura guardada en {os.path.basename(save_path)}")
        self.capture_button.setEnabled(True)
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.stop_camera()
        event.accept()