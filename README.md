# 🎓 EvalExpo AI

**Sistema de Evaluación Automática de Exposiciones Académicas con Inteligencia Artificial**

## 🎯 Descripción

EvalExpo AI es una plataforma web innovadora que utiliza inteligencia artificial para evaluar automáticamente presentaciones académicas. El sistema permite a estudiantes subir videos de sus exposiciones y recibir retroalimentación objetiva e inmediata a través de análisis avanzados de IA.

## ✨ Características Principales

### 🎤 **Transcripción Automática**
- Conversión de audio a texto usando Whisper AI de OpenAI
- Generación de timestamps precisos
- Soporte para múltiples formatos de video (MP4, AVI, MOV, etc.)

### 👥 **Gestión de Usuarios**
- **Estudiantes**: Suben presentaciones y reciben evaluaciones
- **Docentes**: Crean asignaciones y revisan resultados
- **Administradores**: Gestionan usuarios y configuraciones del sistema

### 📊 **Análisis Inteligente** (En desarrollo)
- Detección de rostros múltiples en presentaciones grupales
- Medición de participación individual por tiempo frente a cámara
- Análisis de coherencia temática comparando discurso vs tema asignado
- Calificación automática basada en métricas objetivas

## 🏗️ Arquitectura del Sistema

### **Backend**
- **Django 5.2.1**: Framework web principal
- **PostgreSQL**: Base de datos robusta
- **Whisper AI**: Transcripción de voz a texto
- **OpenCV**: Procesamiento de video (futuro)

### **Frontend**
- **Bootstrap 5**: Interfaz responsive
- **JavaScript**: Interactividad dinámica
- **CSS personalizado**: Diseño moderno

### **Inteligencia Artificial**
- **Whisper**: Transcripción automática
- **PyTorch**: Framework de ML
- **Transformers**: Análisis de lenguaje (futuro)
- **Face Recognition**: Detección de rostros (futuro)

## 📂 Estructura del Proyecto

```
evalexpo_ai/
├── apps/
│   ├── ai_processor/          # Módulos de IA
│   ├── notifications/         # Sistema de notificaciones
│   ├── presentaciones/       # Gestión de presentaciones
│   ├── reportes/             # Generación de reportes
│   └── help/                 # Sistema de ayuda
├── authentication/           # Autenticación y usuarios
├── templates/               # Plantillas HTML
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── media/                  # Archivos subidos por usuarios
└── sist_evaluacion_expo/   # Configuración principal
```

## 🚀 Instalación Rápida

1. **Clonar repositorio**:
   ```bash
   git clone https://github.com/LuisAngulo02/evaIA.git
   cd evaIA
   ```

2. **Configurar entorno**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configurar base de datos** (PostgreSQL requerido)

4. **Ejecutar migraciones**:
   ```bash
   python manage.py migrate
   ```

5. **Crear superusuario**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar servidor**:
   ```bash
   python manage.py runserver
   ```

Ver [INSTALACION.md](INSTALACION.md) para guía detallada.

## 📋 Módulos Implementados

### ✅ **Módulo de Gestión de Usuarios**
- ✅ Autenticación segura con roles diferenciados
- ✅ Registro de usuarios con validación
- ✅ Control de acceso basado en permisos
- ✅ Perfiles personalizados por tipo de usuario

### ✅ **Módulo de Transcripción Automática**
- ✅ Procesamiento de video con MoviePy
- ✅ Transcripción con Whisper AI (modelo base)
- ✅ Generación de timestamps automáticos
- ✅ Interfaz web para iniciar transcripción on-demand

### 🔄 **En Desarrollo**
- 📹 Detección y etiquetado de rostros múltiples
- ⏱️ Medición de participación individual por tiempo
- 🎯 Análisis de coherencia temática con IA
- 📊 Calificación automática con métricas combinadas

## 🎮 Funcionalidades por Usuario

### 👨‍🎓 **Estudiantes**
- Subir videos de presentaciones
- Ver transcripciones automáticas
- Recibir evaluaciones de IA
- Consultar historial de presentaciones
- Acceder a retroalimentación detallada

### 👨‍🏫 **Docentes**
- Crear y gestionar cursos
- Definir asignaciones con fechas límite
- Revisar presentaciones de estudiantes
- Acceder a reportes estadísticos
- Supervisar análisis de IA

### 👨‍💼 **Administradores**
- Gestionar usuarios del sistema
- Configurar parámetros globales
- Monitorear uso de recursos
- Administrar cursos y asignaciones
- Acceder a métricas del sistema

## 🔧 Tecnologías Utilizadas

### **Inteligencia Artificial**
- OpenAI Whisper (transcripción)
- PyTorch (framework ML)
- Transformers (análisis de texto)
- OpenCV (visión computacional)
- Face Recognition (detección rostros)

### **Backend**
- Django 5.2.1 (framework web)
- PostgreSQL (base de datos)
- Gunicorn (servidor WSGI)
- WhiteNoise (archivos estáticos)

### **Procesamiento Multimedia**
- MoviePy (edición de video)
- Librosa (análisis de audio)
- ImageIO + FFmpeg (codecs)
- Pillow (procesamiento imágenes)

### **Frontend**
- Bootstrap 5 (CSS framework)
- JavaScript ES6+ (interactividad)
- Font Awesome (iconografía)
- Chart.js (gráficos y métricas)

## 📈 Roadmap de Desarrollo

### **Fase 1: Base (Completada)**
- ✅ Sistema de usuarios y autenticación
- ✅ Subida y gestión de videos
- ✅ Transcripción básica con Whisper

### **Fase 2: IA Avanzada (En Progreso)**
- 🔄 Detección de rostros múltiples
- 🔄 Análisis de participación individual
- 🔄 Coherencia temática con GPT

### **Fase 3: Evaluación Automática (Planificada)**
- 📋 Sistema de calificación integral
- 📋 Retroalimentación personalizada
- 📋 Métricas de desempeño avanzadas

### **Fase 4: Escalabilidad (Futuro)**
- 📋 API REST completa
- 📋 Integración con LMS externos
- 📋 Análisis de emociones en video

## 🤝 Contribuciones

El proyecto está abierto a contribuciones. Para colaborar:

1. Fork del repositorio
2. Crear branch para nueva feature
3. Desarrollar con tests incluidos
4. Crear Pull Request con descripción detallada

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Desarrollador

**Luis Angulo**
- GitHub: [@LuisAngulo02](https://github.com/LuisAngulo02)
- Proyecto: Sistema de Evaluación con IA para Presentaciones Académicas

---

⭐ **Si este proyecto te resulta útil, considera darle una estrella en GitHub**

🚀 **EvalExpo AI** - Revolucionando la evaluación académica con Inteligencia Artificial