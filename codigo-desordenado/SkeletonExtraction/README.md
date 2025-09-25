# Action Recognition System

Sistema de reconocimiento de acciones humanas usando esqueletos 3D capturados con cámaras RealSense y clasificación con Random Forest.

## Estructura del Proyecto

```
SkeletonExtraction/
├── src/                           # Código fuente principal
│   ├── capture/                   # Captura de datos en tiempo real
│   │   ├── realtime_capture_system.py  # Sistema de captura multi-cámara
│   │   └── pose_detector.py       # Detector de poses MediaPipe
│   ├── preprocessing/             # Preprocesamiento de datos
│   │   ├── data_reshaper.py       # Reestructuración de CSVs
│   │   └── missing_data_imputer.py # Imputación de datos faltantes
│   ├── feature_extraction/        # Extracción de características
│   │   └── skeleton_features.py   # Características de esqueletos
│   ├── ml/                        # Machine Learning
│   │   ├── training/               # Entrenamiento de modelos
│   │   │   └── random_forest_trainer.py
│   │   ├── evaluation/             # Evaluación de modelos
│   │   │   └── model_evaluator.py
│   │   └── inference/              # Inferencia en tiempo real
│   │       └── action_classifier.py
│   ├── gui/                       # Interfaz gráfica PyQt
│   │   ├── main_window.py         # Ventana principal
│   │   ├── development/           # Interfaz de desarrollo
│   │   │   └── dev_interface.py
│   │   ├── production/            # Interfaz de producción
│   │   │   └── prod_interface.py
│   │   └── components/            # Componentes reutilizables
│   │       └── widgets.py
│   └── utils/                     # Utilidades
│       └── helpers.py
├── data/                          # Datos del proyecto
│   ├── raw/                       # Datos crudos capturados
│   ├── processed/                 # Datos procesados
│   ├── features/                  # Características extraídas
│   ├── train/                     # Datos de entrenamiento
│   └── test/                      # Datos de prueba
├── models/                        # Modelos entrenados
├── config/                        # Archivos de configuración
├── tests/                         # Pruebas unitarias
└── docs/                          # Documentación
```

## Funcionalidades

### Modo Desarrollo
- Captura y etiquetado de datos
- Preprocesamiento y limpieza
- Entrenamiento de modelos
- Evaluación y métricas
- Visualización de datos y resultados

### Modo Producción
- Captura en tiempo real (5 segundos)
- Clasificación automática de acciones
- Interfaz simplificada para usuario final

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```python
# Ejecutar interfaz principal
python main.py
```