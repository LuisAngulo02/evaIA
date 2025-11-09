# EvalExpo AI - Sistema de Evaluación de Presentaciones con IA# EvalExpo AI - Sistema de Evaluación de Presentaciones con IA # EvalExpo AI - Sistema de Evaluación de Presentaciones con IA



<div align="center">



![Version](https://img.shields.io/badge/version-1.0.10-blue.svg)<div align="center"><div align="center">

![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-green.svg)

![Django](https://img.shields.io/badge/django-5.2.7-darkgreen.svg)

![License](https://img.shields.io/badge/license-MIT-orange.svg)

![Version](https://img.shields.io/badge/version-1.0.10-blue.svg)![Version](https://img.shields.io/badge/version-1.0.10-blue.svg)

**Sistema inteligente para evaluar presentaciones académicas mediante Inteligencia Artificial**

![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-green.svg)![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-green.svg)

[Instalación](#guía-de-instalación) • [Ejecución](#guía-de-uso) • [Manual de Usuario](#guía-de-uso)

![Django](https://img.shields.io/badge/django-5.2.7-darkgreen.svg)![Django](https://img.shields.io/badge/django-5.2.7-darkgreen.svg)

</div>

![License](https://img.shields.io/badge/license-MIT-orange.svg)![License](https://img.shields.io/badge/license-MIT-orange.svg)

---



## Tabla de Contenidos

**Sistema inteligente para evaluar presentaciones académicas mediante Inteligencia Artificial****Sistema inteligente para evaluar presentaciones académicas mediante Inteligencia Artificial**

1. [Guía de Instalación](#guía-de-instalación)

2. [Guía de Uso](#guía-de-uso)

3. [Guía Técnica](#guía-técnica)

</div>[Instalación](#manual-de-instalación) • [Ejecución](#manual-de-ejecución) • [Manual de Usuario](#manual-de-usuario)

---



## Guía de Instalación

---</div>

### Paso 1: Preparar el Entorno



#### 1.1 Instalar Python

## Tabla de Contenidos---

**IMPORTANTE: Este proyecto es compatible con Python 3.11+ (incluyendo Python 3.12)**



Las dependencias del proyecto están actualizadas y son compatibles con versiones modernas de Python. Se recomienda usar Python 3.11.8 o superior (hasta Python 3.12).

1. [Guía de Instalación](#guía-de-instalación)## Tabla de Contenidos

**Windows:**

```bash2. [Guía de Uso](#guía-de-uso)

# Opción 1: Descargar Python 3.12 desde: https://www.python.org/downloads/

# Opción 2: Descargar Python 3.11.8 desde: https://www.python.org/downloads/release/python-3118/3. [Guía Técnica](#guía-técnica)1. [Guía de Instalación](#guía-de-instalación)

# Seleccionar: "Windows installer (64-bit)"

# IMPORTANTE: Marcar "Add Python to PATH" durante la instalación2. [Guía de Uso](#guía-de-uso)



# Verificar la instalación:---3. [Guía Técnica](#guía-técnica)

python --version

# Debe mostrar: Python 3.11.x o Python 3.12.x

```

## Guía de Instalación---

**macOS:**

```bash

# Para Python 3.12

brew install python@3.12### 1. Requisitos Previos## Guía de Instalación



# O para Python 3.11

brew install python@3.11

#### Instalar Python 3.11+### Paso 1: Preparar el Entorno

python3 --version

# Debe mostrar: Python 3.11.x o Python 3.12.x

```

**Windows:**#### 1.1 Instalar Python

**Linux (Ubuntu/Debian):**

```bash```bash

sudo apt update

# Descargar desde: https://www.python.org/downloads/**IMPORTANTE: Este proyecto es compatible con Python 3.11+ (incluyendo Python 3.12)**

# Para Python 3.12

sudo apt install python3.12 python3.12-venv python3-pip# Marcar "Add Python to PATH" durante la instalación



# O para Python 3.11Las dependencias del proyecto están actualizadas y son compatibles con versiones modernas de Python. Se recomienda usar Python 3.11.8 o superior (hasta Python 3.12).

sudo apt install python3.11 python3.11-venv python3-pip

# Verificar instalación:

python3 --version

# Debe mostrar: Python 3.11.x o Python 3.12.xpython --version**Windows:**

```

# Debe mostrar: Python 3.11.x o 3.12.x```bash

#### 1.2 Instalar PostgreSQL

```# Opción 1: Descargar Python 3.12 desde: https://www.python.org/downloads/

**Windows:**

```bash# Opción 2: Descargar Python 3.11.8 desde: https://www.python.org/downloads/release/python-3118/

# Descargar desde https://www.postgresql.org/download/windows/

# Usar el instalador gráfico y recordar la contraseña del usuario 'postgres'**macOS:**# Seleccionar: "Windows installer (64-bit)"

```

```bash# IMPORTANTE: Marcar "Add Python to PATH" durante la instalación

**macOS:**

```bashbrew install python@3.11

brew install postgresql@13

brew services start postgresql@13python3 --version# Verificar la instalación:

```

```python --version

**Linux:**

```bash# Debe mostrar: Python 3.11.x o Python 3.12.x

sudo apt install postgresql postgresql-contrib

sudo systemctl start postgresql**Linux (Ubuntu/Debian):**```

sudo systemctl enable postgresql

``````bash



#### 1.3 Instalar Gitsudo apt update**macOS:**



**Windows:**sudo apt install python3.11 python3.11-venv python3-pip```bash

```bash

# Descargar desde https://git-scm.com/download/winpython3 --version# Para Python 3.12

```

```brew install python@3.12

**macOS:**

```bash

brew install git

```#### Instalar PostgreSQL# O para Python 3.11



**Linux:**brew install python@3.11

```bash

sudo apt install git**Windows:**

```

```bashpython3 --version

### Paso 2: Clonar el Repositorio

# Descargar desde: https://www.postgresql.org/download/windows/# Debe mostrar: Python 3.11.x o Python 3.12.x

```bash

# Navegar a la carpeta donde deseas instalar el proyecto# Recordar la contraseña del usuario 'postgres'```

cd C:\Projects  # Windows

# cd ~/Projects  # macOS/Linux```



# Clonar el repositorio (si está en GitHub)**Linux (Ubuntu/Debian):**

git clone https://github.com/LuisAngulo02/evaIA.git

**macOS:**```bash

# O si ya tienes la carpeta, navegar a ella

cd evaIA```bashsudo apt update

```

brew install postgresql@13# Para Python 3.12

### Paso 3: Crear la Base de Datos

brew services start postgresql@13sudo apt install python3.12 python3.12-venv python3-pip

```bash

# Conectarse a PostgreSQL```

psql -U postgres

# O para Python 3.11

# Dentro de psql, ejecutar:

CREATE DATABASE evalexpo_db;**Linux:**sudo apt install python3.11 python3.11-venv python3-pip

CREATE USER evalexpo_user WITH PASSWORD 'tu_contraseña_segura';

ALTER ROLE evalexpo_user SET client_encoding TO 'utf8';```bash

ALTER ROLE evalexpo_user SET default_transaction_isolation TO 'read committed';

ALTER ROLE evalexpo_user SET timezone TO 'UTC';sudo apt install postgresql postgresql-contribpython3 --version

GRANT ALL PRIVILEGES ON DATABASE evalexpo_db TO evalexpo_user;

sudo systemctl start postgresql# Debe mostrar: Python 3.11.x o Python 3.12.x

# Salir de psql

\qsudo systemctl enable postgresql```

```

```

### Paso 4: Configurar el Entorno Virtual

#### 1.2 Instalar PostgreSQL

**Windows (PowerShell):**

```powershell#### Instalar Git

# Navegar a la carpeta del proyecto

cd evaIA**Windows:**



# Crear entorno virtual con Python 3.11**Windows:** Descargar desde https://git-scm.com/download/win```bash

py -3.11 -m venv venv

# Descargar desde https://www.postgresql.org/download/windows/

# Activar entorno virtual

.\venv\Scripts\Activate.ps1**macOS:** `brew install git`# Usar el instalador gráfico y recordar la contraseña del usuario 'postgres'



# Si hay error de permisos, ejecutar:```

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

**Linux:** `sudo apt install git`

# Verificar la versión de Python

python --version**macOS:**

# Debe mostrar: Python 3.11.x o Python 3.12.x

```---```bash



**macOS/Linux:**brew install postgresql@13

```bash

# Navegar a la carpeta del proyecto### 2. Clonar el Repositoriobrew services start postgresql@13

cd evaIA

```

# Crear entorno virtual

python3 -m venv venv```bash



# Activar entorno virtual# Navegar a la carpeta deseada**Linux:**

source venv/bin/activate

cd C:\Projects  # Windows```bash

# Verificar la versión de Python

python --version# cd ~/Projects  # macOS/Linuxsudo apt install postgresql postgresql-contrib

# Debe mostrar: Python 3.11.x o Python 3.12.x

```sudo systemctl start postgresql



### Paso 5: Instalar Dependencias# Clonar el repositoriosudo systemctl enable postgresql



```bashgit clone https://github.com/LuisAngulo02/evaIA.git```

# Actualizar pip

python -m pip install --upgrade pipcd evaIA



# Instalar todas las dependencias```#### 1.3 Instalar Git

pip install -r requirements.txt

```



**⚠️ IMPORTANTE - Conflicto de dependencias resuelto:**---**Windows:**



Si encuentras errores de conflicto entre `tensorflow`, `mediapipe` y `protobuf`, el archivo `requirements.txt` ya está configurado correctamente con las siguientes versiones compatibles:```bash



```txt### 3. Crear Base de Datos# Descargar desde https://git-scm.com/download/win

# Versiones compatibles (YA CONFIGURADAS)

mediapipe>=0.10.9          # Flexible para compatibilidad```

tensorflow>=2.16.0,<2.18.0 # Versión compatible con MediaPipe

tf-keras>=2.16.0           # Compatible con TensorFlow```bash

# protobuf se instala automáticamente (NO especificar versión)

```# Conectarse a PostgreSQL**macOS:**



**Notas importantes:**psql -U postgres```bash



1. **PyTorch y dependencias de IA**: La instalación puede tardar 15-30 minutos dependiendo de tu conexión y hardware.brew install git



2. **Tamaño de descarga**: Aproximadamente 4-6 GB de paquetes.# Ejecutar dentro de psql:```



3. **Si obtienes error con `openai-whisper`**: Este paquete requiere Rust y herramientas de compilación. Si falla:CREATE DATABASE evalexpo_db;

   ```bash

   # Opción 1: Instalar RustCREATE USER evalexpo_user WITH PASSWORD 'tu_contraseña_segura';**Linux:**

   # Windows: https://www.rust-lang.org/tools/install

   # Linux/Mac: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | shALTER ROLE evalexpo_user SET client_encoding TO 'utf8';```bash

   

   # Opción 2: Comentar la línea en requirements.txtALTER ROLE evalexpo_user SET default_transaction_isolation TO 'read committed';sudo apt install git

   # openai-whisper==20231117  # Requiere Rust

   ```ALTER ROLE evalexpo_user SET timezone TO 'UTC';```



4. **Compatibilidad verificada**: GRANT ALL PRIVILEGES ON DATABASE evalexpo_db TO evalexpo_user;

   - ✅ Python 3.11.8

   - ✅ Python 3.12.x### Paso 2: Clonar el Repositorio

   - ✅ Windows 10/11

   - ✅ macOS 12+ (Intel y M1/M2)# Salir

   - ✅ Ubuntu 20.04+ / Debian 11+

\q```bash

5. **Instalación por partes** (si tienes problemas):

   ```bash```# Navegar a la carpeta donde deseas instalar el proyecto

   # 1. Django y dependencias web

   pip install Django==5.2.7 psycopg2-binary==2.9.11 cloudinary==1.44.1cd C:\Projects  # Windows

   

   # 2. PyTorch (instalar primero)---# cd ~/Projects  # macOS/Linux

   pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1

   

   # 3. TensorFlow y visión por computadora

   pip install "tensorflow>=2.16.0,<2.18.0" "mediapipe>=0.10.9" deepface==0.0.95### 4. Configurar Entorno Virtual# Clonar el repositorio (si está en GitHub)

   

   # 4. Resto de dependenciasgit clone https://github.com/LuisAngulo02/evaIA.git

   pip install -r requirements.txt

   ```**Windows (PowerShell):**



### Paso 6: Configurar Variables de Entorno```powershell# O si ya tienes la carpeta, navegar a ella



Crear un archivo `.env` en la raíz del proyecto (solo si no existe):# Crear entorno virtualcd "EvaIa"



```bashpy -3.11 -m venv venv```

# En Windows

notepad .env



# En macOS/Linux# Activar entorno virtual### Paso 3: Crear la Base de Datos

nano .env

```.\venv\Scripts\Activate.ps1



Agregar las siguientes variables:```bash



```env# Si hay error de permisos:# Conectarse a PostgreSQL

# Base de Datos

DB_NAME=evalexpo_dbSet-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUserpsql -U postgres

DB_USER=evalexpo_user

DB_PASSWORD=tu_contraseña_segura

DB_HOST=localhost

DB_PORT=5432# Verificar Python# Dentro de psql, ejecutar:



# Cloudinary (para almacenamiento de archivos)python --versionCREATE DATABASE evalexpo_db;

CLOUDINARY_CLOUD_NAME=tu_cloud_name

CLOUDINARY_API_KEY=tu_api_key```CREATE USER evalexpo_user WITH PASSWORD 'tu_contraseña_segura';

CLOUDINARY_API_SECRET=tu_api_secret

ALTER ROLE evalexpo_user SET client_encoding TO 'utf8';

# API de Groq (para análisis de IA)

GROQ_API_KEY=tu_groq_api_key**macOS/Linux:**ALTER ROLE evalexpo_user SET default_transaction_isolation TO 'read committed';



# Configuración de Django```bashALTER ROLE evalexpo_user SET timezone TO 'UTC';

SECRET_KEY=django-insecure-#l1*xrw5x@0nqr^(ip@71%1z6e1wj_(0etuw2$xjj3w%pq^!33

DEBUG=True# Crear entorno virtualGRANT ALL PRIVILEGES ON DATABASE evalexpo_db TO evalexpo_user;

ALLOWED_HOSTS=127.0.0.1,localhost

```python3 -m venv venv



**Obtener credenciales:**# Salir de psql

- **Cloudinary**: Registrarse en https://cloudinary.com/ (plan gratuito disponible)

- **Groq API**: Registrarse en https://console.groq.com/ (obtener API key gratuita)# Activar entorno virtual\q



### Paso 7: Configurar la Base de Datossource venv/bin/activate```



```bash

# Aplicar migraciones

python manage.py makemigrations# Verificar Python### Paso 4: Configurar el Entorno Virtual

python manage.py migrate

python --version

# Crear grupos de usuarios (Estudiante y Docente) - IMPORTANTE

python manage.py create_groups```**Windows (PowerShell):**



# Crear superusuario para el panel de administración```powershell

python manage.py createsuperuser

# Seguir las instrucciones en pantalla---# Navegar a la carpeta del proyecto

```

cd c:\Users\user\Desktop\evaIA

### Paso 8: Cargar Datos Iniciales (Opcional)

### 5. Instalar Dependencias

```bash

# Si existen fixtures o datos de prueba# Crear entorno virtual con Python 3.11

python manage.py loaddata initial_data.json

``````bashpy -3.11 -m venv venv



### Paso 9: Recolectar Archivos Estáticos# Actualizar pip



```bashpython -m pip install --upgrade pip# Activar entorno virtual

python manage.py collectstatic --noinput

```.\venv\Scripts\Activate.ps1



### Paso 10: Verificar la Instalación# Instalar dependencias



```bashpip install -r requirements.txt# Si hay error de permisos, ejecutar:

# Ejecutar pruebas

python manage.py test```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser



# Si todo está correcto, deberías ver:

# Ran X tests in Y seconds

# OK**⚠️ IMPORTANTE - Solución a conflictos de dependencias:**# Verificar la versión de Python

```

python --version

**✅ Instalación completada exitosamente!**

El archivo `requirements.txt` ya está configurado con las versiones compatibles:# Debe mostrar: Python 3.11.x o Python 3.12.x

---

```

## Guía de Uso

```txt

### 1. Iniciar el Sistema

# Versiones compatibles (YA CONFIGURADAS)**macOS/Linux:**

#### Activar el Entorno Virtual

mediapipe>=0.10.9          # Flexible para compatibilidad```bash

**Windows (PowerShell):**

```powershelltensorflow>=2.16.0,<2.18.0 # Compatible con MediaPipe# Navegar a la carpeta del proyecto

cd "d:\evaIA-main\evaIA"

.\venv\Scripts\Activate.ps1tf-keras>=2.16.0           # Compatible con TensorFlowcd ~/Desktop/evaIA

```

# protobuf se instala automáticamente (NO especificar versión)

**macOS/Linux:**

```bash```# Crear entorno virtual

cd ~/evaIA

source venv/bin/activatepython3 -m venv venv

```

**Notas:**

#### Iniciar el Servidor

- La instalación puede tardar 15-30 minutos# Activar entorno virtual

```bash

python manage.py runserver- Tamaño de descarga: ~4-6 GBsource venv/bin/activate

```

- Si hay error con `openai-whisper`, instalar Rust desde: https://www.rust-lang.org/tools/install

**Acceder a la aplicación:**

- Aplicación principal: http://127.0.0.1:8000/# Verificar la versión de Python

- Panel admin: http://127.0.0.1:8000/admin/

- Login: http://127.0.0.1:8000/auth/login/**Instalación por partes** (si hay problemas):python --version



### 2. Uso para Estudiantes```bash# Debe mostrar: Python 3.11.x o Python 3.12.x



#### Subir una Presentación# 1. Django y dependencias web```



1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**pip install Django==5.2.7 psycopg2-binary==2.9.11 cloudinary==1.44.1

2. Seleccionar la pestaña **"Subir Archivo"**

3. Completar el formulario:### Paso 5: Instalar Dependencias

   - **Asignación**: Seleccionar de la lista desplegable

   - **Título**: Nombre descriptivo de tu presentación# 2. PyTorch

   - **Archivo de video**: 

     - Arrastra el archivo o haz clic para seleccionarpip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1```bash

     - Formatos: MP4, AVI, MOV, MKV, WEBM

     - Tamaño máximo: 500 MB# Actualizar pip

     - Duración máxima: 30 minutos

   - **Descripción** (opcional): Notas adicionales# 3. TensorFlow y visión por computadorapython -m pip install --upgrade pip

4. Clic en **"Subir Presentación"**

5. Esperar la confirmación de cargapip install "tensorflow>=2.16.0,<2.18.0" "mediapipe>=0.10.9" deepface==0.0.95



**Consejos:**# Instalar todas las dependencias

- Buena iluminación y audio claro

- Cámara estable (usar trípode si es posible)# 4. Resto de dependenciaspip install -r requirements.txt

- Hablar con claridad y buen volumen

- Verificar que el video esté completo antes de subirpip install -r requirements.txt```



#### Grabar en Vivo```



1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"****⚠️ IMPORTANTE - Conflicto de dependencias resuelto:**

2. Seleccionar la pestaña **"Grabar en Vivo"**

3. Permitir acceso a la cámara y micrófono cuando el navegador lo solicite---

4. Seleccionar la **asignación**

5. Revisar las instrucciones mostradasSi encuentras errores de conflicto entre `tensorflow`, `mediapipe` y `protobuf`, el archivo `requirements.txt` ya está configurado correctamente con las siguientes versiones compatibles:

6. Verificar que aparezca **"Rostro detectado!"** (indicador verde)

   - Solo debe haber **1 persona** visible en cámara### 6. Configurar Variables de Entorno

   - Si se detectan múltiples personas, la grabación se pausará

7. Clic en **"Iniciar Grabación"**```txt

8. Aparecerá una cuenta regresiva de 3 segundos

9. Realizar la presentaciónCrear archivo `.env` en la raíz del proyecto:# Versiones compatibles (YA CONFIGURADAS)

10. Controles disponibles:

    - **Pausar**: Pausa temporalmente la grabaciónmediapipe>=0.10.9          # Flexible para compatibilidad

    - **Reanudar**: Continúa la grabación

    - **Detener**: Finaliza la grabación```envtensorflow>=2.16.0,<2.18.0 # Versión compatible con MediaPipe

    - **Reiniciar**: Descarta y comienza de nuevo

11. Al detener, revisar la vista previa# Base de Datostf-keras>=2.16.0           # Compatible con TensorFlow

12. Completar **título** y **descripción**

13. Clic en **"Guardar Presentación"**DB_NAME=evalexpo_db# protobuf se instala automáticamente (NO especificar versión)



**Indicadores importantes:**DB_USER=evalexpo_user```

- **Luz roja parpadeante**: Grabando

- **Temporizador**: Muestra el tiempo transcurridoDB_PASSWORD=tu_contraseña_segura

- **Rostro detectado**: Verde = OK, Rojo = Problema

- **Advertencia múltiples personas**: Se pausará automáticamenteDB_HOST=localhost**Notas importantes:**



#### Ver ResultadosDB_PORT=5432



1. Ir a **"Mis Presentaciones"**1. **PyTorch y dependencias de IA**: La instalación puede tardar 15-30 minutos dependiendo de tu conexión y hardware.

2. Buscar tu presentación en la lista

3. Hacer clic en **"Ver Detalles"** o en el título# Cloudinary (obtener en https://cloudinary.com/)

4. Visualizar:

   - **Calificación numérica** (0-100)CLOUDINARY_CLOUD_NAME=tu_cloud_name2. **Tamaño de descarga**: Aproximadamente 4-6 GB de paquetes.

   - **Estado**: Pendiente, En Proceso, Completado

   - **Transcripción** del audioCLOUDINARY_API_KEY=tu_api_key

   - **Análisis de IA** con:

     - Fortalezas identificadasCLOUDINARY_API_SECRET=tu_api_secret3. **Si obtienes error con `openai-whisper`**: Este paquete requiere Rust y herramientas de compilación. Si falla:

     - Áreas de mejora

     - Recomendaciones específicas   ```bash

   - **Comentarios del docente** (si están disponibles)

   - **Desglose por criterios** de evaluación# Groq API (obtener en https://console.groq.com/)   # Opción 1: Instalar Rust

   - **Video de la presentación**

GROQ_API_KEY=tu_groq_api_key   # Windows: https://www.rust-lang.org/tools/install

---

   # Linux/Mac: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

### 3. Uso para Docentes

# Django   

#### Crear un Curso

SECRET_KEY=django-insecure-#l1*xrw5x@0nqr^(ip@71%1z6e1wj_(0etuw2$xjj3w%pq^!33   # Opción 2: Comentar la línea en requirements.txt

1. Ir a **"Mis Cursos"** → **"Nuevo Curso"**

2. Completar:DEBUG=True   # openai-whisper==20231117  # Requiere Rust

   - **Código del curso**: Ej. "CS101"

   - **Nombre**: Ej. "Introducción a la Programación"ALLOWED_HOSTS=127.0.0.1,localhost   ```

   - **Descripción**: Información del curso

   - **Período académico**: Ej. "2025-1"```

3. Clic en **"Crear Curso"**

4. **Compatibilidad verificada**: 

#### Gestionar Estudiantes

---   - ✅ Python 3.11.8

1. Entrar al curso deseado

2. Ir a **"Estudiantes"**   - ✅ Python 3.12.x

3. Opciones:

   - **Agregar estudiante**: Buscar por correo e invitar### 7. Configurar Base de Datos   - ✅ Windows 10/11

   - **Importar lista**: Subir CSV con correos

   - **Eliminar estudiante**: Remover del curso   - ✅ macOS 12+ (Intel y M1/M2)

   - **Ver perfil**: Información detallada del estudiante

```bash   - ✅ Ubuntu 20.04+ / Debian 11+

**Formato CSV para importación:**

```csv# Aplicar migraciones

nombre,apellido,correo

Juan,Pérez,juan.perez@universidad.edupython manage.py makemigrations5. **Instalación por partes** (si tienes problemas):

María,González,maria.gonzalez@universidad.edu

```python manage.py migrate   ```bash



#### Crear una Asignación   # 1. Django y dependencias web



1. Dentro del curso, ir a **"Asignaciones"**# Crear grupos de usuarios (Estudiante y Docente)   pip install Django==5.2.7 psycopg2-binary==2.9.11 cloudinary==1.44.1

2. Clic en **"Nueva Asignación"**

3. Completar el formulario:python manage.py create_groups   

   - **Título**: Ej. "Presentación Final - Proyecto Web"

   - **Descripción**: Explicación detallada   # 2. PyTorch (instalar primero)

   - **Tipo**: Individual o Grupal

   - **Fecha límite**: Seleccionar fecha y hora# Crear superusuario   pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1

   - **Duración máxima**: En minutos (ej. 15)

   - **Puntaje máximo**: Ej. 100python manage.py createsuperuser   

   - **Instrucciones**: Detalles específicos para los estudiantes

   - **Criterios de evaluación**: (Ver sección siguiente)```   # 3. TensorFlow y visión por computadora

4. Clic en **"Crear Asignación"**

   pip install "tensorflow>=2.16.0,<2.18.0" "mediapipe>=0.10.9" deepface==0.0.95

#### Configurar Rúbrica

---   

Al crear o editar una asignación:

   # 4. Resto de dependencias

1. Scroll hasta **"Criterios de Evaluación"**

2. Agregar criterios, por ejemplo:### 8. Recolectar Archivos Estáticos   pip install -r requirements.txt

   - **Contenido** (30 puntos)

     - Dominio del tema   ```

     - Profundidad del análisis

   - **Organización** (20 puntos)```bash

     - Estructura lógica

     - Transiciones claraspython manage.py collectstatic --noinput### Paso 6: Configurar Variables de Entorno

   - **Expresión Verbal** (25 puntos)

     - Claridad al hablar```

     - Volumen y tono adecuados

   - **Lenguaje Corporal** (15 puntos)Crear un archivo `.env` en la raíz del proyecto (solo si no existe):

     - Contacto visual

     - Postura profesional---

   - **Tiempo** (10 puntos)

     - Cumplimiento del tiempo asignado```bash



3. Especificar ponderaciones para cada criterio### 9. Verificar Instalación# En Windows

4. Guardar la rúbrica

notepad .env

#### Revisar y Calificar

```bash

1. Ir a **"Presentaciones"** → **"Pendientes de Calificar"**

2. Seleccionar una presentación# Ejecutar servidor# En macOS/Linux

3. Revisar:

   - **Video de la presentación**python manage.py runservernano .env

   - **Transcripción automática**

   - **Análisis preliminar de IA**```

   - **Sugerencias de calificación**

# Abrir en navegador: http://127.0.0.1:8000/

**Opciones de calificación:**

```Agregar las siguientes variables:

1. En la página de detalles de la presentación

2. Clic en **"Calificar"**

3. Opciones:

   - **Aceptar calificación de IA**: Usar la evaluación automática**✅ Instalación completada exitosamente!**```env

   - **Modificar calificación**: Ajustar puntos por criterio

   - **Calificación personalizada**: Ingresar manualmente# Base de Datos

4. Agregar **comentarios** para el estudiante:

   - Fortalezas observadas---DB_NAME=evalexpo_db

   - Áreas de mejora específicas

   - Consejos para futuras presentacionesDB_USER=evalexpo_user

5. Clic en **"Guardar Calificación"**

## Guía de UsoDB_PASSWORD=tu_contraseña_segura

#### Generar Reportes

DB_HOST=localhost

1. Seleccionar un estudiante

2. Ir a **"Ver Reporte"**### 1. Iniciar el SistemaDB_PORT=5432

3. Descargar en formato:

   - PDF (para imprimir)

   - Excel (para análisis)

   - CSV (para importar a otros sistemas)#### Activar Entorno Virtual# Cloudinary (para almacenamiento de archivos)



**Reportes de curso:**CLOUDINARY_CLOUD_NAME=tu_cloud_name



1. Entrar al curso**Windows:**CLOUDINARY_API_KEY=tu_api_key

2. Clic en **"Reportes"**

3. Visualizar:```powershellCLOUDINARY_API_SECRET=tu_api_secret

   - **Progreso general** del curso

   - **Gráficas de desempeño**cd "d:\evaIA-main\evaIA"

   - **Comparativas entre estudiantes**

   - **Tendencias de mejora**.\venv\Scripts\Activate.ps1# API de Groq (para análisis de IA)

4. Filtros disponibles:

   - Por asignación```GROQ_API_KEY=tu_groq_api_key

   - Por fecha

   - Por rango de calificación



**Exportar Calificaciones:****macOS/Linux:**# Configuración de Django



1. En la vista de curso, ir a **"Calificaciones"**```bashSECRET_KEY=django-insecure-#l1*xrw5x@0nqr^(ip@71%1z6e1wj_(0etuw2$xjj3w%pq^!33

2. Clic en **"Exportar"**

3. Seleccionar formato (Excel, CSV, PDF)cd ~/evaIADEBUG=True

4. Descargar archivo

source venv/bin/activateALLOWED_HOSTS=127.0.0.1,localhost

---

``````

### 4. Manual para Administradores



#### 4.1 Panel de Administración

#### Iniciar Servidor**Obtener credenciales:**

Acceder a: http://127.0.0.1:8000/admin/

- **Cloudinary**: Registrarse en https://cloudinary.com/ (plan gratuito disponible)

Funciones disponibles:

- Gestión completa de usuarios```bash- **Groq API**: Registrarse en https://console.groq.com/ (obtener API key gratuita)

- Supervisión de cursos y asignaciones

- Monitoreo de uso del sistemapython manage.py runserver

- Configuración de parámetros globales

```### Paso 7: Configurar la Base de Datos

#### 4.2 Gestión de Usuarios



1. En el panel admin, ir a **"Authentication"** → **"Users"**

2. Opciones:**Acceder a:**```bash

   - **Crear usuario**: Agregar manualmente

   - **Editar usuario**: Cambiar rol, permisos- Aplicación: http://127.0.0.1:8000/# Aplicar migraciones

   - **Activar/Desactivar**: Suspender cuentas

   - **Eliminar**: Remover permanentemente- Admin: http://127.0.0.1:8000/admin/python manage.py makemigrations



#### 4.3 Configuración del Sistema- Login: http://127.0.0.1:8000/auth/login/python manage.py migrate



1. Ir a **"Settings"** en el panel admin

2. Configurar:

   - **Límites de almacenamiento**---# Crear grupos de usuarios (Estudiante y Docente) - IMPORTANTE

   - **Duración máxima de videos**

   - **Tamaño máximo de archivos**python manage.py create_groups

   - **Cuota de API de IA**

   - **Notificaciones por email**### 2. Para Estudiantes



#### 4.4 Monitoreo de Recursos# Crear superusuario para el panel de administración



1. **Dashboard de Administrador**#### Registro e Inicio de Sesiónpython manage.py createsuperuser

2. Ver:

   - Uso de almacenamiento (Cloudinary)# Seguir las instrucciones en pantalla

   - Consumo de API de IA (Groq/OpenAI)

   - Número de usuarios activos1. Ir a http://127.0.0.1:8000/```

   - Presentaciones procesadas

   - Tiempo promedio de procesamiento2. Clic en **"Registrarse"**



#### 4.5 Backups y Mantenimiento3. Completar formulario (nombre, email, contraseña, rol: Estudiante)### Paso 8: Cargar Datos Iniciales (Opcional)



```bash4. Iniciar sesión con tus credenciales

# Backup de la base de datos

python manage.py dumpdata > backup_$(date +%Y%m%d).json```bash



# Restaurar desde backup#### Subir Presentación (Opción 1: Archivo)# Si existen fixtures o datos de prueba

python manage.py loaddata backup_20251103.json

python manage.py loaddata initial_data.json

# Limpiar archivos temporales

python manage.py clearsessions1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**```

python manage.py cleanup_uploads

2. Seleccionar **"Subir Archivo"**

# Ver logs del sistema

tail -f logs/system.log3. Completar:### Paso 9: Recolectar Archivos Estáticos

```

   - **Asignación**: Seleccionar de la lista

---

   - **Título**: Nombre de la presentación```bash

### 5. Funciones Comunes para Todos los Usuarios

   - **Archivo**: Video (MP4, AVI, MOV, MKV, WEBM - máx 500 MB, 30 min)python manage.py collectstatic --noinput

#### 5.1 Editar Perfil

   - **Descripción** (opcional)```

1. Clic en el **avatar** (esquina superior derecha)

2. Seleccionar **"Mi Perfil"**4. Clic en **"Subir Presentación"**

3. Editar:

   - Foto de perfil### Paso 10: Verificar la Instalación

   - Nombre y apellidos

   - Correo electrónico**Consejos:**

   - Contraseña

   - Preferencias de notificación- Buena iluminación y audio claro```bash

4. Clic en **"Guardar Cambios"**

- Cámara estable# Ejecutar pruebas

#### 5.2 Cambiar Contraseña

- Hablar con claridadpython manage.py test

1. Ir a **"Mi Perfil"** → **"Seguridad"**

2. Ingresar:

   - Contraseña actual

   - Nueva contraseña#### Grabar en Vivo (Opción 2)# Si todo está correcto, deberías ver:

   - Confirmar nueva contraseña

3. Clic en **"Actualizar Contraseña"**# Ran X tests in Y seconds



#### 5.3 Configurar Notificaciones1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**# OK



1. Ir a **"Configuración"** → **"Notificaciones"**2. Seleccionar **"Grabar en Vivo"**```

2. Activar/desactivar:

   - Notificaciones por correo3. Permitir acceso a cámara y micrófono

   - Notificaciones en la app

   - Frecuencia de resúmenes4. Seleccionar asignación**Instalación completada exitosamente!**

3. Guardar preferencias

5. Verificar **"Rostro detectado!"** (verde)

#### 5.4 Centro de Ayuda

6. Clic en **"Iniciar Grabación"**---

1. Clic en el ícono **"?"** (esquina superior)

2. Acceder a:7. Realizar presentación

   - **Preguntas frecuentes (FAQ)**

   - **Tutoriales en video**8. **Detener** cuando termines## Guía de Uso

   - **Documentación técnica**

   - **Contactar soporte**9. Completar título y descripción



#### 5.5 Cerrar Sesión10. **"Guardar Presentación"**### 1. Iniciar el Sistema



1. Clic en el **avatar**

2. Seleccionar **"Cerrar Sesión"**

3. Confirmar**Indicadores:**#### Activar el Entorno Virtual



---- 🔴 Luz roja = Grabando



### 6. Mejores Prácticas- ⏱️ Temporizador activo**Windows (PowerShell):**



#### Para Estudiantes- ✅ Verde = Rostro detectado OK```powershell



**Antes de grabar:**- ⚠️ Rojo = Múltiples personas (se pausa)cd "d:\evaIA-main\evaIA"

- Revisar las instrucciones de la asignación

- Preparar y practicar tu presentación.\venv\Scripts\Activate.ps1

- Verificar audio y video

- Elegir un fondo limpio y profesional#### Ver Resultados```

- Asegurar buena iluminación



**Durante la grabación:**

- Mantener contacto visual con la cámara1. Ir a **"Mis Presentaciones"****macOS/Linux:**

- Hablar con claridad y a buen volumen

- Evitar muletillas ("ehh", "mmm")2. Clic en la presentación deseada```bash

- Controlar el tiempo

- Mantener una postura profesional3. Ver:cd ~/evaIA



**Después de subir:**   - Calificación numérica (0-100)source venv/bin/activate

- Verificar que el video se cargó correctamente

- Revisar la transcripción por si hay errores   - Estado: Pendiente/En Proceso/Completado```

- Estar atento a las notificaciones

- Responder a comentarios del docente   - Transcripción del audio



#### Para Docentes   - Análisis de IA (fortalezas, áreas de mejora, recomendaciones)#### Iniciar el Servidor



**Al crear asignaciones:**   - Comentarios del docente

- Proporcionar instrucciones claras y detalladas

- Establecer criterios de evaluación específicos   - Desglose por criterios```bash

- Dar tiempo suficiente para preparación

- Comunicar expectativas claramente   - Video de la presentaciónpython manage.py runserver



**Al evaluar:**```

- Revisar el análisis de IA como guía inicial

- Proporcionar retroalimentación constructiva---

- Ser específico en los comentarios

- Destacar tanto fortalezas como áreas de mejora**Acceder a la aplicación:**

- Responder dudas de los estudiantes

### 3. Para Docentes- Aplicación principal: http://127.0.0.1:8000/

---

- Panel admin: http://127.0.0.1:8000/admin/

## Guía Técnica

#### Crear Curso- Login: http://127.0.0.1:8000/auth/login/

### Stack Tecnológico



#### Backend

- **Framework**: Django 5.2.71. Ir a **"Mis Cursos"** → **"Nuevo Curso"**### 2. Uso para Estudiantes

- **Base de datos**: PostgreSQL 13+

- **Lenguaje**: Python 3.11+2. Completar:

- **ORM**: Django ORM

   - **Código**: Ej. "CS101"#### Subir una Presentación

#### Inteligencia Artificial

- **Modelos de lenguaje**: Groq API, OpenAI GPT-4   - **Nombre**: Ej. "Introducción a la Programación"

- **Transcripción**: OpenAI Whisper

- **Detección facial**: MediaPipe 0.10.9+   - **Descripción**1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**

- **Análisis facial**: DeepFace 0.0.95

- **Deep Learning**: TensorFlow 2.16-2.17, PyTorch 2.5.1   - **Período académico**: Ej. "2025-1"2. Seleccionar la pestaña **"Subir Archivo"**



#### Procesamiento3. **"Crear Curso"**3. Completar el formulario:

- **Video**: OpenCV 4.9.0.80, MoviePy, ImageIO, FFmpeg

- **Audio**: Librosa, SoundFile, Pydub   - **Asignación**: Seleccionar de la lista desplegable

- **Texto**: Transformers, Sentence-Transformers

#### Gestionar Estudiantes   - **Título**: Nombre descriptivo de tu presentación

#### Frontend

- **Templates**: Django Templates + Jinja2   - **Archivo de video**: 

- **JavaScript**: Vanilla JS

- **CSS**: Bootstrap 51. Entrar al curso     - Arrastra el archivo o haz clic para seleccionar

- **Grabación**: MediaRecorder API

2. Ir a **"Estudiantes"**     - Formatos: MP4, AVI, MOV, MKV, WEBM

#### Almacenamiento

- **Archivos**: Cloudinary3. Opciones:     - Tamaño máximo: 500 MB

- **Base de datos**: PostgreSQL

   - Agregar estudiante (buscar por email)     - Duración máxima: 30 minutos

---

   - Importar lista (CSV: `nombre,apellido,correo`)   - **Descripción** (opcional): Notas adicionales

### Arquitectura del Sistema

   - Eliminar estudiante4. Clic en **"Subir Presentación"**

```

evaIA/   - Ver perfil5. Esperar la confirmación de carga

├── apps/

│   ├── ai_processor/          # Procesamiento de IA

│   │   └── services/          # Audio, video, facial detection

│   ├── presentaciones/        # Gestión de presentaciones#### Crear Asignación**Consejos:**

│   ├── notifications/         # Sistema de notificaciones

│   ├── reportes/             # Generación de reportes- Buena iluminación y audio claro

│   └── help/                 # Centro de ayuda

├── authentication/            # Autenticación y usuarios1. Dentro del curso → **"Asignaciones"** → **"Nueva Asignación"**- Cámara estable (usar trípode si es posible)

├── sist_evaluacion_expo/     # Configuración Django

├── templates/                # Plantillas HTML2. Completar:- Hablar con claridad y buen volumen

├── static/                   # CSS, JS, imágenes

├── docs/                     # Documentación técnica   - **Título**- Verificar que el video esté completo antes de subir

└── requirements.txt          # Dependencias Python

```   - **Descripción**



---   - **Tipo**: Individual/Grupal#### Grabar en Vivo



### Flujo de Procesamiento   - **Fecha límite**



1. **Estudiante sube video** → Almacenamiento en Cloudinary   - **Duración máxima** (minutos)1. Ir a **"Mis Presentaciones"** → **"Nueva Presentación"**

2. **Extracción de audio** → Transcripción con Whisper

3. **Análisis facial** → MediaPipe + DeepFace   - **Puntaje máximo**2. Seleccionar la pestaña **"Grabar en Vivo"**

4. **Procesamiento de video** → OpenCV (frames, movimiento)

5. **Análisis de contenido** → Groq/OpenAI (evaluación de texto)   - **Instrucciones**3. Permitir acceso a la cámara y micrófono cuando el navegador lo solicite

6. **Generación de calificación** → Motor de evaluación con criterios

7. **Notificación** → Estudiante y Docente   - **Criterios de evaluación**4. Seleccionar la **asignación**



---3. **"Crear Asignación"**5. Revisar las instrucciones mostradas



### Configuración de Variables de Entorno6. Verificar que aparezca **"Rostro detectado!"** (indicador verde)



```env#### Configurar Rúbrica   - Solo debe haber **1 persona** visible en cámara

# Django

SECRET_KEY=tu_clave_secreta_muy_larga_y_segura   - Si se detectan múltiples personas, la grabación se pausará

DEBUG=False

ALLOWED_HOSTS=tu-dominio.comAgregar criterios de evaluación:7. Clic en **"Iniciar Grabación"**

DJANGO_SETTINGS_MODULE=sist_evaluacion_expo.settings

- **Contenido** (30 puntos)8. Aparecerá una cuenta regresiva de 3 segundos

# Base de Datos

DB_ENGINE=django.db.backends.postgresql- **Organización** (20 puntos)9. Realizar la presentación

DB_NAME=evalexpo_db

DB_USER=evalexpo_user- **Expresión Verbal** (25 puntos)10. Controles disponibles:

DB_PASSWORD=contraseña_segura

DB_HOST=localhost- **Lenguaje Corporal** (15 puntos)    - **Pausar**: Pausa temporalmente la grabación

DB_PORT=5432

- **Tiempo** (10 puntos)    - **Reanudar**: Continúa la grabación

# Cloudinary

CLOUDINARY_CLOUD_NAME=tu_cloud_name    - **Detener**: Finaliza la grabación

CLOUDINARY_API_KEY=tu_api_key

CLOUDINARY_API_SECRET=tu_api_secret#### Revisar y Calificar    - **Reiniciar**: Descarta y comienza de nuevo



# APIs de IA11. Al detener, revisar la vista previa

GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1. Ir a **"Presentaciones"** → **"Pendientes de Calificar"**12. Completar **título** y **descripción**

AI_PROVIDER=groq  # 'groq' o 'openai'

AI_MODEL=llama-3.3-70b-versatile  # Para Groq2. Seleccionar presentación13. Clic en **"Guardar Presentación"**



# Email (opcional)3. Revisar:

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

EMAIL_HOST=smtp.gmail.com   - Video**Indicadores importantes:**

EMAIL_PORT=587

EMAIL_USE_TLS=True   - Transcripción automática- **Luz roja parpadeante**: Grabando

EMAIL_HOST_USER=tu_email@gmail.com

EMAIL_HOST_PASSWORD=tu_app_password   - Análisis preliminar de IA- **Temporizador**: Muestra el tiempo transcurrido



# Seguridad (producción)   - Sugerencias de calificación- **Rostro detectado**: Verde = OK, Rojo = Problema

SECURE_SSL_REDIRECT=True

SESSION_COOKIE_SECURE=True4. Clic en **"Calificar"**- **Advertencia múltiples personas**: Se pausará automáticamente

CSRF_COOKIE_SECURE=True

SECURE_HSTS_SECONDS=315360005. Opciones:

```

   - **Aceptar calificación de IA**#### Ver Resultados

---

   - **Modificar calificación** por criterio

### Configuración Avanzada (settings.py)

   - **Calificación personalizada**1. Ir a **"Mis Presentaciones"**

```python

# Configuración de procesamiento de IA6. Agregar comentarios2. Buscar tu presentación en la lista

AI_PROCESSING_CONFIG = {

    'video': {7. **"Guardar Calificación"**3. Hacer clic en **"Ver Detalles"** o en el título

        'max_resolution': (1920, 1080),

        'frame_sample_rate': 1,4. Visualizar:

        'max_duration_seconds': 1800,  # 30 minutos

    },#### Generar Reportes   - **Calificación numérica** (0-100)

    'audio': {

        'sample_rate': 16000,   - **Estado**: Pendiente, En Proceso, Completado

        'whisper_model': 'medium',

    },1. Seleccionar estudiante → **"Ver Reporte"**   - **Transcripción** del audio

    'face_detection': {

        'min_detection_confidence': 0.5,2. Descargar: PDF, Excel, o CSV   - **Análisis de IA** con:

        'min_tracking_confidence': 0.5,

        'max_num_faces': 1,     - Fortalezas identificadas

    },

    'evaluation': {**Reportes de curso:**     - Áreas de mejora

        'use_facial_analysis': True,

        'use_emotion_detection': True,1. Entrar al curso → **"Reportes"**     - Recomendaciones específicas

        'use_gesture_analysis': True,

    }2. Ver:   - **Comentarios del docente** (si están disponibles)

}

   - Progreso general   - **Desglose por criterios** de evaluación

# Límites de carga

DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500 MB   - Gráficas de desempeño   - **Video de la presentación**

FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000

MAX_VIDEO_DURATION = 1800  # 30 minutos   - Comparativas



# Formatos permitidos   - Tendencias---

ALLOWED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm']

ALLOWED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a', '.ogg']3. Filtros: por asignación, fecha, calificación

```

4. **"Exportar"** → Seleccionar formato### 3. Uso para Docentes

---



### Solución de Problemas Comunes

---1. Ir a **"Mis Cursos"** → **"Nuevo Curso"**

#### Error: Conflicto de dependencias TensorFlow/MediaPipe

2. Completar:

```bash

# Usar versiones compatibles (ya configuradas en requirements.txt)## Guía Técnica   - **Código del curso**: Ej. "CS101"

mediapipe>=0.10.9

tensorflow>=2.16.0,<2.18.0   - **Nombre**: Ej. "Introducción a la Programación"

# NO especificar versión de protobuf

### Stack Tecnológico   - **Descripción**: Información del curso

# Si persiste:

pip uninstall tensorflow mediapipe protobuf -y   - **Período académico**: Ej. "2025-1"

pip install "tensorflow>=2.16.0,<2.18.0"

pip install "mediapipe>=0.10.9"#### Backend3. Clic en **"Crear Curso"**

```

- **Framework**: Django 5.2.7

#### Error: PostgreSQL no conecta

- **Base de datos**: PostgreSQL 13+#### Gestionar Estudiantes

```bash

# Verificar servicio- **Lenguaje**: Python 3.11+

# Windows: Services → PostgreSQL

# Linux: sudo systemctl status postgresql- **ORM**: Django ORM1. Entrar al curso deseado

# macOS: brew services list

2. Ir a **"Estudiantes"**

# Verificar credenciales en .env

DB_USER=evalexpo_user#### Inteligencia Artificial3. Opciones:

DB_PASSWORD=tu_contraseña_correcta

```- **Modelos de lenguaje**: Groq API, OpenAI GPT-4   - **Agregar estudiante**: Buscar por correo e invitar



#### Error: Video no se procesa- **Transcripción**: OpenAI Whisper   - **Importar lista**: Subir CSV con correos



```bash- **Detección facial**: MediaPipe 0.10.21   - **Eliminar estudiante**: Remover del curso

# Verificar FFmpeg instalado

ffmpeg -version- **Análisis facial**: DeepFace 0.0.95   - **Ver perfil**: Información detallada del estudiante



# Instalar:- **Deep Learning**: TensorFlow 2.16-2.17, PyTorch 2.5.1

# Windows: https://ffmpeg.org/download.html

# Linux: sudo apt install ffmpeg**Formato CSV para importación:**

# macOS: brew install ffmpeg

```#### Procesamiento```csv



#### Error: "No se detecta rostro"- **Video**: OpenCV 4.9.0.80, MoviePy, ImageIO, FFmpegnombre,apellido,correo



```python- **Audio**: Librosa, SoundFile, PydubJuan,Pérez,juan.perez@universidad.edu

# Ajustar sensibilidad en settings.py

FACE_DETECTION_CONFIG = {- **Texto**: Transformers, Sentence-Transformersmaría,gonzalez,maria.gonzalez@universidad.edu

    'min_detection_confidence': 0.3,  # Reducir umbral

}```



# Verificar:#### Frontend

# - Buena iluminación

# - Cámara a altura de ojos- **Templates**: Django Templates + Jinja2#### Crear Asignación

# - Distancia: 50-100 cm

```- **JavaScript**: Vanilla JS```



#### Alto uso de memoria- **CSS**: Bootstrap 5



```bash- **Grabación**: MediaRecorder API#### 3.4 Crear una Asignación

# Limpiar caché y sesiones

python manage.py clear_cache

python manage.py clearsessions

```#### Almacenamiento1. Dentro del curso, ir a **"Asignaciones"**



---- **Archivos**: Cloudinary2. Clic en **"Nueva Asignación"**



### Comandos Útiles- **Base de datos**: PostgreSQL3. Completar el formulario:



```bash   - **Título**: Ej. "Presentación Final - Proyecto Web"

# Verificar instalación

python manage.py check---   - **Descripción**: Explicación detallada



# Ver migraciones   - **Tipo**: Individual o Grupal

python manage.py showmigrations

### Arquitectura del Sistema   - **Fecha límite**: Seleccionar fecha y hora

# Crear superusuario

python manage.py createsuperuser   - **Duración máxima**: En minutos (ej. 15)



# Recolectar estáticos```   - **Puntaje máximo**: Ej. 100

python manage.py collectstatic

evaIA/   - **Instrucciones**: Detalles específicos para los estudiantes

# Shell de Django

python manage.py shell├── apps/   - **Criterios de evaluación**: (Ver sección siguiente)



# Backup de BD│   ├── ai_processor/          # Procesamiento de IA4. Clic en **"Crear Asignación"**

python manage.py dumpdata > backup.json

│   │   └── services/          # Audio, video, facial detection

# Restaurar BD

python manage.py loaddata backup.json│   ├── presentaciones/        # Gestión de presentaciones#### Configurar Rúbrica

```

│   ├── notifications/         # Sistema de notificaciones

---

│   ├── reportes/             # Generación de reportesAl crear o editar una asignación:

### API Endpoints

│   └── help/                 # Centro de ayuda

#### Autenticación

```http├── authentication/            # Autenticación y usuarios1. Scroll hasta **"Criterios de Evaluación"**

POST /auth/login/

POST /auth/register/├── sist_evaluacion_expo/     # Configuración Django2. Agregar criterios, por ejemplo:

```

├── templates/                # Plantillas HTML   - **Contenido** (30 puntos)

#### Presentaciones

```http├── static/                   # CSS, JS, imágenes     - Dominio del tema

GET /api/presentaciones/

POST /api/presentaciones/upload/├── docs/                     # Documentación técnica     - Profundidad del análisis

GET /api/presentaciones/{id}/

```└── requirements.txt          # Dependencias Python   - **Organización** (20 puntos)



#### Evaluación```     - Estructura lógica

```http

POST /api/ai/evaluate/     - Transiciones claras

```

---   - **Expresión Verbal** (25 puntos)

---

     - Claridad al hablar

### Configuración de Producción

### Flujo de Procesamiento     - Volumen y tono adecuados

```bash

# Instalar Gunicorn   - **Lenguaje Corporal** (15 puntos)

pip install gunicorn

1. **Estudiante sube video** → Almacenamiento en Cloudinary     - Contacto visual

# Ejecutar

gunicorn sist_evaluacion_expo.wsgi:application --bind 0.0.0.0:8000 --workers 42. **Extracción de audio** → Transcripción con Whisper     - Postura profesional



# Variables de entorno de producción3. **Análisis facial** → MediaPipe + DeepFace   - **Tiempo** (10 puntos)

DEBUG=False

SECURE_SSL_REDIRECT=True4. **Procesamiento de video** → OpenCV (frames, movimiento)     - Cumplimiento del tiempo asignado

SESSION_COOKIE_SECURE=True

CSRF_COOKIE_SECURE=True5. **Análisis de contenido** → Groq/OpenAI (evaluación de texto)

```

6. **Generación de calificación** → Motor de evaluación con criterios3. Especificar ponderaciones para cada criterio

**Nginx config:**

```nginx7. **Notificación** → Estudiante y Docente4. Guardar la rúbrica

location /static/ {

    alias /ruta/a/staticfiles/;

}

---#### Revisar y Calificar

location / {

    proxy_pass http://127.0.0.1:8000;

}

```### Configuración de Variables de Entorno1. Ir a **"Presentaciones"** → **"Pendientes de Calificar"**



---2. Seleccionar una presentación



### Documentación Adicional```env3. Revisar:



- **Arquitectura**: `docs/ARQUITECTURA_SISTEMA.md`# Django   - **Video de la presentación**

- **Detección facial**: `docs/MEJORAS_DETECCION_ROSTROS.md`

- **Optimización**: `docs/OPTIMIZACION_RENDIMIENTO.md`SECRET_KEY=tu_clave_secreta_muy_larga_y_segura   - **Transcripción automática**

- **Soluciones**: `docs/SOLUCION_*.md`

DEBUG=False   - **Análisis preliminar de IA**

---

ALLOWED_HOSTS=tu-dominio.com   - **Sugerencias de calificación**

<div align="center">

DJANGO_SETTINGS_MODULE=sist_evaluacion_expo.settings

**EvalExpo AI v1.0.10**

**Opciones de calificación:**

Desarrollado con ❤️ usando Django, Python e Inteligencia Artificial

# Base de Datos

[GitHub](https://github.com/LuisAngulo02/evaIA) • [Documentación](./docs/) • [Reportar Bug](https://github.com/LuisAngulo02/evaIA/issues)

DB_ENGINE=django.db.backends.postgresql1. En la página de detalles de la presentación

**Licencia MIT**

DB_NAME=evalexpo_db2. Clic en **"Calificar"**

</div>

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