# EvalExpo AI - Sistema de Evaluación de Presentaciones con IA # EvalExpo AI - Sistema de Evaluación de Presentaciones con IA



<div align="center"><div align="center">



![Version](https://img.shields.io/badge/version-1.0.10-blue.svg)![Version](https://img.shields.io/badge/version-1.0.10-blue.svg)

![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-green.svg)![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-green.svg)

![Django](https://img.shields.io/badge/django-5.2.7-darkgreen.svg)![Django](https://img.shields.io/badge/django-5.2.7-darkgreen.svg)

![License](https://img.shields.io/badge/license-MIT-orange.svg)![License](https://img.shields.io/badge/license-MIT-orange.svg)



**Sistema inteligente para evaluar presentaciones académicas mediante Inteligencia Artificial****Sistema inteligente para evaluar presentaciones académicas mediante Inteligencia Artificial**



</div>[Instalación](#manual-de-instalación) • [Ejecución](#manual-de-ejecución) • [Manual de Usuario](#manual-de-usuario)



---</div>



## Tabla de Contenidos---



1. [Guía de Instalación](#guía-de-instalación)## Tabla de Contenidos

2. [Guía de Uso](#guía-de-uso)

3. [Guía Técnica](#guía-técnica)1. [Guía de Instalación](#guía-de-instalación)

2. [Guía de Uso](#guía-de-uso)

---3. [Guía Técnica](#guía-técnica)



## Guía de Instalación---



### 1. Requisitos Previos## Guía de Instalación



#### Instalar Python 3.11+### Paso 1: Preparar el Entorno



**Windows:**#### 1.1 Instalar Python

```bash

# Descargar desde: https://www.python.org/downloads/**IMPORTANTE: Este proyecto es compatible con Python 3.11+ (incluyendo Python 3.12)**

# Marcar "Add Python to PATH" durante la instalación

Las dependencias del proyecto están actualizadas y son compatibles con versiones modernas de Python. Se recomienda usar Python 3.11.8 o superior (hasta Python 3.12).

# Verificar instalación:

python --version**Windows:**

# Debe mostrar: Python 3.11.x o 3.12.x```bash

```# Opción 1: Descargar Python 3.12 desde: https://www.python.org/downloads/

# Opción 2: Descargar Python 3.11.8 desde: https://www.python.org/downloads/release/python-3118/

**macOS:**# Seleccionar: "Windows installer (64-bit)"

```bash# IMPORTANTE: Marcar "Add Python to PATH" durante la instalación

brew install python@3.11

python3 --version# Verificar la instalación:

```python --version

# Debe mostrar: Python 3.11.x o Python 3.12.x

**Linux (Ubuntu/Debian):**```

```bash

sudo apt update**macOS:**

sudo apt install python3.11 python3.11-venv python3-pip```bash

python3 --version# Para Python 3.12

```brew install python@3.12



#### Instalar PostgreSQL# O para Python 3.11

brew install python@3.11

**Windows:**

```bashpython3 --version

# Descargar desde: https://www.postgresql.org/download/windows/# Debe mostrar: Python 3.11.x o Python 3.12.x

# Recordar la contraseña del usuario 'postgres'```

```

**Linux (Ubuntu/Debian):**

**macOS:**```bash

```bashsudo apt update

brew install postgresql@13# Para Python 3.12

brew services start postgresql@13sudo apt install python3.12 python3.12-venv python3-pip

```

# O para Python 3.11

**Linux:**sudo apt install python3.11 python3.11-venv python3-pip

```bash

sudo apt install postgresql postgresql-contribpython3 --version

sudo systemctl start postgresql# Debe mostrar: Python 3.11.x o Python 3.12.x

sudo systemctl enable postgresql```

```

#### 1.2 Instalar PostgreSQL

#### Instalar Git

**Windows:**

**Windows:** Descargar desde https://git-scm.com/download/win```bash

# Descargar desde https://www.postgresql.org/download/windows/

**macOS:** `brew install git`# Usar el instalador gráfico y recordar la contraseña del usuario 'postgres'

```

**Linux:** `sudo apt install git`

**macOS:**

---```bash

brew install postgresql@13

### 2. Clonar el Repositoriobrew services start postgresql@13

```

```bash

# Navegar a la carpeta deseada**Linux:**

cd C:\Projects  # Windows```bash

# cd ~/Projects  # macOS/Linuxsudo apt install postgresql postgresql-contrib

sudo systemctl start postgresql

# Clonar el repositoriosudo systemctl enable postgresql

git clone https://github.com/LuisAngulo02/evaIA.git```

cd evaIA

```#### 1.3 Instalar Git



---**Windows:**

```bash

### 3. Crear Base de Datos# Descargar desde https://git-scm.com/download/win

```

```bash

# Conectarse a PostgreSQL**macOS:**

psql -U postgres```bash

brew install git

# Ejecutar dentro de psql:```

CREATE DATABASE evalexpo_db;

CREATE USER evalexpo_user WITH PASSWORD 'tu_contraseña_segura';**Linux:**

ALTER ROLE evalexpo_user SET client_encoding TO 'utf8';```bash

ALTER ROLE evalexpo_user SET default_transaction_isolation TO 'read committed';sudo apt install git

ALTER ROLE evalexpo_user SET timezone TO 'UTC';```

GRANT ALL PRIVILEGES ON DATABASE evalexpo_db TO evalexpo_user;

### Paso 2: Clonar el Repositorio

# Salir

\q```bash

```# Navegar a la carpeta donde deseas instalar el proyecto

cd C:\Projects  # Windows

---# cd ~/Projects  # macOS/Linux



### 4. Configurar Entorno Virtual# Clonar el repositorio (si está en GitHub)

git clone https://github.com/LuisAngulo02/evaIA.git

**Windows (PowerShell):**

```powershell# O si ya tienes la carpeta, navegar a ella

# Crear entorno virtualcd "EvaIa"

py -3.11 -m venv venv```



# Activar entorno virtual### Paso 3: Crear la Base de Datos

.\venv\Scripts\Activate.ps1

```bash

# Si hay error de permisos:# Conectarse a PostgreSQL

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUserpsql -U postgres



# Verificar Python# Dentro de psql, ejecutar:

python --versionCREATE DATABASE evalexpo_db;

```CREATE USER evalexpo_user WITH PASSWORD 'tu_contraseña_segura';

ALTER ROLE evalexpo_user SET client_encoding TO 'utf8';

**macOS/Linux:**ALTER ROLE evalexpo_user SET default_transaction_isolation TO 'read committed';

```bashALTER ROLE evalexpo_user SET timezone TO 'UTC';

# Crear entorno virtualGRANT ALL PRIVILEGES ON DATABASE evalexpo_db TO evalexpo_user;

python3 -m venv venv

# Salir de psql

# Activar entorno virtual\q

source venv/bin/activate```



# Verificar Python### Paso 4: Configurar el Entorno Virtual

python --version

```**Windows (PowerShell):**

```powershell

---# Navegar a la carpeta del proyecto

cd c:\Users\user\Desktop\evaIA

### 5. Instalar Dependencias

# Crear entorno virtual con Python 3.11

```bashpy -3.11 -m venv venv

# Actualizar pip

python -m pip install --upgrade pip# Activar entorno virtual

.\venv\Scripts\Activate.ps1

# Instalar dependencias

pip install -r requirements.txt# Si hay error de permisos, ejecutar:

```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser



**⚠️ IMPORTANTE - Solución a conflictos de dependencias:**# Verificar la versión de Python

python --version

El archivo `requirements.txt` ya está configurado con las versiones compatibles:# Debe mostrar: Python 3.11.x o Python 3.12.x

```

```txt

# Versiones compatibles (YA CONFIGURADAS)**macOS/Linux:**

mediapipe>=0.10.9          # Flexible para compatibilidad```bash

tensorflow>=2.16.0,<2.18.0 # Compatible con MediaPipe# Navegar a la carpeta del proyecto

tf-keras>=2.16.0           # Compatible con TensorFlowcd ~/Desktop/evaIA

# protobuf se instala automáticamente (NO especificar versión)

```# Crear entorno virtual

python3 -m venv venv

**Notas:**

- La instalación puede tardar 15-30 minutos# Activar entorno virtual

- Tamaño de descarga: ~4-6 GBsource venv/bin/activate

- Si hay error con `openai-whisper`, instalar Rust desde: https://www.rust-lang.org/tools/install

# Verificar la versión de Python

**Instalación por partes** (si hay problemas):python --version

```bash# Debe mostrar: Python 3.11.x o Python 3.12.x

# 1. Django y dependencias web```

pip install Django==5.2.7 psycopg2-binary==2.9.11 cloudinary==1.44.1

### Paso 5: Instalar Dependencias

# 2. PyTorch

pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1```bash

# Actualizar pip

# 3. TensorFlow y visión por computadorapython -m pip install --upgrade pip

pip install "tensorflow>=2.16.0,<2.18.0" "mediapipe>=0.10.9" deepface==0.0.95

# Instalar todas las dependencias

# 4. Resto de dependenciaspip install -r requirements.txt

pip install -r requirements.txt```

```

**⚠️ IMPORTANTE - Conflicto de dependencias resuelto:**

---

Si encuentras errores de conflicto entre `tensorflow`, `mediapipe` y `protobuf`, el archivo `requirements.txt` ya está configurado correctamente con las siguientes versiones compatibles:

### 6. Configurar Variables de Entorno

```txt

Crear archivo `.env` en la raíz del proyecto:# Versiones compatibles (YA CONFIGURADAS)

mediapipe>=0.10.9          # Flexible para compatibilidad

```envtensorflow>=2.16.0,<2.18.0 # Versión compatible con MediaPipe

# Base de Datostf-keras>=2.16.0           # Compatible con TensorFlow

DB_NAME=evalexpo_db# protobuf se instala automáticamente (NO especificar versión)

DB_USER=evalexpo_user```

DB_PASSWORD=tu_contraseña_segura

DB_HOST=localhost**Notas importantes:**

DB_PORT=5432

1. **PyTorch y dependencias de IA**: La instalación puede tardar 15-30 minutos dependiendo de tu conexión y hardware.

# Cloudinary (obtener en https://cloudinary.com/)

CLOUDINARY_CLOUD_NAME=tu_cloud_name2. **Tamaño de descarga**: Aproximadamente 4-6 GB de paquetes.

CLOUDINARY_API_KEY=tu_api_key

CLOUDINARY_API_SECRET=tu_api_secret3. **Si obtienes error con `openai-whisper`**: Este paquete requiere Rust y herramientas de compilación. Si falla:

   ```bash

# Groq API (obtener en https://console.groq.com/)   # Opción 1: Instalar Rust

GROQ_API_KEY=tu_groq_api_key   # Windows: https://www.rust-lang.org/tools/install

   # Linux/Mac: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Django   

SECRET_KEY=django-insecure-#l1*xrw5x@0nqr^(ip@71%1z6e1wj_(0etuw2$xjj3w%pq^!33   # Opción 2: Comentar la línea en requirements.txt

DEBUG=True   # openai-whisper==20231117  # Requiere Rust

ALLOWED_HOSTS=127.0.0.1,localhost   ```

```

4. **Compatibilidad verificada**: 

---   - ✅ Python 3.11.8

   - ✅ Python 3.12.x

### 7. Configurar Base de Datos   - ✅ Windows 10/11

   - ✅ macOS 12+ (Intel y M1/M2)

```bash   - ✅ Ubuntu 20.04+ / Debian 11+

# Aplicar migraciones

python manage.py makemigrations5. **Instalación por partes** (si tienes problemas):

python manage.py migrate   ```bash

   # 1. Django y dependencias web

# Crear grupos de usuarios (Estudiante y Docente)   pip install Django==5.2.7 psycopg2-binary==2.9.11 cloudinary==1.44.1

python manage.py create_groups   

   # 2. PyTorch (instalar primero)

# Crear superusuario   pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1

python manage.py createsuperuser   

```   # 3. TensorFlow y visión por computadora

   pip install "tensorflow>=2.16.0,<2.18.0" "mediapipe>=0.10.9" deepface==0.0.95

---   

   # 4. Resto de dependencias

### 8. Recolectar Archivos Estáticos   pip install -r requirements.txt

   ```

```bash

python manage.py collectstatic --noinput### Paso 6: Configurar Variables de Entorno

```

Crear un archivo `.env` en la raíz del proyecto (solo si no existe):

---

```bash

### 9. Verificar Instalación# En Windows

notepad .env

```bash

# Ejecutar servidor# En macOS/Linux

python manage.py runservernano .env

```

# Abrir en navegador: http://127.0.0.1:8000/

```Agregar las siguientes variables:



**✅ Instalación completada exitosamente!**```env

# Base de Datos

---DB_NAME=evalexpo_db

DB_USER=evalexpo_user

## Guía de UsoDB_PASSWORD=tu_contraseña_segura

DB_HOST=localhost

### 1. Iniciar el SistemaDB_PORT=5432



#### Activar Entorno Virtual# Cloudinary (para almacenamiento de archivos)

CLOUDINARY_CLOUD_NAME=tu_cloud_name

**Windows:**CLOUDINARY_API_KEY=tu_api_key

```powershellCLOUDINARY_API_SECRET=tu_api_secret

cd "d:\evaIA-main\evaIA"

.\venv\Scripts\Activate.ps1# API de Groq (para análisis de IA)

```GROQ_API_KEY=tu_groq_api_key



**macOS/Linux:**# Configuración de Django

```bashSECRET_KEY=django-insecure-#l1*xrw5x@0nqr^(ip@71%1z6e1wj_(0etuw2$xjj3w%pq^!33

cd ~/evaIADEBUG=True

source venv/bin/activateALLOWED_HOSTS=127.0.0.1,localhost

``````



#### Iniciar Servidor**Obtener credenciales:**

- **Cloudinary**: Registrarse en https://cloudinary.com/ (plan gratuito disponible)

```bash- **Groq API**: Registrarse en https://console.groq.com/ (obtener API key gratuita)

python manage.py runserver

```### Paso 7: Configurar la Base de Datos



**Acceder a:**```bash

- Aplicación: http://127.0.0.1:8000/# Aplicar migraciones

- Admin: http://127.0.0.1:8000/admin/python manage.py makemigrations

- Login: http://127.0.0.1:8000/auth/login/python manage.py migrate



---# Crear grupos de usuarios (Estudiante y Docente) - IMPORTANTE

python manage.py create_groups

### 2. Para Estudiantes

# Crear superusuario para el panel de administración

#### Registro e Inicio de Sesiónpython manage.py createsuperuser

# Seguir las instrucciones en pantalla

1. Ir a http://127.0.0.1:8000/```

2. Clic en **"Registrarse"**

3. Completar formulario (nombre, email, contraseña, rol: Estudiante)### Paso 8: Cargar Datos Iniciales (Opcional)

4. Iniciar sesión con tus credenciales

```bash

#### Subir Presentación (Opción 1: Archivo)# Si existen fixtures o datos de prueba

python manage.py loaddata initial_data.json

1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**```

2. Seleccionar **"Subir Archivo"**

3. Completar:### Paso 9: Recolectar Archivos Estáticos

   - **Asignación**: Seleccionar de la lista

   - **Título**: Nombre de la presentación```bash

   - **Archivo**: Video (MP4, AVI, MOV, MKV, WEBM - máx 500 MB, 30 min)python manage.py collectstatic --noinput

   - **Descripción** (opcional)```

4. Clic en **"Subir Presentación"**

### Paso 10: Verificar la Instalación

**Consejos:**

- Buena iluminación y audio claro```bash

- Cámara estable# Ejecutar pruebas

- Hablar con claridadpython manage.py test



#### Grabar en Vivo (Opción 2)# Si todo está correcto, deberías ver:

# Ran X tests in Y seconds

1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**# OK

2. Seleccionar **"Grabar en Vivo"**```

3. Permitir acceso a cámara y micrófono

4. Seleccionar asignación**Instalación completada exitosamente!**

5. Verificar **"Rostro detectado!"** (verde)

6. Clic en **"Iniciar Grabación"**---

7. Realizar presentación

8. **Detener** cuando termines## Guía de Uso

9. Completar título y descripción

10. **"Guardar Presentación"**### 1. Iniciar el Sistema



**Indicadores:**#### Activar el Entorno Virtual

- 🔴 Luz roja = Grabando

- ⏱️ Temporizador activo**Windows (PowerShell):**

- ✅ Verde = Rostro detectado OK```powershell

- ⚠️ Rojo = Múltiples personas (se pausa)cd "d:\evaIA-main\evaIA"

.\venv\Scripts\Activate.ps1

#### Ver Resultados```



1. Ir a **"Mis Presentaciones"****macOS/Linux:**

2. Clic en la presentación deseada```bash

3. Ver:cd ~/evaIA

   - Calificación numérica (0-100)source venv/bin/activate

   - Estado: Pendiente/En Proceso/Completado```

   - Transcripción del audio

   - Análisis de IA (fortalezas, áreas de mejora, recomendaciones)#### Iniciar el Servidor

   - Comentarios del docente

   - Desglose por criterios```bash

   - Video de la presentaciónpython manage.py runserver

```

---

**Acceder a la aplicación:**

### 3. Para Docentes- Aplicación principal: http://127.0.0.1:8000/

- Panel admin: http://127.0.0.1:8000/admin/

#### Crear Curso- Login: http://127.0.0.1:8000/auth/login/



1. Ir a **"Mis Cursos"** → **"Nuevo Curso"**### 2. Uso para Estudiantes

2. Completar:

   - **Código**: Ej. "CS101"#### Subir una Presentación

   - **Nombre**: Ej. "Introducción a la Programación"

   - **Descripción**1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**

   - **Período académico**: Ej. "2025-1"2. Seleccionar la pestaña **"Subir Archivo"**

3. **"Crear Curso"**3. Completar el formulario:

   - **Asignación**: Seleccionar de la lista desplegable

#### Gestionar Estudiantes   - **Título**: Nombre descriptivo de tu presentación

   - **Archivo de video**: 

1. Entrar al curso     - Arrastra el archivo o haz clic para seleccionar

2. Ir a **"Estudiantes"**     - Formatos: MP4, AVI, MOV, MKV, WEBM

3. Opciones:     - Tamaño máximo: 500 MB

   - Agregar estudiante (buscar por email)     - Duración máxima: 30 minutos

   - Importar lista (CSV: `nombre,apellido,correo`)   - **Descripción** (opcional): Notas adicionales

   - Eliminar estudiante4. Clic en **"Subir Presentación"**

   - Ver perfil5. Esperar la confirmación de carga



#### Crear Asignación**Consejos:**

- Buena iluminación y audio claro

1. Dentro del curso → **"Asignaciones"** → **"Nueva Asignación"**- Cámara estable (usar trípode si es posible)

2. Completar:- Hablar con claridad y buen volumen

   - **Título**- Verificar que el video esté completo antes de subir

   - **Descripción**

   - **Tipo**: Individual/Grupal#### Grabar en Vivo

   - **Fecha límite**

   - **Duración máxima** (minutos)1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**

   - **Puntaje máximo**2. Seleccionar la pestaña **"Grabar en Vivo"**

   - **Instrucciones**3. Permitir acceso a la cámara y micrófono cuando el navegador lo solicite

   - **Criterios de evaluación**4. Seleccionar la **asignación**

3. **"Crear Asignación"**5. Revisar las instrucciones mostradas

6. Verificar que aparezca **"Rostro detectado!"** (indicador verde)

#### Configurar Rúbrica   - Solo debe haber **1 persona** visible en cámara

   - Si se detectan múltiples personas, la grabación se pausará

Agregar criterios de evaluación:7. Clic en **"Iniciar Grabación"**

- **Contenido** (30 puntos)8. Aparecerá una cuenta regresiva de 3 segundos

- **Organización** (20 puntos)9. Realizar la presentación

- **Expresión Verbal** (25 puntos)10. Controles disponibles:

- **Lenguaje Corporal** (15 puntos)    - **Pausar**: Pausa temporalmente la grabación

- **Tiempo** (10 puntos)    - **Reanudar**: Continúa la grabación

    - **Detener**: Finaliza la grabación

#### Revisar y Calificar    - **Reiniciar**: Descarta y comienza de nuevo

11. Al detener, revisar la vista previa

1. Ir a **"Presentaciones"** → **"Pendientes de Calificar"**12. Completar **título** y **descripción**

2. Seleccionar presentación13. Clic en **"Guardar Presentación"**

3. Revisar:

   - Video**Indicadores importantes:**

   - Transcripción automática- **Luz roja parpadeante**: Grabando

   - Análisis preliminar de IA- **Temporizador**: Muestra el tiempo transcurrido

   - Sugerencias de calificación- **Rostro detectado**: Verde = OK, Rojo = Problema

4. Clic en **"Calificar"**- **Advertencia múltiples personas**: Se pausará automáticamente

5. Opciones:

   - **Aceptar calificación de IA**#### Ver Resultados

   - **Modificar calificación** por criterio

   - **Calificación personalizada**1. Ir a **"Mis Presentaciones"**

6. Agregar comentarios2. Buscar tu presentación en la lista

7. **"Guardar Calificación"**3. Hacer clic en **"Ver Detalles"** o en el título

4. Visualizar:

#### Generar Reportes   - **Calificación numérica** (0-100)

   - **Estado**: Pendiente, En Proceso, Completado

1. Seleccionar estudiante → **"Ver Reporte"**   - **Transcripción** del audio

2. Descargar: PDF, Excel, o CSV   - **Análisis de IA** con:

     - Fortalezas identificadas

**Reportes de curso:**     - Áreas de mejora

1. Entrar al curso → **"Reportes"**     - Recomendaciones específicas

2. Ver:   - **Comentarios del docente** (si están disponibles)

   - Progreso general   - **Desglose por criterios** de evaluación

   - Gráficas de desempeño   - **Video de la presentación**

   - Comparativas

   - Tendencias---

3. Filtros: por asignación, fecha, calificación

4. **"Exportar"** → Seleccionar formato### 3. Uso para Docentes



---1. Ir a **"Mis Cursos"** → **"Nuevo Curso"**

2. Completar:

## Guía Técnica   - **Código del curso**: Ej. "CS101"

   - **Nombre**: Ej. "Introducción a la Programación"

### Stack Tecnológico   - **Descripción**: Información del curso

   - **Período académico**: Ej. "2025-1"

#### Backend3. Clic en **"Crear Curso"**

- **Framework**: Django 5.2.7

- **Base de datos**: PostgreSQL 13+#### Gestionar Estudiantes

- **Lenguaje**: Python 3.11+

- **ORM**: Django ORM1. Entrar al curso deseado

2. Ir a **"Estudiantes"**

#### Inteligencia Artificial3. Opciones:

- **Modelos de lenguaje**: Groq API, OpenAI GPT-4   - **Agregar estudiante**: Buscar por correo e invitar

- **Transcripción**: OpenAI Whisper   - **Importar lista**: Subir CSV con correos

- **Detección facial**: MediaPipe 0.10.21   - **Eliminar estudiante**: Remover del curso

- **Análisis facial**: DeepFace 0.0.95   - **Ver perfil**: Información detallada del estudiante

- **Deep Learning**: TensorFlow 2.16-2.17, PyTorch 2.5.1

**Formato CSV para importación:**

#### Procesamiento```csv

- **Video**: OpenCV 4.9.0.80, MoviePy, ImageIO, FFmpegnombre,apellido,correo

- **Audio**: Librosa, SoundFile, PydubJuan,Pérez,juan.perez@universidad.edu

- **Texto**: Transformers, Sentence-Transformersmaría,gonzalez,maria.gonzalez@universidad.edu

```

#### Frontend

- **Templates**: Django Templates + Jinja2#### Crear Asignación

- **JavaScript**: Vanilla JS```

- **CSS**: Bootstrap 5

- **Grabación**: MediaRecorder API#### 3.4 Crear una Asignación



#### Almacenamiento1. Dentro del curso, ir a **"Asignaciones"**

- **Archivos**: Cloudinary2. Clic en **"Nueva Asignación"**

- **Base de datos**: PostgreSQL3. Completar el formulario:

   - **Título**: Ej. "Presentación Final - Proyecto Web"

---   - **Descripción**: Explicación detallada

   - **Tipo**: Individual o Grupal

### Arquitectura del Sistema   - **Fecha límite**: Seleccionar fecha y hora

   - **Duración máxima**: En minutos (ej. 15)

```   - **Puntaje máximo**: Ej. 100

evaIA/   - **Instrucciones**: Detalles específicos para los estudiantes

├── apps/   - **Criterios de evaluación**: (Ver sección siguiente)

│   ├── ai_processor/          # Procesamiento de IA4. Clic en **"Crear Asignación"**

│   │   └── services/          # Audio, video, facial detection

│   ├── presentaciones/        # Gestión de presentaciones#### Configurar Rúbrica

│   ├── notifications/         # Sistema de notificaciones

│   ├── reportes/             # Generación de reportesAl crear o editar una asignación:

│   └── help/                 # Centro de ayuda

├── authentication/            # Autenticación y usuarios1. Scroll hasta **"Criterios de Evaluación"**

├── sist_evaluacion_expo/     # Configuración Django2. Agregar criterios, por ejemplo:

├── templates/                # Plantillas HTML   - **Contenido** (30 puntos)

├── static/                   # CSS, JS, imágenes     - Dominio del tema

├── docs/                     # Documentación técnica     - Profundidad del análisis

└── requirements.txt          # Dependencias Python   - **Organización** (20 puntos)

```     - Estructura lógica

     - Transiciones claras

---   - **Expresión Verbal** (25 puntos)

     - Claridad al hablar

### Flujo de Procesamiento     - Volumen y tono adecuados

   - **Lenguaje Corporal** (15 puntos)

1. **Estudiante sube video** → Almacenamiento en Cloudinary     - Contacto visual

2. **Extracción de audio** → Transcripción con Whisper     - Postura profesional

3. **Análisis facial** → MediaPipe + DeepFace   - **Tiempo** (10 puntos)

4. **Procesamiento de video** → OpenCV (frames, movimiento)     - Cumplimiento del tiempo asignado

5. **Análisis de contenido** → Groq/OpenAI (evaluación de texto)

6. **Generación de calificación** → Motor de evaluación con criterios3. Especificar ponderaciones para cada criterio

7. **Notificación** → Estudiante y Docente4. Guardar la rúbrica



---#### Revisar y Calificar



### Configuración de Variables de Entorno1. Ir a **"Presentaciones"** → **"Pendientes de Calificar"**

2. Seleccionar una presentación

```env3. Revisar:

# Django   - **Video de la presentación**

SECRET_KEY=tu_clave_secreta_muy_larga_y_segura   - **Transcripción automática**

DEBUG=False   - **Análisis preliminar de IA**

ALLOWED_HOSTS=tu-dominio.com   - **Sugerencias de calificación**

DJANGO_SETTINGS_MODULE=sist_evaluacion_expo.settings

**Opciones de calificación:**

# Base de Datos

DB_ENGINE=django.db.backends.postgresql1. En la página de detalles de la presentación

DB_NAME=evalexpo_db2. Clic en **"Calificar"**

DB_USER=evalexpo_user3. Opciones:

DB_PASSWORD=contraseña_segura   - **Aceptar calificación de IA**: Usar la evaluación automática

DB_HOST=localhost   - **Modificar calificación**: Ajustar puntos por criterio

DB_PORT=5432   - **Calificación personalizada**: Ingresar manualmente

4. Agregar **comentarios** para el estudiante:

# Cloudinary   - Fortalezas observadas

CLOUDINARY_CLOUD_NAME=tu_cloud_name   - Áreas de mejora específicas

CLOUDINARY_API_KEY=tu_api_key   - Consejos para futuras presentaciones

CLOUDINARY_API_SECRET=tu_api_secret5. Clic en **"Guardar Calificación"**



# APIs de IA#### Generar Reportes

GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1. Seleccionar un estudiante

AI_PROVIDER=groq  # 'groq' o 'openai'2. Ir a **"Ver Reporte"**

AI_MODEL=llama-3.3-70b-versatile  # Para Groq3. Descargar en formato:

   - PDF (para imprimir)

# Email (opcional)   - Excel (para análisis)

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend   - CSV (para importar a otros sistemas)

EMAIL_HOST=smtp.gmail.com

EMAIL_PORT=587**Reportes de curso:**

EMAIL_USE_TLS=True

EMAIL_HOST_USER=tu_email@gmail.com1. Entrar al curso

EMAIL_HOST_PASSWORD=tu_app_password2. Clic en **"Reportes"**

3. Visualizar:

# Seguridad (producción)   - **Progreso general** del curso

SECURE_SSL_REDIRECT=True   - **Gráficas de desempeño**

SESSION_COOKIE_SECURE=True   - **Comparativas entre estudiantes**

CSRF_COOKIE_SECURE=True   - **Tendencias de mejora**

SECURE_HSTS_SECONDS=315360004. Filtros disponibles:

```   - Por asignación

   - Por fecha

---   - Por rango de calificación



### Configuración Avanzada (settings.py)##### Exportar Calificaciones



```python1. En la vista de curso, ir a **"Calificaciones"**

# Configuración de procesamiento de IA2. Clic en **"Exportar"**

AI_PROCESSING_CONFIG = {3. Seleccionar formato (Excel, CSV, PDF)

    'video': {4. Descargar archivo

        'max_resolution': (1920, 1080),

        'frame_sample_rate': 1,---

        'max_duration_seconds': 1800,  # 30 minutos

    },### 4. Manual para Administradores

    'audio': {

        'sample_rate': 16000,#### 4.1 Panel de Administración

        'whisper_model': 'medium',

    },Acceder a: http://127.0.0.1:8000/admin/

    'face_detection': {

        'min_detection_confidence': 0.5,Funciones disponibles:

        'min_tracking_confidence': 0.5,- Gestión completa de usuarios

        'max_num_faces': 1,- Supervisión de cursos y asignaciones

    },- Monitoreo de uso del sistema

    'evaluation': {- Configuración de parámetros globales

        'use_facial_analysis': True,

        'use_emotion_detection': True,#### 4.2 Gestión de Usuarios

        'use_gesture_analysis': True,

    }1. En el panel admin, ir a **"Authentication"** → **"Users"**

}2. Opciones:

   - **Crear usuario**: Agregar manualmente

# Límites de carga   - **Editar usuario**: Cambiar rol, permisos

DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500 MB   - **Activar/Desactivar**: Suspender cuentas

FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000   - **Eliminar**: Remover permanentemente

MAX_VIDEO_DURATION = 1800  # 30 minutos

#### 4.3 Configuración del Sistema

# Formatos permitidos

ALLOWED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm']1. Ir a **"Settings"** en el panel admin

ALLOWED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a', '.ogg']2. Configurar:

```   - **Límites de almacenamiento**

   - **Duración máxima de videos**

---   - **Tamaño máximo de archivos**

   - **Cuota de API de IA**

### Solución de Problemas Comunes   - **Notificaciones por email**



#### Error: Conflicto de dependencias TensorFlow/MediaPipe#### 4.4 Monitoreo de Recursos



```bash1. **Dashboard de Administrador**

# Usar versiones compatibles (ya configuradas en requirements.txt)2. Ver:

mediapipe>=0.10.9   - Uso de almacenamiento (Cloudinary)

tensorflow>=2.16.0,<2.18.0   - Consumo de API de IA (Groq/OpenAI)

# NO especificar versión de protobuf   - Número de usuarios activos

   - Presentaciones procesadas

# Si persiste:   - Tiempo promedio de procesamiento

pip uninstall tensorflow mediapipe protobuf -y

pip install "tensorflow>=2.16.0,<2.18.0"#### 4.5 Backups y Mantenimiento

pip install "mediapipe>=0.10.9"

``````bash

# Backup de la base de datos

#### Error: PostgreSQL no conectapython manage.py dumpdata > backup_$(date +%Y%m%d).json



```bash# Restaurar desde backup

# Verificar serviciopython manage.py loaddata backup_20251103.json

# Windows: Services → PostgreSQL

# Linux: sudo systemctl status postgresql# Limpiar archivos temporales

# macOS: brew services listpython manage.py clearsessions

python manage.py cleanup_uploads

# Verificar credenciales en .env

DB_USER=evalexpo_user# Ver logs del sistema

DB_PASSWORD=tu_contraseña_correctatail -f logs/system.log

``````



#### Error: Video no se procesa---



```bash### 5. Funciones Comunes para Todos los Usuarios

# Verificar FFmpeg instalado

ffmpeg -version#### 5.1 Editar Perfil



# Instalar:1. Clic en el **avatar** (esquina superior derecha)

# Windows: https://ffmpeg.org/download.html2. Seleccionar **"Mi Perfil"**

# Linux: sudo apt install ffmpeg3. Editar:

# macOS: brew install ffmpeg   - Foto de perfil

```   - Nombre y apellidos

   - Correo electrónico

#### Error: "No se detecta rostro"   - Contraseña

   - Preferencias de notificación

```python4. Clic en **"Guardar Cambios"**

# Ajustar sensibilidad en settings.py

FACE_DETECTION_CONFIG = {#### 5.2 Cambiar Contraseña

    'min_detection_confidence': 0.3,  # Reducir umbral

}1. Ir a **"Mi Perfil"** → **"Seguridad"**

2. Ingresar:

# Verificar:   - Contraseña actual

# - Buena iluminación   - Nueva contraseña

# - Cámara a altura de ojos   - Confirmar nueva contraseña

# - Distancia: 50-100 cm3. Clic en **"Actualizar Contraseña"**

```

#### 5.3 Configurar Notificaciones

#### Alto uso de memoria

1. Ir a **"Configuración"** → **"Notificaciones"**

```bash2. Activar/desactivar:

# Limpiar caché y sesiones   - Notificaciones por correo

python manage.py clear_cache   - Notificaciones en la app

python manage.py clearsessions   - Frecuencia de resúmenes

```3. Guardar preferencias



---#### 5.4 Centro de Ayuda



### Comandos Útiles1. Clic en el ícono **"?"** (esquina superior)

2. Acceder a:

```bash   - **Preguntas frecuentes (FAQ)**

# Verificar instalación   - **Tutoriales en video**

python manage.py check   - **Documentación técnica**

   - **Contactar soporte**

# Ver migraciones

python manage.py showmigrations#### 5.5 Cerrar Sesión



# Crear superusuario1. Clic en el **avatar**

python manage.py createsuperuser2. Seleccionar **"Cerrar Sesión"**

3. Confirmar

# Recolectar estáticos

python manage.py collectstatic---



# Shell de Django### 6. Mejores Prácticas

python manage.py shell

#### Para Estudiantes

# Backup de BD

python manage.py dumpdata > backup.json**Antes de grabar:**

- Revisar las instrucciones de la asignación

# Restaurar BD- Preparar y practicar tu presentación

python manage.py loaddata backup.json- Verificar audio y video

```- Elegir un fondo limpio y profesional

- Asegurar buena iluminación

---

**Durante la grabación:**

### API Endpoints- Mantener contacto visual con la cámara

- Hablar con claridad y a buen volumen

#### Autenticación- Evitar muletillas ("ehh", "mmm")

```http- Controlar el tiempo

POST /auth/login/- Mantener una postura profesional

POST /auth/register/

```**Después de subir:**

- Verificar que el video se cargó correctamente

#### Presentaciones- Revisar la transcripción por si hay errores

```http- Estar atento a las notificaciones

GET /api/presentaciones/- Responder a comentarios del docente

POST /api/presentaciones/upload/

GET /api/presentaciones/{id}/#### Para Docentes

```

**Al crear asignaciones:**

#### Evaluación- Proporcionar instrucciones claras y detalladas

```http- Establecer criterios de evaluación específicos

POST /api/ai/evaluate/- Dar tiempo suficiente para preparación

```- Comunicar expectativas claramente



---**Al evaluar:**

- Revisar el análisis de IA como guía inicial

### Configuración de Producción- Proporcionar retroalimentación constructiva

- Ser específico en los comentarios

```bash- Destacar tanto fortalezas como áreas de mejora

# Instalar Gunicorn- Responder dudas de los estudiantes

pip install gunicorn

---

# Ejecutar

gunicorn sist_evaluacion_expo.wsgi:application --bind 0.0.0.0:8000 --workers 4<div align="center">



# Variables de entorno de producción**EvalExpo AI - Sistema de Evaluación de Presentaciones con IA**

DEBUG=False

SECURE_SSL_REDIRECT=True[Volver arriba](#evalexpo-ai---sistema-de-evaluación-de-presentaciones-con-ia)

SESSION_COOKIE_SECURE=True

CSRF_COOKIE_SECURE=True</div>

```

---

**Nginx config:**

```nginx## Solución de Problemas

location /static/ {

    alias /ruta/a/staticfiles/;### Problemas de Instalación

}

#### Error: "No matching distribution found for protobuf"

location / {

    proxy_pass http://127.0.0.1:8000;**Causa**: Conflicto entre versiones de TensorFlow y MediaPipe.

}

```**Solución**:

```bash

---# 1. Asegúrate de tener la versión correcta en requirements.txt

mediapipe>=0.10.9

### Documentación Adicionaltensorflow>=2.16.0,<2.18.0



- **Arquitectura**: `docs/ARQUITECTURA_SISTEMA.md`# 2. NO especificar versión de protobuf

- **Detección facial**: `docs/MEJORAS_DETECCION_ROSTROS.md`# Dejar que TensorFlow instale la versión compatible

- **Optimización**: `docs/OPTIMIZACION_RENDIMIENTO.md`

- **Soluciones**: `docs/SOLUCION_*.md`# 3. Reinstalar en orden correcto

pip uninstall tensorflow mediapipe protobuf -y

---pip install "tensorflow>=2.16.0,<2.18.0"

pip install "mediapipe>=0.10.9"

<div align="center">```



**EvalExpo AI v1.0.10**#### Error: "Microsoft Visual C++ 14.0 or greater is required"



Desarrollado con ❤️ usando Django, Python e Inteligencia Artificial**Causa**: Falta compilador C++ en Windows.



[GitHub](https://github.com/LuisAngulo02/evaIA) • [Documentación](./docs/) • [Reportar Bug](https://github.com/LuisAngulo02/evaIA/issues)**Solución**:

```bash

**Licencia MIT**# Descargar e instalar:

# Microsoft C++ Build Tools

</div># https://visualstudio.microsoft.com/visual-cpp-build-tools/


# O instalar Visual Studio Community con "Desktop development with C++"
```

#### Error al instalar openai-whisper

**Causa**: Requiere Rust y herramientas de compilación.

**Solución Opción 1 - Instalar Rust**:
```bash
# Windows: Descargar desde https://www.rust-lang.org/tools/install
# Linux/Mac:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
pip install openai-whisper==20231117
```

**Solución Opción 2 - Omitir Whisper**:
```bash
# Comentar en requirements.txt:
# openai-whisper==20231117

# El sistema usará alternativas para transcripción
```

#### Error: "psycopg2 installation error"

**Solución**:
```bash
# Windows
pip install psycopg2-binary==2.9.11

# Linux (instalar dependencias primero)
sudo apt-get install libpq-dev python3-dev
pip install psycopg2==2.9.11
```

### Problemas de Base de Datos

#### Error: "FATAL: password authentication failed"

**Solución**:
```bash
# 1. Verificar credenciales en .env
DB_USER=evalexpo_user
DB_PASSWORD=tu_contraseña_correcta

# 2. Recrear usuario en PostgreSQL
psql -U postgres
DROP USER IF EXISTS evalexpo_user;
CREATE USER evalexpo_user WITH PASSWORD 'nueva_contraseña';
GRANT ALL PRIVILEGES ON DATABASE evalexpo_db TO evalexpo_user;
\q

# 3. Actualizar .env con la nueva contraseña
```

#### Error: "django.db.utils.OperationalError: could not connect to server"

**Solución**:
```bash
# Verificar que PostgreSQL esté ejecutándose

# Windows
# Abrir "Services" y verificar "PostgreSQL"

# Linux
sudo systemctl status postgresql
sudo systemctl start postgresql

# macOS
brew services list
brew services start postgresql@13
```

#### Error: "relation does not exist"

**Solución**:
```bash
# Aplicar migraciones
python manage.py migrate

# Si persiste, resetear migraciones
python manage.py migrate --run-syncdb
```

### Problemas con APIs

#### Error: "Groq API rate limit exceeded"

**Solución**:
```python
# En settings.py, reducir frecuencia de análisis
AI_ANALYSIS_CONFIG = {
    'rate_limit': 10,  # Reducir de 20 a 10 por minuto
    'retry_attempts': 3,
    'retry_delay': 5,
}

# O usar OpenAI como alternativa
AI_PROVIDER = 'openai'  # en lugar de 'groq'
```

#### Error: "Cloudinary upload failed"

**Solución**:
```bash
# 1. Verificar credenciales en .env
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# 2. Verificar conectividad
python manage.py shell
>>> import cloudinary
>>> cloudinary.config(cloud_name="tu_cloud_name")
>>> # Si no hay errores, la configuración es correcta

# 3. Verificar límites del plan gratuito
# Cloudinary Free: 25 GB almacenamiento, 25 GB transferencia/mes
```

### Problemas de Video/Audio

#### Video no se procesa o se queda "En Proceso"

**Diagnóstico**:
```bash
# Ver logs de procesamiento
python manage.py shell
>>> from apps.presentaciones.models import Presentacion
>>> p = Presentacion.objects.get(id=TU_ID)
>>> print(p.estado)
>>> print(p.error_message)  # Si existe

# Ver logs del servidor
tail -f logs/django.log
```

**Soluciones comunes**:
```bash
# 1. Verificar FFmpeg instalado
ffmpeg -version

# Si no está instalado:
# Windows: https://ffmpeg.org/download.html
# Linux: sudo apt install ffmpeg
# macOS: brew install ffmpeg

# 2. Reprocesar video manualmente
python manage.py shell
>>> from apps.ai_processor.services.video_processor import VideoProcessor
>>> processor = VideoProcessor()
>>> result = processor.process_video('URL_DEL_VIDEO')
>>> print(result)
```

#### Error: "Codec not supported"

**Solución**:
```bash
# Convertir video a formato compatible (MP4 H.264)
ffmpeg -i video_original.avi -c:v libx264 -c:a aac video_convertido.mp4

# O configurar formatos aceptados en settings.py
ALLOWED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
```

#### Audio no se transcribe correctamente

**Solución**:
```python
# Mejorar calidad de transcripción en settings.py
WHISPER_CONFIG = {
    'model': 'medium',  # Cambiar de 'base' a 'medium' o 'large'
    'language': 'es',   # Español
    'task': 'transcribe',
}
```

### Problemas de Detección Facial

#### "Múltiples rostros detectados" aunque solo hay una persona

**Solución**:
```python
# Ajustar sensibilidad en settings.py
FACE_DETECTION_CONFIG = {
    'min_detection_confidence': 0.7,  # Aumentar de 0.5 a 0.7
    'min_tracking_confidence': 0.7,
    'max_num_faces': 1,
}
```

#### "No se detecta ningún rostro"

**Solución**:
```python
# Reducir sensibilidad
FACE_DETECTION_CONFIG = {
    'min_detection_confidence': 0.3,  # Reducir umbral
}

# Verificar iluminación y posición de la cámara
# - Rostro debe estar bien iluminado
# - Cámara a la altura de los ojos
# - Distancia: 50-100 cm de la cámara
```

### Problemas de Rendimiento

#### Sistema lento al procesar videos

**Optimizaciones**:
```python
# 1. En settings.py, reducir resolución de procesamiento
VIDEO_PROCESSING_CONFIG = {
    'max_resolution': (640, 480),  # Reducir de (1920, 1080)
    'frame_sample_rate': 5,        # Procesar cada 5 frames en lugar de todos
}

# 2. Usar GPU si está disponible
USE_GPU = True  # En settings.py

# 3. Implementar cola de tareas con Celery (avanzado)
```

#### Alto uso de memoria

**Solución**:
```bash
# 1. Limpiar caché de Django
python manage.py clear_cache

# 2. Limpiar sesiones expiradas
python manage.py clearsessions

# 3. Limpiar archivos temporales
python manage.py cleanup_temp_files

# 4. Ajustar configuración de memoria en settings.py
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600
```

### Problemas en Producción

#### Error 500 - Internal Server Error

**Diagnóstico**:
```bash
# 1. Ver logs detallados
tail -f /var/log/your-app/error.log

# 2. Activar modo debug temporalmente (solo para diagnóstico)
# En .env
DEBUG=True

# 3. Verificar collectstatic
python manage.py collectstatic --noinput
```

#### Archivos estáticos no se cargan

**Solución**:
```bash
# 1. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 2. Verificar configuración de servidor web (Nginx)
# En nginx.conf:
location /static/ {
    alias /ruta/a/staticfiles/;
}

# 3. Verificar permisos
chmod -R 755 /ruta/a/staticfiles/
```

#### Gunicorn no inicia

**Solución**:
```bash
# 1. Verificar sintaxis
gunicorn --check-config sist_evaluacion_expo.wsgi:application

# 2. Ver logs
journalctl -u gunicorn -f

# 3. Reiniciar servicio
sudo systemctl restart gunicorn
```

### Comandos de Diagnóstico Útiles

```bash
# Ver todas las migraciones
python manage.py showmigrations

# Verificar configuración de Django
python manage.py check

# Ver configuración actual
python manage.py diffsettings

# Crear un reporte de sistema
python manage.py shell
>>> from django.core import management
>>> management.call_command('check', '--deploy')

# Verificar dependencias instaladas
pip list
pip check  # Verifica conflictos

# Ver uso de base de datos
python manage.py dbshell
SELECT pg_size_pretty(pg_database_size('evalexpo_db'));
```

---

## API y Documentación Técnica

### Endpoints Principales

#### Autenticación

```http
POST /auth/login/
Content-Type: application/json

{
    "email": "usuario@example.com",
    "password": "contraseña"
}

Response: 200 OK
{
    "token": "jwt_token_here",
    "user": {
        "id": 1,
        "email": "usuario@example.com",
        "nombre": "Juan",
        "rol": "Estudiante"
    }
}
```

```http
POST /auth/register/
Content-Type: application/json

{
    "email": "nuevo@example.com",
    "password": "contraseña_segura",
    "nombre": "Juan",
    "apellido": "Pérez",
    "rol": "Estudiante"
}
```

#### Presentaciones

```http
GET /api/presentaciones/
Authorization: Bearer {token}

Response: 200 OK
{
    "count": 10,
    "results": [
        {
            "id": 1,
            "titulo": "Presentación Final",
            "estudiante": "Juan Pérez",
            "calificacion": 85.5,
            "estado": "Completado",
            "fecha_subida": "2025-11-03T14:30:00Z"
        }
    ]
}
```

```http
POST /api/presentaciones/upload/
Authorization: Bearer {token}
Content-Type: multipart/form-data

{
    "asignacion_id": 5,
    "titulo": "Mi Presentación",
    "video": [archivo_video],
    "descripcion": "Descripción opcional"
}

Response: 201 Created
{
    "id": 15,
    "mensaje": "Video subido exitosamente",
    "estado": "En Proceso"
}
```

```http
GET /api/presentaciones/{id}/
Authorization: Bearer {token}

Response: 200 OK
{
    "id": 1,
    "titulo": "Presentación Final",
    "video_url": "https://cloudinary.com/video.mp4",
    "transcripcion": "Texto transcrito...",
    "calificacion": 85.5,
    "analisis_ia": {
        "fortalezas": [...],
        "areas_mejora": [...],
        "recomendaciones": [...]
    },
    "comentarios": [...]
}
```

#### Evaluación con IA

```http
POST /api/ai/evaluate/
Authorization: Bearer {token}
Content-Type: application/json

{
    "presentacion_id": 1,
    "criterios": {
        "contenido": 30,
        "organizacion": 20,
        "expresion_verbal": 25,
        "lenguaje_corporal": 15,
        "tiempo": 10
    }
}

Response: 200 OK
{
    "calificacion_total": 85.5,
    "desglose": {
        "contenido": 26,
        "organizacion": 18,
        "expresion_verbal": 22,
        "lenguaje_corporal": 13,
        "tiempo": 6.5
    },
    "analisis": {
        "fortalezas": [...],
        "areas_mejora": [...],
        "recomendaciones": [...]
    }
}
```

### Configuración Avanzada

#### Variables de Entorno Completas

```env
# Django
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DJANGO_SETTINGS_MODULE=sist_evaluacion_expo.settings

# Base de Datos
DB_ENGINE=django.db.backends.postgresql
DB_NAME=evalexpo_db
DB_USER=evalexpo_user
DB_PASSWORD=contraseña_segura
DB_HOST=localhost
DB_PORT=5432

# Cloudinary
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# APIs de IA
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Configuración de IA
AI_PROVIDER=groq  # 'groq' o 'openai'
AI_MODEL=llama-3.3-70b-versatile  # Para Groq
# AI_MODEL=gpt-4  # Para OpenAI

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_app

# Seguridad (solo en producción)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Logs
LOG_LEVEL=INFO
LOG_FILE=logs/django.log
```

#### Configuración de settings.py personalizada

```python
# En sist_evaluacion_expo/settings.py

# Configuración de procesamiento de IA
AI_PROCESSING_CONFIG = {
    'video': {
        'max_resolution': (1920, 1080),
        'frame_sample_rate': 1,  # Procesar todos los frames
        'max_duration_seconds': 1800,  # 30 minutos
    },
    'audio': {
        'sample_rate': 16000,
        'whisper_model': 'medium',  # 'tiny', 'base', 'small', 'medium', 'large'
    },
    'face_detection': {
        'min_detection_confidence': 0.5,
        'min_tracking_confidence': 0.5,
        'max_num_faces': 1,
    },
    'evaluation': {
        'use_facial_analysis': True,
        'use_emotion_detection': True,
        'use_gesture_analysis': True,
    }
}

# Límites de carga
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500 MB
MAX_VIDEO_DURATION = 1800  # 30 minutos en segundos

# Formatos permitidos
ALLOWED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
ALLOWED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a', '.ogg']
```

### Documentación de Modelos

Consultar la documentación técnica detallada en:
- **Arquitectura del sistema**: `docs/ARQUITECTURA_SISTEMA.md`
- **Detección de rostros**: `docs/MEJORAS_DETECCION_ROSTROS.md`
- **Optimización de rendimiento**: `docs/OPTIMIZACION_RENDIMIENTO.md`
- **Solución de problemas**: `docs/SOLUCION_*.md`

### Contribuir al Proyecto

```bash
# 1. Fork del repositorio
# 2. Crear rama para tu feature
git checkout -b feature/nueva-funcionalidad

# 3. Hacer commits descriptivos
git commit -m "feat: Agregar análisis de gestos mejorado"

# 4. Push a tu fork
git push origin feature/nueva-funcionalidad

# 5. Crear Pull Request en GitHub
```

### Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

<div align="center">

**EvalExpo AI v1.0.10**

Desarrollado con ❤️ usando Django, Python e Inteligencia Artificial

[GitHub](https://github.com/LuisAngulo02/evaIA) • [Documentación](./docs/) • [Reportar Bug](https://github.com/LuisAngulo02/evaIA/issues)

</div>