#!/usr/bin/env python
"""
Script de verificación completa del sistema EvalExpo AI
Verifica todas las configuraciones: Email, Cloudinary, Base de Datos, IA, etc.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sist_evaluacion_expo.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from django.db import connection
from django.contrib.auth.models import User
import cloudinary
import cloudinary.api

def print_header(title):
    """Imprimir encabezado de sección"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_status(label, status, details=""):
    """Imprimir estado con formato"""
    status_icon = "✅" if status else "❌"
    print(f"{status_icon} {label}: {details if details else ('OK' if status else 'ERROR')}")

def verify_environment_variables():
    """Verificar variables de entorno"""
    print_header("🔧 VARIABLES DE ENTORNO")
    
    env_vars = {
        'EMAIL_HOST_USER': os.getenv('EMAIL_HOST_USER'),
        'EMAIL_HOST_PASSWORD': os.getenv('EMAIL_HOST_PASSWORD'),
        'CLOUDINARY_CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'CLOUDINARY_API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'CLOUDINARY_API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
    }
    
    for var_name, var_value in env_vars.items():
        if var_value:
            # Mostrar solo parte del valor para seguridad
            if 'PASSWORD' in var_name or 'SECRET' in var_name or 'KEY' in var_name:
                display_value = f"{var_value[:4]}...{var_value[-4:]}" if len(var_value) > 8 else "***"
            else:
                display_value = var_value
            print_status(var_name, True, display_value)
        else:
            print_status(var_name, False, "No configurado")

def verify_email_configuration():
    """Verificar configuración de email"""
    print_header("📧 CONFIGURACIÓN DE EMAIL")
    
    print_status("Backend", True, settings.EMAIL_BACKEND)
    print_status("Host", True, settings.EMAIL_HOST)
    print_status("Port", True, str(settings.EMAIL_PORT))
    print_status("TLS", settings.EMAIL_USE_TLS, str(settings.EMAIL_USE_TLS))
    print_status("User", bool(settings.EMAIL_HOST_USER), settings.EMAIL_HOST_USER)
    print_status("Password", bool(settings.EMAIL_HOST_PASSWORD), "Configurado" if settings.EMAIL_HOST_PASSWORD else "No configurado")
    print_status("From Email", True, settings.DEFAULT_FROM_EMAIL)
    
    # Probar envío de email (opcional)
    print("\n📤 Prueba de envío de email:")
    test_email = input("   ¿Deseas probar el envío de email? (s/n): ").lower().strip()
    
    if test_email in ['s', 'si', 'sí', 'y', 'yes']:
        recipient = input("   Ingresa el email destino: ").strip()
        if recipient:
            try:
                send_mail(
                    subject='✅ Prueba EvalExpo AI',
                    message='Este es un email de prueba del sistema EvalExpo AI.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                print_status("Envío de email", True, f"Email enviado a {recipient}")
            except Exception as e:
                print_status("Envío de email", False, str(e)[:100])
        else:
            print("   ⏭️  Prueba de email omitida")
    else:
        print("   ⏭️  Prueba de email omitida")

def verify_cloudinary_configuration():
    """Verificar configuración de Cloudinary"""
    print_header("☁️  CONFIGURACIÓN DE CLOUDINARY")
    
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    
    print_status("Cloud Name", bool(cloud_name), cloud_name or "No configurado")
    print_status("API Key", bool(api_key), f"{api_key[:8]}..." if api_key else "No configurado")
    print_status("API Secret", bool(api_secret), "Configurado" if api_secret else "No configurado")
    
    if cloud_name and api_key and api_secret:
        print_status("Storage Backend", True, settings.DEFAULT_FILE_STORAGE)
        
        # Probar conexión con Cloudinary
        try:
            result = cloudinary.api.ping()
            print_status("Conexión Cloudinary", True, "Conexión exitosa")
            
            # Obtener información de uso
            try:
                usage = cloudinary.api.usage()
                credits = usage.get('credits', {})
                used = credits.get('usage', 0)
                limit = credits.get('limit', 0)
                print(f"   📊 Uso: {used}/{limit} créditos")
            except:
                pass
                
        except Exception as e:
            print_status("Conexión Cloudinary", False, str(e)[:100])
    else:
        print_status("Configuración completa", False, "Faltan variables de entorno")

def verify_database_configuration():
    """Verificar configuración de base de datos"""
    print_header("🗄️  CONFIGURACIÓN DE BASE DE DATOS")
    
    db = settings.DATABASES['default']
    print_status("Engine", True, db['ENGINE'])
    print_status("Name", True, db['NAME'])
    print_status("User", True, db.get('USER', 'N/A'))
    print_status("Host", True, db.get('HOST', 'localhost'))
    print_status("Port", True, str(db.get('PORT', 'default')))
    
    # Probar conexión
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print_status("Conexión DB", True, "Conexión exitosa")
        
        # Contar usuarios
        user_count = User.objects.count()
        print(f"   👥 Usuarios registrados: {user_count}")
        
    except Exception as e:
        print_status("Conexión DB", False, str(e)[:100])

def verify_ai_configuration():
    """Verificar configuración de IA"""
    print_header("🤖 CONFIGURACIÓN DE IA")
    
    groq_key = os.getenv('GROQ_API_KEY')
    print_status("Groq API Key", bool(groq_key), "Configurado" if groq_key else "No configurado")
    print_status("Coherencia Avanzada", settings.USE_ADVANCED_COHERENCE, 
                 "Activada" if settings.USE_ADVANCED_COHERENCE else "Desactivada")
    
    if settings.USE_ADVANCED_COHERENCE:
        config = settings.COHERENCE_CONFIG
        print(f"   🔧 Modelo: {config.get('model')}")
        print(f"   🌡️  Temperature: {config.get('temperature')}")
        print(f"   📝 Max Tokens: {config.get('max_tokens')}")
        print(f"   ⏱️  Timeout: {config.get('timeout')}s")

def verify_media_configuration():
    """Verificar configuración de archivos multimedia"""
    print_header("📁 CONFIGURACIÓN DE ARCHIVOS MULTIMEDIA")
    
    print_status("MEDIA_URL", True, settings.MEDIA_URL)
    print_status("MEDIA_ROOT", True, str(settings.MEDIA_ROOT))
    print_status("STATIC_URL", True, settings.STATIC_URL)
    print_status("STATIC_ROOT", True, str(settings.STATIC_ROOT))
    
    # Verificar que los directorios existen
    media_exists = settings.MEDIA_ROOT.exists() if hasattr(settings.MEDIA_ROOT, 'exists') else os.path.exists(settings.MEDIA_ROOT)
    print_status("Directorio MEDIA existe", media_exists, str(settings.MEDIA_ROOT))
    
    # Verificar permisos de escritura
    try:
        test_file = settings.MEDIA_ROOT / 'test_write.tmp'
        test_file.touch()
        test_file.unlink()
        print_status("Permisos de escritura", True, "OK")
    except Exception as e:
        print_status("Permisos de escritura", False, str(e)[:100])

def verify_security_configuration():
    """Verificar configuración de seguridad"""
    print_header("🔒 CONFIGURACIÓN DE SEGURIDAD")
    
    print_status("DEBUG", settings.DEBUG, "Activado (⚠️ Desactivar en producción)" if settings.DEBUG else "Desactivado")
    print_status("SECRET_KEY", len(settings.SECRET_KEY) > 0, 
                 f"{len(settings.SECRET_KEY)} caracteres" if settings.SECRET_KEY else "No configurado")
    print_status("ALLOWED_HOSTS", len(settings.ALLOWED_HOSTS) > 0, 
                 ", ".join(settings.ALLOWED_HOSTS) if settings.ALLOWED_HOSTS else "No configurado")
    print_status("CSRF_COOKIE_SECURE", settings.CSRF_COOKIE_SECURE, str(settings.CSRF_COOKIE_SECURE))
    print_status("SESSION_COOKIE_AGE", True, f"{settings.SESSION_COOKIE_AGE}s ({settings.SESSION_COOKIE_AGE/3600}h)")

def verify_installed_apps():
    """Verificar apps instaladas"""
    print_header("📦 APLICACIONES INSTALADAS")
    
    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django.')]
    
    print("\n🔧 Apps propias:")
    for app in custom_apps:
        if app.startswith('apps.') or app == 'authentication':
            print(f"   ✅ {app}")
    
    print("\n📚 Apps de terceros:")
    for app in custom_apps:
        if not app.startswith('apps.') and app != 'authentication':
            print(f"   ✅ {app}")

def generate_summary():
    """Generar resumen final"""
    print_header("📊 RESUMEN DE VERIFICACIÓN")
    
    issues = []
    
    # Verificar problemas críticos
    if not os.getenv('EMAIL_HOST_PASSWORD'):
        issues.append("❌ Falta contraseña de email")
    
    if not os.getenv('CLOUDINARY_CLOUD_NAME'):
        issues.append("⚠️  Cloudinary no configurado (opcional)")
    
    if not os.getenv('GROQ_API_KEY'):
        issues.append("⚠️  Groq API no configurada (opcional)")
    
    if settings.DEBUG:
        issues.append("⚠️  DEBUG está activado (desactivar en producción)")
    
    if issues:
        print("\n🔍 Problemas detectados:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\n✅ No se detectaron problemas críticos")
    
    print("\n📋 Estado general:")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Django: {django.get_version()}")
    print(f"   Apps instaladas: {len(settings.INSTALLED_APPS)}")
    print(f"   Middleware: {len(settings.MIDDLEWARE)}")

def main():
    """Función principal"""
    print("=" * 70)
    print("  🚀 VERIFICACIÓN COMPLETA DEL SISTEMA EVALEXPO AI")
    print("=" * 70)
    
    try:
        verify_environment_variables()
        verify_email_configuration()
        verify_cloudinary_configuration()
        verify_database_configuration()
        verify_ai_configuration()
        verify_media_configuration()
        verify_security_configuration()
        verify_installed_apps()
        generate_summary()
        
        print("\n" + "=" * 70)
        print("  ✅ VERIFICACIÓN COMPLETADA")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante la verificación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
