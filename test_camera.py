"""
Prueba de cámara Intel RealSense con detección de puntos del cuerpo
Este archivo abre una ventana para ver la cámara y detectar el esqueleto humano
"""

import cv2
import pyrealsense2 as rs
import numpy as np
import mediapipe as mp
import json
import os
import time
from datetime import datetime

class PoseDetector:
    """Detector de poses usando MediaPipe"""
    
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
        """Detecta poses en la imagen"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        return results
    
    def draw_landmarks(self, image, results, show_names=False):
        """Dibuja los landmarks detectados"""
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
        """Extrae coordenadas 3D de los joints detectados"""
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

def test_realsense_camera():
    """
    Prueba la conexión con la cámara RealSense y detecta poses en tiempo real
    """
    print("🔍 Buscando cámaras Intel RealSense...")
    
    # Configurar el pipeline de RealSense
    pipeline = rs.pipeline()
    config = rs.config()
    
    # Inicializar detector de poses
    pose_detector = PoseDetector()
    print("🤖 Detector de poses MediaPipe inicializado")
    
    try:
        # Verificar dispositivos conectados
        context = rs.context()
        devices = context.devices
        
        if len(devices) == 0:
            print("❌ No se encontraron cámaras Intel RealSense conectadas.")
            print("   Verifica que:")
            print("   - La cámara esté conectada por USB")
            print("   - Los drivers de Intel RealSense estén instalados")
            print("   - La cámara tenga alimentación suficiente")
            return False
        
        print(f"✅ Encontradas {len(devices)} cámara(s) RealSense:")
        for i, device in enumerate(devices):
            serial = device.get_info(rs.camera_info.serial_number)
            name = device.get_info(rs.camera_info.name)
            print(f"   Cámara {i+1}: {name} (Serial: {serial})")
        
        # Configurar streams
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        
        # Iniciar pipeline
        print("\n🎥 Iniciando detección de poses en tiempo real...")
        print("   Controles:")
        print("   - 'q': Salir")
        print("   - 'd': Alternar mapa de profundidad")
        print("   - 'p': Alternar detección de poses")
        print("   - 'n': Alternar nombres de joints")
        print("   - 's': Mostrar estadísticas de joints")
        
        pipeline.start(config)
        
        show_depth = False
        show_poses = True
        show_names = False
        frame_count = 0
        joints_detected = 0
        # --- Inicializar grabación ---
        output_dir = os.path.join(os.getcwd(), "recordings")
        os.makedirs(output_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = os.path.join(output_dir, f"realsense_record_{ts}.mp4")
        jsonl_path = os.path.join(output_dir, f"realsense_joints_{ts}.jsonl")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = None  # se inicializa tras obtener el primer frame
        joints_log_file = open(jsonl_path, 'w', encoding='utf-8')
        print(f"📁 Grabando video en: {video_path}")
        print(f"📁 Guardando joints en: {jsonl_path}")
        
        try:
            while True:
                # Esperar frames
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
                
                # Detectar poses si está habilitado
                pose_results = None
                joints_3d = []
                if show_poses:
                    pose_results = pose_detector.detect_pose(color_image)
                    joints_3d = pose_detector.get_joint_coordinates(pose_results, depth_frame)
                    if joints_3d:
                        joints_detected += 1

                # Preparar imagen para mostrar
                if show_depth:
                    # Aplicar colormap al mapa de profundidad
                    depth_colormap = cv2.applyColorMap(
                        cv2.convertScaleAbs(depth_image, alpha=0.03), 
                        cv2.COLORMAP_JET
                    )
                    display_image = depth_colormap.copy()
                    mode_text = "Profundidad"
                else:
                    display_image = color_image.copy()
                    mode_text = "Color"

                # Dibujar poses si están habilitadas
                if show_poses and pose_results:
                    pose_detector.draw_landmarks(display_image, pose_results, show_names)

                # Agregar información de estado
                cv2.putText(display_image, f"Modo: {mode_text}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(display_image, f"Poses: {'ON' if show_poses else 'OFF'}", 
                           (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(display_image, f"Joints detectados: {len(joints_3d)}/33", 
                           (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if frame_count > 0:
                    detection_rate = (joints_detected / frame_count) * 100
                    cv2.putText(display_image, f"Tasa detección: {detection_rate:.1f}%", 
                               (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Inicializar writer si aún no se hizo (usar tamaño del display_image)
                if video_writer is None:
                    h, w = display_image.shape[:2]
                    video_writer = cv2.VideoWriter(video_path, fourcc, 30.0, (w, h))

                # Escribir frame al archivo de video
                try:
                    video_writer.write(display_image)
                except Exception:
                    # evitar que errores en escritura rompan la captura
                    pass

                # Guardar la información de joints en JSONL (un registro por frame)
                record = {
                    'timestamp': time.time(),
                    'frame': frame_count,
                    'joints': joints_3d
                }
                joints_log_file.write(json.dumps(record, ensure_ascii=False) + "\n")

                # Mostrar joints importantes detectados
                if joints_3d and show_poses:
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
                cv2.putText(display_image, "Presiona 'q' para salir", 
                           (10, display_image.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                # Mostrar imagen
                window_title = f"RealSense + MediaPipe - {mode_text}"
                cv2.imshow(window_title, display_image)
                
                # Manejar teclas
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n👋 Cerrando aplicación...")
                    break
                elif key == ord('d'):
                    show_depth = not show_depth
                    print(f"🔄 Modo: {'Profundidad' if show_depth else 'Color'}")
                elif key == ord('p'):
                    show_poses = not show_poses
                    print(f"🔄 Detección de poses: {'ON' if show_poses else 'OFF'}")
                elif key == ord('n'):
                    show_names = not show_names
                    print(f"🔄 Nombres de joints: {'ON' if show_names else 'OFF'}")
                elif key == ord('s'):
                    if joints_3d:
                        print(f"\n📊 ESTADÍSTICAS DEL FRAME ACTUAL:")
                        print(f"   Total joints detectados: {len(joints_3d)}/33")
                        print(f"   Joints con alta confianza (>0.8): {sum(1 for j in joints_3d if j['confidence'] > 0.8)}")
                        print(f"   Joints con coordenada Z válida: {sum(1 for j in joints_3d if j['z'] > 0)}")
                        
                        # Mostrar joints más importantes para el proyecto
                        target_joints = [13, 14, 15, 16, 25, 26, 29, 30]  # Los que usa el proyecto
                        detected_target = [j for j in joints_3d if j['id'] in target_joints and j['confidence'] > 0.5]
                        print(f"   Joints objetivo detectados: {len(detected_target)}/8")
                        for joint in detected_target:
                            print(f"     {joint['name']}: confianza={joint['confidence']:.2f}, z={joint['z']:.3f}m")
                    else:
                        print("📊 No hay poses detectadas en el frame actual")
                
        except Exception as e:
            print(f"❌ Error durante la captura: {e}")
            return False
            
        finally:
            # Cerrar escritor de video y archivo de logs
            try:
                if video_writer is not None:
                    video_writer.release()
                    print(f"✅ Video guardado en: {video_path}")
            except Exception:
                pass

            try:
                if joints_log_file:
                    joints_log_file.close()
                    print(f"✅ Joints guardados en: {jsonl_path}")
            except Exception:
                pass

            # Limpiar recursos
            try:
                pipeline.stop()
            except Exception:
                pass
            cv2.destroyAllWindows()
            print("✅ Recursos liberados correctamente")

            # Mostrar estadísticas finales
            if frame_count > 0:
                final_detection_rate = (joints_detected / frame_count) * 100
                print(f"\n📊 ESTADÍSTICAS FINALES:")
                print(f"   Frames procesados: {frame_count}")
                print(f"   Frames con poses detectadas: {joints_detected}")
                print(f"   Tasa de detección: {final_detection_rate:.1f}%")

        return True

    except Exception as e:
        print(f"❌ Error al configurar la cámara: {e}")
        print("   Posibles soluciones:")
        print("   - Reinstalar Intel RealSense SDK")
        print("   - Verificar permisos de la cámara")
        print("   - Probar con otro puerto USB")
        return False


def main():
    """Función principal"""
    print("🚀 PRUEBA DE CÁMARA INTEL REALSENSE")
    print("=" * 45)
    
    # Verificar que las librerías estén instaladas
    try:
        import pyrealsense2 as rs
        import cv2
        import mediapipe as mp
        print("✅ Librerías instaladas correctamente")
    except ImportError as e:
        print(f"❌ Error: Librería faltante - {e}")
        print("   Instala las dependencias con:")
        print("   pip install pyrealsense2 opencv-python mediapipe")
        return
    
    # Probar la cámara
    success = test_realsense_camera()
    
    if success:
        print("\n🎉 ¡Prueba completada exitosamente!")
        print("   Tu cámara RealSense está funcionando correctamente")
    else:
        print("\n⚠️  La prueba no se completó correctamente")
        print("   Revisa las sugerencias anteriores")


if __name__ == "__main__":
    main()
