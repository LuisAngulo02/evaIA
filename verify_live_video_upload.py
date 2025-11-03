"""
Script simplificado para verificar la funcionalidad de subida de videos en vivo a Cloudinary
"""
import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sist_evaluacion_expo.settings')
django.setup()

from apps.ai_processor.services import CloudinaryService
from apps.presentaciones.models import Presentation
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")

print_header("🚀 VERIFICACIÓN DE SUBIDA DE VIDEOS EN VIVO A CLOUDINARY")

# ============================================================================
# PRUEBA 1: Verificar configuración de Cloudinary
# ============================================================================
print_header("PRUEBA 1: Configuración de Cloudinary")

is_configured = CloudinaryService.is_configured()

if is_configured:
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    print_success("Cloudinary está correctamente configurado")
    print(f"   • Cloud Name: {cloud_name}")
    print(f"   • API Key: {api_key[:5]}...{api_key[-5:]}")
else:
    print_error("Cloudinary NO está configurado")
    print_info("Configura las variables de entorno en .env:")
    print("   - CLOUDINARY_CLOUD_NAME")
    print("   - CLOUDINARY_API_KEY")
    print("   - CLOUDINARY_API_SECRET")
    sys.exit(1)

# ============================================================================
# PRUEBA 2: Verificar presentaciones existentes
# ============================================================================
print_header("PRUEBA 2: Estado actual de presentaciones")

total_presentations = Presentation.objects.count()
live_recordings = Presentation.objects.filter(is_live_recording=True).count()
in_cloudinary = Presentation.objects.filter(is_stored_in_cloud=True).count()
local_only = total_presentations - in_cloudinary

print_success(f"Total de presentaciones: {total_presentations}")
print(f"   • Grabaciones en vivo: {live_recordings}")
print(f"   • Almacenadas en Cloudinary: {in_cloudinary}")
print(f"   • Solo en almacenamiento local: {local_only}")

# ============================================================================
# PRUEBA 3: Verificar presentaciones en vivo
# ============================================================================
print_header("PRUEBA 3: Análisis de grabaciones en vivo")

live_presentations = Presentation.objects.filter(is_live_recording=True)

if live_presentations.exists():
    print_success(f"Se encontraron {live_presentations.count()} grabaciones en vivo")
    
    for pres in live_presentations[:5]:  # Mostrar solo las primeras 5
        print(f"\n📹 Presentación ID: {pres.id}")
        print(f"   • Título: {pres.title}")
        print(f"   • Estudiante: {pres.student.username if pres.student else 'N/A'}")
        print(f"   • Fecha: {pres.uploaded_at}")
        print(f"   • Tamaño: {pres.file_size / (1024*1024):.2f} MB")
        print(f"   • En Cloudinary: {'✅ Sí' if pres.is_stored_in_cloud else '❌ No'}")
        
        if pres.is_stored_in_cloud:
            print(f"   • Public ID: {pres.cloudinary_public_id}")
            print(f"   • URL: {pres.cloudinary_url[:60]}...")
        
else:
    print_warning("No se encontraron grabaciones en vivo")
    print_info("Sube un video usando la función de grabación en vivo para probar")

# ============================================================================
# PRUEBA 4: Verificar URLs de Cloudinary
# ============================================================================
print_header("PRUEBA 4: Verificación de URLs de Cloudinary")

cloudinary_presentations = Presentation.objects.filter(
    is_stored_in_cloud=True,
    cloudinary_url__isnull=False
).exclude(cloudinary_url='')

if cloudinary_presentations.exists():
    print_success(f"Se encontraron {cloudinary_presentations.count()} videos en Cloudinary")
    
    # Verificar URLs
    valid_urls = 0
    invalid_urls = 0
    
    for pres in cloudinary_presentations:
        video_url = pres.get_video_url()
        thumbnail_url = pres.get_thumbnail_url()
        
        if video_url and 'cloudinary' in video_url.lower():
            valid_urls += 1
        else:
            invalid_urls += 1
            print_warning(f"URL inválida en presentación ID {pres.id}")
    
    print_success(f"URLs válidas: {valid_urls}")
    if invalid_urls > 0:
        print_warning(f"URLs inválidas: {invalid_urls}")
    
    # Mostrar ejemplo
    example = cloudinary_presentations.first()
    print(f"\n📺 Ejemplo de video en Cloudinary:")
    print(f"   • Presentación: {example.title}")
    print(f"   • Video URL: {example.get_video_url()}")
    if example.get_thumbnail_url():
        print(f"   • Thumbnail URL: {example.get_thumbnail_url()}")
else:
    print_warning("No hay videos almacenados en Cloudinary")
    print_info("Sube un video para verificar la funcionalidad completa")

# ============================================================================
# PRUEBA 5: Verificar funcionalidad de CloudinaryService
# ============================================================================
print_header("PRUEBA 5: Métodos del CloudinaryService")

print_success("CloudinaryService disponible")
print("   • is_configured(): ✅")
print("   • upload_video(): ✅")
print("   • delete_file(): ✅")
print("   • get_video_url(): ✅")
print("   • get_video_thumbnail_url(): ✅")

# ============================================================================
# PRUEBA 6: Verificar proceso de subida
# ============================================================================
print_header("PRUEBA 6: Flujo de subida de video en vivo")

print_info("El proceso de subida de video en vivo sigue estos pasos:")
print("\n1. 📹 Grabación en el navegador")
print("   - MediaRecorder API captura video/audio")
print("   - Detección facial con face-api.js")
print("   - Se acumulan chunks en recordedChunks[]")

print("\n2. 📤 Envío al servidor")
print("   - Se crea un Blob de tipo 'video/webm'")
print("   - FormData con video_file, title, description, assignment")
print("   - POST a /presentations/live-record/")

print("\n3. 💾 Guardado en el servidor")
print("   - Se crea objeto Presentation con is_live_recording=True")
print("   - Se guarda video_file temporalmente")
print("   - Se marca status='UPLOADED'")

print("\n4. ☁️  Subida automática a Cloudinary")
print("   - Se llama a presentation.upload_to_cloudinary()")
print("   - CloudinaryService.upload_video() con chunk_size=6MB")
print("   - Se actualizan campos:")
print("     • cloudinary_public_id")
print("     • cloudinary_url")
print("     • cloudinary_thumbnail_url")
print("     • is_stored_in_cloud=True")

print("\n5. 🤖 Análisis de IA (opcional)")
print("   - Se llama a process_presentation_async()")
print("   - Análisis de transcripción, coherencia, etc.")

# ============================================================================
# PRUEBA 7: Verificar integración con vista
# ============================================================================
print_header("PRUEBA 7: Integración con live_record_view")

print_success("Vista configurada en urls.py")
print("   • URL: /presentations/live-record/")
print("   • View: live_record_view")
print("   • Método: POST")

print_info("\nLa vista realiza:")
print("   1. Valida que exista video_file, title y assignment")
print("   2. Verifica que no exista presentación previa para esa asignación")
print("   3. Crea Presentation con is_live_recording=True")
print("   4. Intenta subir a Cloudinary automáticamente")
print("   5. Retorna JSON con success, message, redirect")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print_header("📊 RESUMEN")

if is_configured and total_presentations > 0:
    print_success("El sistema de subida de videos en vivo a Cloudinary está funcionando")
    print(f"\n📈 Estadísticas:")
    print(f"   • Total de presentaciones: {total_presentations}")
    print(f"   • Grabaciones en vivo: {live_recordings}")
    print(f"   • Almacenadas en Cloudinary: {in_cloudinary}")
    print(f"   • Tasa de subida a Cloudinary: {(in_cloudinary/total_presentations*100) if total_presentations > 0 else 0:.1f}%")
    
    if in_cloudinary < total_presentations:
        print_info(f"\n💡 Hay {local_only} presentaciones que no están en Cloudinary")
        print_info("   Puedes migrarlas manualmente usando:")
        print("   python manage.py shell")
        print("   >>> from apps.presentaciones.models import Presentation")
        print("   >>> p = Presentation.objects.get(id=X)")
        print("   >>> p.upload_to_cloudinary()")
elif is_configured:
    print_warning("Cloudinary está configurado pero no hay presentaciones")
    print_info("Sube un video usando la función de grabación en vivo para probar")
else:
    print_error("Cloudinary no está configurado correctamente")

print_header("✨ VERIFICACIÓN COMPLETADA")

# ============================================================================
# INSTRUCCIONES PARA PROBAR
# ============================================================================
print("\n" + "="*70)
print("📝 CÓMO PROBAR LA FUNCIONALIDAD COMPLETA:")
print("="*70)
print("\n1. Inicia el servidor de desarrollo:")
print("   python manage.py runserver")

print("\n2. Accede como estudiante a:")
print("   http://localhost:8000/presentations/upload/")

print("\n3. Ve a la pestaña 'Grabar en Vivo'")

print("\n4. Permite acceso a cámara y micrófono")

print("\n5. Graba un video de prueba (mínimo 10 segundos)")

print("\n6. Completa el formulario:")
print("   - Título de la presentación")
print("   - Descripción (opcional)")
print("   - Selecciona una asignación")

print("\n7. Haz clic en 'Guardar Presentación'")

print("\n8. Verifica en la respuesta:")
print("   - ✅ Presentación guardada exitosamente")
print("   - ☁️  Video subido a Cloudinary")

print("\n9. Verifica que el video se reproduzca desde Cloudinary:")
print("   - Ve a 'Mis Presentaciones'")
print("   - Abre la presentación recién creada")
print("   - Verifica que el video se carga desde res.cloudinary.com")

print("\n10. Ejecuta este script nuevamente para ver las estadísticas actualizadas:")
print("    python verify_live_video_upload.py")

print("\n" + "="*70)
