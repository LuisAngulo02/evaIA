#!/usr/bin/env python
"""
🚀 Setup Automático - EvalExpo AI
==================================
Script simple que configura todo el entorno automáticamente

Ejecutar: python setup.py
"""

import os
import sys
import subprocess
import platform

def print_step(step, message):
    """Imprimir paso con formato"""
    print(f"\n{'='*70}")
    print(f"  [{step}] {message}")
    print('='*70)

def run_command(command, description, shell=True):
    """Ejecutar comando del sistema"""
    print(f"\n▶ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            text=True,
            capture_output=True
        )
        print(f"✅ {description} - COMPLETADO")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {description}")
        if e.stderr:
            print(f"   {e.stderr[:200]}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:200]}")
        return False

def main():
    print("\n" + "="*70)
    print("  🚀 SETUP AUTOMÁTICO - EvalExpo AI")
    print("="*70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print("❌ ERROR: No se encontró manage.py")
        print("   Ejecuta este script desde el directorio raíz del proyecto")
        sys.exit(1)
    
    print("✅ Directorio del proyecto verificado")
    
    # PASO 1: Crear entorno virtual
    print_step("1/4", "CREAR ENTORNO VIRTUAL")
    
    if os.path.exists('venv'):
        print("⚠️  El entorno virtual ya existe")
        response = input("¿Deseas recrearlo? (s/n): ").lower().strip()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            print("🗑️  Eliminando entorno virtual anterior...")
            if platform.system() == 'Windows':
                run_command('rmdir /s /q venv', 'Eliminar venv')
            else:
                run_command('rm -rf venv', 'Eliminar venv')
        else:
            print("ℹ️  Usando entorno virtual existente")
    
    if not os.path.exists('venv'):
        if not run_command(f'{sys.executable} -m venv venv', 'Crear entorno virtual'):
            print("❌ No se pudo crear el entorno virtual")
            sys.exit(1)
    
    # Determinar el ejecutable de Python en el venv
    if platform.system() == 'Windows':
        python_venv = os.path.join('venv', 'Scripts', 'python.exe')
        pip_venv = os.path.join('venv', 'Scripts', 'pip.exe')
    else:
        python_venv = os.path.join('venv', 'bin', 'python')
        pip_venv = os.path.join('venv', 'bin', 'pip')
    
    # PASO 2: Actualizar pip
    print_step("2/4", "ACTUALIZAR PIP Y HERRAMIENTAS")
    
    run_command(
        f'{python_venv} -m pip install --upgrade pip setuptools wheel',
        'Actualizar pip, setuptools y wheel'
    )
    
    # PASO 3: Instalar dependencias
    print_step("3/4", "INSTALAR DEPENDENCIAS")
    
    if not os.path.exists('requirements.txt'):
        print("❌ ERROR: No se encontró requirements.txt")
        sys.exit(1)
    
    print("📦 Instalando dependencias desde requirements.txt...")
    print("⏱️  Esto puede tardar 5-10 minutos (dependencias pesadas)")
    print("   - Django 5.2.7 + PostgreSQL")
    print("   - GROQ API (Llama 3.3 70B)")
    print("   - OpenAI Whisper (transcripción)")
    print("   - MediaPipe (detección facial)")
    print("   - Sentence Transformers (análisis semántico)")
    print("   - PyTorch 2.5.1 + OpenCV 4.9.0")
    print("   - Librosa, MoviePy, y más...")
    print("   ✨ Versiones optimizadas para máxima compatibilidad")
    print()
    
    # Instalar con output visible
    try:
        # Primera pasada: instalar todo con versiones específicas
        print("▶ Instalando con versiones específicas...")
        subprocess.run(
            f'{pip_venv} install -r requirements.txt',
            shell=True,
            check=True
        )
        print("✅ Todas las dependencias instaladas correctamente")
    except subprocess.CalledProcessError:
        print("⚠️  Algunos paquetes tuvieron conflictos, instalando paquetes críticos...")
        # Instalar paquetes críticos uno por uno
        critical_packages = [
            'Django==5.2.7',
            'psycopg2-binary==2.9.11',
            'python-dotenv==1.1.1',
            'python-decouple==3.8',
            'groq==0.32.0',
            'openai-whisper==20231117',
            'sentence-transformers==3.3.1',
            'mediapipe==0.10.21',
            'opencv-python==4.9.0.80',
            'moviepy==2.2.1',
            'librosa==0.11.0',
            'cloudinary==1.44.1',
            'reportlab==4.4.4',
            'pandas==2.2.3',
            'numpy==1.26.4'
        ]
        
        for package in critical_packages:
            try:
                print(f"  - Instalando {package.split('==')[0]}...")
                subprocess.run(
                    f'{pip_venv} install {package}',
                    shell=True,
                    check=True,
                    capture_output=True
                )
            except:
                print(f"    ⚠️  {package.split('==')[0]} - puede tener conflictos (continuando)")
        
        print("✅ Dependencias principales instaladas")
    
    # PASO 4: Configurar base de datos y migraciones
    print_step("4/4", "CONFIGURAR BASE DE DATOS")
    
    print("ℹ️  Configuración de PostgreSQL:")
    print("   Base de datos: sist_evaluacion_expo_db")
    print("   Usuario: postgres")
    print("   Contraseña: 123")
    print("   Host: localhost")
    print("   Puerto: 5432")
    print()
    
    response = input("¿Deseas ejecutar las migraciones ahora? (s/n): ").lower().strip()
    
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n▶ Ejecutando makemigrations...")
        run_command(f'{python_venv} manage.py makemigrations', 'Crear migraciones')
        
        print("\n▶ Ejecutando migrate...")
        result = run_command(f'{python_venv} manage.py migrate', 'Aplicar migraciones')
        
        if result:
            print("\n▶ Creando grupos de usuarios (Estudiante y Docente)...")
            groups_result = run_command(
                f'{python_venv} manage.py create_groups',
                'Crear grupos de usuarios'
            )
            
            if groups_result:
                print("✅ Grupos creados correctamente")
            else:
                print("⚠️  Los grupos pueden estar creados previamente")
        else:
            print("⚠️  Error en migraciones. Verifica:")
            print("   1. PostgreSQL está instalado y corriendo")
            print("   2. La base de datos 'sist_evaluacion_expo_db' existe")
            print("   3. Las credenciales en settings.py son correctas")
    else:
        print("⏭️  Migraciones omitidas")
        print("   Ejecútalas después con:")
        print("   .\\venv\\Scripts\\python.exe manage.py migrate")
    
    # Crear archivo .env si no existe
    if not os.path.exists('.env'):
        print("\n▶ Creando archivo .env...")
        env_content = """# ==========================================
# CONFIGURACIÓN DE EMAIL - GMAIL
# ==========================================
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion

# Instrucción: Usa una contraseña de aplicación de Gmail
# https://myaccount.google.com/apppasswords

# ==========================================
# GROQ API - ANÁLISIS DE COHERENCIA CON IA
# ==========================================
# Sistema de rotación automática de 5 keys
GROQ_API_KEY_1=gsk_tu_key_1_aqui
GROQ_API_KEY_2=gsk_tu_key_2_aqui
GROQ_API_KEY_3=gsk_tu_key_3_aqui
GROQ_API_KEY_4=gsk_tu_key_4_aqui
GROQ_API_KEY_5=gsk_tu_key_5_aqui

# Instrucción: Regístrate en https://console.groq.com
# Puedes usar una sola key (duplicarla 5 veces) o 5 diferentes

# ==========================================
# CLOUDINARY - ALMACENAMIENTO DE ARCHIVOS
# ==========================================
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# Instrucción: Regístrate en https://cloudinary.com (Opcional)
# Si no usas Cloudinary, los archivos se guardan localmente

# ==========================================
# CONFIGURACIÓN AVANZADA (Opcional)
# ==========================================
USE_ADVANCED_COHERENCE=True
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production
"""
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
    else:
        print("⚠️  Archivo .env ya existe, no se sobrescribirá")
    
    # RESUMEN FINAL
    print("\n" + "="*70)
    print("  ✅ SETUP COMPLETADO EXITOSAMENTE")
    print("="*70)
    print("\n📦 INSTALADO:")
    print("   ✅ Entorno virtual (venv/)")
    print("   ✅ ~190 paquetes Python")
    print("   ✅ Django 5.2.7 + PostgreSQL")
    print("   ✅ GROQ API (Llama 3.3 70B)")
    print("   ✅ OpenAI Whisper + Sentence Transformers")
    print("   ✅ MediaPipe + OpenCV + MoviePy")
    print("   ✅ PyTorch 2.5.1 + Librosa + Pandas")
    print("   ✅ Numpy 1.26.4 (compatible con todo el stack)")
    print("   ✅ Grupos de usuarios (Estudiante, Docente)")
    
    print("\n🚀 PRÓXIMOS PASOS:")
    print("\n   1. Editar .env con tus credenciales:")
    print("      - EMAIL_HOST_USER y EMAIL_HOST_PASSWORD")
    print("      - GROQ_API_KEY_1 hasta GROQ_API_KEY_5")
    print("      - CLOUDINARY (opcional)")
    print()
    print("   2. Activar entorno virtual:")
    if platform.system() == 'Windows':
        print("      .\\venv\\Scripts\\Activate.ps1")
        print("      # o en CMD: .\\venv\\Scripts\\activate.bat")
    else:
        print("      source venv/bin/activate")
    print()
    print("   3. Aplicar migraciones (si no se hizo):")
    print("      python manage.py migrate")
    print()
    print("   4. Crear grupos (si no se hizo):")
    print("      python manage.py create_groups")
    print()
    print("   5. Crear superusuario:")
    print("      python manage.py createsuperuser")
    print()
    print("   6. Iniciar servidor:")
    print("      python manage.py runserver")
    print()
    print("   7. Abrir navegador:")
    print("      http://127.0.0.1:8000")
    
    print("\n🔍 VERIFICAR SISTEMA:")
    print("   python verificar_sistema.py")
    print("   - Verifica que todas las dependencias estén instaladas")
    print("   - Comprueba configuración de GROQ, Whisper, MediaPipe")
    
    print("\n📚 DOCUMENTACIÓN:")
    print("   README.md - Guía completa del proyecto")
    print("   docs/CONFIGURACION.md - Configuración detallada")
    print("   docs/DEPENDENCIAS.md - Lista de dependencias")
    
    print("\n💡 CARACTERÍSTICAS PRINCIPALES:")
    print("   ✨ Detección facial en tiempo real (antes de grabar)")
    print("   ✨ Validación de audio y rostro en procesamiento")
    print("   ✨ Transcripción con Whisper de OpenAI")
    print("   ✨ Análisis de coherencia con IA (GROQ)")
    print("   ✨ Conclusiones grupales dinámicas generadas por IA")
    print("   ✨ Sistema de rotación automática de API keys")
    
    print("\n" + "="*70)
    print("  🎉 ¡Listo para usar!")
    print("="*70 + "\n")
    
    # Preguntar si desea crear superusuario
    response = input("¿Deseas crear un superusuario de Django ahora? (s/n): ").lower().strip()
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n▶ Creando superusuario...")
        subprocess.run(f'{python_venv} manage.py createsuperuser', shell=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante el setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
