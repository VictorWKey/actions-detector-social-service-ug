"""
Script de prueba rápida para verificar la GUI con cámara
"""

import sys
import os
from pathlib import Path

# Agregar directorio src
sys.path.append(str(Path(__file__).parent / 'src'))

def quick_test():
    """Prueba rápida de los componentes principales"""
    
    print("🔍 PRUEBA RÁPIDA DE COMPONENTES")
    print("=" * 40)
    
    # Test 1: Verificar imports
    try:
        import tkinter as tk
        from tkinter import ttk
        import cv2
        import numpy as np
        from PIL import Image, ImageTk
        import pyrealsense2 as rs
        print("✅ Imports básicos - OK")
    except ImportError as e:
        print(f"❌ Error en imports: {e}")
        return False
    
    # Test 2: Verificar cámaras RealSense
    try:
        context = rs.context()
        devices = context.devices
        if len(devices) > 0:
            print(f"✅ Cámaras RealSense - {len(devices)} detectadas")
            for i, device in enumerate(devices):
                name = device.get_info(rs.camera_info.name)
                serial = device.get_info(rs.camera_info.serial_number)
                print(f"   Cámara {i+1}: {name} (Serial: {serial})")
        else:
            print("⚠️ Cámaras RealSense - No detectadas")
            print("   La GUI funcionará pero sin vista en vivo")
    except Exception as e:
        print(f"❌ Error verificando cámaras: {e}")
    
    # Test 3: Verificar módulos del proyecto
    try:
        from src.capture import RealSenseCapture
        from src.capture import PoseDetector
        print("✅ Módulos del proyecto - OK")
    except ImportError as e:
        print(f"❌ Error en módulos del proyecto: {e}")
        return False
    
    # Test 4: Probar creación del detector
    try:
        detector = PoseDetector()
        print("✅ PoseDetector - OK")
    except Exception as e:
        print(f"❌ Error creando PoseDetector: {e}")
        return False
    
    print("\n🎉 PRUEBA COMPLETADA")
    print("Ejecuta la GUI con: python gui_main.py")
    return True

if __name__ == "__main__":
    success = quick_test()
    input("\nPresiona Enter para continuar...")
    
    if success:
        import subprocess
        import sys
        print("\n🚀 Iniciando GUI...")
        subprocess.run([sys.executable, "gui_main.py"])
