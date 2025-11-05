# EvalExpo AI - Sistema de Evaluación de Presentaciones con IA

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.10-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-green.svg)
![Django](https://img.shields.io/badge/django-5.2.7-darkgreen.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Sistema inteligente para evaluar presentaciones académicas mediante Inteligencia Artificial**

[Instalación](#manual-de-instalación) • [Ejecución](#manual-de-ejecución) • [Manual de Usuario](#manual-de-usuario)

</div>

---

## Tabla de Contenidos

1. [Manual de Instalación](#manual-de-instalación)
2. [Manual de Ejecución](#manual-de-ejecución)
3. [Manual de Usuario](#manual-de-usuario)

---

## Manual de Instalación

### Paso 1: Preparar el Entorno

#### 1.1 Instalar Python

**IMPORTANTE: Este proyecto es compatible con Python 3.11+ (incluyendo Python 3.12)**

Las dependencias del proyecto están actualizadas y son compatibles con versiones modernas de Python. Se recomienda usar Python 3.11.8 o superior (hasta Python 3.12).

**Windows:**
```bash
# Opción 1: Descargar Python 3.12 desde: https://www.python.org/downloads/
# Opción 2: Descargar Python 3.11.8 desde: https://www.python.org/downloads/release/python-3118/
# Seleccionar: "Windows installer (64-bit)"
# IMPORTANTE: Marcar "Add Python to PATH" durante la instalación

# Verificar la instalación:
python --version
# Debe mostrar: Python 3.11.x o Python 3.12.x
```

**macOS:**
```bash
# Para Python 3.12
brew install python@3.12

# O para Python 3.11
brew install python@3.11

python3 --version
# Debe mostrar: Python 3.11.x o Python 3.12.x
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
# Para Python 3.12
sudo apt install python3.12 python3.12-venv python3-pip

# O para Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

python3 --version
# Debe mostrar: Python 3.11.x o Python 3.12.x
```

#### 1.2 Instalar PostgreSQL

**Windows:**
```bash
# Descargar desde https://www.postgresql.org/download/windows/
# Usar el instalador gráfico y recordar la contraseña del usuario 'postgres'
```

**macOS:**
```bash
brew install postgresql@13
brew services start postgresql@13
```

**Linux:**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 1.3 Instalar Git

**Windows:**
```bash
# Descargar desde https://git-scm.com/download/win
```

**macOS:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

### Paso 2: Clonar el Repositorio

```bash
# Navegar a la carpeta donde deseas instalar el proyecto
cd C:\Projects  # Windows
# cd ~/Projects  # macOS/Linux

# Clonar el repositorio (si está en GitHub)
git clone https://github.com/LuisAngulo02/evaIA.git

# O si ya tienes la carpeta, navegar a ella
cd "EvaIa V1.0.10"
```

### Paso 3: Crear la Base de Datos

```bash
# Conectarse a PostgreSQL
psql -U postgres

# Dentro de psql, ejecutar:
CREATE DATABASE evalexpo_db;
CREATE USER evalexpo_user WITH PASSWORD 'tu_contraseña_segura';
ALTER ROLE evalexpo_user SET client_encoding TO 'utf8';
ALTER ROLE evalexpo_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE evalexpo_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE evalexpo_db TO evalexpo_user;

# Salir de psql
\q
```

### Paso 4: Configurar el Entorno Virtual

**Windows (PowerShell):**
```powershell
# Navegar a la carpeta del proyecto
cd c:\Users\user\Desktop\evaIA

# Crear entorno virtual con Python
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar la versión de Python
python --version
# Debe mostrar: Python 3.11.x o Python 3.12.x
```

**macOS/Linux:**
```bash
# Navegar a la carpeta del proyecto
cd ~/Desktop/evaIA

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Verificar la versión de Python
python --version
# Debe mostrar: Python 3.11.x o Python 3.12.x
```

### Paso 5: Instalar Dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

**Notas importantes:**

1. **PyTorch y dependencias de IA**: La instalación puede tardar varios minutos dependiendo de tu conexión.

2. **Si obtienes error con `openai-whisper`**: Este paquete requiere Rust y herramientas de compilación. Si falla, comenta la línea en `requirements.txt`:
   ```python
   # openai-whisper==20231117  # Requiere Rust
   ```

3. **Compatibilidad**: Todas las versiones en `requirements.txt` están probadas y son compatibles con Python 3.11.8 y Python 3.12.

### Paso 6: Configurar Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```bash
# En Windows
notepad .env

# En macOS/Linux
nano .env
```

Agregar las siguientes variables:

```env
# Base de Datos
DB_NAME=evalexpo_db
DB_USER=evalexpo_user
DB_PASSWORD=tu_contraseña_segura
DB_HOST=localhost
DB_PORT=5432

# Cloudinary (para almacenamiento de archivos)
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# API de Groq (para análisis de IA)
GROQ_API_KEY=tu_groq_api_key

# Configuración de Django
SECRET_KEY=django-insecure-#l1*xrw5x@0nqr^(ip@71%1z6e1wj_(0etuw2$xjj3w%pq^!33
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

**Obtener credenciales:**
- **Cloudinary**: Registrarse en https://cloudinary.com/ (plan gratuito disponible)
- **Groq API**: Registrarse en https://console.groq.com/ (obtener API key gratuita)

### Paso 7: Configurar la Base de Datos

```bash
# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario para el panel de administración
python manage.py createsuperuser
# Seguir las instrucciones en pantalla
```

### Paso 8: Cargar Datos Iniciales (Opcional)

```bash
# Si existen fixtures o datos de prueba
python manage.py loaddata initial_data.json
```

### Paso 9: Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### Paso 10: Verificar la Instalación

```bash
# Ejecutar pruebas
python manage.py test

# Si todo está correcto, deberías ver:
# Ran X tests in Y seconds
# OK
```

**Instalación completada exitosamente!**

---

## Manual de Ejecución

### Ejecución en Modo Desarrollo

#### 1. Activar el Entorno Virtual

**Windows (PowerShell):**
```powershell
cd "d:\Descargas\EvaIa V1.0.10"
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
cd ~/Descargas/EvaIa\ V1.0.10
source venv/bin/activate
```

#### 2. Iniciar el Servidor de Desarrollo

```bash
python manage.py runserver
```

**Salida esperada:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 03, 2025 - 15:30:00
Django version 5.2.7, using settings 'sist_evaluacion_expo.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

#### 3. Acceder a la Aplicación

Abrir el navegador y visitar:

- **Aplicación principal**: http://127.0.0.1:8000/
- **Panel de administración**: http://127.0.0.1:8000/admin/
- **Login de usuarios**: http://127.0.0.1:8000/auth/login/

#### 4. Detener el Servidor

Presionar `CTRL + C` en la terminal.

### Ejecución en Otro Puerto

```bash
# Si el puerto 8000 está ocupado
python manage.py runserver 8080

# O especificar IP y puerto
python manage.py runserver 0.0.0.0:8080
```

### Ejecución con Recarga Automática

```bash
# Django recarga automáticamente al detectar cambios en archivos .py
# No es necesaria configuración adicional
```

### Comandos Útiles de Gestión

```bash
# Ver migraciones pendientes
python manage.py showmigrations

# Crear un nuevo superusuario
python manage.py createsuperuser

# Limpiar sesiones expiradas
python manage.py clearsessions

# Ver la shell de Django (para pruebas)
python manage.py shell

# Crear una app nueva
python manage.py startapp nombre_app
```

### Ejecución en Modo Producción (Básico)

**Advertencia:** No usar el servidor de desarrollo en producción.

Para producción, usar un servidor WSGI como Gunicorn:

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn sist_evaluacion_expo.wsgi:application --bind 0.0.0.0:8000

# Con workers múltiples
gunicorn sist_evaluacion_expo.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Logs y Depuración

```bash
# Ver logs en tiempo real (si están configurados)
tail -f logs/django.log

# Ejecutar con más verbosidad
python manage.py runserver --verbosity 2
```

##  Manual de Usuario

### 1. Primer Acceso al Sistema

#### 1.1 Registro de Usuarios

1. Visitar http://127.0.0.1:8000/
2. Hacer clic en **"Registrarse"** o **"Sign Up"**
3. Completar el formulario con:
   - Nombre completo
   - Correo electrónico institucional
   - Contraseña segura (mínimo 8 caracteres)
   - Tipo de usuario: **Estudiante** o **Docente**
4. Hacer clic en **"Crear Cuenta"**
5. Revisar el correo electrónico de confirmación (si está configurado)

#### 1.2 Inicio de Sesión

1. Ir a http://127.0.0.1:8000/auth/login/
2. Ingresar:
   - **Correo electrónico**
   - **Contraseña**
3. Hacer clic en **"Iniciar Sesión"**

#### 1.3 Recuperación de Contraseña

1. En la página de login, clic en **"¿Olvidaste tu contraseña?"**
2. Ingresar el correo electrónico registrado
3. Seguir las instrucciones del correo recibido

---

### 2. Manual para Estudiantes

#### 2.1 Dashboard del Estudiante

Después de iniciar sesión, verás:
- **Resumen de cursos** en los que estás inscrito
- **Asignaciones pendientes** con fechas límite
- **Notificaciones** de calificaciones y comentarios
- **Estadísticas** de tus presentaciones

#### 2.2 Subir una Presentación

##### Opción A: Subir Archivo de Video

1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**
2. Seleccionar la pestaña **"Subir Archivo"**
3. Completar el formulario:
   - **Asignación**: Seleccionar de la lista desplegable
   - **Título**: Nombre descriptivo de tu presentación
   - **Archivo de video**: 
     - Arrastra el archivo o haz clic para seleccionar
     - Formatos: MP4, AVI, MOV, MKV, WEBM
     - Tamaño máximo: 500 MB
     - Duración máxima: 30 minutos
   - **Descripción** (opcional): Notas adicionales
4. Clic en **"Subir Presentación"**
5. Esperar la confirmación de carga

**Consejos:**
- Buena iluminación y audio claro
- Cámara estable (usar trípode si es posible)
- Hablar con claridad y buen volumen
- Verificar que el video esté completo antes de subir

##### Opción B: Grabar en Vivo

1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**
2. Seleccionar la pestaña **"Grabar en Vivo"**
3. Permitir acceso a la cámara y micrófono cuando el navegador lo solicite
4. Seleccionar la **asignación**
5. Revisar las instrucciones mostradas
6. Verificar que aparezca **"Rostro detectado!"** (indicador verde)
   - Solo debe haber **1 persona** visible en cámara
   - Si se detectan múltiples personas, la grabación se pausará
7. Clic en **"Iniciar Grabación"**
8. Aparecerá una cuenta regresiva de 3 segundos
9. Realizar la presentación
10. Controles disponibles:
    - **Pausar**: Pausa temporalmente la grabación
    - **Reanudar**: Continúa la grabación
    - **Detener**: Finaliza la grabación
    - **Reiniciar**: Descarta y comienza de nuevo
11. Al detener, revisar la vista previa
12. Completar **título** y **descripción**
13. Clic en **"Guardar Presentación"**

**Indicadores importantes:**
- **Luz roja parpadeante**: Grabando
- **Temporizador**: Muestra el tiempo transcurrido
- **Rostro detectado**: Verde = OK, Rojo = Problema
- **Advertencia múltiples personas**: Se pausará automáticamente

#### 2.3 Ver Resultados de Evaluación

1. Ir a **"Mis Presentaciones"**
2. Buscar tu presentación en la lista
3. Hacer clic en **"Ver Detalles"** o en el título
4. Visualizar:
   - **Calificación numérica** (0-100)
   - **Estado**: Pendiente, En Proceso, Completado
   - **Transcripción** del audio
   - **Análisis de IA** con:
     - Fortalezas identificadas
     - Áreas de mejora
     - Recomendaciones específicas
   - **Comentarios del docente** (si están disponibles)
   - **Desglose por criterios** de evaluación
   - **Video de la presentación**

#### 2.4 Responder a Comentarios

1. En la página de detalles de la presentación
2. Scroll hasta la sección **"Comentarios"**
3. Escribir tu respuesta en el cuadro de texto
4. Clic en **"Enviar Comentario"**
5. El docente recibirá una notificación

#### 2.5 Notificaciones

- **Campana de notificaciones**: Esquina superior derecha
- Tipos de notificaciones:
  - Nueva calificación disponible
  - Nuevo comentario del docente
  - Recordatorio de fecha límite próxima
  - Presentación procesada exitosamente
- Hacer clic en una notificación para ir directamente al detalle

---

### 3. Manual para Docentes

#### 3.1 Dashboard del Docente

Al iniciar sesión como docente, verás:
- **Cursos que impartes**
- **Asignaciones activas**
- **Presentaciones pendientes de calificar**
- **Estadísticas generales** de los estudiantes

#### 3.2 Crear un Curso

1. Ir a **"Mis Cursos"** → **"Nuevo Curso"**
2. Completar:
   - **Código del curso**: Ej. "CS101"
   - **Nombre**: Ej. "Introducción a la Programación"
   - **Descripción**: Información del curso
   - **Período académico**: Ej. "2025-1"
3. Clic en **"Crear Curso"**

#### 3.3 Gestionar Estudiantes

1. Entrar al curso deseado
2. Ir a **"Estudiantes"**
3. Opciones:
   - **Agregar estudiante**: Buscar por correo e invitar
   - **Importar lista**: Subir CSV con correos
   - **Eliminar estudiante**: Remover del curso
   - **Ver perfil**: Información detallada del estudiante

**Formato CSV para importación:**
```csv
nombre,apellido,correo
Juan,Pérez,juan.perez@universidad.edu
María,González,maria.gonzalez@universidad.edu
```

#### 3.4 Crear una Asignación

1. Dentro del curso, ir a **"Asignaciones"**
2. Clic en **"Nueva Asignación"**
3. Completar el formulario:
   - **Título**: Ej. "Presentación Final - Proyecto Web"
   - **Descripción**: Explicación detallada
   - **Tipo**: Individual o Grupal
   - **Fecha límite**: Seleccionar fecha y hora
   - **Duración máxima**: En minutos (ej. 15)
   - **Puntaje máximo**: Ej. 100
   - **Instrucciones**: Detalles específicos para los estudiantes
   - **Criterios de evaluación**: (Ver sección 3.5)
4. Clic en **"Crear Asignación"**

#### 3.5 Configurar Rúbrica de Evaluación

Al crear o editar una asignación:

1. Scroll hasta **"Criterios de Evaluación"**
2. Agregar criterios, por ejemplo:
   - **Contenido** (30 puntos)
     - Dominio del tema
     - Profundidad del análisis
   - **Organización** (20 puntos)
     - Estructura lógica
     - Transiciones claras
   - **Expresión Verbal** (25 puntos)
     - Claridad al hablar
     - Volumen y tono adecuados
   - **Lenguaje Corporal** (15 puntos)
     - Contacto visual
     - Postura profesional
   - **Tiempo** (10 puntos)
     - Cumplimiento del tiempo asignado

3. Especificar ponderaciones para cada criterio
4. Guardar la rúbrica

**Nota:** La IA utilizará estos criterios para generar evaluaciones detalladas.

#### 3.6 Revisar Presentaciones

##### Revisión Individual

1. Ir a **"Presentaciones"** → **"Pendientes de Calificar"**
2. Seleccionar una presentación
3. Revisar:
   - **Video de la presentación**
   - **Transcripción automática**
   - **Análisis preliminar de IA**
   - **Sugerencias de calificación**

##### Calificación Manual

1. En la página de detalles de la presentación
2. Clic en **"Calificar"**
3. Opciones:
   - **Aceptar calificación de IA**: Usar la evaluación automática
   - **Modificar calificación**: Ajustar puntos por criterio
   - **Calificación personalizada**: Ingresar manualmente
4. Agregar **comentarios** para el estudiante:
   - Fortalezas observadas
   - Áreas de mejora específicas
   - Consejos para futuras presentaciones
5. Clic en **"Guardar Calificación"**

**El estudiante recibirá una notificación automática.**

##### Calificación por Lotes

1. Ir a **"Calificaciones"** → **"Calificar Múltiples"**
2. Seleccionar las presentaciones
3. Aplicar criterios comunes
4. Clic en **"Guardar Todas"**

#### 3.7 Configuración de IA

1. Ir a **"Configuración"** → **"IA y Análisis"**
2. Ajustar:
   - **Modelo de lenguaje**: Groq (rápido) u OpenAI (preciso)
   - **Nivel de detalle**: Básico, Intermedio, Avanzado
   - **Idioma de análisis**: Español, Inglés
   - **Sensibilidad de evaluación**: Estricto, Moderado, Flexible
3. **Probar configuración**: Ejecutar análisis de prueba
4. Guardar cambios

#### 3.8 Reportes y Estadísticas

##### Reporte Individual

1. Seleccionar un estudiante
2. Ir a **"Ver Reporte"**
3. Descargar en formato:
   - PDF (para imprimir)
   - Excel (para análisis)
   - CSV (para importar a otros sistemas)

##### Reporte de Curso

1. Entrar al curso
2. Clic en **"Reportes"**
3. Visualizar:
   - **Progreso general** del curso
   - **Gráficas de desempeño**
   - **Comparativas entre estudiantes**
   - **Tendencias de mejora**
4. Filtros disponibles:
   - Por asignación
   - Por fecha
   - Por rango de calificación

##### Exportar Calificaciones

1. En la vista de curso, ir a **"Calificaciones"**
2. Clic en **"Exportar"**
3. Seleccionar formato (Excel, CSV, PDF)
4. Descargar archivo

---

### 4. Manual para Administradores

#### 4.1 Panel de Administración

Acceder a: http://127.0.0.1:8000/admin/

Funciones disponibles:
- Gestión completa de usuarios
- Supervisión de cursos y asignaciones
- Monitoreo de uso del sistema
- Configuración de parámetros globales

#### 4.2 Gestión de Usuarios

1. En el panel admin, ir a **"Authentication"** → **"Users"**
2. Opciones:
   - **Crear usuario**: Agregar manualmente
   - **Editar usuario**: Cambiar rol, permisos
   - **Activar/Desactivar**: Suspender cuentas
   - **Eliminar**: Remover permanentemente

#### 4.3 Configuración del Sistema

1. Ir a **"Settings"** en el panel admin
2. Configurar:
   - **Límites de almacenamiento**
   - **Duración máxima de videos**
   - **Tamaño máximo de archivos**
   - **Cuota de API de IA**
   - **Notificaciones por email**

#### 4.4 Monitoreo de Recursos

1. **Dashboard de Administrador**
2. Ver:
   - Uso de almacenamiento (Cloudinary)
   - Consumo de API de IA (Groq/OpenAI)
   - Número de usuarios activos
   - Presentaciones procesadas
   - Tiempo promedio de procesamiento

#### 4.5 Backups y Mantenimiento

```bash
# Backup de la base de datos
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Restaurar desde backup
python manage.py loaddata backup_20251103.json

# Limpiar archivos temporales
python manage.py clearsessions
python manage.py cleanup_uploads

# Ver logs del sistema
tail -f logs/system.log
```

---

### 5. Funciones Comunes para Todos los Usuarios

#### 5.1 Editar Perfil

1. Clic en el **avatar** (esquina superior derecha)
2. Seleccionar **"Mi Perfil"**
3. Editar:
   - Foto de perfil
   - Nombre y apellidos
   - Correo electrónico
   - Contraseña
   - Preferencias de notificación
4. Clic en **"Guardar Cambios"**

#### 5.2 Cambiar Contraseña

1. Ir a **"Mi Perfil"** → **"Seguridad"**
2. Ingresar:
   - Contraseña actual
   - Nueva contraseña
   - Confirmar nueva contraseña
3. Clic en **"Actualizar Contraseña"**

#### 5.3 Configurar Notificaciones

1. Ir a **"Configuración"** → **"Notificaciones"**
2. Activar/desactivar:
   - Notificaciones por correo
   - Notificaciones en la app
   - Frecuencia de resúmenes
3. Guardar preferencias

#### 5.4 Centro de Ayuda

1. Clic en el ícono **"?"** (esquina superior)
2. Acceder a:
   - **Preguntas frecuentes (FAQ)**
   - **Tutoriales en video**
   - **Documentación técnica**
   - **Contactar soporte**

#### 5.5 Cerrar Sesión

1. Clic en el **avatar**
2. Seleccionar **"Cerrar Sesión"**
3. Confirmar

---

### 6. Mejores Prácticas

#### Para Estudiantes

**Antes de grabar:**
- Revisar las instrucciones de la asignación
- Preparar y practicar tu presentación
- Verificar audio y video
- Elegir un fondo limpio y profesional
- Asegurar buena iluminación

**Durante la grabación:**
- Mantener contacto visual con la cámara
- Hablar con claridad y a buen volumen
- Evitar muletillas ("ehh", "mmm")
- Controlar el tiempo
- Mantener una postura profesional

**Después de subir:**
- Verificar que el video se cargó correctamente
- Revisar la transcripción por si hay errores
- Estar atento a las notificaciones
- Responder a comentarios del docente

#### Para Docentes

**Al crear asignaciones:**
- Proporcionar instrucciones claras y detalladas
- Establecer criterios de evaluación específicos
- Dar tiempo suficiente para preparación
- Comunicar expectativas claramente

**Al evaluar:**
- Revisar el análisis de IA como guía inicial
- Proporcionar retroalimentación constructiva
- Ser específico en los comentarios
- Destacar tanto fortalezas como áreas de mejora
- Responder dudas de los estudiantes

---

<div align="center">

**EvalExpo AI - Sistema de Evaluación de Presentaciones con IA**

[Volver arriba](#evalexpo-ai---sistema-de-evaluación-de-presentaciones-con-ia)

</div>

