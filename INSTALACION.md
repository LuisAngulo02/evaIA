# 🎓 EVALEXPO AI - GUÍA DE INSTALACIÓN COMPLETA

## 📋 REQUISITOS PREVIOS

### Sistema Operativo
- Windows 10/11
- Python 3.9 - 3.12
- Git

### Herramientas Necesarias
- PostgreSQL 14+
- Visual Studio Build Tools (para bibliotecas de C++)

## 🚀 INSTALACIÓN PASO A PASO

### 1. Clonar el repositorio
```bash
git clone https://github.com/LuisAngulo02/evaIA.git
cd evaIA
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias principales
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos PostgreSQL
```sql
-- Crear base de datos
CREATE DATABASE evalexpo_db;
CREATE USER evalexpo_user WITH PASSWORD 'tu_password_segura';
GRANT ALL PRIVILEGES ON DATABASE evalexpo_db TO evalexpo_user;
```

### 5. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
DEBUG=True
SECRET_KEY=tu_clave_secreta_muy_segura
DATABASE_URL=postgresql://evalexpo_user:tu_password_segura@localhost:5432/evalexpo_db
OPENAI_API_KEY=tu_api_key_opcional
```

### 6. Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario
```bash
python manage.py createsuperuser
```

### 8. Configurar FFmpeg (para transcripción)
```bash
# Se instala automáticamente con imageio-ffmpeg
# Si hay problemas, descargar FFmpeg manualmente desde:
# https://ffmpeg.org/download.html
```

### 9. Ejecutar servidor
```bash
python manage.py runserver
```

## 🧪 VERIFICAR INSTALACIÓN

### Probar módulos principales:
```bash
# Probar transcripción
python -c "import whisper; print('Whisper OK')"

# Probar video processing
python -c "import moviepy; print('MoviePy OK')"

# Probar base de datos
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('DB OK')"
```

## 📦 DEPENDENCIAS EXPLICADAS

### CORE (Django)
- `Django==5.2.1` - Framework web principal
- `psycopg2-binary==2.9.9` - Conector PostgreSQL

### INTELIGENCIA ARTIFICIAL
- `openai-whisper==20240930` - Transcripción de voz a texto
- `torch==2.5.1` - Machine Learning backend
- `transformers==4.46.3` - Modelos de lenguaje (futuro)
- `openai==1.54.4` - API OpenAI (futuro análisis)

### PROCESAMIENTO MULTIMEDIA
- `moviepy==1.0.3` - Procesamiento de video
- `imageio-ffmpeg==0.6.0` - FFmpeg integrado
- `librosa==0.11.0` - Análisis de audio
- `opencv-python==4.10.0.84` - Visión computacional

### ANÁLISIS AVANZADO (Preparado para futuro)
- `face-recognition==1.3.0` - Detección de rostros
- `scikit-learn==1.7.2` - Machine Learning
- `pandas==2.2.3` - Análisis de datos

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "No module named cv2"
```bash
pip install opencv-python
```

### Error: FFmpeg no encontrado
```bash
pip install --upgrade imageio-ffmpeg
```

### Error: dlib installation failed
```bash
# En Windows, descargar wheel precompilado:
pip install dlib-19.24.6-cp311-cp311-win_amd64.whl
```

### Error: PostgreSQL connection
- Verificar que PostgreSQL esté corriendo
- Revisar credenciales en archivo `.env`
- Verificar permisos de usuario en base de datos

## 🎯 FUNCIONALIDADES DISPONIBLES

### ✅ IMPLEMENTADO
- Sistema de usuarios (estudiantes, docentes, admin)
- Subida de videos de presentaciones
- Transcripción automática con Whisper AI
- Dashboard para cada tipo de usuario
- Sistema de notificaciones

### 🔄 EN DESARROLLO
- Detección de rostros múltiples
- Análisis de participación individual
- Calificación automática con métricas IA
- Análisis de coherencia temática

### 📋 PLANIFICADO
- Reportes estadísticos avanzados
- Exportación de datos
- API REST completa
- Análisis de emociones en video

## 🚀 DESPLIEGUE EN PRODUCCIÓN

### Preparar para producción:
```bash
# Instalar servidor web
pip install gunicorn

# Configurar archivos estáticos
python manage.py collectstatic

# Variables de entorno para producción
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com
```

