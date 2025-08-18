"""
Script para verificar que todas las dependencias estén instaladas correctamente
antes de ejecutar la aplicación GUI
"""

import sys
import importlib.util

def check_module(module_name, pip_name=None):
    """Verifica si un módulo está instalado"""
    if pip_name is None:
        pip_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        print(f"✅ {module_name} - OK")
        return True
    else:
        print(f"❌ {module_name} - FALTA (instalar con: pip install {pip_name})")
        return False

def main():
    print("🔍 VERIFICACIÓN DE DEPENDENCIAS")
    print("=" * 40)
    
    all_ok = True
    
    # Verificar módulos esenciales
    modules_to_check = [
        ("tkinter", "tkinter (incluido con Python)"),
        ("cv2", "opencv-python"),
        ("mediapipe", "mediapipe"),
        ("pyrealsense2", "pyrealsense2"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("sklearn", "scikit-learn"),
        ("joblib", "joblib"),
        ("matplotlib", "matplotlib"),
        ("plotly", "plotly"),
        ("PIL", "Pillow")
    ]
    
    for module, pip_name in modules_to_check:
        if not check_module(module, pip_name):
            all_ok = False
    
    print("\n" + "=" * 40)
    
    if all_ok:
        print("✅ TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS")
        print("🚀 Puedes ejecutar la aplicación GUI con: python gui_main.py")
    else:
        print("❌ FALTAN ALGUNAS DEPENDENCIAS")
        print("📦 Instala las dependencias faltantes con:")
        print("   pip install -r requirements.txt")
    
    print("\n📋 INFORMACIÓN DEL SISTEMA:")
    print(f"   Python: {sys.version}")
    print(f"   Plataforma: {sys.platform}")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...")
