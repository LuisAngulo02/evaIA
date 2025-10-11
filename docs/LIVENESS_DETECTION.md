# 🎥 Sistema de Detección de Liveness y Grabación en Vivo

## 📋 Descripción General

Este módulo implementa dos funcionalidades clave:

1. **Detección de Liveness:** Analiza videos para determinar si fueron grabados en vivo o son material pregrabado
2. **Grabación en Vivo:** Permite a los estudiantes grabar presentaciones directamente desde su navegador

Cumple con el objetivo específico del proyecto:
> **"Verificar si la exposición es en vivo o corresponde a material previamente grabado"**

---

## ✨ Funcionalidades Principales

### 1. 🔍 Detección de Liveness

Analiza múltiples aspectos del video para determinar su autenticidad:

#### Métodos de Detección:
- ✅ **Análisis de ruido de cámara** (videos en vivo tienen más ruido natural)
- ✅ **Variaciones de brillo** (luz natural vs iluminación artificial)
- ✅ **Patrones de movimiento** (movimientos naturales vs edición)
- ✅ **Análisis temporal** (consistencia a lo largo del tiempo)
- ✅ **Metadatos del archivo** (timestamps de creación/modificación)

####Scoring System:
- **Score 75-100:** Grabación en vivo (LIVE)
- **Score 50-74:** Probablemente en vivo (LIKELY_LIVE)
- **Score 25-49:** Probablemente pregrabado (LIKELY_RECORDED)
- **Score 0-24:** Pregrabado (RECORDED)

### 2. 🎬 Grabación en Vivo

Interfaz web completa para grabar directamente desde el navegador:

#### Características:
- ✅ Acceso directo a cámara y micrófono
- ✅ Vista previa en tiempo real
- ✅ Countdown de 3 segundos antes de grabar
- ✅ Controles de grabación (iniciar, pausar, reanudar, detener)
- ✅ Timer en tiempo real
- ✅ Límite de duración automático
- ✅ Indicador visual de grabación
- ✅ Subida automática al finalizar

---

## 🏗️ Arquitectura

```
apps/ai_processor/services/
├── liveness_detection_service.py  # ⭐ Servicio de detección
├── ai_service.py                  # Integración con análisis IA
└── __init__.py                    # Exportación de servicios

apps/presentaciones/
├── views.py                       # Vista live_record_view
└── urls.py                        # URL: /presentations/live-record/

templates/presentations/
└── live_record.html               # Interfaz de grabación

test_liveness_detection.py         # Script de prueba
```

---

## 🔧 Uso del Sistema

### Para Estudiantes

#### Opción 1: Grabar en Vivo (Recomendado)

1. Ir al dashboard
2. Clic en **"Grabar en Vivo"**
3. Permitir acceso a cámara y micrófono
4. Clic en **"Iniciar Grabación"**
5. Realizar la presentación
6. Clic en **"Detener y Guardar"**
7. Ingresar título y descripción
8. El video se procesa automáticamente

#### Opción 2: Subir Video Pregrabado

1. Ir al dashboard  
2. Clic en **"Subir Video"**
3. Seleccionar archivo
4. El sistema analizará si es en vivo o pregrabado

### Para Desarrolladores

#### Uso del Servicio de Liveness

```python
from apps.ai_processor.services import LivenessDetectionService

service = LivenessDetectionService()
result = service.analyze_video('/path/to/video.mp4')

if result['success']:
    print(f"Tipo: {result['type_display']}")
    print(f"Score: {result['liveness_score']:.1f}/100")
    print(f"Es en vivo: {result['is_live']}")
```

#### Resultado del Análisis

```python
{
    'success': True,
    'is_live': True,
    'liveness_score': 85.3,
    'confidence': 85.3,
    'recording_type': 'LIVE',
    'type_display': 'En Vivo',
    'details': {
        'metadata_score': 70.0,
        'noise_level': 58.5,
        'brightness_variation': 65.2,
        'motion_consistency': 55.8,
        'temporal_consistency': 72.3
    }
}
```

---

## 🎯 Integración con Sistema de IA

El análisis de liveness se ejecuta automáticamente como parte del flujo de análisis completo:

```python
# En AIService.analyze_presentation()

1. ✅ Transcripción de audio (Whisper AI)
2. ✅ Análisis de coherencia temática
3. ✅ **Detección de liveness** ⭐ NUEVO
4. ✅ Detección de rostros y participación
5. ✅ Generación de feedback
```

### Campos en el Modelo `Presentation`

```python
class Presentation(models.Model):
    # ... campos existentes ...
    
    # Campos de liveness
    is_live_recording = models.BooleanField(default=False)
    liveness_score = models.DecimalField(max_digits=5, decimal_places=2)
    liveness_confidence = models.DecimalField(max_digits=5, decimal_places=2)
    recording_type = models.CharField(
        max_length=20,
        choices=[
            ('LIVE', 'En Vivo'),
            ('LIKELY_LIVE', 'Probablemente en Vivo'),
            ('LIKELY_RECORDED', 'Probablemente Pregrabado'),
            ('RECORDED', 'Pregrabado'),
            ('UNKNOWN', 'Desconocido'),
        ]
    )
```

---

## 🧪 Pruebas

### Test con Script Standalone

```bash
# Con video específico
python test_liveness_detection.py ruta/al/video.mp4

# Buscar automáticamente
python test_liveness_detection.py
```

### Salida Esperada

```
==================================================================
🔍 TEST DE DETECCIÓN DE LIVENESS
==================================================================

📹 Archivo de video: uploads/presentations/test.mp4
📊 Tamaño: 12.45 MB

🚀 Inicializando servicio de detección de liveness...

⏳ Analizando video...
------------------------------------------------------------------
📊 Analizando características del video...
⏳ Analizados 100 frames...
⏳ Analizados 200 frames...
✅ Análisis completado: 300 frames procesados
------------------------------------------------------------------

✅ ANÁLISIS COMPLETADO

==================================================================
📊 RESULTADOS DEL ANÁLISIS DE LIVENESS
==================================================================

🎥 Tipo de grabación detectado: En Vivo
📈 Score de Liveness: 85.3/100
🎯 Confianza: 85.3%
✓  Es grabación en vivo: Sí

==================================================================
💡 INTERPRETACIÓN
==================================================================

✅ GRABACIÓN EN VIVO DETECTADA

Este video muestra características consistentes con una grabación en vivo:
• Alto nivel de ruido natural de cámara
• Variaciones naturales de iluminación
• Patrones de movimiento orgánicos
• Metadatos consistentes con captura directa

==================================================================
🔬 DETALLES TÉCNICOS DEL ANÁLISIS
==================================================================

📊 Nivel de ruido de cámara:
   • Score: 58.5/100
   • Interpretación: Alto (típico de grabación en vivo)

💡 Variación de brillo:
   • Score: 65.2/100
   • Interpretación: Alta variabilidad (luz natural)

🎬 Consistencia de movimiento:
   • Score: 55.8/100

⏱️ Consistencia temporal:
   • Score: 72.3/100
   • Interpretación: Alta variabilidad temporal (natural)

==================================================================
✅ TEST COMPLETADO
==================================================================
```

---

## 📊 Grabación en Vivo - Interfaz Web

### Características de la Interfaz

1. **Vista Previa de Cámara**
   - Stream en tiempo real
   - Resolución 1280x720
   - Auto-detección de dispositivos

2. **Countdown Pre-Grabación**
   - 3, 2, 1... antes de iniciar
   - Overlay visual
   - Animación de pulso

3. **Controles de Grabación**
   ```
   [Iniciar Grabación] → [Pausar] / [Detener y Guardar]
                        ↓
                    [Reanudar]
   ```

4. **Timer en Tiempo Real**
   - Formato HH:MM:SS
   - Cambio de color al acercarse al límite:
     - Verde: < 75% del tiempo
     - Amarillo: 75-90% del tiempo
     - Rojo: > 90% del tiempo

5. **Indicador de Grabación**
   - Dot rojo parpadeante
   - Texto "GRABANDO"
   - Se oculta al pausar

6. **Información del Dispositivo**
   - Nombre de cámara detectada
   - Nombre de micrófono detectado
   - Estado de conexión

7. **Consejos y Recomendaciones**
   - Tips para buena iluminación
   - Posicionamiento de cámara
   - Verificación de audio

### Tecnologías Utilizadas

- **MediaRecorder API:** Captura de video/audio
- **getUserMedia API:** Acceso a dispositivos
- **WebRTC:** Streaming en tiempo real
- **JavaScript Fetch API:** Subida de video

### Formato de Video

- **Codec preferido:** VP9 + Opus
- **Contenedor:** WebM
- **Bitrate:** 2.5 Mbps
- **Fallback:** Formato por defecto del navegador

---

## 🔬 Algoritmo de Detección

### 1. Análisis de Metadatos (Peso: 20%)

```python
# Comparar timestamps de creación y modificación
time_diff = abs(modification_time - creation_time).seconds

if time_diff < 5:     score += 20  # Muy reciente
elif time_diff < 30:  score += 10  # Reciente
elif time_diff > 300: score -= 20  # Muy antiguo
```

### 2. Análisis de Ruido (Peso: 25%)

```python
# Usar operador Laplacian para detectar ruido
laplacian = cv2.Laplacian(gray_frame, cv2.CV_64F)
noise_variance = laplacian.var()

# Videos en vivo: 50-500
# Videos pregrabados: 10-100
```

### 3. Análisis de Brillo (Peso: 20%)

```python
# Calcular variación de brillo entre frames
brightness_diff = np.mean(np.abs(current - previous))

# Alta variación = luz natural (en vivo)
# Baja variación = luz artificial (pregrabado)
```

### 4. Análisis de Movimiento (Peso: 15%)

```python
# Diferencia absoluta entre frames consecutivos
diff = cv2.absdiff(current_gray, prev_gray)
motion_score = np.mean(diff)

# Movimiento natural vs movimiento editado
```

### 5. Consistencia Temporal (Peso: 20%)

```python
# Variabilidad de características a lo largo del tiempo
noise_variability = np.std(noise_levels) / np.mean(noise_levels)

# Alta variabilidad = en vivo
# Baja variabilidad = pregrabado (muy constante)
```

### Score Final

```python
final_score = (
    metadata_score * 0.20 +
    noise_score * 0.25 +
    brightness_score * 0.20 +
    motion_score * 0.15 +
    temporal_score * 0.20
)
```

---

## 📈 Feedback Generado

El sistema genera feedback detallado sobre la autenticidad:

```
🎥 **Autenticidad de la Grabación:**
- Tipo: En Vivo
- Score de Liveness: 85.3/100
- Confianza: 85.3%

✅ Video grabado en vivo detectado

[... resto del análisis ...]
```

---

## ⚙️ Configuración

### Parámetros del LivenessDetectionService

```python
service = LivenessDetectionService()

# Parámetros configurables
service.max_frames_to_analyze = 300  # Analizar primeros 10s
```

### Ajustar Umbrales

En `liveness_detection_service.py`:

```python
# Cambiar umbrales de clasificación
if final_score >= 75:     # Muy seguro que es en vivo
    recording_type = 'LIVE'
elif final_score >= 50:   # Probablemente en vivo
    recording_type = 'LIKELY_LIVE'
# ...
```

---

## 🐛 Troubleshooting

### Problema: "No se pudo acceder a la cámara"

**Causas:**
- Permisos de navegador no otorgados
- Cámara en uso por otra aplicación
- Navegador no soporta MediaRecorder API

**Soluciones:**
1. Verificar permisos en el navegador
2. Cerrar otras apps que usen la cámara
3. Usar navegadores modernos (Chrome, Firefox, Edge)

### Problema: Score de liveness muy bajo para video en vivo

**Causas:**
- Video muy comprimido
- Iluminación muy estable (artificial)
- Edición posterior a la grabación

**Soluciones:**
1. Usar la función "Grabar en Vivo" del sistema
2. Evitar comprimir el video antes de subirlo
3. Grabar con luz natural cuando sea posible

### Problema: "Error subiendo video"

**Causas:**
- Video muy grande
- Timeout de servidor
- Error de red

**Soluciones:**
1. Verificar duración (no exceder máximo)
2. Verificar conexión a internet
3. Intentar nuevamente

---

## 📚 Dependencias

```python
# Análisis de video
opencv-python==4.10.0.84   # Procesamiento de frames
numpy==2.3.1               # Cálculos numéricos

# Django
Django>=5.2.1              # Framework web
```

---

## 🎯 Estado de Implementación

- ✅ **COMPLETADO**: Servicio de detección de liveness
- ✅ **COMPLETADO**: Integración con AIService
- ✅ **COMPLETADO**: Interfaz de grabación en vivo
- ✅ **COMPLETADO**: Almacenamiento en base de datos
- ✅ **COMPLETADO**: Generación de feedback
- ✅ **COMPLETADO**: Scripts de prueba
- ✅ **COMPLETADO**: Documentación completa

---

## 📝 TODO / Mejoras Futuras

- [ ] Optimizar análisis con GPU (CUDA)
- [ ] Análisis de audio para detectar voces sintéticas
- [ ] Detección de deepfakes
- [ ] Soporte para múltiples cámaras
- [ ] Análisis de metadatos EXIF avanzado
- [ ] Machine Learning para mejorar precisión
- [ ] Análisis de compresión de video
- [ ] Detección de pantalla compartida

---

## 📖 Referencias

- [MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder)
- [getUserMedia API](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)
- [OpenCV Video Processing](https://docs.opencv.org/master/dd/d43/tutorial_py_video_display.html)
- [Liveness Detection Techniques](https://en.wikipedia.org/wiki/Liveness_detection)

---

**Última actualización:** Octubre 9, 2025  
**Versión:** 1.0.0  
**Estado:** ✅ Producción Ready
