# 📚 DOCUMENTACIÓN COMPLETA DEL SISTEMA EVALEXPO AI

## 📋 Tabla de Contenidos
1. [Introducción General](#introducción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Módulos y Componentes](#módulos-y-componentes)
5. [Flujo de Funcionamiento](#flujo-de-funcionamiento)
6. [Base de Datos](#base-de-datos)
7. [Inteligencia Artificial](#inteligencia-artificial)
8. [APIs y Servicios Externos](#apis-y-servicios-externos)
9. [Seguridad](#seguridad)
10. [Instalación y Configuración](#instalación-y-configuración)

---

## 1. INTRODUCCIÓN GENERAL

### ¿Qué es EvalExpo AI?

**EvalExpo AI** es un sistema integral de evaluación de presentaciones académicas que utiliza inteligencia artificial avanzada para analizar y calificar exposiciones de estudiantes. El sistema automatiza gran parte del proceso de evaluación, proporcionando retroalimentación detallada tanto a estudiantes como a docentes.

### Objetivo Principal

Facilitar la evaluación objetiva y consistente de presentaciones orales mediante el análisis automatizado de múltiples aspectos como:
- Contenido y coherencia temática
- Fluidez y claridad del discurso
- Lenguaje corporal y postura
- Participación individual en exposiciones grupales
- Calidad vocal y dicción

### Usuarios del Sistema

1. **Estudiantes**: Suben sus presentaciones en video y reciben retroalimentación automatizada
2. **Docentes**: Gestionan cursos, asignaciones y califican presentaciones con apoyo de IA
3. **Administradores**: Gestionan usuarios, configuran el sistema y monitorean el rendimiento

---

## 2. ARQUITECTURA DEL SISTEMA

### Patrón de Arquitectura: MVT (Model-View-Template)

El sistema está construido siguiendo el patrón MVT de Django, una variación del patrón MVC:

```
┌─────────────────────────────────────────────────────────────┐
│                      NAVEGADOR WEB                          │
│              (Chrome, Firefox, Edge, etc.)                  │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP Request/Response
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   DJANGO WEB SERVER                         │
│                  (Puerto 8000 local)                        │
├─────────────────────────────────────────────────────────────┤
│  URL Router  →  Views  →  Templates  →  Static Files       │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌───────────┐  ┌──────────┐  ┌─────────────┐
│  MODELS   │  │  FORMS   │  │  SERVICES   │
│ (ORM)     │  │          │  │  (Lógica)   │
└─────┬─────┘  └──────────┘  └──────┬──────┘
      │                              │
      ▼                              ▼
┌─────────────────┐         ┌──────────────────┐
│   PostgreSQL    │         │  APIs Externas   │
│   (Base Datos)  │         │  - Groq AI       │
│                 │         │  - Whisper       │
│                 │         │  - Cloudinary    │
└─────────────────┘         └──────────────────┘
```

### Capas del Sistema

#### 1. **Capa de Presentación** (Frontend)
- **Templates HTML**: Utilizan Django Template Language (DTL)
- **CSS**: Bootstrap 5.3 + estilos personalizados
- **JavaScript**: Vanilla JS para interactividad dinámica
- **Componentes**: Modales, formularios, tablas dinámicas, reproductor de video

#### 2. **Capa de Lógica de Negocio** (Backend)
- **Views**: Controlan el flujo de la aplicación
- **Services**: Contienen la lógica compleja (análisis IA, procesamiento video)
- **Forms**: Validación y procesamiento de datos de entrada
- **Signals**: Eventos automáticos del sistema

#### 3. **Capa de Datos**
- **Models (ORM)**: Abstracción de la base de datos
- **Migraciones**: Control de versiones del esquema de BD
- **Queries**: Optimizadas con select_related y prefetch_related

#### 4. **Capa de Servicios Externos**
- **Groq API**: Análisis de coherencia con LLMs (Llama 3.3 70B)
- **Whisper (OpenAI)**: Transcripción de audio a texto
- **Cloudinary**: Almacenamiento en la nube de videos
- **MediaPipe**: Detección de rostros y seguimiento

---

## 3. TECNOLOGÍAS UTILIZADAS

### Backend Core

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.10+ | Lenguaje principal |
| **Django** | 5.2.7 | Framework web |
| **PostgreSQL** | 15.x | Base de datos relacional |
| **psycopg2** | 2.9.11 | Adaptador PostgreSQL para Python |

### Inteligencia Artificial

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Groq SDK** | 0.32.0 | API para modelos LLM (Llama 3.3 70B) |
| **OpenAI Whisper** | 20231117 | Transcripción de audio |
| **PyTorch** | 2.5.1 | Framework de Deep Learning |
| **Transformers** | 4.46.3 | Modelos de Hugging Face |
| **Sentence-Transformers** | 3.3.1 | Embeddings semánticos |
| **MediaPipe** | 0.10.21 | Detección facial y tracking |

### Procesamiento Multimedia

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **OpenCV** | 4.9.0.80 | Visión por computadora |
| **MoviePy** | 2.2.1 | Procesamiento de video |
| **Librosa** | 0.11.0 | Análisis de audio |
| **Pydub** | 0.25.1 | Manipulación de audio |
| **FFmpeg** | (binario) | Codecs y conversión |

### Ciencia de Datos

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **NumPy** | 1.26.4 | Operaciones numéricas |
| **Pandas** | 2.2.3 | Manipulación de datos |
| **Scikit-learn** | 1.5.2 | Machine Learning clásico |
| **Matplotlib** | 3.9.3 | Visualización de datos |
| **SciPy** | 1.14.1 | Computación científica |

### Almacenamiento en la Nube

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Cloudinary** | 1.44.1 | CDN y almacenamiento de videos |
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
│   │   └── services.py            # Lógica de notificaciones
│   │
│   ├── reportes/                  # Generación de reportes
│   │   ├── views.py               # Reportes PDF/Excel
│   │   └── models.py              # Métricas
│   │
│   └── help/                      # Ayuda y documentación
│       ├── views.py               # Guías de usuario
│       └── urls.py                # Rutas de ayuda
│
├── templates/                     # Plantillas HTML
│   ├── base.html                  # Plantilla base
│   ├── auth/                      # Login, registro
│   ├── dashboard/                 # Dashboards de usuarios
│   ├── presentations/             # CRUD de presentaciones
│   ├── notifications/             # UI de notificaciones
│   └── reportes/                  # Visualización de reportes
│
├── static/                        # Archivos estáticos
│   ├── css/                       # Estilos personalizados
│   ├── js/                        # JavaScript
│   └── img/                       # Imágenes
│
├── uploads/                       # Archivos subidos (local)
│   ├── presentations/             # Videos de presentaciones
│   ├── avatars/                   # Fotos de perfil
│   └── participant_photos/        # Fotos de participantes
│
├── docs/                          # Documentación
│   ├── ARQUITECTURA_SISTEMA.md    # Este archivo
│   ├── CONFIGURACION.md           # Guía de configuración
│   └── DEPENDENCIAS.md            # Descripción de dependencias
│
├── manage.py                      # CLI de Django
├── requirements.txt               # Dependencias Python
├── setup.py                       # Script de instalación
└── .env                           # Variables de entorno
```

---

## 5. FLUJO DE FUNCIONAMIENTO

### A. Flujo del Estudiante

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INICIO DE SESIÓN                                         │
│    - El estudiante ingresa credenciales                     │
│    - Sistema valida y crea sesión                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. DASHBOARD ESTUDIANTIL                                    │
│    - Ve asignaciones pendientes                             │
│    - Ve historial de presentaciones                         │
│    - Estadísticas personales                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SUBIR PRESENTACIÓN                                       │
│    a. Selecciona asignación                                 │
│    b. Completa formulario (título, descripción)             │
│    c. Sube archivo de video (.mp4, .avi, .mov)              │
│    d. Validaciones:                                         │
│       - Tamaño máximo: 100 MB                               │
│       - Duración máxima: según asignación                   │
│       - Formato de video válido                             │
│       - Resolución mínima: 640x480                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. PROCESAMIENTO AUTOMÁTICO (Backend)                       │
│    Estado: PROCESSING                                       │
│                                                              │
│    a. Extracción de metadatos                               │
│       - Duración, resolución, FPS, codec                    │
│       - Generación de miniatura                             │
│                                                              │
│    b. Subida a Cloudinary (opcional)                        │
│       - Video almacenado en CDN                             │
│       - URL segura generada                                 │
│                                                              │
│    c. Extracción de audio                                   │
│       - FFmpeg extrae pista de audio                        │
│       - Conversión a formato WAV                            │
│                                                              │
│    d. Transcripción con Whisper                             │
│       - Audio → Texto                                       │
│       - Detección de segmentos temporales                   │
│       - Identificación de hablantes                         │
│                                                              │
│    e. Detección de rostros con MediaPipe                    │
│       - Identificación de participantes                     │
│       - Captura de fotos de cada rostro                     │
│       - Cálculo de tiempo de participación                  │
│       - Análisis de expresiones faciales                    │
│                                                              │
│    f. Análisis de coherencia con Groq AI (Llama 3.3)        │
│       - Análisis semántico del contenido                    │
│       - Evaluación de palabras clave                        │
│       - Profundidad del tema                                │
│       - Generación de feedback detallado                    │
│                                                              │
│    g. Calificación automática                               │
│       - Puntajes individuales por participante              │
│       - Retroalimentación personalizada                     │
│       - Recomendaciones de mejora                           │
│                                                              │
│    Estado cambia a: ANALYZED                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. NOTIFICACIÓN AL ESTUDIANTE                               │
│    - Email: "Tu presentación ha sido analizada"             │
│    - Notificación in-app                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. VER RESULTADOS                                           │
│    El estudiante puede:                                     │
│    - Ver puntaje de IA                                      │
│    - Leer retroalimentación detallada                       │
│    - Ver análisis por participante (si es grupal)           │
│    - Descargar transcripción                                │
│    - Esperar calificación final del docente                 │
└─────────────────────────────────────────────────────────────┘
```

### B. Flujo del Docente

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DASHBOARD DOCENTE                                        │
│    - Lista de cursos activos                                │
│    - Asignaciones pendientes                                │
│    - Presentaciones por calificar                           │
│    - Estadísticas del curso                                 │
└────────────────────┬────────────────────────────────────────┘
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

## 6. BASE DE DATOS

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

## 📊 MÉTRICAS Y ESTADÍSTICAS

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

## 🔄 CICLO DE VIDA DE UNA PRESENTACIÓN

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

---

## 🚀 ROADMAP FUTURO

### Funcionalidades planificadas:

1. **IA Avanzada**:
   - Análisis de emociones con reconocimiento facial
   - Detección de nerviosismo por voz
   - Sugerencias de mejora en tiempo real

2. **Grabación en vivo**:
   - Grabar directamente desde navegador
   - Detección de liveness (anti-trampa)
   - Streaming en vivo

3. **Gamificación**:
   - Insignias y logros
   - Rankings de estudiantes
   - Desafíos semanales

4. **Integraciones**:
   - Google Classroom
   - Microsoft Teams
   - Canvas LMS
   - Moodle

5. **Móvil**:
   - App nativa iOS/Android
   - Grabación móvil optimizada
   - Notificaciones push

---

## 📞 SOPORTE Y CONTACTO

- **GitHub**: https://github.com/LuisAngulo02/evaIA
- **Documentación**: `docs/`
- **Issues**: Reportar bugs en GitHub Issues

---

## 📝 LICENCIA

Este proyecto es privado y de uso académico.

---

## 🙏 AGRADECIMIENTOS

- **OpenAI** - Whisper para transcripción
- **Groq** - API de LLMs de alta velocidad
- **Google** - MediaPipe para detección facial
- **Cloudinary** - Almacenamiento en la nube
- **Django Community** - Framework web excepcional

---

**Última actualización**: Octubre 2025  
**Versión del sistema**: 0.5  
**Autor**: Luis Angulo  
**Email**: contacto@evalexpoai.com

---

¡Gracias por usar EvalExpo AI! 🎓✨
