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

- **Python 3.11.8** (obligatorio)
- **PostgreSQL** 12 o superior
- **Git** para clonar el repositorio
- **FFmpeg** para procesamiento de video
- **pip** actualizado

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/LuisAngulo02/evaIA.git
cd evaIA
```

### Paso 2: Crear Entorno Virtual con Python 3.11.8

Es **crucial** utilizar Python 3.11.8 para garantizar la compatibilidad con todas las dependencias, especialmente TensorFlow y PyTorch.

#### En Windows (PowerShell):

```powershell
# Verificar que tienes Python 3.11.8 instalado
python --version

# Crear el entorno virtual
py -3.11 -m venv venv

# Activar el entorno virtual
.\venv\Scripts\Activate.ps1
```

#### En Linux/macOS:

```bash
# Verificar que tienes Python 3.11.8 instalado
python3.11 --version

# Crear el entorno virtual
python3.11 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

> **Nota**: Si no tienes Python 3.11.8, descárgalo desde [python.org](https://www.python.org/downloads/release/python-3118/)

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
- **Modelos de Lenguaje**: Groq API (LLaMA 3.1)
- **Transcripción**: OpenAI Whisper
- **Embeddings**: Sentence Transformers
- **Visión por Computadora**: OpenCV, MediaPipe, DeepFace
- **Deep Learning**: TensorFlow 2.16+, PyTorch 2.5.1

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

#### 1. Detección y Agrupación de Rostros (Hierarchical Clustering)

**Archivo**: `apps/presentaciones/services/face_detector.py`

**Método**: Clustering Jerárquico con Distancia de Ward

```python
# Proceso:
1. Detectar rostros en cada frame (MediaPipe)
2. Extraer embeddings faciales (DeepFace - VGG-Face)
3. Calcular matriz de distancias entre embeddings
4. Aplicar clustering jerárquico
5. Determinar número óptimo de clusters (personas)
6. Asignar cada detección a una persona
```

**Ventajas**:
- No requiere número predefinido de personas
- Robusto ante variaciones de iluminación
- Maneja rotaciones y parcial oclusión

#### 2. Análisis de Contenido con LLM (Groq)

**Archivo**: `apps/presentaciones/ai_utils.py`

**Modelo**: LLaMA 3.1 70B vía Groq API

```python
# Prompt Engineering:
- Contexto: Transcripción completa
- Criterios: Coherencia, claridad, profundidad
- Output: JSON estructurado con scores y feedback
```

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
- **Propósito**: Reconocimiento facial
- **Modelo**: VGG-Face
- **Backend**: TensorFlow
- **Métricas**: Cosine similarity

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
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=sk-...

# Media Settings
MEDIA_ROOT=./uploads/
MEDIA_URL=/media/
MAX_UPLOAD_SIZE=524288000  # 500MB en bytes

# Processing Settings
FACE_DETECTION_CONFIDENCE=0.7
MIN_FACE_DETECTION_SIZE=50
CLUSTERING_LINKAGE=ward
CLUSTERING_METRIC=euclidean

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

#### Problema: Error al instalar TensorFlow

**Solución**: Asegúrate de usar Python 3.11.8 exactamente:
```bash
python --version  # Debe ser 3.11.8
pip install tensorflow==2.16.0
```

#### Problema: Error de memoria al procesar videos largos

**Solución**: Procesar por chunks o aumentar límites:
```python
# settings.py
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000
```

#### Problema: Face detection no encuentra rostros

**Solución**: Verificar calidad de video y ajustar threshold:
```python
# ai_utils.py
FACE_DETECTION_CONFIDENCE = 0.5  # Reducir para mayor sensibilidad
```

#### Problema: Groq API rate limit exceeded

**Solución**: Implementar retry con backoff exponencial:
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
            time.sleep(2 ** attempt)
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
- **V11_HIERARCHICAL_CLUSTERING_SOLUCION_DEFINITIVA.md**: Detalles del algoritmo de clustering
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

---

## Autores

- **Luis Angulo** - Desarrollo principal - [@LuisAngulo02](https://github.com/LuisAngulo02)

---

## Contacto

Para soporte o consultas, contacta a: [tu-email@ejemplo.com]

---

## Roadmap

### Próximas Funcionalidades

- [ ] Soporte para presentaciones en vivo (streaming)
- [ ] Análisis de emociones en tiempo real
- [ ] Integración con Microsoft Teams / Zoom
- [ ] App móvil (iOS/Android)
- [ ] Soporte multiidioma completo
- [ ] Dashboard avanzado con gráficos interactivos
- [ ] Sistema de gamificación para estudiantes
- [ ] API REST pública para integraciones

---

**Versión**: 1.0.0  
**Última actualización**: Noviembre 2025  
**Python requerido**: 3.11.8 (exacto)  
**Django**: 5.2.7
