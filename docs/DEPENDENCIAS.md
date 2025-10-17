# 📦 Dependencias del Proyecto EvalExpo AI

**Última actualización:** Octubre 2025  
**Total de paquetes:** 102  
**Estado:** ✅ Sincronizado y actualizado

---

## 📋 Índice

- [Framework Web](#framework-web)
- [Almacenamiento en Nube](#almacenamiento-en-nube)
- [Inteligencia Artificial](#inteligencia-artificial)
- [Procesamiento de Video/Imagen](#procesamiento-de-videoimagen)
- [Procesamiento de Audio](#procesamiento-de-audio)
- [Machine Learning](#machine-learning)
- [Análisis y Reportes](#análisis-y-reportes)
- [Base de Datos](#base-de-datos)
- [Configuración](#configuración)
- [HTTP y Networking](#http-y-networking)
- [Instalación](#instalación)
- [Actualización](#actualización)

---

## 🌐 Framework Web

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **Django** | 5.2.7 | Framework web principal |
| asgiref | 3.10.0 | Servidor ASGI para Django |
| sqlparse | 0.5.3 | Parser SQL para Django |

---

## ☁️ Almacenamiento en Nube

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **cloudinary** | 1.44.1 | SDK de Cloudinary para almacenamiento |
| **django-cloudinary-storage** | 0.3.0 | Integración de Cloudinary con Django |

**Uso:** Almacenamiento de videos de presentaciones y fotos de participantes en la nube.

---

## 🤖 Inteligencia Artificial

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **groq** | 0.32.0 | API de Groq para análisis de coherencia |
| **openai** | 2.3.0 | SDK de OpenAI |
| **openai-whisper** | 20250625 | Transcripción automática de audio |
| **transformers** | 4.57.0 | Modelos NLP de Hugging Face |
| **sentence-transformers** | 5.1.1 | Embeddings semánticos |
| huggingface-hub | 0.35.3 | Cliente para Hugging Face Hub |
| tokenizers | 0.22.1 | Tokenización de texto |
| tiktoken | 0.12.0 | Tokenización para OpenAI |
| sentencepiece | 0.2.1 | Tokenización de texto |

**Uso:** 
- Transcripción automática de presentaciones
- Análisis de coherencia del discurso
- Evaluación de contenido
- Generación de retroalimentación

---

## 👁️ Procesamiento de Video/Imagen

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **mediapipe** | 0.10.21 | Detección facial y seguimiento |
| **opencv-python** | 4.12.0.88 | Procesamiento de imágenes/video |
| **opencv-contrib-python** | 4.11.0.86 | Módulos adicionales de OpenCV |
| **moviepy** | 2.2.1 | Edición de video |
| **imageio** | 2.37.0 | Lectura/escritura de imágenes |
| imageio-ffmpeg | 0.6.0 | Integración con FFmpeg |
| pillow | 11.3.0 | Procesamiento de imágenes |

**Uso:**
- Detección de rostros en video
- Cálculo de tiempo de contacto visual
- Análisis de expresiones faciales
- Procesamiento de frames

---

## 🎵 Procesamiento de Audio

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **librosa** | 0.11.0 | Análisis de audio |
| **pydub** | 0.25.1 | Manipulación de audio |
| **soundfile** | 0.13.1 | Lectura/escritura de archivos de audio |
| sounddevice | 0.5.2 | Captura de audio |
| audioread | 3.0.1 | Lectura de formatos de audio |
| soxr | 1.0.0 | Resampleo de audio |

**Uso:**
- Extracción de audio de videos
- Análisis de pausas y muletillas
- Procesamiento de señales de audio
- Transcripción de voz a texto

---

## 🧠 Machine Learning

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **torch** | 2.8.0 | Framework de Deep Learning |
| **torchaudio** | 2.8.0 | Procesamiento de audio con PyTorch |
| **torchvision** | 0.23.0 | Visión por computadora con PyTorch |
| **scikit-learn** | 1.7.2 | Machine Learning tradicional |
| **numpy** | 1.26.4 | Computación numérica |
| **scipy** | 1.16.2 | Algoritmos científicos |
| jax | 0.7.1 | Computación numérica acelerada |
| jaxlib | 0.7.1 | Backend de JAX |
| numba | 0.62.1 | Compilación JIT de Python |
| joblib | 1.5.2 | Paralelización de tareas |

**Uso:**
- Modelos de IA para evaluación
- Procesamiento de embeddings
- Análisis de patrones
- Optimización de cálculos

---

## 📊 Análisis y Reportes

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **pandas** | 2.3.3 | Análisis de datos |
| **matplotlib** | 3.10.7 | Visualización de datos |
| **reportlab** | 4.4.4 | Generación de PDFs |
| **openpyxl** | 3.1.5 | Lectura/escritura de Excel |
| networkx | 3.5 | Análisis de redes |
| sympy | 1.14.0 | Matemática simbólica |

**Uso:**
- Generación de reportes en PDF
- Exportación de datos a Excel
- Gráficos de rendimiento
- Análisis estadístico

---

## 🗄️ Base de Datos

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **psycopg2-binary** | 2.9.11 | Adaptador de PostgreSQL |

**Uso:**
- Conexión con base de datos PostgreSQL
- Almacenamiento de usuarios, presentaciones y evaluaciones

---

## ⚙️ Configuración

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **python-dotenv** | 1.1.1 | Carga de variables de entorno |
| **python-decouple** | 3.8 | Separación de configuración |
| PyYAML | 6.0.3 | Parser de YAML |
| Jinja2 | 3.1.6 | Motor de plantillas |

**Uso:**
- Gestión segura de credenciales (.env)
- Configuración por entornos
- Templates de configuración

---

## 🌍 HTTP y Networking

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| **requests** | 2.32.5 | Cliente HTTP simple |
| **httpx** | 0.28.1 | Cliente HTTP asíncrono |
| **urllib3** | 2.5.0 | Librería HTTP de bajo nivel |
| certifi | 2025.10.5 | Certificados SSL |
| idna | 3.10 | Soporte de dominios internacionales |

**Uso:**
- Comunicación con APIs externas (Groq, OpenAI, Cloudinary)
- Descarga de modelos de IA
- Requests HTTP seguros

---

## 📥 Instalación

### Instalación completa

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# Linux/Mac:
source venv/bin/activate

# 3. Instalar todas las dependencias
pip install -r requirements.txt
```

### Instalación por categorías (opcional)

```bash
# Solo Django y base de datos
pip install Django==5.2.7 psycopg2-binary==2.9.11

# Agregar almacenamiento en nube
pip install cloudinary==1.44.1 django-cloudinary-storage==0.3.0

# Agregar IA y procesamiento
pip install openai-whisper==20250625 groq==0.32.0 mediapipe==0.10.21
```

---

## 🔄 Actualización

### Actualizar todas las dependencias

```bash
pip install --upgrade -r requirements.txt
```

### Actualizar paquete específico

```bash
pip install --upgrade nombre-paquete
```

### Generar requirements.txt actualizado

```bash
pip freeze > requirements.txt
```

### Verificar versiones instaladas

```bash
pip list
```

---

## 🔍 Verificación de Dependencias

### Script de verificación automática

Ejecutar el script de verificación del sistema:

```bash
python verificar_sistema.py
```

Este script verifica:
- ✅ Versiones de Django y Python
- ✅ Conexión a base de datos
- ✅ Configuración de Cloudinary
- ✅ APIs de IA (Groq, OpenAI)
- ✅ Variables de entorno
- ✅ Modelos de IA descargados

---

## 📌 Notas Importantes

### Compatibilidad

- **Python:** 3.11.8 (recomendado)
- **Sistema Operativo:** Windows 10/11, Linux, macOS
- **RAM recomendada:** 8 GB mínimo (16 GB para modelos de IA grandes)
- **Espacio en disco:** ~5 GB para modelos de IA

### Dependencias Pesadas

Los siguientes paquetes son los más pesados (~3-4 GB):

- torch + torchaudio + torchvision (~2 GB)
- transformers + modelos (~1 GB)
- opencv + mediapipe (~500 MB)
- scipy + numpy (~300 MB)

### Problemas Conocidos

1. **Error con mediapipe en Windows:**
   - Solución: Instalar Microsoft Visual C++ Redistributable

2. **Error con psycopg2 en Windows:**
   - Solución: Usar `psycopg2-binary` en lugar de `psycopg2`

3. **Modelos de Whisper muy lentos:**
   - Solución: Usar GPU con CUDA o modelos más pequeños (tiny, base)

---

## 🆘 Soporte

Si encuentras problemas con las dependencias:

1. Verifica que estés usando Python 3.11.8
2. Ejecuta `pip install --upgrade pip setuptools wheel`
3. Limpia caché: `pip cache purge`
4. Reinstala entorno virtual completo
5. Consulta la documentación oficial de cada paquete

---

**Última verificación:** Octubre 17, 2025  
**Estado:** ✅ Todas las dependencias instaladas y funcionando correctamente
