"""
Script para verificar la configuración y funcionamiento de Cloudinary
"""
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sist_evaluacion_expo.settings')
django.setup()

from apps.ai_processor.services import CloudinaryService
from apps.presentaciones.models import Presentation
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("="*60)
print("VERIFICACIÓN DE CLOUDINARY")
print("="*60)

# 1. Verificar configuración
print("\n1️⃣ Verificando configuración...")
is_configured = CloudinaryService.is_configured()

if is_configured:
    print("✅ Cloudinary está configurado correctamente")
    print(f"   Cloud Name: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
    print(f"   API Key: {os.getenv('CLOUDINARY_API_KEY')[:5]}...{os.getenv('CLOUDINARY_API_KEY')[-5:]}")
else:
    print("❌ Cloudinary NO está configurado")
    print("   Verifica las variables de entorno:")
    print("   - CLOUDINARY_CLOUD_NAME")
    print("   - CLOUDINARY_API_KEY")
    print("   - CLOUDINARY_API_SECRET")
    exit(1)

# 2. Verificar presentaciones existentes
print("\n2️⃣ Verificando presentaciones existentes...")
presentations = Presentation.objects.all()
total = presentations.count()
in_cloud = presentations.filter(is_stored_in_cloud=True).count()
local = total - in_cloud

print(f"   Total de presentaciones: {total}")
print(f"   En Cloudinary: {in_cloud}")
print(f"   En local: {local}")

# 3. Verificar presentaciones con video
print("\n3️⃣ Verificando presentaciones con archivos de video...")
with_video = presentations.exclude(video_file='').exclude(video_file=None)
print(f"   Presentaciones con video: {with_video.count()}")

if with_video.exists():
    print("\n   Detalles de últimas 5 presentaciones:")
    for p in with_video[:5]:
        print(f"\n   📹 {p.title}")
        print(f"      Estudiante: {p.student.username}")
        print(f"      Estado: {p.status}")
        print(f"      En Cloudinary: {'✅ Sí' if p.is_stored_in_cloud else '❌ No'}")
        
        if p.is_stored_in_cloud:
            print(f"      Public ID: {p.cloudinary_public_id}")
            print(f"      URL: {p.cloudinary_url[:60]}...")
        else:
            print(f"      Archivo local: {p.video_file.name if p.video_file else 'N/A'}")
            
            # Verificar si el archivo existe
            if p.video_file:
                try:
                    file_exists = os.path.exists(p.video_file.path)
                    file_size = os.path.getsize(p.video_file.path) if file_exists else 0
                    print(f"      Archivo existe: {'✅ Sí' if file_exists else '❌ No'}")
                    if file_exists:
                        print(f"      Tamaño: {file_size / (1024*1024):.2f} MB")
                except:
                    print(f"      Archivo existe: ❌ Error al verificar")

# 4. Probar conexión con Cloudinary API
print("\n4️⃣ Probando conexión con Cloudinary API...")
try:
    import cloudinary
    import cloudinary.api
    
    # Intentar listar recursos
    result = cloudinary.api.resources(
        resource_type='video',
        max_results=1
    )
    print("✅ Conexión exitosa con Cloudinary API")
    print(f"   Total de videos en Cloudinary: {result.get('total_count', 0)}")
    
except Exception as e:
    print(f"❌ Error conectando con Cloudinary API: {e}")

# 5. Resumen
print("\n" + "="*60)
print("RESUMEN")
print("="*60)

if is_configured:
    print("✅ Configuración: OK")
else:
    print("❌ Configuración: FALTA")

if total > 0:
    print(f"📊 Presentaciones: {total} ({in_cloud} en cloud, {local} locales)")
else:
    print("⚠️  No hay presentaciones para verificar")

print("\n💡 RECOMENDACIONES:")
if local > 0:
    print(f"   - Tienes {local} presentación(es) en almacenamiento local")
    print("   - Puedes migrarlas a Cloudinary con: python manage.py migrate_to_cloudinary")

print("\n✨ Para subir un nuevo video:")
print("   1. Accede como estudiante")
print("   2. Ve a 'Subir Presentación'")
print("   3. Selecciona asignación, título y video")
print("   4. El video se subirá automáticamente a Cloudinary")

print("\n" + "="*60)
