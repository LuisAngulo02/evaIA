# 🧹 Limpieza de Servicios - Octubre 2025

## 📋 Resumen de Cambios

### ✅ Archivo Movido a Backup

**Archivo**: `face_detection_mediapipe.py`
- **Razón**: Implementación alternativa que nunca se integró al flujo principal
- **Ubicación nueva**: `apps/ai_processor/services/backups/`
- **Impacto**: NINGUNO - No se usaba en ninguna parte del código

### 🔍 Verificación Realizada

Se verificó que el archivo **NO** estaba siendo importado o usado en:
- ❌ `ai_service.py` - Usa `FaceDetectionService` 
- ❌ `tasks.py` - No lo importa
- ❌ `views.py` - No lo referencia
- ✅ Solo estaba en `__init__.py` pero nunca se usaba

---

## 📁 Estructura Final de Servicios

```
apps/ai_processor/services/
├── __init__.py                         ✅ Actualizado (removida importación)
├── ai_service.py                       ✅ Servicio principal/orquestador
├── transcription_service.py            ✅ Transcripción con Groq Whisper
├── face_detection_service.py           ✅ ACTIVO - Detección facial avanzada
├── coherence_analyzer.py               ✅ Analizador de coherencia (orquestador)
├── advanced_coherence_service.py       ✅ Motor de IA con Groq Llama
├── audio_segmentation_service.py       ✅ Segmentación de audio por participante
├── liveness_detection_service.py       ✅ Detección de video en vivo vs grabado
├── cloudinary_service.py               ✅ Gestión de almacenamiento en la nube
├── groq_key_manager.py                 ✅ Rotación de API keys
└── backups/                            📁 Archivos antiguos
    └── face_detection_mediapipe.py     ⚠️ Implementación alternativa no usada
```

---

## 🎯 Servicios Activos (Explicación)

### 1. **ai_service.py** 🧠
**Rol**: Orquestador principal del análisis de presentaciones

**Coordina**:
- Transcripción de audio
- Detección de rostros y participantes
- Análisis de coherencia
- Cálculo de calificaciones
- Guardado en base de datos

**Usa**:
```python
from .transcription_service import TranscriptionService
from .face_detection_service import FaceDetectionService
from .coherence_analyzer import CoherenceAnalyzer
```

---

### 2. **face_detection_service.py** 👤
**Rol**: Detección y seguimiento de participantes en video

**Tecnologías**:
- MediaPipe (detección avanzada)
- OpenCV (procesamiento de frames)
- Clustering visual (agrupación de rostros)

**Características**:
- Detecta múltiples rostros simultáneos
- Sistema de tracking sofisticado
- Comparación visual de rostros
- Cálculo de tiempo de participación
- Guarda fotos de participantes
- Configuración personalizable por docente

**NO confundir con**: `face_detection_mediapipe.py` (backup - versión simplificada no usada)

---

### 3. **transcription_service.py** 🎤
**Rol**: Conversión de audio a texto

**Tecnología**: Groq Whisper Large V3

**Funciones**:
- Extrae audio del video
- Transcribe audio completo
- Transcribe segmentos por participante
- Maneja chunks para límites de API

---

### 4. **coherence_analyzer.py** 📊
**Rol**: Orquestador del análisis de coherencia

**Sistema de Fallback**:
1. **Primero**: Intenta usar `AdvancedCoherenceService` (Groq IA)
2. **Si falla**: Usa Sentence Transformers (embeddings)
3. **Último recurso**: Análisis básico

**Responsabilidades**:
- Calcular coherencia semántica
- Detectar palabras clave
- Evaluar profundidad
- Generar puntajes finales
- Crear reportes individuales

---

### 5. **advanced_coherence_service.py** 🤖
**Rol**: Motor de IA puro para análisis semántico

**Tecnología**: Groq Llama 3.3 70B

**Usado por**: `coherence_analyzer.py`

**Características**:
- Análisis profundo con LLM
- Evaluación de relevancia temática
- Generación de feedback detallado
- Sistema de rotación de API keys

**NO es duplicado**: Es el motor especializado usado POR coherence_analyzer

---

### 6. **audio_segmentation_service.py** ✂️
**Rol**: Dividir audio por participante

**Función**:
- Recibe transcripción con timestamps
- Asocia segmentos a cada participante
- Extrae fragmentos de audio individuales

---

### 7. **liveness_detection_service.py** 🎬
**Rol**: Detectar si el video es en vivo o pregrabado

**Analiza**:
- Movimientos naturales vs artificiales
- Patrones de edición
- Continuidad temporal
- Características de cámara en vivo

---

### 8. **cloudinary_service.py** ☁️
**Rol**: Gestión de archivos en la nube

**Funciones**:
- Upload de videos a Cloudinary
- Generación de URLs seguras
- Conversión de formatos
- Eliminación de archivos

---

### 9. **groq_key_manager.py** 🔑
**Rol**: Gestión y rotación de API keys

**Características**:
- Maneja hasta 5 API keys de Groq
- Rotación automática en caso de rate limit
- Fallback inteligente
- Seguimiento de uso por key

---

## 🔄 Flujo de Procesamiento Completo

```
📹 VIDEO SUBIDO
    ↓
┌─────────────────────────────────────────────┐
│   ai_service.py (ORQUESTADOR PRINCIPAL)     │
└─────────────────────────────────────────────┘
    ↓
    ├→ 1. cloudinary_service.py
    │      └→ Descarga video si está en cloud
    │
    ├→ 2. transcription_service.py
    │      └→ Extrae audio
    │      └→ Transcribe con Groq Whisper
    │      └→ Retorna texto + timestamps
    │
    ├→ 3. face_detection_service.py
    │      └→ Detecta rostros con MediaPipe
    │      └→ Agrupa participantes (clustering)
    │      └→ Calcula tiempos de participación
    │      └→ Guarda fotos de cada persona
    │
    ├→ 4. audio_segmentation_service.py
    │      └→ Divide audio por participante
    │      └→ Asigna transcripción a cada uno
    │
    ├→ 5. coherence_analyzer.py
    │      ├→ advanced_coherence_service.py
    │      │     └→ Análisis con Groq Llama 3.3
    │      │     └→ Evalúa coherencia temática
    │      │     └→ Genera feedback
    │      │
    │      └→ Calcula puntajes finales
    │      └→ Genera calificaciones individuales
    │
    ├→ 6. liveness_detection_service.py
    │      └→ Detecta si es en vivo
    │      └→ Score de liveness
    │
    └→ 7. Guarda resultados en BD
           └→ Presentation
           └→ Participant (cada persona)
```

---

## ⚠️ NO Eliminar Estos Archivos

Todos los archivos actuales en `services/` son necesarios:

```
✅ ai_service.py                    (Cerebro del sistema)
✅ transcription_service.py         (Whisper)
✅ face_detection_service.py        (Detección facial ACTIVA)
✅ coherence_analyzer.py            (Orquestador de coherencia)
✅ advanced_coherence_service.py    (Motor de IA)
✅ audio_segmentation_service.py    (Segmentación)
✅ liveness_detection_service.py    (Anti-trampa)
✅ cloudinary_service.py            (Cloud storage)
✅ groq_key_manager.py             (Gestión de keys)
✅ __init__.py                      (Imports)
```

---

## 📊 Comparación: ¿Por qué 2 servicios de coherencia?

### `coherence_analyzer.py` vs `advanced_coherence_service.py`

**NO son duplicados**, son complementarios:

| Aspecto | coherence_analyzer.py | advanced_coherence_service.py |
|---------|----------------------|------------------------------|
| **Rol** | Orquestador | Motor de IA especializado |
| **Propósito** | Gestionar todo el análisis | Solo interactuar con Groq API |
| **Dependencias** | Usa AdvancedCoherenceService | Usa Groq SDK directamente |
| **Fallbacks** | Sí (3 niveles) | No (solo Groq) |
| **Calcula scores** | Sí (finales ponderados) | No (solo análisis semántico) |
| **Genera reportes** | Sí (individuales y grupales) | No |
| **Usado por** | ai_service.py | coherence_analyzer.py |

**Analogía**:
- `coherence_analyzer` = Director de orquesta
- `advanced_coherence_service` = Violinista especializado

---

## 📊 Comparación: ¿Por qué teníamos 2 servicios de detección facial?

### `face_detection_service.py` vs `face_detection_mediapipe.py` (ELIMINADO)

| Aspecto | face_detection_service.py ✅ | face_detection_mediapipe.py ❌ |
|---------|------------------------------|-------------------------------|
| **Estado** | ACTIVO | BACKUP (no usado) |
| **Líneas** | ~850 | ~340 |
| **Tecnología** | MediaPipe + OpenCV + Clustering | Solo MediaPipe |
| **Tracking** | Sistema avanzado | Básico |
| **Comparación** | Visual (histogramas) | No implementado |
| **Fotos** | Guarda fotos | No guarda |
| **Config** | Personalizable | Fija |
| **Usado en** | ai_service.py | Ninguna parte |

**Conclusión**: `face_detection_mediapipe.py` era una implementación simplificada que nunca se terminó de integrar.

---

## ✅ Verificación Post-Limpieza

### Tests Realizados:

1. ✅ Verificar imports en `__init__.py`
2. ✅ Buscar referencias en todo el código
3. ✅ Comprobar errores de sintaxis
4. ✅ Confirmar que `ai_service.py` no rompe

### Resultado:
```
✅ No hay errores
✅ Sistema funcional
✅ Archivo duplicado movido a backup
✅ __init__.py actualizado correctamente
```

---

## 🎯 Próximos Pasos (Opcional)

Si quieres seguir limpiando:

1. **Revisar archivos en otras carpetas**:
   ```bash
   # Buscar otros posibles duplicados
   Get-ChildItem -Recurse -Filter "*backup*"
   Get-ChildItem -Recurse -Filter "*old*"
   Get-ChildItem -Recurse -Filter "*temp*"
   ```

2. **Limpiar archivos `.pyc`**:
   ```bash
   Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item
   ```

3. **Revisar migraciones antiguas** (si tienes muchas)

---

## 📞 Contacto

Si necesitas restaurar `face_detection_mediapipe.py`:
```bash
# Desde: apps/ai_processor/services/
Move-Item "backups\face_detection_mediapipe.py" "."
```

Pero **NO** es necesario, el sistema funciona perfectamente sin él.

---

**Fecha de limpieza**: 22 de Octubre 2025  
**Archivos movidos**: 1  
**Archivos eliminados**: 0  
**Sistema**: ✅ Funcionando correctamente

---

¡Repositorio más limpio y organizado! 🎉
