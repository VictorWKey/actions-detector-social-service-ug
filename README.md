# Sistema de Recon└── 📁 utils/             # Utilidades y constantes
       └── joint_utils.py     # Diccionarios y funciones auxiliares
   └── 📁 legacy_tools/      # Herramientas para datos históricos
       ├── legacy_processor.py # Procesamiento de datos antiguos
       └── skeleton_visualizer.py # Visualización 3D y animacionesimiento de Actividades Humanas

Sistema automatizado para capturar, procesar y clasificar actividades humanas usando cámaras Intel RealSense y análisis de esqueleto 3D.

## 🏗️ Estructura del Proyecto

```
📁 proyecto/
├── 📁 src/                    # Código fuente modular
│   ├── 📁 capture/           # Captura de datos con RealSense
│   │   ├── pose_detector.py   # Detección de poses con MediaPipe
│   │   └── realsense_capture.py # Captura con cámaras RealSense
│   ├── 📁 preprocessing/     # Preprocesamiento de datos
│   │   └── data_cleaner.py    # Limpieza y normalización
│   ├── 📁 features/          # Extracción de características
│   │   └── feature_extractor.py # Cálculo de distancias y velocidades
│   ├── 📁 classification/    # Clasificación de actividades
│   │   └── activity_classifier.py # Modelo ML para clasificación
│   └── 📁 utils/             # Utilidades y constantes
│       └── joint_utils.py     # Diccionarios y funciones auxiliares
├── 📁 models/                # Modelos entrenados
├── 📁 temp_data/             # Datos temporales de captura
├── main.py                   # Sistema principal
├── requirements.txt          # Dependencias
└── README.md                # Este archivo
```

## 🚀 Instalación

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Conectar cámara Intel RealSense**

3. **Ejecutar el sistema:**
   ```bash
   python main.py
   ```

## 🎮 Uso del Sistema

### Comandos Disponibles

- **`detectar`**: Inicia el proceso completo de detección de actividad
- **`entrenar`**: Entrena el modelo con un dataset existente
- **`estado`**: Muestra el estado actual del sistema
- **`legacy`**: Herramientas para procesar datos históricos
- **`visualizar`**: Herramientas de visualización 3D y animaciones
- **`salir`**: Termina el programa

### Flujo de Detección

1. **Captura** (10 segundos con RealSense)
   - Detección de 33 joints del esqueleto
   - Coordenadas 3D (x, y, z) por frame
   - ~300 frames capturados

2. **Preprocesamiento**
   - Limpieza de anomalías
   - Submuestreo a 100 frames
   - Imputación de valores faltantes
   - Cálculo de punto de espina (centroide)

3. **Extracción de Características**
   - Distancias de 8 joints hacia la espina
   - Velocidades de cambio entre frames
   - 64 características estadísticas (media, varianza, máx, mín)

4. **Clasificación**
   - Modelo Random Forest entrenado
   - Predicción de actividad con probabilidades

## 🎯 Actividades Detectables

El sistema puede detectar actividades como:
- Aplaudir
- Saludar  
- Sentarse
- Pararse
- Martillar
- Tomar agua
- Y más...

## 📊 Modelo de Machine Learning

- **Algoritmo**: Random Forest Classifier
- **Características**: 64 features extraídas de distancias y velocidades
- **Normalización**: StandardScaler
- **Evaluación**: Accuracy score y classification report

## 🔧 Componentes Técnicos

### PoseDetector
- Utiliza MediaPipe para detectar 33 joints del cuerpo
- Genera esqueleto 2D y obtiene coordenadas de pixels

### RealSenseCapture  
- Integra cámaras Intel RealSense
- Combina RGB + Depth para obtener coordenadas 3D reales
- Captura sincronizada de múltiples cámaras

### DataPreprocessor
- Detección y limpieza de outliers
- Submuestreo uniforme
- Imputación KNN para valores faltantes
- Cálculo de punto de referencia (espina)

### FeatureExtractor
- Cálculo de 8 distancias euclidianas hacia la espina
- Cálculo de velocidades entre frames consecutivos  
- Extracción de estadísticas descriptivas

### ActivityClassifier
- Modelo Random Forest para clasificación multiclase
- Normalización de características
- Predicción con probabilidades por clase

## 🛠️ Desarrollo

### Agregar Nueva Actividad
1. Capturar datos de la nueva actividad
2. Procesar con el pipeline existente
3. Agregar al dataset de entrenamiento
4. Re-entrenar el modelo

### Personalizar Características
Modificar `FeatureExtractor` para:
- Agregar nuevos joints objetivo
- Cambiar métricas estadísticas
- Incluir características temporales adicionales

## 📋 Requisitos del Sistema

- **Hardware**: Cámara Intel RealSense (D415, D435, etc.)
- **SO**: Windows 10/11, Linux, macOS
- **Python**: 3.8+
- **RAM**: 4GB mínimo, 8GB recomendado
- **Espacio**: 2GB para dependencias y modelos

## 🐛 Solución de Problemas

### Error: "No RealSense device connected"
- Verificar conexión USB de la cámara
- Instalar Intel RealSense SDK
- Verificar drivers de la cámara

### Error: Import "mediapipe" could not be resolved
- Instalar dependencias: `pip install -r requirements.txt`
- Verificar versión de Python compatible

### Baja precisión del modelo
- Capturar más datos de entrenamiento
- Verificar calidad de las capturas
- Ajustar parámetros del modelo

## 📈 Mejoras Futuras

- [ ] Detección en tiempo real sin guardar archivos
- [ ] Interfaz gráfica de usuario
- [ ] Soporte para más tipos de cámaras
- [ ] Detección de múltiples personas
- [ ] Análisis de secuencias temporales más complejas
- [ ] Exportación de modelos optimizados

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## 👥 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request
