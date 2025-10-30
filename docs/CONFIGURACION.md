# 📚 DOCUMENTACIÓN DE CONFIGURACIÓN - EVALEXPO AI

## 🎯 RESUMEN DEL SISTEMA

EvalExpo AI es un sistema de evaluación de exposiciones académicas que utiliza:
- **Django 5.2.7** - Framework web
- **PostgreSQL** - Base de datos
- **Cloudinary** - Almacenamiento en la nube
- **Gmail SMTP** - Envío de emails
- **Groq API** - Análisis de IA avanzado
- **MediaPipe** - Detección facial

---

## 🔧 VARIABLES DE ENTORNO (.env)

### Configuración Mínima Requerida

```bash
# Configuración de Email (Gmail)
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=contraseña-de-aplicacion-gmail

# Configuración de Cloudinary (Opcional pero Recomendado)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret

# Configuración de IA (Opcional)
GROQ_API_KEY=tu-groq-api-key
```

---

## 📧 CONFIGURACIÓN DE EMAIL (Gmail)

### Paso 1: Activar Verificación en 2 Pasos
1. Ve a https://myaccount.google.com/
2. Navega a **Seguridad**
3. Activa **Verificación en 2 pasos**

### Paso 2: Generar Contraseña de Aplicación
1. En la misma página de seguridad
2. Busca **Contraseñas de aplicaciones**
3. Crea una nueva para "Correo" o "Django App"
4. Copia la contraseña de 16 caracteres (sin espacios)

### Paso 3: Configurar en .env
```bash
EMAIL_HOST_USER=evalexpo@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop  # Sin espacios ni guiones
```

### Probar Configuración
```bash
python test_email.py
```

---

## ☁️ CONFIGURACIÓN DE CLOUDINARY

### ¿Por qué Cloudinary?
- ✅ **10GB gratis** al mes
- ✅ **CDN global** para carga rápida de videos
- ✅ **Optimización automática** de archivos
- ✅ **Transformaciones on-the-fly**
- ✅ **No llena tu servidor**

### Paso 1: Crear Cuenta
1. Ve a https://cloudinary.com/
2. Regístrate gratis
3. Accede al Dashboard

### Paso 2: Obtener Credenciales
En el Dashboard encontrarás:
- **Cloud Name** - Nombre de tu nube
- **API Key** - Clave de API
- **API Secret** - Secreto de API

### Paso 3: Configurar en .env
```bash
CLOUDINARY_CLOUD_NAME=evalexpo
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
```

### Paso 4: Probar Configuración
```bash
python test_cloudinary.py
```

### Estructura de Carpetas en Cloudinary
```
cloudinary/
├── presentations/          # Videos de presentaciones
│   ├── username1/
│   ├── username2/
│   └── ...
├── participant_photos/     # Fotos de participantes
└── test_evalexpo/         # Archivos de prueba
```

---

## 🤖 CONFIGURACIÓN DE IA (Groq API)

### ¿Qué hace Groq?
Groq proporciona análisis avanzado de coherencia en las presentaciones usando el modelo Llama 3.3 70B.

### Paso 1: Obtener API Key
1. Ve a https://console.groq.com/
2. Crea una cuenta
3. Genera una API Key

### Paso 2: Configurar en .env
```bash
GROQ_API_KEY=gsk_tu_api_key_aqui
```

### Configuración Actual
- **Modelo**: llama-3.3-70b-versatile
- **Temperature**: 0.3 (baja para consistencia)
- **Max Tokens**: 2000
- **Timeout**: 45 segundos

---

## 🗄️ CONFIGURACIÓN DE BASE DE DATOS

### PostgreSQL (Producción)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'evalexpo_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### SQLite (Desarrollo - Por defecto)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 🚀 INSTALACIÓN Y CONFIGURACIÓN INICIAL

### 1. Clonar Repositorio
```bash
git clone https://github.com/tu-usuario/evalexpo-ai.git
cd evalexpo-ai
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# o
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Crear archivo .env en la raíz del proyecto
# Copiar el contenido de .env.example y completar
```

### 5. Ejecutar Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear Superusuario
```bash
python manage.py createsuperuser
```

### 7. Verificar Sistema
```bash
python verificar_sistema.py
```

### 8. Ejecutar Servidor
```bash
python manage.py runserver
```

---

## 🧪 SCRIPTS DE PRUEBA

### Verificación Completa del Sistema
```bash
python verificar_sistema.py
```
Verifica todas las configuraciones: email, Cloudinary, DB, IA, etc.

### Prueba de Email
```bash
python test_email.py
```
Envía un email de prueba.

### Prueba de Cloudinary
```bash
python test_cloudinary.py
```
Prueba subida, descarga y eliminación de archivos en Cloudinary.

### Prueba de Tokens Groq
```bash
python test_groq_tokens.py
```
Verifica disponibilidad y uso de tokens de Groq API.

### Prueba de Detección Facial
```bash
python test_face_detection_filters.py
```
Prueba filtros de detección facial con MediaPipe.

---

## 📦 ESTRUCTURA DEL PROYECTO

```
evalexpo-ai/
├── apps/
│   ├── ai_processor/
│   │   └── services/
│   │       ├── ai_service.py
│   │       ├── cloudinary_service.py
│   │       ├── face_detection_service.py
│   │       ├── transcription_service.py
│   │       └── ...
│   ├── presentaciones/
│   ├── reportes/
│   ├── notifications/
│   └── help/
├── authentication/
├── sist_evaluacion_expo/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
├── static/
├── media/
├── .env
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔒 SEGURIDAD

### Producción
- ✅ `DEBUG = False`
- ✅ Configurar `SECRET_KEY` único
- ✅ Configurar `ALLOWED_HOSTS` correctamente
- ✅ Usar HTTPS (`CSRF_COOKIE_SECURE = True`)
- ✅ Usar PostgreSQL en lugar de SQLite
- ✅ Configurar firewall y permisos

### Variables Sensibles
Nunca subas al repositorio:
- ❌ `.env`
- ❌ `db.sqlite3`
- ❌ Contraseñas o API Keys
- ❌ Archivos en `media/` o `uploads/`

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Authentication unsuccessful" (Email)
**Causa**: Contraseña incorrecta o 2FA no activado
**Solución**: 
1. Verifica que la verificación en 2 pasos esté activada
2. Genera una nueva contraseña de aplicación
3. Copia la contraseña sin espacios ni guiones

### Error: "Cloudinary not configured"
**Causa**: Variables de entorno faltantes
**Solución**: 
1. Verifica que `.env` tenga las 3 variables de Cloudinary
2. Reinicia el servidor después de modificar `.env`
3. Ejecuta `python test_cloudinary.py` para verificar

### Error: "No module named 'cloudinary'"
**Causa**: Paquete no instalado
**Solución**:
```bash
pip install cloudinary django-cloudinary-storage
```

### Error: Base de datos bloqueada
**Causa**: SQLite no soporta múltiples escrituras simultáneas
**Solución**: Usa PostgreSQL en producción

---

## 📞 SOPORTE

- **Repositorio**: https://github.com/LuisAngulo02/evaIA
- **Documentación Django**: https://docs.djangoproject.com/
- **Documentación Cloudinary**: https://cloudinary.com/documentation
- **Documentación Groq**: https://console.groq.com/docs

---

## 📝 NOTAS ADICIONALES

### Límites de Servicios Gratuitos
- **Cloudinary**: 10GB/mes, 25 créditos de transformación
- **Groq**: Según plan gratuito actual
- **Gmail SMTP**: 500 emails/día

### Recomendaciones
- Usa Cloudinary para videos (evita llenar el servidor)
- Configura backups regulares de la base de datos
- Monitorea el uso de APIs para evitar límites
- Usa PostgreSQL en producción por rendimiento

---

**Última actualización**: Octubre 2025
**Versión del sistema**: 0.02
