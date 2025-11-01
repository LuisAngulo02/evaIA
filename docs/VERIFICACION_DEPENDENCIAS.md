# 📦 Verificación de Dependencias - EvalExpo AI

## Scripts de Verificación Disponibles

### 1. `verificar_dependencias.py` - Verifica paquetes Python
Verifica que todas las dependencias de Python estén instaladas correctamente.

```bash
python verificar_dependencias.py
```

**Verifica:**
- ✅ Framework Web (Django, PostgreSQL)
- ✅ IA (Whisper, Groq, Transformers)
- ✅ Procesamiento Video/Imagen (MediaPipe, OpenCV, MoviePy)
- ✅ Procesamiento Audio (Librosa, Pydub)
- ✅ Machine Learning (PyTorch, Scikit-learn)
- ✅ Reportes (Pandas, Matplotlib, ReportLab)
- ✅ Almacenamiento (Cloudinary)

### 2. `verificar_sistema.py` - Verifica configuración completa
Verifica toda la configuración del sistema incluyendo APIs y base de datos.

```bash
python verificar_sistema.py
```

**Verifica:**
- ✅ Variables de entorno (.env)
- ✅ Configuración de Email (Gmail)
- ✅ Cloudinary (almacenamiento en nube)
- ✅ Base de datos PostgreSQL
- ✅ Groq API (análisis de coherencia)
- ✅ Archivos multimedia
- ✅ Configuración de seguridad

---

## Dependencias Críticas por Funcionalidad

### 🎤 Transcripción de Audio (Whisper)

**Paquetes necesarios:**
```
openai-whisper==20250625
torch>=2.0.0
torchaudio>=2.0.0
numpy>=1.20.0
ffmpeg (via imageio-ffmpeg)
```

**Uso en el proyecto:**
- `apps/ai_processor/services/transcription_service.py`
- `apps/presentaciones/views.py` (proceso de transcripción)

**Verificación:**
```python
import whisper
model = whisper.load_model("base")
print("✅ Whisper funcionando")
```

**Problemas comunes:**
- ❌ FFmpeg no encontrado → Instalar: `pip install imageio-ffmpeg`
- ❌ Muy lento → Usar modelo más pequeño (`tiny`, `base`)
- ❌ Error de memoria → Reducir tamaño del modelo o aumentar RAM

---

### 👁️ Detección Facial (MediaPipe)

**Paquetes necesarios:**
```
mediapipe==0.10.21
opencv-python>=4.0.0
opencv-contrib-python>=4.0.0
numpy>=1.20.0
```

**Uso en el proyecto:**
- `apps/ai_processor/services/face_detection_mediapipe.py`
- `apps/ai_processor/services/face_detection_service.py`
- `apps/ai_processor/services/liveness_detection_service.py`

**Verificación:**
```python
import mediapipe as mp
import cv2

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
print("✅ MediaPipe funcionando")
```

**Problemas comunes:**
- ❌ Error en Windows → Instalar Visual C++ Redistributable
- ❌ `cannot import name 'modelBuilder'` → Reinstalar: `pip install mediapipe==0.10.21`
- ❌ Detección lenta → Reducir `sample_rate` en el servicio

---

### 🤖 Análisis de Coherencia (Groq API)

**Paquetes necesarios:**
```
groq==0.32.0
httpx>=0.20.0
pydantic>=2.0.0
```

**Configuración requerida:**
```env
GROQ_API_KEY=gsk_...
```

**Uso en el proyecto:**
- `apps/ai_processor/services/advanced_coherence_service.py`

**Verificación:**
```python
from groq import Groq
import os

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "test"}]
)
print("✅ Groq API funcionando")
```

**Problemas comunes:**
- ❌ API Key inválida → Verificar en https://console.groq.com
- ❌ Timeout → Aumentar timeout en settings.py
- ❌ Modelo no disponible → Usar `llama-3.3-70b-versatile` (actualizado)

---

### 🎬 Procesamiento de Video (MoviePy + OpenCV)

**Paquetes necesarios:**
```
moviepy==2.2.1
opencv-python==4.12.0.88
imageio==2.37.0
imageio-ffmpeg==0.6.0
numpy>=1.20.0
```

**Uso en el proyecto:**
- `apps/ai_processor/services/transcription_service.py` (extracción de audio)
- Procesamiento de frames de video

**Verificación:**
```python
import cv2
from moviepy.editor import VideoFileClip
import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
print(f"✅ FFmpeg: {ffmpeg_path}")
print("✅ MoviePy y OpenCV funcionando")
```

**Problemas comunes:**
- ❌ FFmpeg no encontrado → Instalar: `pip install imageio-ffmpeg`
- ❌ Error con codec → Actualizar: `pip install --upgrade imageio-ffmpeg`
- ❌ Video sin duración (WebM) → Usar extracción directa con subprocess

---

### 🧠 Modelos NLP (Transformers)

**Paquetes necesarios:**
```
transformers==4.57.0
sentence-transformers==5.1.1
torch>=2.0.0
tokenizers==0.22.1
safetensors>=0.6.0
```

**Uso en el proyecto:**
- Análisis semántico de textos
- Embeddings para comparación de contenido

**Verificación:**
```python
from transformers import pipeline
from sentence_transformers import SentenceTransformer

# Test transformers
print("✅ Transformers funcionando")

# Test sentence-transformers
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Sentence-Transformers funcionando")
```

**Problemas comunes:**
- ❌ Descarga lenta de modelos → Primera vez tarda en descargar
- ❌ Error de memoria → Usar modelos más pequeños
- ❌ Error de tokenizer → Actualizar: `pip install --upgrade tokenizers`

---

### 📊 Generación de Reportes

**Paquetes necesarios:**
```
reportlab==4.4.4
pandas==2.3.3
matplotlib==3.10.7
openpyxl==3.1.5
```

**Uso en el proyecto:**
- `apps/reportes/views.py` (generación de PDFs y Excel)

**Verificación:**
```python
from reportlab.pdfgen import canvas
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

print("✅ Reportes funcionando")
```

---

### ☁️ Almacenamiento en Nube (Cloudinary)

**Paquetes necesarios:**
```
cloudinary==1.44.1
django-cloudinary-storage==0.3.0
```

**Configuración requerida:**
```env
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

**Uso en el proyecto:**
- Almacenamiento de videos de presentaciones
- Almacenamiento de fotos de participantes

**Verificación:**
```python
import cloudinary
import cloudinary.api

cloudinary.config(
    cloud_name="tu_cloud_name",
    api_key="tu_api_key",
    api_secret="tu_api_secret"
)

result = cloudinary.api.ping()
print("✅ Cloudinary funcionando")
```

**Problemas comunes:**
- ❌ Credenciales inválidas → Verificar en dashboard de Cloudinary
- ❌ Límite de almacenamiento → Plan gratuito tiene límites
- ⚠️ Opcional → Sistema funciona con almacenamiento local

---

## Checklist de Verificación Completa

### Paso 1: Verificar Instalación de Paquetes
```bash
python verificar_dependencias.py
```

Debe mostrar:
- ✅ 95%+ de paquetes instalados
- ✅ Todos los componentes críticos OK
- ✅ FFmpeg ejecutable encontrado

### Paso 2: Verificar Configuración del Sistema
```bash
python verificar_sistema.py
```

Debe verificar:
- ✅ Variables de entorno configuradas
- ✅ Email configurado
- ✅ Base de datos conectada
- ✅ APIs de IA funcionando

### Paso 3: Probar Componentes Individuales

**Test Whisper:**
```python
import whisper
model = whisper.load_model("base")
# Debe cargar sin errores
```

**Test MediaPipe:**
```python
import mediapipe as mp
mp_face = mp.solutions.face_detection
# Debe importar sin errores
```

**Test Groq API:**
```python
from groq import Groq
client = Groq(api_key="tu_api_key")
# Debe inicializar sin errores
```

**Test FFmpeg:**
```python
import imageio_ffmpeg
print(imageio_ffmpeg.get_ffmpeg_exe())
# Debe mostrar ruta al ejecutable
```

### Paso 4: Verificar Base de Datos
```bash
python manage.py migrate
# Debe ejecutar sin errores
```

### Paso 5: Iniciar Servidor
```bash
python manage.py runserver
# Debe iniciar en http://127.0.0.1:8000
```

---

## Tabla de Dependencias por Archivo

| Archivo | Dependencias Críticas |
|---------|----------------------|
| `transcription_service.py` | whisper, imageio-ffmpeg, moviepy, subprocess |
| `face_detection_mediapipe.py` | mediapipe, cv2, numpy |
| `advanced_coherence_service.py` | groq, pydantic |
| `face_detection_service.py` | cv2, mediapipe (opcional) |
| `liveness_detection_service.py` | cv2, numpy |
| `views.py` (presentaciones) | cloudinary, whisper, Django |
| `views.py` (reportes) | reportlab, pandas, matplotlib, openpyxl |

---

## Resolución de Problemas por Síntomas

### 🔴 Síntoma: Transcripción falla con "FFmpeg not found"
**Solución:**
```bash
pip install --upgrade imageio-ffmpeg
```

### 🔴 Síntoma: MediaPipe error "cannot import name 'modelBuilder'"
**Solución:**
```bash
pip uninstall mediapipe
pip install mediapipe==0.10.21
```

### 🔴 Síntoma: Groq API timeout
**Solución:**
Editar `sist_evaluacion_expo/settings.py`:
```python
COHERENCE_CONFIG = {
    'timeout': 60,  # Aumentar de 45 a 60
}
```

### 🔴 Síntoma: PyTorch muy lento (CPU)
**Solución:**
- Usar modelos más pequeños
- Considerar instalación con soporte CUDA (GPU NVIDIA)

### 🔴 Síntoma: Error de memoria al procesar video
**Solución:**
- Reducir `sample_rate` en MediaPipe
- Procesar videos más cortos
- Aumentar RAM del sistema

---

## Comandos Útiles

### Reinstalar todas las dependencias
```bash
pip install --upgrade --force-reinstall -r requirements.txt
```

### Ver versión de un paquete
```bash
pip show whisper
pip show mediapipe
pip show groq
```

### Limpiar caché de pip
```bash
pip cache purge
```

### Crear nuevo requirements.txt
```bash
pip freeze > requirements_nuevo.txt
```

### Verificar paquetes desactualizados
```bash
pip list --outdated
```

---

## Estado Esperado

Después de una instalación exitosa:

✅ **Python:** 3.10+ instalado y en PATH  
✅ **Entorno virtual:** Creado y activado  
✅ **Dependencias:** 100+ paquetes instalados (~4 GB)  
✅ **FFmpeg:** Disponible vía imageio-ffmpeg  
✅ **PostgreSQL:** Base de datos creada y conectada  
✅ **Variables .env:** Configuradas  
✅ **Migraciones:** Ejecutadas sin errores  
✅ **Servidor:** Inicia correctamente  

**Total de tiempo de setup:** 10-20 minutos (primera vez)

---

## Contacto y Soporte

Si después de verificar todo sigue habiendo problemas:

1. Ejecuta ambos scripts de verificación
2. Guarda la salida completa
3. Revisa los logs de error específicos
4. Busca el error en la documentación oficial del paquete

**Documentación oficial:**
- Whisper: https://github.com/openai/whisper
- MediaPipe: https://google.github.io/mediapipe/
- Groq: https://console.groq.com/docs
- Django: https://docs.djangoproject.com/
