# Sistema de Reconocimiento de Acciones - SkeletonExtraction

Este proyecto es un **sistema completo de reconocimiento de acciones corporales** que utiliza cámaras Intel RealSense para capturar datos de movimiento 3D y realizar clasificación de acciones mediante análisis de esqueletos usando MediaPipe Pose. El sistema incluye tanto herramientas de desarrollo para captura y entrenamiento como interfaces de producción para reconocimiento en tiempo real.

## 🎯 Características Principales

- **Captura en tiempo real** de poses 3D usando cámaras Intel RealSense
- **Detección de esqueletos** con MediaPipe Pose (33 puntos anatómicos)
- **Interfaz gráfica PyQt5** con modos de desarrollo y producción
- **Pipeline completo de ML** para entrenamiento y clasificación
- **Preprocesamiento avanzado** de datos con imputación automática
- **Visualización 3D** de esqueletos capturados

## 📦 Instalación

```bash
pip install -r requirements.txt
```

### Dependencias principales:
- **OpenCV** >= 4.8.0 - Procesamiento de video e imágenes
- **MediaPipe** >= 0.10.0 - Detección de poses corporales
- **Intel RealSense SDK** >= 2.54.0 - Captura de datos 3D
- **PyQt5** >= 5.15.0 - Interfaz gráfica de usuario
- **Scikit-learn** >= 1.3.0 - Machine Learning
- **NumPy, Pandas, Matplotlib** - Procesamiento y visualización de datos

## 🚀 Uso

### Ejecución Principal
```bash
python main.py
```

### Interfaz de Desarrollo (para captura de datos)
```bash
python test_camera_gui.py
```

## 📁 Estructura Detallada del Proyecto

### **Archivos Principales**
- **`main.py`** - Punto de entrada principal del sistema. Inicializa la aplicación PyQt5 y carga la ventana principal con pestañas de desarrollo y producción.
- **`test_camera_gui.py`** - Aplicación de prueba idéntica a main.py, utilizada para verificar la integración de cámara con PyQt.
- **`requirements.txt`** - Lista completa de dependencias Python necesarias, incluyendo versiones específicas para compatibilidad.

### **⚙️ config/**
- **`settings.py`** - Configuración centralizada del sistema que incluye:
  - Resolución de cámara (640x480) y frame rate (30 FPS)
  - Duración de captura (5 segundos por defecto)
  - Rutas de archivos y modelos
  - Lista de acciones soportadas: "wave", "clap", "point", "raise_hand", "thumbs_up"
  - Configuración de características para ML (velocidad, aceleración, ángulos)

### **📹 src/capture/** - Sistema de Captura
- **`camera_widget.py`** - **Núcleo del sistema de captura** (274 líneas). Implementa:
  - Clase `CameraCapture` que hereda de QThread para captura en tiempo real
  - Sistema de countdown de 5 segundos antes de iniciar captura
  - Captura de 150 frames (5 segundos a 30 FPS) por sesión
  - Procesamiento automático de coordenadas 3D con validación de bounds
  - Guardado automático de archivos CSV por frame
  - Señales PyQt para comunicación con la GUI (progreso, estado, frames)

- **`pose_detector.py`** - **Detector de poses corporales** usando MediaPipe:
  - Clase `PoseDetector` que encapsula la funcionalidad de MediaPipe Pose
  - Método `findPose()` que procesa imágenes y detecta 33 puntos anatómicos
  - Método `getPosition()` que extrae coordenadas (x,y) de cada punto
  - Genera tanto la imagen con pose superpuesta como el esqueleto en fondo negro

- **`realtime_capture_system.py`** - **Sistema de captura original** (multihilo, 200+ líneas):
  - Maneja múltiples cámaras RealSense simultáneamente usando threading
  - Captura de 10 segundos por sesión (configurable)
  - Guarda datos en estructura: `acción/timestamp/camera_X/{xyz, rgb, skeleton}/`
  - Control por teclado: ESPACIO para iniciar/detener, ESC para salir
  - Validación automática de coordenadas y filtrado de puntos inválidos

- **`simple_camera.py`** - Archivo vacío (placeholder para futuras implementaciones)

### **🧠 src/feature_extraction/** - Extracción de Características
- **`skeleton_features.py`** - Módulo para extraer características avanzadas del esqueleto (actualmente placeholder). Destinado a calcular:
  - Velocidades y aceleraciones entre frames
  - Ángulos articulares
  - Distancias relativas entre puntos
  - Features estadísticas para clasificación

### **🖥️ src/gui/** - Interfaz Gráfica
- **`main_window.py`** - **Ventana principal del sistema**:
  - Implementa `QMainWindow` con sistema de pestañas
  - Pestaña "Desarrollo" para captura y entrenamiento de datos
  - Pestaña "Producción" para uso final (actualmente placeholder)
  - Gestión centralizada de interfaces y navegación

#### **src/gui/development/**
- **`dev_interface.py`** - **Interfaz completa de desarrollo** (165 líneas):
  - Controles de cámara: Iniciar/Detener con manejo de estados
  - Selector de acciones: dropdown con 5 acciones predefinidas
  - Sistema de captura con countdown visual
  - Display en tiempo real del feed de cámara con poses superpuestas
  - Indicadores de progreso durante captura
  - Manejo robusto de errores y estados de la cámara

#### **src/gui/components/**, **src/gui/data/**, **src/gui/production/**
- Directorios con archivos `__init__.py` (placeholders para futuras expansiones)

### **🤖 src/ml/** - Machine Learning
#### **src/ml/training/**
- **`random_forest_trainer.py`** - Placeholder para entrenador de Random Forest

#### **src/ml/evaluation/**
- **`model_evaluator.py`** - Placeholder para evaluación de modelos (métricas, validación cruzada)

#### **src/ml/inference/**
- **`action_classifier.py`** - Placeholder para clasificación en tiempo real

### **⚡ src/preprocessing/** - Preprocesamiento de Datos
- **`data_reshaper.py`** - **Reorganizador de datos CSV** (77 líneas):
  - Procesa carpetas con archivos CSV de poses capturadas
  - Reshapea matrices de 33x3 (33 joints × xyz) → vectores de 99 elementos
  - Genera nombres de columnas estructurados: `joint0_x`, `joint0_y`, `joint0_z`, etc.
  - Consolida múltiples capturas en archivos CSV únicos
  - Validación automática de formatos y manejo de archivos vacíos

- **`missing_data_imputer.py`** - **Sistema de imputación de datos faltantes** (47 líneas):
  - Detecta archivos CSV con menos de 33 filas (joints faltantes)
  - Implementa imputación por K-Nearest Neighbors (K=3)
  - Completa datos faltantes duplicando filas hasta alcanzar 33 joints
  - Validación de datos numéricos y manejo de errores

### **🛠️ src/utils/** - Utilidades
- **`helpers.py`** - Placeholder para funciones de utilidad común
- **`skeleton_viewer.py`** - **Visualizador 3D de esqueletos** (100 líneas):
  - Diccionario completo de 33 joints de MediaPipe Pose en español
  - Mapeo anatómico preciso: desde "Nariz" hasta "Dedo del Pie Derecho"
  - Conexiones anatómicas correctas para renderizado de esqueleto
  - Visualización interactiva 3D usando Matplotlib
  - Etiquetado automático de puntos con nombres de joints

### **📊 data/** - Datos del Sistema
#### **data/raw/** - Datos Crudos Capturados
Estructura automática generada por el sistema:
```
acción_YYYY_MM_DD_HH_MM_SS/
├── capture_1.csv    # Frame 1: [joint_id, x, y, z] × 33 joints
├── capture_2.csv    # Frame 2: datos del siguiente frame
├── ...
└── capture_150.csv  # Frame 150: último frame de la secuencia
```

**Ejemplos de carpetas existentes:**
- **`aplaudir_2025_09_26_12_53_21/`** - 150 archivos CSV con datos de acción "aplaudir"
- **`dibujar circulo_2025_09_26_12_56_53/`** - Datos de acción "dibujar círculo"
- **`saludar_2025_09_26_12_53_39/`** - Datos de acción "saludar"
- **`sentadilla_2025_09_26_12_57_16/`** - Datos de acción "sentadilla"
- **`vieneviene_2025_09_26_12_56_04/`** - Datos de acción "viene-viene"

**Formato de datos CSV:** Cada archivo contiene 33-34 filas (una por joint detectado) con 4 columnas:
- Columna 0: ID del joint (0-32)
- Columna 1: Coordenada X (píxeles)
- Columna 2: Coordenada Y (píxeles)  
- Columna 3: Coordenada Z (metros, profundidad RealSense)

### **🧪 tests/** - Pruebas
- **`test_example.py`** - Archivo placeholder para tests unitarios

### **📁 __pycache__/**
- **`PoseDetector.cpython-311.pyc`** - Bytecode compilado de Python

## 🎯 Acciones Soportadas

El sistema está configurado para reconocer las siguientes acciones:
1. **Aplaudir** - Movimiento de palmadas
2. **Saludar** - Gesto de saludo con la mano
3. **Viene-viene** - Gesto de llamar con la mano
4. **Dibujar círculo** - Movimiento circular con el brazo
5. **Sentadilla** - Ejercicio de flexión de piernas

## 🔧 Flujo de Trabajo del Sistema

### 1. **Captura de Datos**
- Ejecutar interfaz de desarrollo
- Seleccionar acción a capturar
- Iniciar cámara RealSense
- Capturar 5 segundos de datos (150 frames)
- Datos se guardan automáticamente en `data/raw/`

### 2. **Preprocesamiento**
- Ejecutar `data_reshaper.py` para reorganizar datos
- Ejecutar `missing_data_imputer.py` para completar datos faltantes
- Validar formato y calidad de datos

### 3. **Entrenamiento** (En desarrollo)
- Extraer características con `skeleton_features.py`
- Entrenar modelo con `random_forest_trainer.py`
- Evaluar rendimiento con `model_evaluator.py`

### 4. **Inferencia** (En desarrollo)
- Usar `action_classifier.py` para reconocimiento en tiempo real
- Interfaz de producción para usuarios finales

## 📋 Estado del Proyecto

### ✅ **Implementado**
- ✅ Sistema completo de captura de datos
- ✅ Interfaz gráfica funcional
- ✅ Detección de poses con MediaPipe
- ✅ Integración con cámaras RealSense
- ✅ Preprocesamiento y limpieza de datos
- ✅ Visualización 3D de esqueletos
- ✅ Almacenamiento estructurado de datos

### 🚧 **En Desarrollo**
- 🚧 Extracción de características avanzadas
- 🚧 Entrenamiento de modelos ML
- 🚧 Sistema de clasificación en tiempo real
- 🚧 Interfaz de producción
- 🚧 Tests unitarios completos

## 👨‍💻 Desarrollo y Contribución

Este es un proyecto de investigación en **reconocimiento de acciones corporales** que combina:
- Visión por computadora (OpenCV, MediaPipe)
- Sensores de profundidad (Intel RealSense)
- Machine Learning (Scikit-learn)
- Interfaces gráficas (PyQt5)
- Procesamiento de datos 3D

El código está estructurado de manera modular para facilitar la extensión y el mantenimiento, con una clara separación entre captura, procesamiento, ML e interfaces.
