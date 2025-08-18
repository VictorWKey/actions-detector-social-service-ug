# 🚀 Sistema de Reconocimiento de Actividades - Interfaz Gráfica

## 📋 Descripción

Interfaz gráfica moderna para el sistema de reconocimiento de actividades humanas que reemplaza la interfaz de consola con una aplicación visual intuitiva.

## ✨ Características de la GUI

### 🎯 Panel de Detección

- **Vista en vivo de la cámara**: Ve en tiempo real lo que detecta el sistema
- **Detección de esqueleto**: Visualización de joints y pose en vivo
- **Countdown de 3 segundos**: Tiempo para posicionarte antes de grabar
- **Botón principal**: Inicia la detección de actividad con un solo clic
- **Barra de progreso**: Muestra el progreso en tiempo real durante la captura
- **Resultados visuales**: Muestra la actividad detectada y probabilidades en formato fácil de leer

### 📹 Vista en Vivo de Cámara

- **Transmisión en tiempo real**: Ve exactamente lo que ve la cámara
- **Detección de pose en vivo**: Esqueleto superpuesto en tiempo real
- **Control de cámara**: Botones para iniciar/detener la transmisión
- **Estado visual**: Indicadores claros del estado de la cámara
- **Redimensionamiento automático**: La imagen se ajusta al tamaño de la ventana

### 🎓 Panel de Entrenamiento
- **Selector de dataset**: Interfaz gráfica para seleccionar archivos CSV
- **Entrenamiento con progreso**: Barra de progreso durante el entrenamiento
- **Resultados detallados**: Muestra precisión y clases detectadas

### 🛠️ Herramientas Legacy
- **Limpieza de carpetas**: Botón para ejecutar dataElimination
- **Eliminación de columnas**: Botón para eliminar columnas extra
- **Conversión de CSVs**: Botón para reshapeCSVs

### 📊 Visualización
- **Esqueleto 3D**: Genera visualizaciones 3D de esqueletos
- **Animaciones**: Crea animaciones de movimiento

### 📟 Console de Sistema
- **Log en tiempo real**: Muestra todos los mensajes del sistema
- **Timestamps**: Cada mensaje incluye hora de ejecución
- **Estilo terminal**: Fondo oscuro para mejor legibilidad

## 🚀 Cómo usar

### Instalación
1. Asegúrate de tener Python instalado
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución
#### Opción 1: Archivo batch (Windows)

```bash
start_gui.bat
```

#### Opción 2: Modo Demo (sin cámara)

```bash
start_demo.bat
```

#### Opción 3: Python directo

```bash
python gui_main.py
```

### Uso paso a paso

#### 1. 🔧 Inicialización
- Al abrir la aplicación, el sistema se inicializa automáticamente
- Los indicadores de estado muestran:
  - ✅/❌ Estado de inicialización
  - 📷 Cámaras conectadas
  - 🤖 Estado del modelo
  - 🏷️ Clases disponibles

#### 2. 🎓 Entrenar un modelo (primera vez)
1. Ve a la pestaña "🎓 Entrenamiento"
2. Haz clic en "📂 Buscar" para seleccionar tu archivo CSV de dataset
3. Haz clic en "🚀 ENTRENAR MODELO"
4. Espera a que termine el entrenamiento
5. Los resultados aparecerán en el área de texto

#### 3. 🎯 Detectar actividades

1. Ve a la pestaña "🎯 Detección de Actividades"
2. **NUEVO**: Haz clic en "🎥 Iniciar Cámara" para ver la transmisión en vivo
3. Verifica que puedas verte en la pantalla con el esqueleto detectado
4. Asegúrate de que el modelo esté entrenado (indicador verde)
5. Haz clic en "🚀 INICIAR DETECCIÓN"
6. **NUEVO**: Aparecerá un countdown de 3 segundos para posicionarte
7. El sistema capturará durante 10 segundos mientras ves "🎬 ¡GRABANDO!"
8. Los resultados aparecerán mostrando:
   - Actividad detectada
   - Nivel de confianza
   - Probabilidades de todas las clases

#### 4. 🛠️ Herramientas adicionales
- **Herramientas Legacy**: Para procesar datos antiguos
- **Visualización**: Para crear gráficos y animaciones

## 💡 Ventajas de la GUI

### ✅ Facilidad de uso
- **Sin comandos de texto**: Todo mediante botones e interfaces gráficas
- **Feedback visual**: Barras de progreso y indicadores de estado
- **Mensajes claros**: Ventanas de confirmación y error explicativas

### ✅ Mejor experiencia
- **Interfaz moderna**: Diseño limpio y profesional
- **Organización por pestañas**: Funcionalidades bien separadas
- **Console integrada**: Ver logs sin perder la interfaz principal

### ✅ Robustez
- **Ejecución asíncrona**: No se congela durante operaciones largas
- **Manejo de errores**: Mensajes de error claros y recuperación automática
- **Estado del sistema**: Siempre sabes qué está funcionando

## 🎨 Detalles de diseño

### Colores y estilo
- **Azul principal**: #0078d4 (botones principales)
- **Fondo claro**: #ffffff (áreas de contenido)
- **Texto oscuro**: #323130 (fácil lectura)
- **Console oscura**: #1e1e1e (estilo terminal)

### Tipografía
- **Principal**: Segoe UI (nativa de Windows)
- **Console**: Consolas (fuente monoespaciada)
- **Tamaños**: Jerarquía clara (18pt títulos, 11pt texto)

## 🔧 Resolución de problemas

### Si no inicia la aplicación
1. Verifica que Python esté instalado: `python --version`
2. Instala dependencias: `pip install -r requirements.txt`
3. Ejecuta desde terminal para ver errores: `python gui_main.py`

### Si no detecta cámaras
- Asegúrate de que la cámara RealSense esté conectada
- Verifica que no esté siendo usada por otra aplicación
- Reinicia la aplicación

### Si el entrenamiento falla
- Verifica que el archivo CSV tenga el formato correcto
- Asegúrate de que la última columna sean las etiquetas
- Revisa la console para mensajes de error específicos

## 🆚 Comparación: Console vs GUI

| Característica | Console Anterior | GUI Nueva |
|----------------|------------------|-----------|
| **Facilidad de uso** | Comandos de texto | Botones intuitivos |
| **Feedback visual** | Solo texto | Barras de progreso + texto |
| **Organización** | Menú lineal | Pestañas organizadas |
| **Estado del sistema** | Comandos manuales | Indicadores automáticos |
| **Selección de archivos** | Escritura manual | Selector gráfico |
| **Multitarea** | Bloquea interface | Operaciones asíncronas |
| **Aspecto** | Terminal básica | Interfaz moderna |

## 📝 Notas técnicas

### Arquitectura
- **Tkinter**: GUI nativa de Python (no requiere instalación extra)
- **Threading**: Operaciones largas en hilos separados
- **MVC**: Separación clara entre lógica y presentación

### Compatibilidad
- **Windows**: Completamente compatible
- **macOS/Linux**: Compatible con ajustes menores en estilos

### Rendimiento
- **Memoria**: Similar uso que la versión console
- **CPU**: Mínimo overhead por la GUI
- **Respuesta**: Interfaz siempre responsiva
