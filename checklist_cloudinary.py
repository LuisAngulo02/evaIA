"""
✅ CHECKLIST DE VERIFICACIÓN - SUBIDA DE VIDEOS EN VIVO A CLOUDINARY
============================================================================

Este checklist te permite verificar paso a paso que la funcionalidad de 
subida de videos en vivo a Cloudinary está funcionando correctamente.

Ejecuta este script para obtener un reporte detallado.
"""

import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sist_evaluacion_expo.settings')
django.setup()

from apps.ai_processor.services import CloudinaryService
from apps.presentaciones.models import Presentation, Assignment
from django.contrib.auth.models import User
import logging

logging.basicConfig(level=logging.WARNING)

def check(condition, success_msg, fail_msg):
    """Helper para mostrar resultados de verificación"""
    if condition:
        print(f"✅ {success_msg}")
        return True
    else:
        print(f"❌ {fail_msg}")
        return False

def info(message):
    """Mostrar información"""
    print(f"ℹ️  {message}")

def section(title):
    """Mostrar sección"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

# ============================================================================
# CHECKLIST DE VERIFICACIÓN
# ============================================================================

print("\n" + "="*70)
print("  ✅ CHECKLIST DE VERIFICACIÓN - VIDEOS EN VIVO A CLOUDINARY")
print("="*70)

results = {
    'total': 0,
    'passed': 0,
    'failed': 0
}

# ============================================================================
section("1. CONFIGURACIÓN DE CLOUDINARY")
results['total'] += 1

is_configured = CloudinaryService.is_configured()
cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')

if check(
    is_configured and cloud_name and api_key and api_secret,
    "Cloudinary está correctamente configurado",
    "Cloudinary NO está configurado - falta configuración en .env"
):
    results['passed'] += 1
    info(f"Cloud Name: {cloud_name}")
    info(f"API Key: {api_key[:5]}...{api_key[-5:]}")
else:
    results['failed'] += 1
    info("Agrega estas variables a tu archivo .env:")
    info("  CLOUDINARY_CLOUD_NAME=tu_cloud_name")
    info("  CLOUDINARY_API_KEY=tu_api_key")
    info("  CLOUDINARY_API_SECRET=tu_api_secret")

# ============================================================================
section("2. SERVICIO CLOUDINARY")
results['total'] += 1

try:
    # Verificar que los métodos existen
    has_methods = all([
        hasattr(CloudinaryService, 'is_configured'),
        hasattr(CloudinaryService, 'upload_video'),
        hasattr(CloudinaryService, 'delete_file'),
        hasattr(CloudinaryService, 'get_video_url'),
        hasattr(CloudinaryService, 'get_video_thumbnail_url'),
    ])
    
    if check(
        has_methods,
        "CloudinaryService tiene todos los métodos requeridos",
        "CloudinaryService está incompleto"
    ):
        results['passed'] += 1
    else:
        results['failed'] += 1
        
except Exception as e:
    check(False, "", f"Error verificando CloudinaryService: {e}")
    results['failed'] += 1

# ============================================================================
section("3. MODELO PRESENTATION")
results['total'] += 1

try:
    # Verificar que el modelo tiene los campos necesarios
    has_fields = all([
        hasattr(Presentation, 'is_live_recording'),
        hasattr(Presentation, 'cloudinary_public_id'),
        hasattr(Presentation, 'cloudinary_url'),
        hasattr(Presentation, 'cloudinary_thumbnail_url'),
        hasattr(Presentation, 'is_stored_in_cloud'),
        hasattr(Presentation, 'upload_to_cloudinary'),
        hasattr(Presentation, 'delete_from_cloudinary'),
        hasattr(Presentation, 'get_video_url'),
        hasattr(Presentation, 'get_thumbnail_url'),
    ])
    
    if check(
        has_fields,
        "Modelo Presentation tiene todos los campos y métodos necesarios",
        "Modelo Presentation está incompleto"
    ):
        results['passed'] += 1
    else:
        results['failed'] += 1
        
except Exception as e:
    check(False, "", f"Error verificando modelo Presentation: {e}")
    results['failed'] += 1

# ============================================================================
section("4. VISTA live_record_view")
results['total'] += 1

try:
    from apps.presentaciones import views
    
    has_view = hasattr(views, 'live_record_view')
    
    if check(
        has_view,
        "Vista live_record_view existe y está disponible",
        "Vista live_record_view NO encontrada"
    ):
        results['passed'] += 1
    else:
        results['failed'] += 1
        
except Exception as e:
    check(False, "", f"Error verificando vista: {e}")
    results['failed'] += 1

# ============================================================================
section("5. CONFIGURACIÓN DE URLs")
results['total'] += 1

try:
    from django.urls import resolve, reverse
    
    # Intentar resolver la URL
    url = reverse('presentations:live_record')
    resolved = resolve(url)
    
    if check(
        resolved.url_name == 'live_record',
        f"URL configurada correctamente: {url}",
        "URL live_record NO configurada"
    ):
        results['passed'] += 1
    else:
        results['failed'] += 1
        
except Exception as e:
    check(False, "", f"Error verificando URLs: {e}")
    results['failed'] += 1

# ============================================================================
section("6. TEMPLATE presentations_upload.html")
results['total'] += 1

template_path = os.path.join(
    os.path.dirname(__file__),
    'templates', 'presentations', 'presentations_upload.html'
)

has_template = os.path.exists(template_path)

if check(
    has_template,
    f"Template encontrado: {template_path}",
    "Template presentations_upload.html NO encontrado"
):
    results['passed'] += 1
    
    # Verificar que tiene las funciones JavaScript necesarias
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        js_functions = [
            'startRecording',
            'stopRecording',
            'mediaRecorder',
            'recordedChunks',
            'liveRecordForm'
        ]
        
        has_all_js = all(func in content for func in js_functions)
        
        if has_all_js:
            info("Template tiene todas las funciones JavaScript necesarias")
        else:
            info("⚠️  Algunas funciones JavaScript podrían faltar")
            
    except Exception as e:
        info(f"⚠️  No se pudo verificar el contenido del template: {e}")
else:
    results['failed'] += 1

# ============================================================================
section("7. DATOS DE PRUEBA")
results['total'] += 1

# Verificar que hay usuarios estudiantes
students = User.objects.filter(groups__name='Estudiante')
has_students = students.exists()

if check(
    has_students,
    f"Hay {students.count()} estudiantes en el sistema",
    "NO hay estudiantes en el sistema"
):
    results['passed'] += 1
else:
    results['failed'] += 1
    info("Crea al menos un usuario estudiante para probar")

# ============================================================================
section("8. ASIGNACIONES DISPONIBLES")
results['total'] += 1

from django.utils import timezone

active_assignments = Assignment.objects.filter(
    is_active=True,
    due_date__gte=timezone.now()
)

has_assignments = active_assignments.exists()

if check(
    has_assignments,
    f"Hay {active_assignments.count()} asignaciones activas disponibles",
    "NO hay asignaciones activas"
):
    results['passed'] += 1
else:
    results['failed'] += 1
    info("Crea al menos una asignación activa para probar")

# ============================================================================
section("9. PRESENTACIONES EXISTENTES")
results['total'] += 1

total_presentations = Presentation.objects.count()
live_recordings = Presentation.objects.filter(is_live_recording=True).count()
in_cloudinary = Presentation.objects.filter(is_stored_in_cloud=True).count()

info(f"Total de presentaciones: {total_presentations}")
info(f"Grabaciones en vivo: {live_recordings}")
info(f"Almacenadas en Cloudinary: {in_cloudinary}")

if check(
    True,  # Siempre pasa, solo es informativo
    "Estadísticas de presentaciones revisadas",
    ""
):
    results['passed'] += 1

# ============================================================================
section("10. FUNCIONALIDAD DE SUBIDA")
results['total'] += 1

# Verificar si hay presentaciones en vivo en Cloudinary
live_in_cloudinary = Presentation.objects.filter(
    is_live_recording=True,
    is_stored_in_cloud=True
).exists()

if check(
    live_in_cloudinary,
    "Hay grabaciones en vivo subidas a Cloudinary ✨",
    "Aún no hay grabaciones en vivo en Cloudinary (prueba subiendo una)"
):
    results['passed'] += 1
    
    # Mostrar ejemplo
    example = Presentation.objects.filter(
        is_live_recording=True,
        is_stored_in_cloud=True
    ).first()
    
    if example:
        info(f"\n📺 Ejemplo: '{example.title}'")
        info(f"   URL: {example.cloudinary_url[:60]}...")
else:
    results['failed'] += 1
    info("Esto es esperado si acabas de configurar Cloudinary")
    info("Graba un video en vivo para verificar que funciona")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
section("📊 RESUMEN DE VERIFICACIÓN")

print(f"Total de verificaciones: {results['total']}")
print(f"✅ Pasadas: {results['passed']}")
print(f"❌ Fallidas: {results['failed']}")

percentage = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
print(f"\n📈 Porcentaje de éxito: {percentage:.1f}%\n")

if results['failed'] == 0:
    print("🎉 ¡PERFECTO! Todas las verificaciones pasaron exitosamente")
    print("✨ El sistema está listo para grabar y subir videos en vivo a Cloudinary")
elif results['failed'] <= 2:
    print("✅ El sistema está mayormente configurado")
    print("⚠️  Revisa las verificaciones fallidas arriba")
else:
    print("⚠️  Hay varios problemas que necesitan atención")
    print("📝 Revisa la documentación en docs/VERIFICACION_VIDEO_CLOUDINARY.md")

# ============================================================================
# INSTRUCCIONES DE PRUEBA
# ============================================================================
section("🧪 INSTRUCCIONES PARA PROBAR")

print("Para probar la funcionalidad completa:")
print()
print("1. Inicia el servidor:")
print("   python manage.py runserver")
print()
print("2. Accede como estudiante:")
print("   http://localhost:8000/presentations/upload/?tab=record")
print()
print("3. Permite acceso a cámara y micrófono")
print()
print("4. Graba un video de prueba (10-30 segundos)")
print()
print("5. Completa el formulario y guarda")
print()
print("6. Verifica que aparezca el mensaje:")
print("   ✅ Presentación guardada exitosamente")
print("   ☁️  Video subido a Cloudinary")
print()
print("7. Ve a 'Mis Presentaciones' y reproduce el video")
print()
print("8. Verifica en las herramientas de desarrollo (F12)")
print("   que la URL del video sea de res.cloudinary.com")
print()

print("="*70)
print("Para más información, consulta:")
print("  📄 docs/VERIFICACION_VIDEO_CLOUDINARY.md")
print("="*70)
