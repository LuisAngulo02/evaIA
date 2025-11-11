# EvalExpo AI - Sistema de Evaluación de Presentaciones con IA

Sistema integral de evaluación de presentaciones académicas que utiliza inteligencia artificial avanzada para analizar y calificar exposiciones de estudiantes, proporcionando retroalimentación automatizada sobre contenido, fluidez, lenguaje corporal y participación.

---

## Tabla de Contenidos

1. [Guía de Instalación](#guía-de-instalación)
2. [Guía de Uso](#guía-de-uso)
3. [Guía Técnica](#guía-técnica)

---

## Guía de Instalación

### Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.11.9** (recomendado - versión probada y estable)
- **PostgreSQL** 12 o superior
- **Git** para clonar el repositorio
- **FFmpeg** para procesamiento de video/audio
- **pip** actualizado (versión 23.0 o superior)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/LuisAngulo02/evaIA.git
cd evaIA
```

### Paso 2: Crear Entorno Virtual con Python 3.11.9

Es **crucial** utilizar Python 3.11.9 para garantizar la compatibilidad con todas las dependencias, especialmente TensorFlow 2.18.0 y PyTorch 2.5.1.

#### En Windows (PowerShell):

```powershell
# Verificar que tienes Python 3.11.9 instalado
python --version

# Crear el entorno virtual
py -3.11 -m venv venv

# Activar el entorno virtual
.\venv\Scripts\Activate.ps1
```

#### En Linux/macOS:

```bash
# Verificar que tienes Python 3.11.9 instalado
python3.11 --version

# Crear el entorno virtual
python3.11 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

> **Nota**: Si no tienes Python 3.11.9, descárgalo desde [python.org](https://www.python.org/downloads/release/python-3119/)

### Paso 3: Instalar Dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

> **Tiempo estimado**: 10-15 minutos dependiendo de tu conexión a internet.

### Paso 4: Configurar la Base de Datos PostgreSQL

1. **Crear la base de datos**:

```sql
CREATE DATABASE sist_evaluacion_expo_db;
CREATE USER postgres WITH PASSWORD 'tu_contraseña';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sist_evaluacion_expo_db TO postgres;
```

2. **Configurar las credenciales** en el archivo `.env` (ver siguiente paso).

### Paso 5: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Django Configuration
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True

# Database Configuration
DB_NAME=sist_evaluacion_expo_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

# Cloudinary Configuration (para almacenamiento de archivos)
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# Groq API Configuration (para IA)
GROQ_API_KEY=tu_groq_api_key

# OpenAI API Configuration (opcional)
OPENAI_API_KEY=tu_openai_api_key
```

> **Importante**: No compartas tu archivo `.env` públicamente. Ya está incluido en `.gitignore`.

### Paso 6: Ejecutar Migraciones

```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar las migraciones a la base de datos
python manage.py migrate
```

### Paso 7: Crear Superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones en pantalla para crear tu cuenta de administrador.

### Paso 8: Recopilar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### Paso 9: Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

El sistema estará disponible en: **http://127.0.0.1:8000/**

Panel de administración: **http://127.0.0.1:8000/admin/**

---

## Guía de Uso

### Roles del Sistema

El sistema cuenta con tres tipos de usuarios principales:

#### 1. **Administradores**
- Gestión completa del sistema
- Creación y administración de usuarios
- Configuración de parámetros del sistema
- Acceso al panel de Django Admin

#### 2. **Docentes**
- Crear y gestionar cursos
- Crear asignaciones de presentaciones
- Revisar y calificar presentaciones
- Ver reportes de estudiantes
- Recibir notificaciones de nuevas presentaciones

#### 3. **Estudiantes**
- Inscribirse en cursos
- Subir presentaciones en video
- Ver retroalimentación de IA
- Ver calificaciones y comentarios
- Acceder a estadísticas personales

### Flujo de Trabajo Principal

#### Para Docentes:

1. **Crear un Curso**:
   - Navegar a "Mis Cursos" → "Crear Nuevo Curso"
   - Completar información: nombre, descripción, código
   - Guardar el curso

2. **Crear una Asignación**:
   - Desde el curso, ir a "Nueva Asignación"
   - Definir título, descripción, fecha de entrega
   - Configurar parámetros de evaluación
   - Publicar la asignación

3. **Evaluar Presentaciones**:
   - Ir a "Presentaciones Pendientes"
   - Seleccionar una presentación
   - Revisar análisis de IA (automático)
   - Ajustar calificación si es necesario
   - Agregar comentarios adicionales
   - Guardar evaluación

4. **Ver Reportes**:
   - Acceder a "Reportes"
   - Filtrar por curso, estudiante o fecha
   - Exportar datos en Excel o PDF

#### Para Estudiantes:

1. **Inscribirse en un Curso**:
   - Ir a "Cursos Disponibles"
   - Buscar el curso por código o nombre
   - Hacer clic en "Inscribirse"

2. **Subir una Presentación**:
   - Navegar a "Mis Asignaciones"
   - Seleccionar la asignación activa
   - Hacer clic en "Subir Presentación"
   - Subir archivo de video (MP4, AVI, MOV)
   - Agregar información de participantes (si es grupal)
   - Confirmar envío

3. **Ver Retroalimentación**:
   - Ir a "Mis Presentaciones"
   - Seleccionar una presentación evaluada
   - Ver calificación automática de IA
   - Ver comentarios del docente
   - Revisar análisis detallado:
     - Fluidez y coherencia
     - Lenguaje corporal
     - Participación individual
     - Calidad vocal

4. **Consultar Estadísticas**:
   - Acceder a "Mi Dashboard"
   - Ver progreso en cursos
   - Comparar desempeño histórico
   - Identificar áreas de mejora

### Funcionalidades Clave

#### Análisis Automático de IA

El sistema analiza automáticamente cada presentación evaluando:

- **Transcripción de Audio**: Convierte el audio en texto usando Whisper de OpenAI
- **Análisis de Contenido**: Evalúa coherencia, claridad y profundidad temática con modelos de lenguaje (Groq)
- **Detección Facial**: Identifica y rastrea participantes usando MediaPipe y DeepFace
- **Análisis de Lenguaje Corporal**: Evalúa postura, gestos y contacto visual
- **Análisis de Voz**: Mide fluidez, pausas, tono y claridad
- **Detección de Participación**: Calcula tiempo de participación individual en presentaciones grupales

#### Sistema de Notificaciones

- Notificaciones en tiempo real
- Alertas de nuevas asignaciones
- Avisos de presentaciones calificadas
- Recordatorios de fechas límite

#### Reportes y Estadísticas

- Reportes individuales por estudiante
- Reportes grupales por curso
- Gráficos de progreso temporal
- Exportación a Excel y PDF

---

## Guía Técnica

### Arquitectura del Sistema

#### Stack Tecnológico

**Backend:**
- **Framework**: Django 5.2.7 (Python)
- **Base de Datos**: PostgreSQL
- **ORM**: Django ORM
- **API**: Django REST Framework (para endpoints internos)

**Frontend:**
- **Templates**: Django Templates (Jinja2)
- **CSS**: CSS personalizado + Bootstrap
- **JavaScript**: JavaScript vanilla + jQuery

**Inteligencia Artificial:**
- **Modelos de Lenguaje**: Groq API (LLaMA 3.1 70B)
- **Transcripción**: OpenAI Whisper (modelo large-v3)
- **Reconocimiento Facial**: DeepFace con Facenet512 (512-dim embeddings)
- **Detección Facial**: MediaPipe Face Detection + Face Mesh
- **Embeddings de Texto**: Sentence Transformers
- **Visión por Computadora**: OpenCV 4.9.0.80
- **Deep Learning**: TensorFlow 2.18.0, PyTorch 2.5.1
- **Análisis de Coherencia**: Sistema de verificación temática estricta

**Almacenamiento:**
- **Archivos Estáticos**: Cloudinary
- **Archivos Locales**: Sistema de archivos local (desarrollo)

### Estructura del Proyecto

```
evaIA/
├── manage.py                      # Script principal de Django
├── requirements.txt               # Dependencias del proyecto
├── setup.py                       # Configuración de instalación
├── .env                          # Variables de entorno (no versionado)
├── .gitignore                    # Archivos ignorados por Git
│
├── sist_evaluacion_expo/         # Configuración principal
│   ├── settings.py               # Configuración de Django
│   ├── urls.py                   # URLs principales
│   ├── wsgi.py                   # Punto de entrada WSGI
│   └── asgi.py                   # Punto de entrada ASGI
│
├── authentication/               # Módulo de autenticación
│   ├── models.py                 # Modelo de Usuario personalizado
│   ├── views.py                  # Vistas de login/registro
│   ├── forms.py                  # Formularios de autenticación
│   ├── urls.py                   # URLs de autenticación
│   └── decoradores.py            # Decoradores de permisos
│
├── apps/                         # Aplicaciones del sistema
│   ├── presentaciones/           # Módulo principal de presentaciones
│   │   ├── models.py             # Modelos: Presentation, Assignment, etc.
│   │   ├── views.py              # Vistas de presentaciones
│   │   ├── forms.py              # Formularios de presentaciones
│   │   ├── ai_utils.py           # Utilidades de IA
│   │   ├── tasks.py              # Tareas asíncronas (Celery)
│   │   └── services/             # Servicios de procesamiento
│   │       ├── video_processor.py
│   │       ├── audio_processor.py
│   │       ├── face_detector.py
│   │       └── ai_evaluator.py
│   │
│   ├── reportes/                 # Módulo de reportes
│   │   ├── models.py
│   │   ├── views.py
│   │   └── utils.py
│   │
│   ├── notifications/            # Sistema de notificaciones
│   │   ├── models.py
│   │   ├── services.py
│   │   └── signals.py
│   │
│   ├── ai_processor/             # Procesamiento de IA centralizado
│   │   └── services/
│   │
│   └── help/                     # Sistema de ayuda
│
├── templates/                    # Plantillas HTML
│   ├── base.html                 # Plantilla base
│   ├── base_auth.html            # Plantilla para autenticación
│   ├── presentations/            # Templates de presentaciones
│   ├── courses/                  # Templates de cursos
│   ├── dashboard/                # Templates del dashboard
│   └── reportes/                 # Templates de reportes
│
├── static/                       # Archivos estáticos
│   ├── css/                      # Estilos CSS
│   └── js/                       # Scripts JavaScript
│
├── uploads/                      # Archivos subidos localmente
│   ├── presentations/            # Videos de presentaciones
│   ├── thumbnails/               # Miniaturas de videos
│   ├── participant_photos/       # Fotos de participantes
│   └── avatars/                  # Avatares de usuarios
│
└── docs/                         # Documentación técnica
    ├── ARQUITECTURA_SISTEMA.md
    ├── OPTIMIZACION_RENDIMIENTO.md
    └── ... (otros documentos técnicos)
```

### Modelos de Datos Principales

#### Usuario (CustomUser)
```python
- id: UUID
- username: str
- email: str
- first_name: str
- last_name: str
- role: str (ADMIN, TEACHER, STUDENT)
- avatar: ImageField
- created_at: DateTime
- updated_at: DateTime
```

#### Curso (Course)
```python
- id: UUID
- name: str
- code: str (único)
- description: TextField
- teacher: ForeignKey(User)
- students: ManyToManyField(User)
- created_at: DateTime
- is_active: bool
```

#### Asignación (Assignment)
```python
- id: UUID
- title: str
- description: TextField
- course: ForeignKey(Course)
- due_date: DateTime
- max_participants: int
- min_duration: int (minutos)
- max_duration: int (minutos)
- created_at: DateTime
```

#### Presentación (Presentation)
```python
- id: UUID
- assignment: ForeignKey(Assignment)
- video_file: FileField
- thumbnail: ImageField
- status: str (PENDING, PROCESSING, COMPLETED, ERROR)
- duration: int (segundos)
- uploaded_by: ForeignKey(User)
- uploaded_at: DateTime
- processed_at: DateTime
```

#### Participante (Participant)
```python
- id: UUID
- presentation: ForeignKey(Presentation)
- student: ForeignKey(User)
- photo: ImageField
- participation_percentage: float
- speaking_time: int (segundos)
- facial_landmarks_data: JSONField
```

#### Evaluación (Evaluation)
```python
- id: UUID
- presentation: ForeignKey(Presentation)
- ai_score: float (0-100)
- final_score: float (0-100)
- content_score: float
- fluency_score: float
- body_language_score: float
- voice_quality_score: float
- ai_feedback: TextField
- teacher_feedback: TextField
- evaluated_by: ForeignKey(User)
- evaluated_at: DateTime
```

### Pipeline de Procesamiento de IA

El sistema procesa las presentaciones en video siguiendo este pipeline:

```
1. UPLOAD
   ↓
2. VIDEO VALIDATION
   - Formato válido (MP4, AVI, MOV)
   - Duración dentro de límites
   - Tamaño máximo: 500MB
   ↓
3. AUDIO EXTRACTION
   - Extracción de audio con MoviePy
   - Conversión a WAV mono 16kHz
   ↓
4. TRANSCRIPTION (Whisper)
   - Transcripción automática
   - Detección de idioma
   - Timestamps por segmento
   ↓
5. FACE DETECTION & TRACKING
   - Detección facial con MediaPipe
   - Tracking de rostros por frame
   - Extracción de landmarks faciales
   - Clustering jerárquico para identificación
   ↓
6. PARTICIPANT IDENTIFICATION
   - Matching con fotos de participantes (DeepFace)
   - Cálculo de tiempo de participación
   - Generación de estadísticas individuales
   ↓
7. CONTENT ANALYSIS (Groq/LLaMA)
   - Análisis de coherencia temática
   - Evaluación de profundidad
   - Detección de estructura lógica
   ↓
8. VOICE ANALYSIS
   - Análisis de fluidez
   - Detección de pausas
   - Medición de tono y velocidad
   ↓
9. BODY LANGUAGE ANALYSIS
   - Análisis de postura
   - Detección de gestos
   - Evaluación de contacto visual
   ↓
10. SCORE CALCULATION
    - Ponderación de criterios
    - Cálculo de score final de IA
    - Generación de retroalimentación
    ↓
11. STORAGE & NOTIFICATION
    - Guardar evaluación en BD
    - Notificar a estudiante y docente
    - Actualizar estadísticas
```

### Algoritmos Clave

#### 1. Detección y Agrupación de Rostros (V12 Optimizado)

**Archivo**: `apps/ai_processor/services/face_detection_service.py`

**Tecnología**: 
- **Detección**: MediaPipe Face Detection + Face Mesh
- **Embeddings**: DeepFace con Facenet512 (512 dimensiones)
- **Clustering**: Jerárquico con Distancia de Ward

**Optimizaciones de Rendimiento** (Noviembre 2025):

```python
# Sample Rate Agresivo (procesa solo 3-5 fps):
60 fps → sample_rate=15 (~4 fps procesados) 
30 fps → sample_rate=8  (~4 fps procesados)
<25 fps → sample_rate=5  (~5 fps procesados)

# Detección más estricta (reduce falsos positivos):
min_detection_confidence = 0.50  # Antes: 0.40
max_num_faces = 3                # Antes: 5
min_tracking_confidence = 0.6    # Face Mesh

# Thresholds de Similitud (Facenet512):
tracking_threshold = 0.30        # Seguimiento de rostros
template_threshold = 0.15        # Actualización de templates
fusion_threshold = 0.12          # Fusión de duplicados

# Caché de Embeddings:
- Hash MD5 de ROIs faciales (32x32 grayscale)
- Eficiencia: 40-60% cache hits
- 2-3x speedup en extracción
```

**Rendimiento**:
- Video de 3 minutos @ 30fps: **2-4 minutos** de procesamiento
- Speedup total: **2.5-5x** vs versión sin optimizaciones
- Reducción de frames procesados: **60-70%**
- CPU usage: 10-20% (single-thread optimizado)

**Ventajas**:
- No requiere número predefinido de personas
- Robusto ante variaciones de iluminación y rotaciones
- Maneja oclusión parcial
- Procesamiento ultra-rápido sin sacrificar precisión

#### 2. Análisis de Contenido con LLM (Groq) - Sistema Mejorado

**Archivo**: `apps/ai_processor/services/advanced_coherence_service.py`

**Modelo**: LLaMA 3.1 70B vía Groq API

**Mejoras Implementadas** (Noviembre 2025):

```python
# Verificación Temática Prioritaria (NUEVO):
1. PRIMERO: Verifica si el estudiante habla del tema asignado
2. SEGUNDO: Si el tema es correcto, evalúa profundidad y calidad  
3. TERCERO: Si el tema es incorrecto, califica bajo independiente del esfuerzo

# Niveles de Evaluación:
- ESTRICTO: 0% si tema diferente, 85-100% solo con dominio excepcional
- MODERADO: 0-30% si tema diferente, 70-95% si tema correcto
- SUAVE: 0-40% si tema diferente, 70-95% si tema correcto con esfuerzo

# Criterios de Evaluación (ponderados):
1. Coherencia Temática (40%): ¿Habla del tema correcto?
2. Comprensión y Profundidad (30%): ¿Demuestra dominio del tema?
3. Relevancia del Contenido (20%): ¿Información valiosa y pertinente?
4. Estructura y Claridad (10%): ¿Bien organizado y expresado?
```

**Prompt Engineering**:
```
⚠️ VERIFICACIÓN TEMÁTICA PRIORITARIA:
✅ SI habla del tema asignado → Valora esfuerzo y calidad
❌ SI habla de OTRO tema → Califica bajo sin importar el esfuerzo
⚠️ SI menciona tema pero divaga → Califica medio
```

**Output**: JSON estructurado con scores detallados, feedback constructivo, fortalezas, mejoras y conceptos clave

#### 3. Cálculo de Participación Individual

**Archivo**: `apps/presentaciones/services/participation_calculator.py`

```python
# Fórmula:
participation_percentage = (speaking_time / total_video_duration) * 100

# Consideraciones:
- Detección de rostro visible y centrado
- Filtrado de falsos positivos
- Umbral mínimo de confianza: 0.7
```

### APIs y Servicios Externos

#### Groq API
- **Propósito**: Análisis de contenido con LLaMA
- **Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
- **Autenticación**: API Key
- **Rate Limits**: 30 req/min (tier gratuito)

#### OpenAI Whisper
- **Propósito**: Transcripción de audio
- **Modelo**: `whisper-1`
- **Formato**: Audio WAV 16kHz mono
- **Idiomas**: Español, Inglés (automático)

#### Cloudinary
- **Propósito**: Almacenamiento de archivos multimedia
- **Configuración**: `CLOUDINARY_URL` en `.env`
- **Transformaciones**: Redimensionado de imágenes, generación de thumbnails

#### DeepFace
- **Propósito**: Reconocimiento facial y extracción de embeddings
- **Modelo**: Facenet512 (512 dimensiones)
- **Backend**: TensorFlow 2.18.0
- **Métricas**: Similitud coseno
- **Rendimiento**: 150-200ms por rostro (con caché: 40-60% hits)
- **Thresholds**: 0.30 (tracking), 0.15 (template), 0.12 (fusion)

### Configuración Avanzada

#### Variables de Entorno Completas

```env
# Django Core
SECRET_KEY=tu_clave_secreta_larga_y_aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sist_evaluacion_expo_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

# Cloudinary
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# AI APIs
GROQ_API_KEY_1=gsk_...  # Key principal
GROQ_API_KEY_2=gsk_...  # Backup key 2
GROQ_API_KEY_3=gsk_...  # Backup key 3
GROQ_API_KEY_4=gsk_...  # Backup key 4
GROQ_API_KEY_5=gsk_...  # Backup key 5
GROQ_API_KEY=gsk_...    # Alias para compatibilidad
OPENAI_API_KEY=sk-...

# Email Configuration (Gmail)
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_16_chars

# Media Settings
MEDIA_ROOT=./uploads/
MEDIA_URL=/media/
MAX_UPLOAD_SIZE=524288000  # 500MB en bytes

# Face Detection Optimizations (V12 - Noviembre 2025)
FACE_DETECTION_CONFIDENCE=0.50          # Detección estricta (antes: 0.40)
FACE_MESH_CONFIDENCE=0.75               # Face Mesh estricto (antes: 0.70)
MAX_FACES_PER_FRAME=3                   # Máx rostros simultáneos (antes: 5)
FACE_TRACKING_THRESHOLD=0.30            # Threshold para tracking (Facenet512)
FACE_TEMPLATE_THRESHOLD=0.15            # Threshold para templates
FACE_FUSION_THRESHOLD=0.12              # Threshold para fusión de duplicados
EMBEDDING_CACHE_ENABLED=True            # Caché de embeddings (40-60% hits)

# Sample Rate Configuration (procesar menos frames = más rápido)
SAMPLE_RATE_60FPS=15    # 60fps → ~4 fps procesados
SAMPLE_RATE_30FPS=8     # 30fps → ~4 fps procesados  
SAMPLE_RATE_LOW=5       # <25fps → ~5 fps procesados

# Coherence Analysis (Groq)
COHERENCE_STRICTNESS=moderate  # strict, moderate, lenient
USE_ADVANCED_COHERENCE=True    # Sistema de verificación temática

# Celery (opcional para tareas asíncronas)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

#### Configuración de PostgreSQL para Producción

```sql
-- Optimizaciones recomendadas
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;

-- Recargar configuración
SELECT pg_reload_conf();
```

#### Optimización de Rendimiento

**1. Caché con Redis (opcional)**:
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

**2. Compresión de Respuestas**:
```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... otros middleware
]
```

**3. Índices de Base de Datos**:
```python
# Agregar en models.py
class Meta:
    indexes = [
        models.Index(fields=['status', 'created_at']),
        models.Index(fields=['course', 'due_date']),
    ]
```

### Testing

#### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests de una app específica
python manage.py test apps.presentaciones

# Tests con cobertura
coverage run --source='.' manage.py test
coverage report
coverage html
```

#### Tests Disponibles

- **Unit Tests**: Pruebas de modelos y funciones individuales
- **Integration Tests**: Pruebas de flujos completos
- **API Tests**: Pruebas de endpoints
- **AI Tests**: Pruebas de procesamiento de IA (`test_face_detection.py`)

### Deployment (Producción)

#### Preparación para Producción

1. **Configurar DEBUG=False**:
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']
```

2. **Configurar HTTPS**:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

3. **Configurar servidor WSGI** (Gunicorn):
```bash
pip install gunicorn
gunicorn sist_evaluacion_expo.wsgi:application --bind 0.0.0.0:8000
```

4. **Configurar servidor web** (Nginx):
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /ruta/a/staticfiles/;
    }

    location /media/ {
        alias /ruta/a/uploads/;
    }
}
```

### Solución de Problemas Comunes

#### Problema: Error al instalar TensorFlow en Windows

**Error**: `Could not find a version that satisfies the requirement tensorflow`

**Solución**: Asegúrate de usar Python 3.11.9 exactamente:
```bash
python --version  # Debe ser 3.11.9
pip install --upgrade pip
pip install tensorflow==2.18.0
```

#### Problema: UnicodeDecodeError al conectar con PostgreSQL

**Error**: `'utf-8' codec can't decode byte 0xf3 in position 85`

**Solución**: Verifica que tu contraseña de PostgreSQL no tenga caracteres especiales o usa variables de entorno:
```bash
# En .env
DB_PASSWORD=tu_password_sin_caracteres_especiales

# O en PowerShell, configura codificación UTF-8:
$env:PYTHONIOENCODING = "utf-8"
```

#### Problema: Error "protobuf version conflict" con MediaPipe

**Error**: `Failed to parse text-format mediapipe.CalculatorGraphConfig`

**Solución**: MediaPipe requiere protobuf <5.0.0:
```bash
pip uninstall protobuf
pip install protobuf==4.25.5
```

#### Problema: Error de memoria al procesar videos largos

**Solución**: Ajustar límites o usar sample rate más agresivo:
```python
# settings.py
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000

# O aumentar sample_rate en .env para procesar menos frames
SAMPLE_RATE_30FPS=10  # Procesar aún menos frames
```

#### Problema: Face detection no encuentra rostros

**Solución 1**: Reducir threshold de confianza:
```python
# .env
FACE_DETECTION_CONFIDENCE=0.40  # Más permisivo (default: 0.50)
```

**Solución 2**: Verificar calidad del video:
- Resolución mínima: 640x480
- Rostros visibles y bien iluminados
- Formato compatible: MP4, AVI, MOV

#### Problema: Groq API rate limit exceeded

**Error**: `Rate limit reached for requests`

**Solución**: El sistema usa rotación automática de 5 API keys. Verifica que todas estén configuradas:
```env
# .env - Configura las 5 keys
GROQ_API_KEY_1=gsk_...
GROQ_API_KEY_2=gsk_...
GROQ_API_KEY_3=gsk_...
GROQ_API_KEY_4=gsk_...
GROQ_API_KEY_5=gsk_...
```

O implementa retry con backoff:
```python
import time
from groq import RateLimitError

max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.chat.completions.create(...)
        break
    except RateLimitError:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Espera exponencial
```

#### Problema: Procesamiento muy lento (>10 minutos para 3 min de video)

**Solución**: Verificar que las optimizaciones estén activas:

```bash
# Verificar versión del servicio
python -c "from apps.ai_processor.services import FaceDetectionService; print(FaceDetectionService.__module__)"

# Debe imprimir: apps.ai_processor.services.face_detection_service

# Verificar que sample_rate sea agresivo
grep -r "sample_rate = 15" apps/ai_processor/services/face_detection_service.py
# O en Windows PowerShell:
Select-String -Path "apps\ai_processor\services\face_detection_service.py" -Pattern "sample_rate = 15"
```

Si el procesamiento sigue lento:
1. Verifica que `min_detection_confidence=0.50` (más estricto = más rápido)
2. Verifica que `max_num_faces=3` (menos rostros = más rápido)
3. Revisa que el video tenga buena calidad y resolución adecuada

#### Problema: Git rebase conflict al hacer push

**Error**: `Updates were rejected because the remote contains work`

**Solución**:
```bash
# Opción 1: Rebase (recomendado)
git pull --rebase origin main
# Resolver conflictos si aparecen
git add .
git rebase --continue
git push origin main

# Opción 2: Merge (más simple)
git pull origin main --no-rebase
git push origin main

# Opción 3: Force push (solo si estás seguro)
git push origin main --force
```

### Mantenimiento

#### Backup de Base de Datos

```bash
# Crear backup
pg_dump -U postgres -d sist_evaluacion_expo_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
psql -U postgres -d sist_evaluacion_expo_db < backup_20250109.sql
```

#### Limpieza de Archivos Antiguos

```bash
# Eliminar presentaciones procesadas hace más de 6 meses
python manage.py shell
>>> from apps.presentaciones.models import Presentation
>>> from datetime import datetime, timedelta
>>> old_date = datetime.now() - timedelta(days=180)
>>> Presentation.objects.filter(processed_at__lt=old_date).delete()
```

#### Monitoreo de Logs

```bash
# Ver logs en tiempo real
tail -f logs/django.log

# Filtrar errores
grep ERROR logs/django.log
```

---

## Documentación Adicional

Para información técnica más detallada, consulta la carpeta `docs/`:

- **ARQUITECTURA_SISTEMA.md**: Documentación completa de la arquitectura
- **OPTIMIZACION_RENDIMIENTO.md**: Guías de optimización
- **MEJORAS_DETECCION_ROSTROS.md**: Mejoras en detección facial

---

## Contribución

Si deseas contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## Licencia

Este proyecto es privado y confidencial. Todos los derechos reservados.

