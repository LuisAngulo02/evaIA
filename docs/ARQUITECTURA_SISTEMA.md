# DOCUMENTACIÓN COMPLETA DEL SISTEMA EVALEXPO AI

**Última actualización:** Noviembre 2025  
**Versión del Sistema:** 2.0  
**Estado:** Producción

## Tabla de Contenidos
1. [Introducción General](#introducción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Módulos y Componentes](#módulos-y-componentes)
5. [Flujo de Funcionamiento](#flujo-de-funcionamiento)
6. [Base de Datos](#base-de-datos)
7. [Inteligencia Artificial](#inteligencia-artificial)
8. [APIs y Servicios Externos](#apis-y-servicios-externos)
9. [Seguridad y Privacidad](#seguridad-y-privacidad)
10. [Instalación y Configuración](#instalación-y-configuración)

---

## 1. INTRODUCCIÓN GENERAL

### ¿Qué es EvalExpo AI?

**EvalExpo AI** es un sistema integral de evaluación de presentaciones académicas que utiliza inteligencia artificial avanzada para analizar y calificar exposiciones de estudiantes de manera automatizada, objetiva y escalable. El sistema combina múltiples tecnologías de IA de última generación para proporcionar evaluaciones completas y retroalimentación detallada en tiempo real.

### Objetivo Principal

Facilitar la evaluación objetiva, consistente y escalable de presentaciones orales mediante el análisis automatizado de múltiples dimensiones:

**Análisis de Contenido:**
- Coherencia temática con las instrucciones de la asignación
- Relevancia y profundidad del contenido expuesto
- Estructura y organización del discurso
- Calidad argumentativa y ejemplos utilizados

**Análisis de Participación:**
- Detección automática de participantes en presentaciones grupales
- Medición individual de tiempo de participación por persona
- Identificación de participantes activos vs pasivos
- Análisis de distribución equitativa del tiempo

**Análisis de Autenticidad:**
- Detección de videos grabados en vivo vs pregrabados
- Verificación de autenticidad mediante análisis de liveness
- Identificación de patrones de edición o manipulación

**Análisis de Desempeño:**
- Transcripción automática de audio con timestamps
- Análisis de fluidez verbal y pausas
- Evaluación de dicción y claridad del habla
- Detección de muletillas y repeticiones

### Usuarios del Sistema

1. **Estudiantes**: 
   - Suben videos de presentaciones individuales o grupales
   - Reciben retroalimentación automatizada de IA en minutos
   - Consultan calificaciones, estadísticas y reportes personalizados
   - Visualizan análisis detallado de participación

2. **Docentes**: 
   - Crean y gestionan cursos y asignaciones
   - Configuran parámetros de evaluación y nivel de rigurosidad de IA
   - Revisan análisis automatizado de IA antes de calificar
   - Ajustan calificaciones manualmente según su criterio
   - Generan reportes académicos en Excel/PDF

3. **Administradores**: 
   - Gestionan usuarios y asignación de roles
   - Configuran parámetros globales del sistema
   - Monitorean rendimiento y uso de APIs
   - Acceden a estadísticas generales del sistema

---

## 2. ARQUITECTURA DEL SISTEMA

### Patrón de Arquitectura: MVT (Model-View-Template) con Microservicios de IA

El sistema está construido siguiendo el patrón MVT de Django con una arquitectura modular orientada a servicios de IA:

```
┌──────────────────────────────────────────────────────────────────┐
│                        NAVEGADOR WEB                             │
│                  (Chrome, Firefox, Edge, Safari)                 │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTPS Request/Response
                            │ WebSocket (Notificaciones en tiempo real)
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│                     DJANGO WEB SERVER                            │
│                      (Puerto 8000 local)                         │
│                    Gunicorn/uWSGI (Producción)                   │
├──────────────────────────────────────────────────────────────────┤
│  URL Router → Middleware → Views → Context Processors            │
│  Authentication → CSRF → Session → Messages                      │
└───────────────────────────┬──────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌────────────────┐
    │   MODELS     │ │    FORMS     │ │   TEMPLATES    │
    │   (ORM)      │ │ (Validación) │ │   (DTL + JS)   │
    └──────┬───────┘ └──────────────┘ └────────────────┘
           │
           ▼
    ┌─────────────────────────────────────────────────────┐
    │           CAPA DE SERVICIOS DE IA                   │
    ├─────────────────────────────────────────────────────┤
    │  • AIService (Orquestador principal)                │
    │  • TranscriptionService (Whisper)                   │
   │  • FaceDetectionService (MediaPipe + DeepFace)       │
    │  • AdvancedCoherenceService (Groq + Llama 3.3)      │
    │  • LivenessDetectionService (OpenCV)                │
    │  • AudioSegmentationService                         │
    │  • CloudinaryService (Almacenamiento)               │
    │  • NotificationService (Notificaciones)             │
    └────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬──────────────┐
        │            │            │              │
        ▼            ▼            ▼              ▼
┌──────────────┐ ┌─────────┐ ┌──────────┐ ┌────────────┐
│  PostgreSQL  │ │ Caché   │ │ APIs     │ │ Cloudinary │
│  (Base de    │ │ Redis   │ │ Externas │ │ (CDN)      │
│   Datos)     │ │(Progreso│ │          │ │            │
│              │ │ Tareas) │ │ • Groq   │ │            │
│              │ │         │ │ • OpenAI │ │            │
└──────────────┘ └─────────┘ └──────────┘ └────────────┘
```

### Capas del Sistema (Detallado)

#### 1. **Capa de Presentación** (Frontend)
**Tecnologías:**
- **Templates HTML**: Django Template Language (DTL) con herencia jerárquica
- **CSS Framework**: Bootstrap 5.3 + estilos personalizados responsivos
- **JavaScript**: Vanilla JS + Fetch API para interactividad asíncrona
- **Componentes UI**: 
  - Modales dinámicos para calificación y detalles
  - Formularios con validación en tiempo real
  - Tablas con ordenamiento y filtrado
  - Reproductor de video con controles personalizados
  - Barras de progreso para procesamiento de IA
  - Sistema de notificaciones toast en tiempo real

**Características:**
- Diseño responsive (mobile-first)
- Progressive Web App (PWA) ready
- Lazy loading de imágenes y videos
- Optimización de rendimiento con minificación CSS/JS

#### 2. **Capa de Lógica de Negocio** (Backend)
**Componentes Principales:**

**Views (Controladores):**
- `upload_presentation_view`: Subida de videos con validación
- `grade_presentations_view`: Panel de calificación para docentes
- `teacher_dashboard_view`: Dashboard con estadísticas en tiempo real
- `student_reports_view`: Visualización de calificaciones y reportes
- Decoradores personalizados: `@student_required`, `@teacher_required`, `@admin_required`

**Services (Lógica de IA):**
- `AIService`: Orquestador principal del flujo de análisis completo
- `TranscriptionService`: Transcripción de audio con Whisper
- `FaceDetectionService`: Detección y tracking de rostros con MediaPipe/DeepFace
- `AdvancedCoherenceService`: Análisis semántico con Llama 3.3 70B
- `LivenessDetectionService`: Detección de autenticidad de videos
- `AudioSegmentationService`: Segmentación de audio por participante
- `CloudinaryService`: Gestión de almacenamiento en la nube
- `NotificationService`: Sistema de notificaciones push

**Forms (Validación):**
- Validación server-side y client-side
- Sanitización de entradas
- Manejo de archivos multimedia grandes (hasta 100MB)

**Signals (Eventos Automáticos):**
- `post_save` en User → Crear Profile automáticamente
- `pre_save` en Presentation → Validar datos antes de guardar
- Notificaciones automáticas en cambios de estado

#### 3. **Capa de Datos**
**Base de Datos: PostgreSQL 12+**

**Optimizaciones:**
- Índices en campos frecuentemente consultados
- `select_related()` para relaciones ForeignKey
- `prefetch_related()` para relaciones ManyToMany
- Particionamiento de tablas grandes (futuro)
- Backup automático diario

**Caché:**
- Django Cache Framework con Redis (opcional)
- Caché de progreso de procesamiento
- Caché de embeddings de rostros para evitar recálculos

#### 4. **Capa de Servicios Externos**

**Groq API (Análisis de Coherencia):**
- Modelo: Llama 3.3 70B Versatile
- Sistema de rotación automática de API keys (hasta 10 keys)
- Manejo inteligente de rate limits
- Retry automático con backoff exponencial
- Timeout: 45 segundos

**OpenAI Whisper (Transcripción):**
- Modelo: Small (balance velocidad/precisión)
- Procesamiento local (sin enviar a API)
- Soporte para múltiples idiomas
- Extracción de timestamps precisos

**Cloudinary (Almacenamiento CDN):**
- Almacenamiento de videos en la nube
- Generación automática de thumbnails
- Streaming optimizado
- Transcoding automático a múltiples formatos

**MediaPipe + DeepFace (Detección y Reconocimiento Facial):**
- Detección en tiempo real de múltiples rostros
- Tracking con identificación de personas únicas
- Análisis de landmarks faciales (468 puntos)
- Clustering jerárquico para agrupar rostros similares

### Arquitectura de Microservicios de IA

Cada servicio de IA es independiente y modular:

```
┌─────────────────────────────────────────────────────────┐
│              AIService (Orquestador)                    │
│  - Coordina el flujo completo de análisis               │
│  - Maneja progreso y reportes de estado                 │
│  - Gestiona errores y reintentos                        │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┬──────────────┐
        │           │           │              │
        ▼           ▼           ▼              ▼
┌─────────────┐ ┌─────────┐ ┌───────────┐ ┌──────────────┐
│ Liveness    │ │  Face   │ │Transcribe │ │  Coherence   │
│ Detection   │ │Detection│ │ Service   │ │   Analyzer   │
│             │ │         │ │           │ │              │
│ • Análisis  │ │• Media- │ │• Whisper  │ │• Groq API    │
│   metadata  │ │  Pipe   │ │• FFmpeg   │ │• Llama 3.3   │
│ • Ruido     │ │• Insight│ │• Segmen-  │ │• Análisis    │
│ • Brillo    │ │  Face   │ │  tación   │ │  semántico   │
│ • Temporal  │ │• OpenCV │ │• Align.   │ │• Evaluación  │
└─────────────┘ └─────────┘ └───────────┘ └──────────────┘
```

### Flujo de Datos (Pipeline de Análisis)

```
1. SUBIDA DE VIDEO
   ↓
2. VALIDACIÓN (formato, tamaño, duración)
   ↓
3. ANÁLISIS DE LIVENESS (15% progreso)
   ↓
4. DETECCIÓN DE ROSTROS (30% progreso)
   ↓
5. TRANSCRIPCIÓN COMPLETA (50% progreso)
   ↓
6. ANÁLISIS DE COHERENCIA POR PARTICIPANTE (70% progreso)
   ↓
7. CÁLCULO DE CALIFICACIONES (90% progreso)
   ↓
8. GENERACIÓN DE RETROALIMENTACIÓN (100% progreso)
   ↓
9. NOTIFICACIÓN AL ESTUDIANTE
```

---

## 3. TECNOLOGÍAS UTILIZADAS

### Backend Core

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.11.9 | Lenguaje principal del sistema |
| **Django** | 5.2.7 | Framework web MVT |
| **PostgreSQL** | 12+ | Base de datos relacional ACID |
| **psycopg2-binary** | 2.9.11 | Adaptador PostgreSQL optimizado |

### Inteligencia Artificial y Machine Learning

#### Modelos de Lenguaje (LLM)
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Groq SDK** | 0.32.0 | API para Llama 3.3 70B (análisis de coherencia) |
| **OpenAI** | 1.59.5 | Cliente OpenAI (Whisper) |
| **OpenAI Whisper** | 20231117 | Transcripción de audio a texto con timestamps |
| **Transformers** | 4.46.3 | Modelos pre-entrenados de Hugging Face |
| **Sentence-Transformers** | 3.3.1 | Embeddings semánticos para análisis de texto |
| **Tokenizers** | 0.20.3 | Tokenización rápida para NLP |
| **TikToken** | 0.12.0 | Tokenizador de OpenAI para conteo de tokens |

#### Deep Learning Frameworks
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **PyTorch** | 2.5.1 | Framework principal de Deep Learning |
| **TorchAudio** | 2.5.1 | Procesamiento de audio con tensores |
| **TorchVision** | 0.20.1 | Visión por computadora con PyTorch |

#### Visión por Computadora
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **OpenCV (cv2)** | 4.9.0.80 | Procesamiento de imágenes y video |
| **MediaPipe** | 0.10.21 | Detección facial y tracking en tiempo real (468 landmarks) |
| **DeepFace** | 0.0.x | Framework de reconocimiento facial (modelos: VGG-Face, Facenet, ArcFace, etc.) |
| **Face Recognition** | 1.3.0 | Comparación de rostros (dlib wrapper) |
| **dlib** | 19.24.6 | Detección de landmarks faciales |

### Procesamiento Multimedia

#### Video
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **MoviePy** | 2.2.1 | Edición y procesamiento de video |
| **ImageIO** | 2.36.1 | Lectura/escritura de frames de video |
| **ImageIO-FFmpeg** | 0.6.0 | Binarios de FFmpeg integrados |
| **Pillow (PIL)** | 11.0.0 | Manipulación de imágenes |

#### Audio
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Librosa** | 0.10.2.post1 | Análisis avanzado de audio (MFCCs, pitch, tempo) |
| **Pydub** | 0.25.1 | Segmentación y manipulación de audio |
| **SoundFile** | 0.13.2 | Lectura/escritura de archivos WAV/FLAC |
| **AudioRead** | 3.0.1 | Decodificación universal de formatos de audio |
| **Resampy** | 0.4.3 | Remuestreo de audio de alta calidad |

### Ciencia de Datos y Análisis

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **NumPy** | 1.26.4 | Operaciones numéricas vectorizadas (IMPORTANTE: <2.0 por compatibilidad con OpenCV) |
| **Pandas** | 2.2.3 | Manipulación y análisis de datos tabulares |
| **Scikit-learn** | 1.5.2 | Clustering (AgglomerativeClustering para rostros) |
| **SciPy** | 1.14.1 | Algoritmos científicos avanzados |
| **Matplotlib** | 3.9.4 | Visualización de gráficos |
| **Joblib** | 1.4.2 | Paralelización y caché de cálculos costosos |

### Almacenamiento y CDN

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Cloudinary** | 1.44.1 | CDN global, almacenamiento de videos/imágenes |
| **django-cloudinary-storage** | 0.3.0 | Integración transparente con Django Storage API |

### Generación de Reportes

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **OpenPyXL** | 3.1.5 | Exportación de Excel con estilos |
| **ReportLab** | 4.2.5 | Generación de PDFs profesionales |
| **XlsxWriter** | 3.2.0 | Generación rápida de Excel |

### Utilidades y Configuración

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **python-dotenv** | 1.1.1 | Gestión de variables de entorno (.env) |
| **python-decouple** | 3.8 | Separación de configuración del código |
| **pytz** | 2025.2 | Manejo de zonas horarias |
| **tzdata** | 2025.2 | Base de datos de zonas horarias |

### Servidor Web y Despliegue

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Gunicorn** | 23.0.0 | Servidor WSGI para producción (multi-worker) |
| **WhiteNoise** | 6.8.2 | Servir archivos estáticos eficientemente |

### Requisitos del Sistema

**Software Externo Necesario:**
- **FFmpeg**: Para procesamiento de video/audio (incluido via imageio-ffmpeg)
- **PostgreSQL 12+**: Base de datos
- **Redis** (Opcional): Caché y tareas asíncronas

**Requisitos de Hardware Recomendados:**
- **CPU**: 4+ cores (Intel i5/i7 o AMD Ryzen 5/7)
- **RAM**: 8GB mínimo, 16GB recomendado
- **GPU**: NVIDIA con CUDA (opcional, acelera PyTorch)
- **Almacenamiento**: 20GB+ espacio libre (para modelos y datos temporales)
- **Conexión**: Internet estable para APIs de Groq y Cloudinary
|------------|---------|-----------|
| **django-extensions** | 4.1 | Comandos adicionales de Django |
| **django-widget-tweaks** | 1.5.0 | Utilidades para formularios |
| **djangorestframework** | 3.16.0 | API REST framework |
| **django-cloudinary-storage** | 0.3.0 | Integración con Django |

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Bootstrap** | 5.3 | Framework CSS |
| **Font Awesome** | 6.x | Iconos |
| **Chart.js** | 4.x | Gráficos interactivos |
| **Vanilla JavaScript** | ES6+ | Interactividad |

---

## 4. MÓDULOS Y COMPONENTES

### Estructura del Proyecto

```
evaIa V0.5/
├── sist_evaluacion_expo/          # Configuración principal
│   ├── settings.py                # Configuración de Django
│   ├── urls.py                    # URLs principales
│   └── wsgi.py                    # Entrada WSGI
│
├── authentication/                # Módulo de autenticación
│   ├── models.py                  # User, Profile
│   ├── views.py                   # Login, registro, dashboard
│   ├── forms.py                   # Formularios de usuario
│   ├── decoradores.py             # @student_required, @teacher_required
│   └── urls.py                    # Rutas de autenticación
│
├── apps/
│   ├── presentaciones/            # Módulo principal de presentaciones
│   │   ├── models.py              # Presentation, Course, Assignment, Participant
│   │   ├── views.py               # CRUD de presentaciones
│   │   ├── forms.py               # Formularios de subida
│   │   ├── tasks.py               # Procesamiento asíncrono
│   │   ├── validators.py          # Validación de videos
│   │   └── services/              # Servicios auxiliares
│   │       └── video_processor.py # Procesamiento de video
│   │
│   ├── ai_processor/              # Motor de Inteligencia Artificial
│   │   ├── services.py            # Servicios de IA
│   │   │   ├── GroqService        # Análisis con Llama 3.3
│   │   │   ├── WhisperService     # Transcripción
│   │   │   ├── FaceDetectionService # Detección facial
│   │   │   ├── CoherenceAnalyzer  # Análisis de coherencia
│   │   │   └── CloudinaryService  # Gestión de archivos
│   │   └── models.py              # Configuración de IA
│   │
│   ├── notifications/             # Sistema de notificaciones
│   │   ├── models.py              # Notification
│   │   ├── views.py               # Gestión de notificaciones
│   │   ├── signals.py             # Triggers automáticos
---

## 4. MÓDULOS Y COMPONENTES

### Estructura de Directorios Completa

```
evaIA/
│
├── sist_evaluacion_expo/          # Configuración principal del proyecto
│   ├── settings.py                # Configuración Django (DB, APIs, IA)
│   ├── urls.py                    # Rutas URL principales
│   ├── wsgi.py                    # Entrada WSGI para producción
│   └── asgi.py                    # Entrada ASGI para websockets (futuro)
│
├── authentication/                # Autenticación y gestión de usuarios
│   ├── models.py                  # Profile (extensión de User)
│   ├── views.py                   # Login, registro, perfil, dashboard
│   ├── forms.py                   # Formularios de autenticación
│   ├── decoradores.py             # @student_required, @teacher_required, @admin_required
│   ├── utils.py                   # Utilidades de autenticación
│   ├── urls.py                    # Rutas de auth/
│   └── management/commands/       # Comandos personalizados
│       └── setup_groups.py        # Crear grupos (Estudiante, Docente, Administrador)
│
├── apps/
│   │
│   ├── presentaciones/            # MÓDULO PRINCIPAL - Gestión de presentaciones
│   │   ├── models.py              # 6 modelos principales:
│   │   │                          #   • Course: Cursos académicos
│   │   │                          #   • Assignment: Asignaciones de presentaciones
│   │   │                          #   • Presentation: Presentaciones de estudiantes
│   │   │                          #   • Participant: Participantes individuales
│   │   │                          #   • AIAnalysis: Análisis detallado de IA
│   │   │                          #   • AIConfiguration: Configuración personalizada de IA
│   │   ├── views.py               # Vistas principales:
│   │   │                          #   • upload_presentation_view: Subir videos
│   │   │                          #   • grade_presentations_view: Calificar
│   │   │                          #   • teacher_dashboard_view: Dashboard docente
│   │   │                          #   • student_dashboard_view: Dashboard estudiante
│   │   │                          #   • edit_participant_grade: Editar participante
│   │   │                          #   • bulk_grade_presentation: Calificación masiva
│   │   ├── forms.py               # Formularios de subida y edición
│   │   ├── forms_grading.py       # Formularios especializados de calificación
│   │   ├── urls.py                # Rutas de presentations/
│   │   ├── ai_utils.py            # Utilidades de cálculo de calificaciones
│   │   ├── validators.py          # Validadores personalizados de archivos
│   │   ├── tasks.py               # Tareas asíncronas (futuro: Celery)
│   │   └── templatetags/          # Template tags personalizados
│   │
│   ├── ai_processor/              # MÓDULO DE IA - Servicios de análisis
│   │   ├── services/              # 8 servicios especializados:
│   │   │   ├── ai_service.py              # ORQUESTADOR PRINCIPAL
│   │   │   │                              #   • analyze_presentation(): Pipeline completo
│   │   │   │                              #   • Coordina todos los demás servicios
│   │   │   │                              #   • Maneja progreso y errores
│   │   │   │
│   │   │   ├── transcription_service.py   # TRANSCRIPCIÓN DE AUDIO
│   │   │   │                              #   • Whisper Small model
│   │   │   │                              #   • Extracción de audio con FFmpeg
│   │   │   │                              #   • Segmentos con timestamps
│   │   │   │                              #   • Detección de pausas
│   │   │   │
│   │   │   ├── face_detection_service.py  # DETECCIÓN DE ROSTROS
│   │   │   │                              #   • MediaPipe Face Detection
│   │   │   │                              #   • DeepFace para embeddings
│   │   │   │                              #   • Clustering jerárquico (V12)
│   │   │   │                              #   • Tracking de participantes
│   │   │   │                              #   • Cálculo de tiempo de participación
│   │   │   │                              #   • Captura de fotos de rostros
│   │   │   │
│   │   │   ├── advanced_coherence_service.py  # ANÁLISIS DE COHERENCIA
│   │   │   │                                  #   • Groq API (Llama 3.3 70B)
│   │   │   │                                  #   • Análisis semántico profundo
│   │   │   │                                  #   • Sistema de rotación de API keys
│   │   │   │                                  #   • 3 niveles de rigurosidad
│   │   │   │                                  #   • Evaluación por participante
│   │   │   │
│   │   │   ├── liveness_detection_service.py  # DETECCIÓN DE AUTENTICIDAD
│   │   │   │                                  #   • Análisis de metadatos
│   │   │   │                                  #   • Detección de ruido de cámara
│   │   │   │                                  #   • Variaciones de brillo
│   │   │   │                                  #   • Consistencia temporal
│   │   │   │                                  #   • Score de liveness (0-100)
│   │   │   │
│   │   │   ├── audio_segmentation_service.py  # SEGMENTACIÓN DE AUDIO
│   │   │   │                                  #   • Separación por participante
│   │   │   │                                  #   • Múltiples estrategias
│   │   │   │                                  #   • Alineación temporal
│   │   │   │
│   │   │   ├── cloudinary_service.py          # ALMACENAMIENTO EN NUBE
│   │   │   │                                  #   • Upload de videos
│   │   │   │                                  #   • Generación de thumbnails
│   │   │   │                                  #   • URLs seguras (HTTPS)
│   │   │   │                                  #   • Eliminación de archivos
│   │   │   │
│   │   │   ├── groq_key_manager.py            # GESTIÓN DE API KEYS
│   │   │   │                                  #   • Rotación automática
│   │   │   │                                  #   • Manejo de rate limits
│   │   │   │                                  #   • Reintentos inteligentes
│   │   │   │                                  #   • Soporte hasta 10 keys
│   │   │   │
│   │   │   └── coherence_analyzer.py          # ANÁLISIS DE COHERENCIA (Legacy)
│   │   │
│   │   └── models.py              # Modelos (si se requieren en el futuro)
│   │
│   ├── notifications/             # Sistema de notificaciones
│   │   ├── models.py              # Notification, NotificationSettings
│   │   ├── views.py               # Lista, marcar como leída, eliminar
│   │   ├── views_simple.py        # API simplificada
│   │   ├── services.py            # NotificationService (crear notificaciones)
│   │   ├── signals.py             # Señales automáticas
│   │   ├── context_processors.py  # Contador de no leídas
│   │   └── management/commands/
│   │       └── send_due_reminders.py  # Recordatorios automáticos
│   │
│   ├── reportes/                  # Generación de reportes académicos
│   │   ├── views.py               # Exportación Excel/PDF
│   │   │                          #   • Estudiante: calificaciones personales
│   │   │                          #   • Docente: reportes de curso
│   │   │                          #   • Admin: estadísticas generales
│   │   ├── models.py              # Modelos de métricas (futuro)
│   │   └── urls.py                # Rutas de reports/
│   │
│   └── help/                      # Ayuda y documentación en línea
│       ├── views.py               # Guías de usuario
│       ├── urls.py                # Rutas de help/
│       └── templates/help/        # Tutoriales HTML
│
├── templates/                     # Plantillas HTML globales
│   ├── base.html                  # Plantilla base con navbar, footer
│   ├── base_auth.html             # Base para páginas de autenticación
│   ├── auth/                      # Login, registro, perfil, dashboard
│   ├── presentations/             # CRUD de presentaciones, calificación
│   ├── notifications/             # UI de notificaciones
│   ├── reportes/                  # Visualización y descarga de reportes
│   └── help/                      # Páginas de ayuda
│
├── static/                        # Archivos estáticos
│   ├── css/
│   │   ├── dashboard.css          # Estilos de dashboards
│   │   ├── grades.css             # Estilos de calificaciones
│   │   └── custom.css             # Estilos personalizados globales
│   ├── js/
│   │   ├── notifications.js       # Notificaciones en tiempo real
│   │   ├── video-player.js        # Reproductor personalizado
│   │   ├── grade-form.js          # Formularios de calificación
│   │   └── progress-tracker.js    # Tracker de progreso de análisis
│   └── img/                       # Logos, iconos, imágenes
│
├── uploads/                       # Almacenamiento local (temporal)
│   ├── presentations/             # Videos de presentaciones
│   ├── avatars/                   # Fotos de perfil
│   ├── participant_photos/        # Fotos de participantes detectados
│   └── thumbnails/                # Miniaturas de videos
│
├── docs/                          # Documentación técnica
│   ├── ARQUITECTURA_SISTEMA.md    # Este archivo (arquitectura completa)
│   ├── V11_HIERARCHICAL_CLUSTERING_SOLUCION_DEFINITIVA.md
│   ├── MEJORA_FILTRADO_FALSOS_POSITIVOS.md
│   ├── OPTIMIZACION_RENDIMIENTO.md
│   └── ...                        # Más documentos técnicos
│
├── manage.py                      # CLI de Django
├── requirements.txt               # Dependencias Python (311 líneas)
├── setup.py                       # Script de instalación automatizada
├── .env                           # Variables de entorno (NO en Git)
├── .gitignore                     # Archivos ignorados por Git
└── README.md                      # Guía de instalación y uso
```

### Modelos de Base de Datos (Resumen)

#### authentication.Profile
- Extensión del modelo User de Django
- Campos: institution, phone, avatar, is_verified
- Métodos: get_role(), is_student(), is_teacher(), is_admin()

#### presentaciones.Course
- Cursos académicos creados por docentes
- Relaciones: teacher (ForeignKey a User), students (ManyToMany)

#### presentaciones.Assignment
- Asignaciones de presentaciones
- Campos importantes: max_duration, due_date, strictness_level, max_score
- Tipos: Individual, Grupal, Debate, Pitch, etc.

#### presentaciones.Presentation
- Presentación de un estudiante
- 50+ campos incluyendo:
  - Video: video_file, cloudinary_url, duration, status
  - Transcripción: transcription_text, transcription_segments
  - Liveness: is_live_recording, liveness_score, recording_type
  - Participación: participation_data (JSON)
  - Calificaciones: ai_score, content_score, fluency_score, final_score

#### presentaciones.Participant
- Participante individual en presentación grupal
- Campos: presentation, participant_number, detected_name, photo
- Calificaciones individuales: coherence_score, participation_time

#### presentaciones.AIConfiguration
- Configuración personalizada de IA por docente
- Pesos: content_weight, fluency_weight, body_language_weight
- Niveles: face_detection_confidence, strictness_level

#### notifications.Notification
- Notificaciones del sistema
- Tipos: PRESENTATION_GRADED, NEW_ASSIGNMENT, SUBMISSION_READY_TO_GRADE
- Prioridades: LOW, MEDIUM, HIGH, URGENT

---

## 5. FLUJO DE FUNCIONAMIENTO COMPLETO

### A. Flujo del Estudiante - Subida y Análisis

**Tiempo total estimado: 2-5 minutos** (dependiendo de la duración del video)

```
1. AUTENTICACIÓN Y DASHBOARD
   ↓
2. SELECCIONAR ASIGNACIÓN
   ↓
3. SUBIR VIDEO (validaciones)
   ↓
4. PIPELINE DE ANÁLISIS DE IA (8 pasos):
   
   [15%]  → Análisis de Liveness (video en vivo vs pregrabado)
   [30%]  → Detección de Rostros (MediaPipe + DeepFace + Clustering V12)
   [50%]  → Transcripción Completa (Whisper con timestamps)
   [60%]  → Segmentación por Participante
   [70-85%] → Análisis de Coherencia por Participante (Llama 3.3 70B)
   [90%]  → Cálculo de Calificaciones Finales
   [100%] → Guardado y Notificación
   
   ↓
5. NOTIFICACIÓN AL ESTUDIANTE
   ↓
6. REVISAR RESULTADOS DE IA
```

#### Detalles del Pipeline de IA:

**PASO 1: Análisis de Liveness (15% progreso)**
- **Servicio:** LivenessDetectionService
- **Objetivo:** Determinar si el video fue grabado en vivo o es material pregrabado
- **Métodos:**
  - Análisis de metadatos del archivo (fecha creación vs modificación)
  - Medición de ruido de cámara (desviación estándar del ruido)
  - Variación de brillo entre frames consecutivos
  - Análisis de consistencia temporal (detección de cortes de edición)
  - Patrones de movimiento de cámara
- **Resultado:** liveness_score (0-100), recording_type (LIVE/RECORDED)

**PASO 2: Detección de Rostros (30% progreso)**
- **Servicio:** FaceDetectionService (Versión V12 - Hierarchical Clustering)
- **Tecnologías:** MediaPipe (detección) + DeepFace (embeddings, Facenet512 por defecto) + Scikit-learn (clustering)
- **Proceso:**
  1. Detección de rostros frame por frame con MediaPipe (468 landmarks faciales)
      2. Extracción de embeddings (vector 512-dim) con DeepFace (modelo base actual: Facenet512). Si InsightFace está instalado en el entorno, el servicio puede priorizar su embedding 512-dim.
  3. Clustering jerárquico (AgglomerativeClustering) con distancia coseno
  4. Asignación de IDs únicos (Persona 1, Persona 2, ...)
  5. Tracking temporal y cálculo de tiempo de participación
  6. Captura de foto representativa de cada participante
- **Resultado:** Lista de participantes con tiempo, porcentaje, foto

**PASO 3: Transcripción Completa (50% progreso)**
- **Servicio:** TranscriptionService
- **Tecnología:** OpenAI Whisper (modelo small)
- **Proceso:**
  1. Extracción de audio con FFmpeg (WAV mono 16kHz)
  2. Transcripción con detección automática de idioma
  3. Generación de timestamps por segmento
  4. Cálculo de palabras por minuto (WPM)
  5. Detección de pausas largas (>2 segundos)
- **Resultado:** Texto completo + segmentos con timestamps

**PASO 4: Segmentación por Participante (60% progreso)**
- **Servicio:** AudioSegmentationService
- **Objetivo:** Asignar texto transcrito a cada participante
- **Método:** Alineación temporal entre timestamps de rostros y transcripción

**PASO 5: Análisis de Coherencia (70-85% progreso)**
- **Servicio:** AdvancedCoherenceService
- **Tecnología:** Groq API con Llama 3.3 70B Versatile
- **Configuración:**
  - Temperature: 0.3 (baja para consistencia)
  - Max tokens: 2000
  - Timeout: 45 segundos
  - Sistema de rotación automática de hasta 10 API keys
- **Análisis por participante:**
  - Coherencia temática con las instrucciones (0-100)
  - Relevancia del contenido expuesto (0-100)
  - Profundidad del análisis (0-100)
  - Estructura y organización (0-100)
  - Uso de ejemplos concretos (0-100)
- **Niveles de rigurosidad:**
  - **Strict (Estricto):** Evaluación rigurosa, penalizaciones altas
  - **Moderate (Moderado):** Evaluación balanceada (recomendado)
  - **Lenient (Permisivo):** Evaluación flexible, enfoque en fortalezas
- **Resultado:** coherence_score + feedback detallado + fortalezas + áreas de mejora

**PASO 6: Cálculo de Calificaciones (90% progreso)**
- **Servicio:** ai_utils.calculate_final_grade()
- **Fórmula personalizable por docente:**
  ```
  final_score = (
    coherence_score * content_weight +
    fluency_score * fluency_weight +
    participation_score * participation_weight +
    liveness_bonus
  ) * (max_score / 100)
  ```
- **Componentes:**
  - coherence_score: de Llama 3.3 (0-100)
  - fluency_score: basado en WPM, pausas, muletillas (0-100)
  - participation_score: tiempo activo, equidad en grupos (0-100)
  - liveness_bonus: +5 puntos si es grabación en vivo

**PASO 7: Guardado y Finalización (100% progreso)**
- Cambio de estado: PROCESSING → ANALYZED
- Creación de registros Participant en base de datos
- Guardado de AIAnalysis con detalles completos
- Subida opcional a Cloudinary CDN
- Limpieza de archivos temporales
- Envío de notificación al estudiante

### B. Flujo del Docente - Revisión y Calificación

```
1. DASHBOARD DOCENTE
   - Ver cursos activos
   - Presentaciones pendientes de calificar (badge con contador)
   - Estadísticas del curso
   ↓
2. PANEL DE CALIFICACIÓN
   - Lista de presentaciones ANALYZED
   - Filtros: por curso, asignación, fecha, estudiante
   - Ordenar: por fecha subida, nombre, estado
   ↓
3. REVISAR ANÁLISIS DE IA
   - Reproducir video con controles
   - Ver transcripción completa con timestamps
   - Revisar análisis por participante:
     * Foto del participante
     * Tiempo de participación
     * Texto transcrito individual
     * Score de coherencia de IA
     * Feedback automático de IA
   - Ver puntajes automáticos sugeridos
   ↓
4. AJUSTAR CALIFICACIONES (opcional)
   - Mantener calificación de IA tal cual
   - Ajustar manualmente por participante
   - Agregar feedback del docente
   - Configurar pesos de evaluación
   ↓
5. CALIFICAR Y PUBLICAR
   - Validar calificaciones (0 a max_score)
   - Agregar comentarios finales
   - Publicar calificación
   - Estado cambia: ANALYZED → GRADED
   ↓
6. NOTIFICACIÓN AUTOMÁTICA
   - Estudiante recibe notificación
   - Email con link a calificación (opcional)
```

### C. Flujo del Administrador

```
1. DASHBOARD ADMIN
   - Gestión de usuarios (crear, editar, eliminar)
   - Asignación de roles (Estudiante, Docente, Administrador)
   - Estadísticas generales del sistema:
     * Total de usuarios por rol
     * Total de presentaciones analizadas
     * Uso de APIs (Groq, Whisper, Cloudinary)
     * Almacenamiento utilizado
   ↓
2. CONFIGURACIÓN GLOBAL
   - Configurar API keys (Groq, Cloudinary, Email)
   - Ajustar parámetros de IA por defecto
   - Configurar límites de subida
   - Gestionar notificaciones del sistema
   ↓
3. MONITOREO Y REPORTES
   - Ver logs de errores
   - Exportar reportes Excel/PDF
   - Analizar estadísticas de uso
```

### D. Sistema de Notificaciones en Tiempo Real

```
EVENTOS AUTOMÁTICOS QUE GENERAN NOTIFICACIONES:

Para Estudiantes:
├─ PRESENTATION_ANALYZED: "Tu presentación ha sido analizada por IA"
├─ PRESENTATION_GRADED: "Tu presentación ha sido calificada"
├─ NEW_ASSIGNMENT: "Nueva asignación disponible en [Curso]"
├─ ASSIGNMENT_DUE_SOON: "Asignación '[Título]' vence en 24 horas"
└─ ASSIGNMENT_OVERDUE: "Asignación '[Título]' ha vencido"

Para Docentes:
├─ NEW_SUBMISSION: "Nuevo envío de [Estudiante] en [Asignación]"
├─ SUBMISSION_READY_TO_GRADE: "[X] presentaciones listas para calificar"
└─ ASSIGNMENT_DEADLINE_APPROACHING: "Asignación '[Título]' vence mañana"

Para Todos:
├─ WELCOME: "Bienvenido a EvalExpo AI"
├─ SYSTEM_UPDATE: "Nueva funcionalidad disponible"
└─ COURSE_UPDATE: "Actualización en el curso [Nombre]"
```

### E. Manejo de Errores y Casos Especiales

**Casos de Error en Análisis de IA:**

1. **Sin audio detectado:**
   - Estado → FAILED
   - Mensaje: "No se detectó audio en el video. Verifica tu micrófono."
   - Acción: Estudiante debe subir nuevamente

2. **Sin rostros detectados (pero hay audio):**
   - Continúa procesamiento solo con audio
   - Warning en participation_data
   - Calificación basada en contenido y transcripción únicamente

3. **Timeout de API (Groq/Whisper):**
   - Reintentos automáticos (3 intentos)
   - Rotación de API key si hay rate limit
   - Si falla: Estado → FAILED con mensaje específico

4. **Video corrupto o formato inválido:**
   - Validación temprana (antes de procesamiento)
   - Mensaje de error claro al estudiante
   - No se crea registro en DB

5. **Almacenamiento lleno (Cloudinary):**
   - Fallback a almacenamiento local
   - Notificación al administrador
   - Sistema continúa funcionando

**Sistema de Caché para Optimización:**
- Caché de embeddings de rostros (evita recálculos)
- Caché de progreso de procesamiento (Redis/Django Cache)
- Caché de modelos de IA (Whisper, MediaPipe en memoria)

---

## 6. DIAGRAMAS DE SECUENCIA

Nota: La versión editable de estos diagramas está disponible en el archivo draw.io: docs/diagrams/diagrama-secuencia.drawio (contiene tres páginas: "Subida y Análisis", "Calificación Docente" y "Notificaciones en Tiempo Real").

### 6.1. Diagrama de Secuencia: Subida y Análisis de Presentación

Este diagrama muestra la interacción completa entre el estudiante, el sistema web, los servicios de IA y las APIs externas durante el proceso de subida y análisis de una presentación.

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐
│Estudiante│  │  Django  │  │   DB     │  │  AIService  │  │ IA Services  │  │  Groq    │  │Cloudinary│
│ (Browser)│  │  Views   │  │PostgreSQL│  │(Orquestador)│  │ (Especiali-  │  │   API    │  │   CDN    │
│          │  │          │  │          │  │             │  │   zados)     │  │          │  │          │
└─────┬────┘  └─────┬────┘  └─────┬────┘  └──────┬──────┘  └──────┬───────┘  └─────┬────┘  └─────┬────┘
      │             │             │               │                │                │             │
      │ 1. Accede a│             │               │                │                │             │
      │  /upload   │             │               │                │                │             │
      ├────────────>│             │               │                │                │             │
      │             │             │               │                │                │             │
      │ 2. Renderiza formulario │               │                │                │             │
      │<────────────┤             │               │                │                │             │
      │             │             │               │                │                │             │
      │ 3. Completa│             │               │                │                │             │
      │  formulario│             │               │                │                │             │
      │  y sube    │             │               │                │                │             │
      │  video.mp4 │             │               │                │                │             │
      ├────────────>│             │               │                │                │             │
      │             │             │               │                │                │             │
      │             │ 4. Valida  │               │                │                │             │
      │             │  (tamaño,  │               │                │                │             │
      │             │   formato) │               │                │                │             │
      │             │             │               │                │                │             │
      │             │ 5. Crea    │               │                │                │             │
      │             │  Presentation              │                │                │             │
      │             │  (status=  │               │                │                │             │
      │             │   UPLOADED)│               │                │                │             │
      │             ├────────────>│               │                │                │             │
      │             │             │               │                │                │             │
      │             │<────────────┤ 6. OK        │                │                │             │
      │             │             │               │                │                │             │
      │ 7. Redirect│             │               │                │                │             │
      │  + Mensaje │             │               │                │                │             │
      │  "Procesando"             │               │                │                │             │
      │<────────────┤             │               │                │                │             │
      │             │             │               │                │                │             │
      │             │ 8. Inicia  │               │                │                │             │
      │             │  tarea async               │                │                │             │
      │             │  (analyze_ │               │                │                │             │
      │             │  presentation)             │                │                │             │
      │             ├────────────────────────────>│                │                │             │
      │             │             │               │                │                │             │
      │             │             │ 9. Actualiza │                │                │             │
      │             │             │  status =    │                │                │             │
      │             │             │  PROCESSING  │                │                │             │
      │             │             │<──────────────┤                │                │             │
      │             │             │               │                │                │             │
      │             │             │               │ 10. LivenessDetectionService    │             │
      │             │             │               │  analyze_video()                │             │
      │             │             │               ├───────────────>│                │             │
      │             │             │               │                │ - Analiza     │             │
      │             │             │               │                │   metadatos   │             │
      │             │             │               │                │ - Mide ruido  │             │
      │             │             │               │                │ - Variación   │             │
      │             │             │               │                │   de brillo   │             │
      │             │             │               │                │                │             │
      │             │             │               │<───────────────┤ 11. Result:   │             │
      │             │             │               │  {is_live: T,  │  liveness_score│            │
      │             │             │               │   score: 78}   │                │             │
      │             │             │               │                │                │             │
      │             │             │               │ 12. FaceDetectionService        │             │
      │             │             │               │  process_video()                │             │
      │             │             │               ├───────────────>│                │             │
      │             │             │               │                │ - MediaPipe   │             │
      │             │             │               │                │   detecta     │             │
      │             │             │               │                │   rostros     │             │
   │             │             │               │                │ - DeepFace    │             │
      │             │             │               │                │   embeddings  │             │
      │             │             │               │                │ - Clustering  │             │
      │             │             │               │                │   jerárquico  │             │
      │             │             │               │                │ - Tracking    │             │
      │             │             │               │                │                │             │
      │             │             │               │<───────────────┤ 13. Result:   │             │
      │             │             │               │  {participants:│  [{id:1, time:│            │
      │             │             │               │   45s}, ...]}  │                │             │
      │             │             │               │                │                │             │
      │             │             │               │ 14. TranscriptionService        │             │
      │             │             │               │  transcribe_video()             │             │
      │             │             │               ├───────────────>│                │             │
      │             │             │               │                │ - Extrae audio│             │
      │             │             │               │                │   con FFmpeg  │             │
      │             │             │               │                │ - Whisper     │             │
      │             │             │               │                │   transcribe  │             │
      │             │             │               │                │ - Genera      │             │
      │             │             │               │                │   timestamps  │             │
      │             │             │               │                │                │             │
      │             │             │               │<───────────────┤ 15. Result:   │             │
      │             │             │               │  {full_text,   │  segments}    │             │
      │             │             │               │                │                │             │
      │             │             │               │ 16. Por cada participante:     │             │
      │             │             │               │  AdvancedCoherenceService      │             │
      │             │             │               │  analyze_participant_coherence()│            │
      │             │             │               ├───────────────>│                │             │
      │             │             │               │                │                │             │
      │             │             │               │                │ 17. Prepara   │             │
      │             │             │               │                │  prompt con   │             │
      │             │             │               │                │  asignación + │             │
      │             │             │               │                │  transcripción│             │
      │             │             │               │                │                │             │
      │             │             │               │                │ 18. Llama a   │             │
      │             │             │               │                │  Groq API     │             │
      │             │             │               │                ├───────────────>│             │
      │             │             │               │                │                │ - Llama 3.3│
      │             │             │               │                │                │   70B       │
      │             │             │               │                │                │ - Análisis  │
      │             │             │               │                │                │   semántico │
      │             │             │               │                │                │             │
      │             │             │               │                │<───────────────┤ 19. Response│
      │             │             │               │                │  {coherence:85,│  feedback} │
      │             │             │               │                │   details...}  │             │
      │             │             │               │<───────────────┤ 20. Result por│             │
      │             │             │               │  participante  │  participante  │             │
      │             │             │               │                │                │             │
      │             │             │               │ 21. Calcula calificaciones     │             │
      │             │             │               │  finales con pesos             │             │
      │             │             │               │  configurados                  │             │
      │             │             │               │                │                │             │
      │             │             │ 22. Guarda   │                │                │             │
      │             │             │  resultados  │                │                │             │
      │             │             │  (Participants,                │                │             │
      │             │             │   AIAnalysis)│                │                │             │
      │             │             │<──────────────┤                │                │             │
      │             │             │               │                │                │             │
      │             │             │ 23. Actualiza│                │                │             │
      │             │             │  status =    │                │                │             │
      │             │             │  ANALYZED    │                │                │             │
      │             │             │<──────────────┤                │                │             │
      │             │             │               │                │                │             │
      │             │             │               │ 24. [OPCIONAL] Sube a Cloudinary│             │
      │             │             │               ├─────────────────────────────────────────────>│
      │             │             │               │                │                │             │
      │             │             │               │<─────────────────────────────────────────────┤
      │             │             │               │  25. {url, public_id}          │             │
      │             │             │               │                │                │             │
      │             │             │               │ 26. NotificationService        │             │
      │             │             │               │  notify_presentation_analyzed()│             │
      │             │             │               ├───────────────>│                │             │
      │             │             │               │                │                │             │
      │             │             │ 27. Crea     │                │                │             │
      │             │             │  Notification│                │                │             │
      │             │             │<──────────────┤                │                │             │
      │             │             │               │                │                │             │
      │             │<────────────────────────────┤ 28. Análisis   │                │             │
      │             │  completado │               │  completado    │                │             │
      │             │             │               │                │                │             │
      │ 29. Polling│             │               │                │                │             │
      │  /check_   │             │               │                │                │             │
      │  progress  │             │               │                │                │             │
      ├────────────>│             │               │                │                │             │
      │             │             │               │                │                │             │
      │             │ 30. Query  │               │                │                │             │
      │             │  cache +   │               │                │                │             │
      │             │  DB status │               │                │                │             │
      │             ├────────────>│               │                │                │             │
      │             │<────────────┤ 31. ANALYZED │                │                │             │
      │             │             │               │                │                │             │
      │ 32. {status:ANALYZED,    │               │                │                │             │
      │  progress:100%}           │               │                │                │             │
      │<────────────┤             │               │                │                │             │
      │             │             │               │                │                │             │
      │ 33. Muestra│             │               │                │                │             │
      │  notificación             │               │                │                │             │
      │  "Análisis │             │               │                │                │             │
      │  completado"              │               │                │                │             │
      │             │             │               │                │                │             │
      │ 34. Click  │             │               │                │                │             │
      │  "Ver      │             │               │                │                │             │
      │  Resultados"              │               │                │                │             │
      ├────────────>│             │               │                │                │             │
      │             │             │               │                │                │             │
      │             │ 35. Query  │               │                │                │             │
      │             │  Presentation              │                │                │             │
      │             │  + Participants            │                │                │             │
      │             │  + AIAnalysis│               │                │                │             │
      │             ├────────────>│               │                │                │             │
      │             │<────────────┤ 36. Datos    │                │                │             │
      │             │             │               │                │                │             │
      │ 37. Renderiza detalle    │               │                │                │             │
      │  con resultados de IA    │               │                │                │             │
      │<────────────┤             │               │                │                │             │
      │             │             │               │                │                │             │
```

**Tiempo total estimado:** 2-5 minutos dependiendo de la duración del video

**Notas importantes:**
- Los pasos 10-20 son asíncronos y pueden ejecutarse en paralelo parcialmente
- El progreso se reporta en caché (Redis/Django Cache) para consultas en tiempo real
- Si falla algún paso, el estado cambia a FAILED con mensaje de error específico
- La rotación de API keys de Groq es automática en caso de rate limits

---

### 6.2. Diagrama de Secuencia: Calificación por Docente

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────────┐
│ Docente  │  │  Django  │  │   DB     │  │Notification  │  │  Estudiante  │
│(Browser) │  │  Views   │  │PostgreSQL│  │  Service     │  │   (Email)    │
└─────┬────┘  └─────┬────┘  └─────┬────┘  └──────┬───────┘  └──────┬───────┘
      │             │             │               │                 │
      │ 1. Accede a│             │               │                 │
      │  /grade    │             │               │                 │
      ├────────────>│             │               │                 │
      │             │             │               │                 │
      │             │ 2. Query   │               │                 │
      │             │  Presentations              │                 │
      │             │  WHERE     │               │                 │
      │             │  status =  │               │                 │
      │             │  ANALYZED  │               │                 │
      │             ├────────────>│               │                 │
      │             │             │               │                 │
      │             │<────────────┤ 3. Lista de  │                 │
      │             │  presentations              │                 │
      │             │             │               │                 │
      │ 4. Renderiza lista con  │               │                 │
      │  scores de IA sugeridos  │               │                 │
      │<────────────┤             │               │                 │
      │             │             │               │                 │
      │ 5. Click en│             │               │                 │
      │  presentación            │               │                 │
      │  específica│             │               │                 │
      ├────────────>│             │               │                 │
      │             │             │               │                 │
      │             │ 6. Query   │               │                 │
      │             │  Presentation              │                 │
      │             │  + Participants            │                 │
      │             │  + AIAnalysis              │                 │
      │             │  (select_related,          │                 │
      │             │   prefetch_related)        │                 │
      │             ├────────────>│               │                 │
      │             │             │               │                 │
      │             │<────────────┤ 7. Datos     │                 │
      │             │  completos  │               │                 │
      │             │             │               │                 │
      │ 8. Renderiza vista detallada:           │                 │
      │  • Video player                          │                 │
      │  • Transcripción completa                │                 │
      │  • Lista de participantes con:           │                 │
      │    - Foto                                │                 │
      │    - Tiempo participación                │                 │
      │    - Texto transcrito                    │                 │
      │    - Score IA                            │                 │
      │    - Feedback IA                         │                 │
      │  • Formulario de calificación            │                 │
      │<────────────┤             │               │                 │
      │             │             │               │                 │
      │ 9. Docente │             │               │                 │
      │  revisa:   │             │               │                 │
      │  • Ve video│             │               │                 │
      │  • Lee análisis          │               │                 │
      │  • Revisa scores         │               │                 │
      │             │             │               │                 │
      │ 10. Decide:│             │               │                 │
      │  [ ] Aceptar IA tal cual │               │                 │
      │  [X] Ajustar manualmente │               │                 │
      │             │             │               │                 │
      │ 11. Modifica:            │               │                 │
      │  • Ajusta score Part. 1: 85→90           │                 │
      │  • Ajusta score Part. 2: 78→80           │                 │
      │  • Agrega feedback manual                │                 │
      │             │             │               │                 │
      │ 12. Click  │             │               │                 │
      │  "Publicar │             │               │                 │
      │  Calificación"           │               │                 │
      ├────────────>│             │               │                 │
      │             │             │               │                 │
      │             │ 13. Valida │               │                 │
      │             │  datos:    │               │                 │
      │             │  • Scores 0-max_score      │                 │
      │             │  • Feedback no vacío       │                 │
      │             │             │               │                 │
      │             │ 14. BEGIN  │               │                 │
      │             │  TRANSACTION               │                 │
      │             ├────────────>│               │                 │
      │             │             │               │                 │
      │             │ 15. UPDATE │               │                 │
      │             │  Participants              │                 │
      │             │  SET manual_grade=X,       │                 │
      │             │  teacher_feedback=Y        │                 │
      │             ├────────────>│               │                 │
      │             │             │               │                 │
      │             │ 16. UPDATE │               │                 │
      │             │  Presentation              │                 │
      │             │  SET status=GRADED,        │                 │
      │             │  final_score=AVG,          │                 │
      │             │  graded_by=docente_id,     │                 │
      │             │  graded_at=NOW()           │                 │
      │             ├────────────>│               │                 │
      │             │             │               │                 │
      │             │ 17. COMMIT │               │                 │
      │             ├────────────>│               │                 │
      │             │<────────────┤ 18. OK       │                 │
      │             │             │               │                 │
      │             │ 19. Llama  │               │                 │
      │             │  NotificationService       │                 │
      │             │  .notify_presentation_graded()              │
      │             ├────────────────────────────>│                 │
      │             │             │               │                 │
      │             │             │ 20. Crea     │                 │
      │             │             │  Notification│                 │
      │             │             │<──────────────┤                 │
      │             │             │               │                 │
      │             │             │               │ 21. [OPCIONAL] │
      │             │             │               │  Envía email   │
      │             │             │               ├────────────────>│
      │             │             │               │  "Tu presentación│
      │             │             │               │  ha sido        │
      │             │             │               │  calificada"    │
      │             │             │               │                 │
      │             │<────────────────────────────┤ 22. OK          │
      │             │             │               │                 │
      │ 23. Redirect + mensaje   │               │                 │
      │  "Calificación publicada"│               │                 │
      │<────────────┤             │               │                 │
      │             │             │               │                 │
      │ 24. Muestra│             │               │                 │
      │  toast de  │             │               │                 │
      │  éxito     │             │               │                 │
      │             │             │               │                 │
      │             │             │               │ 25. Estudiante │
      │             │             │               │  recibe        │
      │             │             │               │  notificación  │
      │             │             │               │  in-app + email│
      │             │             │               │                 │
```

**Tiempo estimado:** 3-10 minutos por presentación (según complejidad)

**Notas:**
- El docente puede calificar múltiples presentaciones en lote
- Los ajustes manuales sobrescriben los scores de IA
- Las notificaciones se envían solo si el estudiante las tiene activadas
- El sistema guarda el historial de cambios para auditoría

---

### 6.3. Diagrama de Secuencia: Creación de Asignación y Notificaciones

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────────┐
│ Docente  │  │  Django  │  │   DB     │  │Notification  │  │ Estudiantes  │
│(Browser) │  │  Views   │  │PostgreSQL│  │  Service     │  │   (N users)  │
└─────┬────┘  └─────┬────┘  └─────┬────┘  └──────┬───────┘  └──────┬───────┘
      │             │             │               │                 │
      │ 1. Accede a│             │               │                 │
      │  /create_  │             │               │                 │
      │  assignment│             │               │                 │
      ├────────────>│             │               │                 │
      │             │             │               │                 │
      │             │ 2. Query   │               │                 │
      │             │  Courses   │               │                 │
      │             │  WHERE     │               │                 │
      │             │  teacher = │               │                 │
      │             │  current_user              │                 │
      │             ├────────────>│               │                 │
      │             │<────────────┤ 3. Cursos    │                 │
      │             │             │               │                 │
      │ 4. Renderiza formulario  │               │                 │
      │<────────────┤             │               │                 │
      │             │             │               │                 │
      │ 5. Completa:│             │               │                 │
      │  • Curso   │             │               │                 │
      │  • Título  │             │               │                 │
      │  • Descripción           │               │                 │
      │  • Instrucciones         │               │                 │
      │  • Duración máx: 10 min  │               │                 │
      │  • Fecha límite: 15/Nov  │               │                 │
      │  • Rigurosidad: Moderate │               │                 │
      │  • Puntaje máx: 20       │               │                 │
      │             │             │               │                 │
      │ 6. Submit  │             │               │                 │
      ├────────────>│             │               │                 │
      │             │             │               │                 │
      │             │ 7. Valida: │               │                 │
      │             │  • Fecha límite > hoy      │                 │
      │             │  • Duración > 0            │                 │
      │             │  • Puntaje > 0             │                 │
      │             │             │               │                 │
      │             │ 8. Crea    │               │                 │
      │             │  Assignment│               │                 │
      │             ├────────────>│               │                 │
      │             │<────────────┤ 9. OK,       │                 │
      │             │  id=123     │               │                 │
      │             │             │               │                 │
      │             │ 10. Query  │               │                 │
      │             │  estudiantes               │                 │
      │             │  del curso │               │                 │
      │             ├────────────>│               │                 │
      │             │<────────────┤ 11. Lista    │                 │
      │             │  [user1,    │               │                 │
      │             │   user2,...]│               │                 │
      │             │             │               │                 │
      │             │ 12. Llama  │               │                 │
      │             │  NotificationService       │                 │
      │             │  .notify_new_assignment()  │                 │
      │             │  (assignment, students)    │                 │
      │             ├────────────────────────────>│                 │
      │             │             │               │                 │
      │             │             │               │ 13. FOR EACH   │
      │             │             │               │  estudiante:   │
      │             │             │               │                 │
      │             │             │ 14. Crea     │                 │
      │             │             │  Notification│                 │
      │             │             │  (recipient= │                 │
      │             │             │   estudiante)│                 │
      │             │             │<──────────────┤                 │
      │             │             │               │                 │
      │             │             │               │ 15. [OPCIONAL] │
      │             │             │               │  Envía email   │
      │             │             │               ├────────────────>│
      │             │             │               │  a cada uno    │
      │             │             │               │                 │
      │             │<────────────────────────────┤ 16. OK,        │
      │             │  N notificaciones creadas   │  enviadas      │
      │             │             │               │                 │
      │ 17. Redirect + mensaje   │               │                 │
      │  "Asignación creada,     │               │                 │
      │   notificaciones enviadas"│              │                 │
      │<────────────┤             │               │                 │
      │             │             │               │                 │
      │             │             │               │ 18. Estudiantes│
      │             │             │               │  reciben       │
      │             │             │               │  notificación  │
      │             │             │               │  (badge en     │
      │             │             │               │   navbar)      │
      │             │             │               │                 │
```

**Tiempo estimado:** <5 segundos

**Notas:**
- Las notificaciones se crean en masa de manera eficiente
- Los emails son opcionales según configuración del estudiante
- El sistema calcula automáticamente la fecha de expiración de notificaciones
- Se registra en logs para auditoría
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. GESTIÓN DE CURSOS Y ASIGNACIONES                         │
│    Puede:                                                    │
│    - Crear/editar cursos                                    │
│    - Inscribir estudiantes                                  │
│    - Crear asignaciones con:                                │
│      * Título y descripción                                 │
│      * Duración máxima                                      │
│      * Fecha límite                                         │
│      * Puntaje máximo                                       │
│      * Instrucciones específicas                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. REVISAR PRESENTACIONES ANALIZADAS                        │
│    Vista incluye:                                            │
│    - Reproductor de video                                   │
│    - Transcripción completa                                 │
│    - Análisis IA detallado:                                 │
│      * Puntaje general de IA                                │
│      * Evaluación individual por participante               │
│      * Coherencia semántica                                 │
│      * Tiempo de participación                              │
│      * Palabras clave detectadas                            │
│    - Sugerencia de calificación automática                  │
│    - Retroalimentación generada por IA                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. CALIFICACIÓN FINAL                                       │
│    El docente puede:                                         │
│    a. Aceptar calificación sugerida por IA                  │
│    b. Modificar la calificación                             │
│    c. Agregar/editar retroalimentación                      │
│    d. Calificar participantes individualmente (grupos)      │
│    e. Guardar calificación final                            │
│                                                              │
│    Estado cambia a: GRADED                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. NOTIFICACIÓN AL ESTUDIANTE                               │
│    - Email: "Tu presentación ha sido calificada"            │
│    - Notificación in-app con puntaje                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. GENERACIÓN DE REPORTES                                   │
│    Puede generar:                                            │
│    - Reporte individual del estudiante (PDF)                │
│    - Reporte del curso completo (Excel)                     │
│    - Estadísticas comparativas                              │
│    - Gráficos de rendimiento                                │
└─────────────────────────────────────────────────────────────┘
```

---

### 6.4. Diagrama de Secuencia: Consulta de Notificaciones en Tiempo Real

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│ Usuario  │  │JavaScript│  │  Django  │  │   DB         │
│(Browser) │  │  Client  │  │  API     │  │ PostgreSQL   │
└─────┬────┘  └─────┬────┘  └─────┬────┘  └──────┬───────┘
      │             │             │               │
      │ 1. Página  │             │               │
      │  carga     │             │               │
      │            │             │               │
      │            │ 2. Inicia  │               │
      │            │  polling   │               │
      │            │  cada 10s  │               │
      │            │             │               │
      │            │ 3. Fetch   │               │
      │            │  /api/     │               │
      │            │  notifications             │
      │            │  /unread_count             │
      │            ├────────────>│               │
      │            │             │               │
      │            │             │ 4. Query     │
      │            │             │  Notification│
      │            │             │  WHERE       │
      │            │             │  recipient = │
      │            │             │  user AND    │
      │            │             │  is_read =   │
      │            │             │  False       │
      │            │             ├──────────────>│
      │            │             │               │
      │            │             │<──────────────┤ 5. COUNT = 3
      │            │             │               │
      │            │<────────────┤ 6. JSON      │
      │            │  {count: 3, │               │
      │            │   latest: [...]}            │
      │            │             │               │
      │            │ 7. Actualiza│               │
      │            │  badge en  │               │
      │ 8. Ve "3" │  navbar    │               │
      │  en badge │             │               │
      │<───────────┤             │               │
      │            │             │               │
      │ 9. Click  │             │               │
      │  en icono │             │               │
      │  campana  │             │               │
      ├───────────>│             │               │
      │            │             │               │
      │            │ 10. Fetch  │               │
      │            │  /api/     │               │
      │            │  notifications             │
      │            │  /list     │               │
      │            ├────────────>│               │
      │            │             │               │
      │            │             │ 11. Query    │
      │            │             │  Notification│
      │            │             │  WHERE       │
      │            │             │  recipient = │
      │            │             │  user        │
      │            │             │  ORDER BY    │
      │            │             │  created_at  │
      │            │             │  DESC        │
      │            │             │  LIMIT 20    │
      │            │             ├──────────────>│
      │            │             │               │
      │            │             │<──────────────┤ 12. Lista
      │            │             │               │
      │            │<────────────┤ 13. JSON     │
      │            │  [{id: 1,   │               │
      │            │    title,   │               │
      │            │    message, │               │
      │            │    is_read, │               │
      │            │    ...}, ...]               │
      │            │             │               │
      │            │ 14. Renderiza              │
      │            │  dropdown  │               │
      │            │  con lista │               │
      │ 15. Ve    │  de        │               │
      │  notifica-│  notificaciones            │
      │  ciones   │             │               │
      │<───────────┤             │               │
      │            │             │               │
      │ 16. Click │             │               │
      │  en una   │             │               │
      │  notificación            │               │
      ├───────────>│             │               │
      │            │             │               │
      │            │ 17. Fetch  │               │
      │            │  /api/     │               │
      │            │  notifications             │
      │            │  /mark_read│               │
      │            │  /{id}     │               │
      │            ├────────────>│               │
      │            │             │               │
      │            │             │ 18. UPDATE   │
      │            │             │  Notification│
      │            │             │  SET is_read │
      │            │             │  = True,     │
      │            │             │  read_at =   │
      │            │             │  NOW()       │
      │            │             │  WHERE id = X│
      │            │             ├──────────────>│
      │            │             │<──────────────┤ 19. OK
      │            │             │               │
      │            │<────────────┤ 20. {success}│
      │            │             │               │
      │            │ 21. Actualiza              │
      │            │  badge     │               │
      │ 22. Badge │  (count-1) │               │
      │  muestra  │             │               │
      │  "2"      │             │               │
      │<───────────┤             │               │
      │            │             │               │
      │            │ 23. Redirect               │
      │            │  a action_url              │
      │            │  (ej: /presentations/123)  │
      │            │             │               │
      │ 24. Navega│             │               │
      │  a destino│             │               │
      │<───────────┤             │               │
      │            │             │               │
```

**Frecuencia de polling:** Cada 10 segundos (configurable)

**Alternativa futura:** WebSockets con Django Channels para notificaciones push en tiempo real

**Optimizaciones:**
- Caché de contador de no leídas (evita queries constantes)
- Índices en base de datos en campos `recipient` + `is_read`
- Paginación en lista de notificaciones (20 por página)

---

### 6.5. Resumen de Diagramas de Secuencia

Los diagramas anteriores ilustran los 4 flujos principales del sistema:

1. **Subida y Análisis de Presentación (Estudiante):**
   - Flujo completo de 8 pasos del pipeline de IA
   - Interacción con APIs externas (Groq, Cloudinary)
   - Manejo asíncrono con reportes de progreso
   - Tiempo: 2-5 minutos

2. **Calificación por Docente:**
   - Revisión de análisis de IA
   - Ajustes manuales opcionales
   - Publicación y notificación automática
   - Tiempo: 3-10 minutos por presentación

3. **Creación de Asignación:**
   - Creación masiva de notificaciones
   - Envío opcional de emails
   - Tiempo: <5 segundos

4. **Sistema de Notificaciones en Tiempo Real:**
   - Polling cada 10 segundos
   - Actualización dinámica de badges
   - Marcado de leídas automático

**Patrones Comunes:**
- Validación temprana de datos
- Transacciones ACID para operaciones críticas
- Notificaciones automáticas en eventos importantes
- Caché para optimizar consultas frecuentes
- Manejo de errores con mensajes claros

---

### 6.6. Diagrama de Secuencia: Manejo de Errores en Análisis de IA

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐  ┌──────────┐
│Estudiante│  │  Django  │  │   DB     │  │  AIService  │  │  Groq    │
│          │  │  Views   │  │PostgreSQL│  │             │  │   API    │
└─────┬────┘  └─────┬────┘  └─────┬────┘  └──────┬──────┘  └─────┬────┘
      │             │             │               │                │
      │             │             │               │                │
      │ CASO 1: SIN AUDIO DETECTADO                                │
      │ ════════════════════════════════════════════════════════   │
      │             │             │               │                │
      │             │ Video sin  │               │                │
      │             │ audio sube │               │                │
      │             ├────────────>│               │                │
      │             │             │               │                │
      │             │ Inicio     │               │                │
      │             │ análisis   │               │                │
      │             ├────────────────────────────>│                │
      │             │             │               │                │
      │             │             │               │ Extracción    │
      │             │             │               │ de audio      │
      │             │             │               │ → WAV vacío   │
      │             │             │               │                │
      │             │             │               │ Transcripción │
      │             │             │               │ Whisper →     │
      │             │             │               │ texto = ""    │
      │             │             │               │                │
      │             │             │               │ ❌ VALIDACIÓN │
      │             │             │               │ FALLA         │
      │             │             │               │                │
      │             │             │ UPDATE status│                │
      │             │             │ = FAILED,    │                │
      │             │             │ ai_feedback =│                │
      │             │             │ "Sin audio"  │                │
      │             │             │<──────────────┤                │
      │             │             │               │                │
      │             │ Crear      │               │                │
      │             │ Notification               │                │
      │             │ (tipo=ERROR)               │                │
      │             ├────────────>│               │                │
      │             │             │               │                │
      │ Recibe      │             │               │                │
      │ notificación│             │               │                │
      │ "❌ No se   │             │               │                │
      │ detectó audio"            │               │                │
      │<────────────┤             │               │                │
      │             │             │               │                │
      │ Debe subir  │             │               │                │
      │ nuevo video │             │               │                │
      │             │             │               │                │
      │             │             │               │                │
      │ CASO 2: TIMEOUT DE API GROQ                                │
      │ ════════════════════════════════════════════════════════   │
      │             │             │               │                │
      │             │ Análisis en│               │                │
      │             │ curso...   │               │                │
      │             │             │               │                │
      │             │             │               │ Llama Groq    │
      │             │             │               │ para coherencia│
      │             │             │               ├───────────────>│
      │             │             │               │                │
      │             │             │               │ ⏱️ Esperando...│
      │             │             │               │ (45 segundos) │
      │             │             │               │                │
      │             │             │               │<───────────────┤
      │             │             │               │ ❌ Timeout     │
      │             │             │               │                │
      │             │             │               │ 🔄 INTENTO 2  │
      │             │             │               │ (con API key  │
      │             │             │               │  diferente)   │
      │             │             │               ├───────────────>│
      │             │             │               │                │
      │             │             │               │<───────────────┤
      │             │             │               │ ❌ Timeout     │
      │             │             │               │                │
      │             │             │               │ 🔄 INTENTO 3  │
      │             │             │               ├───────────────>│
      │             │             │               │                │
      │             │             │               │<───────────────┤
      │             │             │               │ ✅ SUCCESS!    │
      │             │             │               │ {coherence:82} │
      │             │             │               │                │
      │             │             │               │ Continúa      │
      │             │             │               │ normalmente   │
      │             │             │               │                │
      │             │             │               │                │
      │ CASO 3: RATE LIMIT DE GROQ API                             │
      │ ════════════════════════════════════════════════════════   │
      │             │             │               │                │
      │             │             │               │ Llama Groq    │
      │             │             │               ├───────────────>│
      │             │             │               │                │
      │             │             │               │<───────────────┤
      │             │             │               │ ❌ 429 Rate    │
      │             │             │               │ Limit Exceeded │
      │             │             │               │                │
      │             │             │               │ GroqKeyManager│
      │             │             │               │ .rotate_key() │
      │             │             │               │                │
      │             │             │               │ 🔄 Reintenta  │
      │             │             │               │ con KEY #2    │
      │             │             │               ├───────────────>│
      │             │             │               │                │
      │             │             │               │<───────────────┤
      │             │             │               │ ✅ SUCCESS!    │
      │             │             │               │                │
      │             │             │ Log: "Rotación│                │
      │             │             │ de API key    │                │
      │             │             │ exitosa"      │                │
      │             │             │<──────────────┤                │
      │             │             │               │                │
      │             │             │               │                │
      │ CASO 4: VIDEO CORRUPTO (Validación Temprana)               │
      │ ════════════════════════════════════════════════════════   │
      │             │             │               │                │
      │ Sube video │             │               │                │
      │ corrupto   │             │               │                │
      ├────────────>│             │               │                │
      │             │             │               │                │
      │             │ Validación │               │                │
      │             │ de formato │               │                │
      │             │             │               │                │
      │             │ Intenta    │               │                │
      │             │ abrir con  │               │                │
      │             │ OpenCV     │               │                │
      │             │             │               │                │
      │             │ ❌ FALLA   │               │                │
      │             │ (codec     │               │                │
      │             │  inválido) │               │                │
      │             │             │               │                │
      │ Error:     │             │               │                │
      │ "Formato de│             │               │                │
      │ video      │             │               │                │
      │ inválido o │             │               │                │
      │ corrupto"  │             │               │                │
      │<────────────┤             │               │                │
      │             │             │               │                │
      │ NO se crea │             │               │                │
      │ registro en│             │               │                │
      │ BD         │             │               │                │
      │             │             │               │                │
      │             │             │               │                │
      │ CASO 5: SIN ROSTROS (pero hay audio)                       │
      │ ════════════════════════════════════════════════════════   │
      │             │             │               │                │
      │             │ Análisis   │               │                │
      │             │ rostros    │               │                │
      │             │             │               │ FaceDetection │
      │             │             │               │ no detecta    │
      │             │             │               │ ningún rostro │
      │             │             │               │                │
      │             │             │               │ ⚠️ WARNING    │
      │             │             │               │ (no error)    │
      │             │             │               │                │
      │             │             │ Guarda        │                │
      │             │             │ participation_│                │
      │             │             │ data = {      │                │
      │             │             │   no_face:true│                │
      │             │             │   warning:... │                │
      │             │             │ }             │                │
      │             │             │<──────────────┤                │
      │             │             │               │                │
      │             │             │               │ ✅ CONTINÚA   │
      │             │             │               │ solo con audio│
      │             │             │               │ y transcripción│
      │             │             │               │                │
      │             │             │               │ Calificación  │
      │             │             │               │ basada en     │
      │             │             │               │ coherencia +  │
      │             │             │               │ fluidez       │
      │             │             │               │                │
      │             │             │ UPDATE status│                │
      │             │             │ = ANALYZED   │                │
      │             │             │ (con warning)│                │
      │             │             │<──────────────┤                │
      │             │             │               │                │
      │ Recibe      │             │               │                │
      │ notificación│             │               │                │
      │ "⚠️ Análisis│             │               │                │
      │ completado  │             │               │                │
      │ (sin rostros│             │               │                │
      │ detectados)"│             │               │                │
      │<────────────┤             │               │                │
      │             │             │               │                │
```

**Estrategias de Manejo de Errores:**

1. **Validación en Capas:**
   - Client-side (JavaScript): formato, tamaño
   - Server-side (Django): integridad, codec
   - Processing (IA): contenido válido

2. **Reintentos Inteligentes:**
   - Timeouts: 3 intentos con backoff exponencial
   - Rate limits: rotación automática de API keys
   - Transient errors: retry inmediato

3. **Graceful Degradation:**
   - Sin rostros → continúa con audio
   - Sin API key → usa análisis básico
   - Cloudinary down → usa storage local

4. **Logging y Monitoreo:**
   - Todos los errores se registran en logs
   - Notificaciones al admin en errores críticos
   - Métricas de tasa de error por servicio

5. **Feedback Claro al Usuario:**
   - Mensajes descriptivos (no códigos técnicos)
   - Acciones sugeridas para resolver
   - Soporte contextual en ayuda

---

## 7. BASE DE DATOS

### Modelo de Datos (Entidad-Relación)

```
┌─────────────────┐
│      User       │ (Django Auth)
│─────────────────│
│ id (PK)         │
│ username        │
│ email           │
│ first_name      │
│ last_name       │
│ password        │
│ groups          │
└────────┬────────┘
         │ 1:1
         │
┌────────▼────────┐
│    Profile      │
│─────────────────│
│ id (PK)         │
│ user_id (FK)    │
│ institution     │
│ phone           │
│ avatar          │
│ is_verified     │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐
│     Course      │
│─────────────────│
│ id (PK)         │
│ name            │
│ code (unique)   │
│ teacher_id (FK) ├─────────┐
│ description     │         │ N:1
│ students (M2M)  │         │
│ is_active       │         │
│ created_at      │         │
└────────┬────────┘         │
         │ 1:N              │
         │                  │
┌────────▼────────┐         │
│   Assignment    │         │
│─────────────────│         │
│ id (PK)         │         │
│ title           │         │
│ description     │         │
│ course_id (FK)  │         │
│ assignment_type │         │
│ max_duration    │         │
│ due_date        │         │
│ max_score       │         │
│ instructions    │         │
│ is_active       │         │
│ created_at      │         │
└────────┬────────┘         │
         │ 1:N              │
         │                  │
┌────────▼──────────────────┴──┐
│      Presentation            │
│──────────────────────────────│
│ id (PK)                      │
│ title                        │
│ description                  │
│ student_id (FK) ──────────┐  │
│ assignment_id (FK)         │  │
│ video_file                 │  │
│ cloudinary_public_id       │  │
│ cloudinary_url             │  │
│ is_stored_in_cloud         │  │
│ transcript                 │  │
│ duration_seconds           │  │
│ file_size                  │  │
│ status                     │  │
│ uploaded_at                │  │
│ processed_at               │  │
│ ai_score                   │  │
│ content_score              │  │
│ fluency_score              │  │
│ body_language_score        │  │
│ voice_score                │  │
│ ai_feedback (JSON)         │  │
│ final_score                │  │
│ teacher_feedback           │  │
│ graded_at                  │  │
│ graded_by_id (FK) ─────────┼──┘
│ participation_data (JSON)  │
│ analyzed_at                │
└────────┬───────────────────┘
         │ 1:N
         │
┌────────▼────────┐
│  Participant    │ (Evaluación individual)
│─────────────────│
│ id (PK)         │
│ presentation_id │
│ label           │ ("Persona 1", "Persona 2")
│ photo           │
│ participation_time │
│ time_percentage │
│ transcription   │
│ word_count      │
│ semantic_coherence │
│ keywords_score  │
│ depth_score     │
│ coherence_score │
│ contribution_%  │
│ ai_grade        │ (automática 0-20)
│ ai_feedback     │ (generada por IA)
│ manual_grade    │ (editada por docente)
│ teacher_feedback│
│ coherence_level │
│ observations    │
│ keywords_found  │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐
│  Notification   │
│─────────────────│
│ id (PK)         │
│ user_id (FK)    │
│ title           │
│ message         │
│ type            │
│ is_read         │
│ related_model   │
│ related_id      │
│ created_at      │
└─────────────────┘

┌─────────────────┐
│AIConfiguration  │ (Config por docente)
│─────────────────│
│ id (PK)         │
│ teacher_id (FK) │
│ ai_model        │
│ ai_temperature  │
│ face_detection  │
│   _confidence   │
│ coherence_weight│
│ face_detection  │
│   _weight       │
│ duration_weight │
│ manual_weight   │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### Estados de una Presentación

```
UPLOADED  ──────→  PROCESSING  ──────→  ANALYZED  ──────→  GRADED
   │                   │                    │
   │                   ▼                    │
   │               FAILED ◄─────────────────┘
   │
   └──────────────→ REJECTED
```

**Estados:**
- `UPLOADED`: Video recién subido, pendiente de procesamiento
- `PROCESSING`: En proceso de análisis IA (transcripción, detección facial, etc.)
- `ANALYZED`: Análisis IA completado, pendiente de calificación docente
- `GRADED`: Calificado por el docente, proceso completo
- `FAILED`: Error durante el procesamiento
- `REJECTED`: Rechazado por el docente

---

## 7. INTELIGENCIA ARTIFICIAL

### Motor de IA: Arquitectura Multi-Componente

El sistema utiliza múltiples tecnologías de IA especializadas:

```
┌────────────────────────────────────────────────────────────┐
│                  MOTOR DE INTELIGENCIA ARTIFICIAL          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 1. TRANSCRIPCIÓN DE AUDIO                            │ │
│  │    Tecnología: OpenAI Whisper                        │ │
│  │    Modelo: whisper-base (en local)                   │ │
│  │    Input: Archivo de audio (WAV)                     │ │
│  │    Output: Texto transcrito + timestamps             │ │
│  │    Precisión: ~95% en español                        │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 2. DETECCIÓN Y SEGUIMIENTO FACIAL                    │ │
│  │    Tecnología: MediaPipe Face Detection              │ │
│  │    Modelo: BlazeFace (optimizado para mobile)        │ │
│  │    Input: Frames de video                            │ │
│  │    Output:                                           │ │
│  │    - Bounding boxes de rostros                       │ │
│  │    - Landmarks faciales (468 puntos)                 │ │
│  │    - Tracking de personas                            │ │
│  │    - Tiempo de participación                         │ │
│  │    - Capturas de rostros                             │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 3. ANÁLISIS DE COHERENCIA SEMÁNTICA                  │ │
│  │    Tecnología: Groq API + Llama 3.3 70B              │ │
│  │    Modelo: llama-3.3-70b-versatile                   │ │
│  │    Input: Transcripción + tema de asignación         │ │
│  │    Output:                                           │ │
│  │    - Coherencia semántica (0-100)                    │ │
│  │    - Palabras clave detectadas                       │ │
│  │    - Profundidad del contenido                       │ │
│  │    - Alineación con el tema                          │ │
│  │                                                      │ │
│  │    Embeddings: Sentence-Transformers                 │ │
│  │    Modelo: all-MiniLM-L6-v2                          │ │
│  │    Cálculo de similitud coseno entre:                │ │
│  │    - Texto de la presentación                        │ │
│  │    - Descripción del tema                            │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 4. GENERACIÓN DE RETROALIMENTACIÓN                   │ │
│  │    Tecnología: Groq API (Llama 3.3 70B)              │ │
│  │    Input: Todos los puntajes + transcripción         │ │
│  │    Output:                                           │ │
│  │    - Feedback personalizado (150-250 palabras)       │ │
│  │    - Fortalezas identificadas                        │ │
│  │    - Áreas de mejora                                 │ │
│  │    - Recomendaciones específicas                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 5. CALIFICACIÓN AUTOMÁTICA                           │ │
│  │    Fórmula ponderada:                                │ │
│  │    Grade = (                                         │ │
│  │        coherence_score × 0.4 +                       │ │
│  │        participation_time × 0.2 +                    │ │
│  │        keyword_match × 0.2 +                         │ │
│  │        depth_score × 0.2                             │ │
│  │    ) × max_score / 100                               │ │
│  │                                                      │ │
│  │    Escala: 0-20 (sistema vigesimal peruano)         │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Análisis Individual por Participante (Exposiciones Grupales)

Para presentaciones grupales, el sistema realiza:

1. **Identificación de participantes**:
   - Detección facial con MediaPipe
   - Asignación de etiquetas ("Persona 1", "Persona 2", etc.)
   - Captura de foto representativa

2. **Segmentación de transcripción**:
   - División del audio por hablante
   - Asignación de texto a cada participante
   - Cálculo de palabras por persona

3. **Análisis individual de coherencia**:
   ```python
   for each participant:
       # Extraer su transcripción
       participant_text = extract_participant_text(participant_id)
       
       # Análisis semántico con LLM
       coherence_result = analyze_coherence_with_groq(
           text=participant_text,
           topic=assignment.description,
           keywords=assignment.keywords
       )
       
       # Calcular puntajes
       semantic_score = coherence_result['semantic_similarity']
       keywords_score = coherence_result['keyword_match']
       depth_score = coherence_result['content_depth']
       
       # Puntaje ponderado
       final_score = (
           semantic_score * 0.4 +
           keywords_score * 0.3 +
           depth_score * 0.3
       )
       
       # Generar feedback personalizado
       feedback = generate_individual_feedback(
           participant=participant,
           scores=scores,
           strengths=coherence_result['strengths'],
           weaknesses=coherence_result['weaknesses']
       )
       
       # Guardar en BD
       participant.ai_grade = final_score
       participant.ai_feedback = feedback
       participant.save()
   ```

4. **Evaluación de participación equitativa**:
   - Comparación de tiempos de participación
   - Análisis de distribución de palabras
   - Detección de participación desbalanceada

---

## 8. APIS Y SERVICIOS EXTERNOS

### 1. Groq API (Análisis de Coherencia)

**URL**: `https://api.groq.com/openai/v1/chat/completions`

**Autenticación**: Bearer Token (API Key)

**Modelo utilizado**: `llama-3.3-70b-versatile`

**Propósito**: 
- Análisis semántico profundo
- Evaluación de coherencia temática
- Generación de retroalimentación

**Ejemplo de request**:
```python
{
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "system",
            "content": "Eres un evaluador académico experto..."
        },
        {
            "role": "user",
            "content": "Analiza esta transcripción: [texto]"
        }
    ],
    "temperature": 0.3,
    "max_tokens": 2000
}
```

**Sistema de rotación de keys**:
- El sistema soporta hasta 5 API keys
- Rotación automática en caso de límite de rate
- Fallback a modo básico si todas las keys fallan

### 2. Cloudinary (Almacenamiento en la Nube)

**URL**: `https://api.cloudinary.com/v1_1/{cloud_name}/video/upload`

**Autenticación**: API Key + API Secret

**Propósito**:
- Almacenamiento de videos en CDN
- Generación de miniaturas automáticas
- Streaming optimizado
- Transformaciones de video

**Ventajas**:
- CDN global de alta velocidad
- Sin límites de almacenamiento (plan pagado)
- Conversión automática de formatos
- URLs seguras con expiración

**Ejemplo de configuración**:
```python
cloudinary.config(
    cloud_name="tu_cloud_name",
    api_key="tu_api_key",
    api_secret="tu_api_secret",
    secure=True
)
```

### 3. OpenAI Whisper (Transcripción)

**Ejecución**: Local (no requiere API)

**Modelo**: `whisper-base` (74M parámetros)

**Propósito**:
- Conversión de audio a texto
- Detección de idioma automática
- Segmentación por timestamps

**Características**:
- Precisión del 95% en español
- Soporte para 99 idiomas
- Procesamiento offline
- No envía datos a servidores externos

### 4. MediaPipe (Detección Facial)

**Ejecución**: Local (librería Python)

**Modelo**: BlazeFace + FaceMesh

**Propósito**:
- Detección de rostros en tiempo real
- Tracking de múltiples personas
- Extracción de landmarks faciales

**Características**:
- 468 puntos de referencia facial
- Detección en tiempo real (30+ FPS)
- Optimizado para CPU y GPU
- Sin conexión a internet necesaria

---

## 9. SEGURIDAD

### Autenticación y Autorización

1. **Sistema de autenticación**:
   - Django Authentication Backend
   - Sesiones cifradas con cookies HTTP-only
   - Timeout de sesión: 1 hora
   - Logout automático al cerrar navegador

2. **Control de acceso basado en roles**:
   ```python
   # Grupos de usuarios
   - Estudiante: @student_required
   - Docente: @teacher_required  
   - Administrador: @admin_required
   ```

3. **Permisos granulares**:
   - Los estudiantes solo ven sus propias presentaciones
   - Los docentes solo ven presentaciones de sus cursos
   - Los administradores tienen acceso completo

### Protección contra ataques

1. **CSRF Protection**:
   - Tokens CSRF en todos los formularios
   - Validación automática por Django

2. **SQL Injection**:
   - ORM de Django previene inyecciones
   - Queries parametrizadas

3. **XSS (Cross-Site Scripting)**:
   - Auto-escape de templates Django
   - Sanitización de inputs HTML

4. **Validación de archivos**:
   ```python
   # Restricciones de subida
   - Tamaño máximo: 100 MB
   - Formatos permitidos: .mp4, .avi, .mov, .mkv
   - Validación de magic bytes (no solo extensión)
   - Escaneo de metadatos
   ```

5. **Rate Limiting**:
   - Límite de intentos de login
   - Throttling de API de IA
   - Prevención de DDoS

### Seguridad de datos

1. **Contraseñas**:
   - Hasheadas con PBKDF2-SHA256
   - Salt único por usuario
   - Validación de fortaleza

2. **Variables sensibles**:
   - Almacenadas en `.env` (excluido de git)
   - No hardcodeadas en código
   - Rotación periódica de keys

3. **Comunicación**:
   - HTTPS obligatorio en producción
   - Certificados SSL/TLS
   - Headers de seguridad configurados

---

## 10. INSTALACIÓN Y CONFIGURACIÓN

### Requisitos del sistema

- **Python**: 3.10 o superior
- **PostgreSQL**: 15.x o superior
- **FFmpeg**: 4.4 o superior (para procesamiento de video)
- **RAM**: Mínimo 8 GB (recomendado 16 GB para IA)
- **Almacenamiento**: 20 GB libres mínimo
- **SO**: Windows 10/11, macOS, Linux

### Instalación rápida

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/LuisAngulo02/evaIA.git
   cd "evaIa V0.5"
   ```

2. **Ejecutar script de instalación automática**:
   ```bash
   python setup.py
   ```

   Este script:
   - Crea entorno virtual
   - Instala todas las dependencias
   - Configura PostgreSQL
   - Crea archivo `.env`
   - Ejecuta migraciones
   - Crea superusuario

3. **Configurar variables de entorno** (`.env`):
   ```env
   # Email (Gmail)
   EMAIL_HOST_USER=tu_email@gmail.com
   EMAIL_HOST_PASSWORD=tu_app_password

   # Groq API (hasta 5 keys)
   GROQ_API_KEY=tu_groq_key_1
   GROQ_API_KEY_2=tu_groq_key_2
   GROQ_API_KEY_3=tu_groq_key_3
   GROQ_API_KEY_4=tu_groq_key_4
   GROQ_API_KEY_5=tu_groq_key_5

   # Cloudinary (opcional)
   CLOUDINARY_CLOUD_NAME=tu_cloud_name
   CLOUDINARY_API_KEY=tu_api_key
   CLOUDINARY_API_SECRET=tu_api_secret
   ```

4. **Iniciar servidor**:
   ```bash
   # Activar entorno virtual
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate

   # Ejecutar servidor
   python manage.py runserver
   ```

5. **Acceder al sistema**:
   - URL: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

### Configuración de producción

Para deploy en producción, consultar `docs/DEPLOYMENT.md`.

Aspectos clave:
- Configurar `DEBUG=False`
- Usar servidor WSGI (Gunicorn/uWSGI)
- Configurar proxy inverso (Nginx)
- Habilitar HTTPS
- Configurar backup automático de BD
- Monitoreo con logs centralizados

---

## MÉTRICAS Y ESTADÍSTICAS

El sistema genera múltiples métricas:

### Para Estudiantes:
- Promedio general de calificaciones
- Evolución del rendimiento
- Comparación con compañeros (anónima)
- Áreas de fortaleza y mejora

### Para Docentes:
- Rendimiento por curso
- Estadísticas de asignaciones
- Tasa de aprobación
- Tiempo promedio de calificación

### Para Administradores:
- Uso del sistema
- Estadísticas de IA
- Tasa de error de procesamiento
- Uso de almacenamiento

---

## CICLO DE VIDA DE UNA PRESENTACIÓN

```
Día 1:
  09:00 - Estudiante sube video
  09:01 - Sistema inicia procesamiento
  09:05 - Transcripción completada
  09:08 - Detección facial completada
  09:12 - Análisis IA completado
  09:12 - Notificación al estudiante
  09:12 - Notificación al docente

Día 2:
  15:30 - Docente revisa presentación
  15:45 - Docente ajusta calificación
  15:46 - Notificación al estudiante
  
Día 3:
  10:00 - Estudiante ve calificación final
  10:05 - Sistema genera reporte PDF
```

--

Gracias por usar EvalExpo AI.
