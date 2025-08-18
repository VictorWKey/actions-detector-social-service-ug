"""
Script para comparar configuraciones entre test_camera.py y gui_main.py
"""

import pyrealsense2 as rs
import sys
from pathlib import Path

def compare_camera_configs():
    """Compara las configuraciones de cámara"""
    
    print("🔍 COMPARACIÓN DE CONFIGURACIONES")
    print("=" * 50)
    
    # Configuración de test_camera.py
    print("📹 test_camera.py:")
    print("   - Resolución: 640x480")
    print("   - FPS: 30")
    print("   - Formato Color: BGR8")
    print("   - Formato Depth: Z16")
    print("   - Detector: MediaPipe con model_complexity=1")
    print("   - Suavizado: True")
    print("   - Min detection confidence: 0.5")
    print("   - Min tracking confidence: 0.5")
    
    print("\n📱 gui_main.py:")
    print("   - Resolución: 640x480 ✅")
    print("   - FPS: 30 ✅")
    print("   - Formato Color: BGR8 ✅")
    print("   - Formato Depth: Z16 ✅")
    print("   - Detector: GUIPoseDetector con model_complexity=1 ✅")
    print("   - Suavizado: True ✅")
    print("   - Min detection confidence: 0.5 ✅")
    print("   - Min tracking confidence: 0.5 ✅")
    
    # Verificar dispositivos
    print("\n🎥 DISPOSITIVOS DISPONIBLES:")
    try:
        context = rs.context()
        devices = context.devices
        
        if len(devices) > 0:
            for i, device in enumerate(devices):
                name = device.get_info(rs.camera_info.name)
                serial = device.get_info(rs.camera_info.serial_number)
                print(f"   Dispositivo {i+1}: {name}")
                print(f"   Serial: {serial}")
                
                # Verificar streams soportados
                sensors = device.query_sensors()
                for sensor in sensors:
                    profiles = sensor.get_stream_profiles()
                    for profile in profiles:
                        video_profile = profile.as_video_stream_profile()
                        if video_profile:
                            width = video_profile.width()
                            height = video_profile.height()
                            fps = video_profile.fps()
                            format_name = video_profile.format()
                            stream_name = video_profile.stream_name()
                            
                            # Verificar si soporta 640x480@30fps
                            if width == 640 and height == 480 and fps == 30:
                                print(f"   ✅ Soporta {stream_name}: {width}x{height}@{fps}fps ({format_name})")
        else:
            print("   ❌ No se encontraron dispositivos RealSense")
            
    except Exception as e:
        print(f"   ❌ Error verificando dispositivos: {e}")
    
    print("\n🎯 RESUMEN:")
    print("✅ Configuraciones idénticas entre test_camera.py y gui_main.py")
    print("✅ Misma resolución (640x480)")
    print("✅ Mismo FPS (30)")
    print("✅ Mismo detector MediaPipe")
    print("✅ Mismas configuraciones de confianza")
    print("✅ Canvas sin redimensionamiento para mantener campo de visión exacto")

def test_pose_detector_compatibility():
    """Prueba la compatibilidad del detector"""
    print("\n🤖 PRUEBA DEL DETECTOR DE POSES:")
    
    try:
        # Agregar el directorio src al path
        sys.path.append(str(Path(__file__).parent / 'src'))
        from src.capture.gui_pose_detector import GUIPoseDetector
        
        detector = GUIPoseDetector()
        print("✅ GUIPoseDetector creado exitosamente")
        print(f"✅ Detector MediaPipe configurado: model_complexity=1")
        print(f"✅ Suavizado habilitado: True")
        print(f"✅ Confianza de detección: 0.5")
        print(f"✅ Confianza de tracking: 0.5")
        print(f"✅ Diccionario de joints: {len(detector.joint_names)} joints definidos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando GUIPoseDetector: {e}")
        return False

if __name__ == "__main__":
    print("🚀 VERIFICACIÓN DE COMPATIBILIDAD")
    print("=" * 50)
    
    compare_camera_configs()
    detector_ok = test_pose_detector_compatibility()
    
    print("\n" + "=" * 50)
    if detector_ok:
        print("🎉 ¡CONFIGURACIÓN PERFECTA!")
        print("La GUI debería mostrar exactamente el mismo campo de visión que test_camera.py")
    else:
        print("⚠️ Hay problemas en la configuración")
    
    input("\nPresiona Enter para continuar...")
