#!/usr/bin/env python
"""
EVALEXPO AI - SCRIPT DE CONFIGURACIÓN AUTOMÁTICA
Configura el entorno completo para el sistema de evaluación de presentaciones
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Mostrar banner del proyecto"""
    print("=" * 60)
    print("🎓 EVALEXPO AI - CONFIGURACIÓN AUTOMÁTICA")
    print("   Sistema de Evaluación de Presentaciones con IA")
    print("=" * 60)

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"📋 Verificando Python... {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or version.minor < 9:
        print("❌ Python 3.9+ requerido")
        sys.exit(1)
    else:
        print("✅ Versión de Python compatible")

def check_system_requirements():
    """Verificar requisitos del sistema"""
    print("\n🔍 Verificando requisitos del sistema...")
    
    # Verificar Git
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git instalado")
    except:
        print("❌ Git no encontrado - Instalar desde https://git-scm.com/")
        return False
    
    # Verificar pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        print("✅ pip disponible")
    except:
        print("❌ pip no encontrado")
        return False
    
    return True

def install_dependencies():
    """Instalar dependencias del proyecto"""
    print("\n📦 Instalando dependencias...")
    
    try:
        # Actualizar pip
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True)
        print("✅ pip actualizado")
        
        # Instalar requirements
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencias instaladas")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def setup_database():
    """Configurar base de datos"""
    print("\n🗄️ Configurando base de datos...")
    
    try:
        # Verificar migraciones
        subprocess.run([
            sys.executable, "manage.py", "makemigrations"
        ], check=True)
        print("✅ Migraciones creadas")
        
        # Aplicar migraciones
        subprocess.run([
            sys.executable, "manage.py", "migrate"
        ], check=True)
        print("✅ Migraciones aplicadas")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error configurando BD: {e}")
        print("💡 Asegúrate de tener PostgreSQL configurado")
        return False

def test_ai_components():
    """Probar componentes de IA"""
    print("\n🤖 Verificando componentes de IA...")
    
    try:
        # Probar Whisper
        result = subprocess.run([
            sys.executable, "-c", "import whisper; print('Whisper OK')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Whisper AI disponible")
        else:
            print("⚠️ Whisper AI no configurado correctamente")
        
        # Probar MoviePy
        result = subprocess.run([
            sys.executable, "-c", "import moviepy; print('MoviePy OK')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ MoviePy disponible")
        else:
            print("⚠️ MoviePy no configurado correctamente")
        
        return True
    except Exception as e:
        print(f"⚠️ Algunos componentes de IA no están disponibles: {e}")
        return False

def create_superuser():
    """Crear superusuario si no existe"""
    print("\n👨‍💼 Configuración de superusuario...")
    
    response = input("¿Crear superusuario ahora? (s/n): ").lower()
    if response == 's':
        try:
            subprocess.run([
                sys.executable, "manage.py", "createsuperuser"
            ], check=True)
            print("✅ Superusuario creado")
        except subprocess.CalledProcessError:
            print("⚠️ Error creando superusuario (puede ya existir)")

def main():
    """Función principal de configuración"""
    print_banner()
    
    # Verificar Python
    check_python_version()
    
    # Verificar sistema
    if not check_system_requirements():
        print("\n❌ Requisitos del sistema no cumplidos")
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error en instalación de dependencias")
        sys.exit(1)
    
    # Configurar BD
    if not setup_database():
        print("\n⚠️ Continúa con configuración manual de BD")
    
    # Probar IA
    test_ai_components()
    
    # Crear superusuario
    create_superuser()
    
    # Mensaje final
    print("\n" + "=" * 60)
    print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("=" * 60)
    print("🚀 Para iniciar el servidor:")
    print("   python manage.py runserver")
    print("\n📖 Documentación completa:")
    print("   - README.md")
    print("   - INSTALACION.md")
    print("\n🌐 Acceder en: http://127.0.0.1:8000")
    print("=" * 60)

if __name__ == "__main__":
    main()