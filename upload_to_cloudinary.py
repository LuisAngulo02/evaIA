"""
Script para probar la subida de un video existente a Cloudinary
Simula el proceso de grabación en vivo
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

def main():
    print("="*70)
    print("  🧪 PRUEBA PRÁCTICA DE SUBIDA A CLOUDINARY")
    print("="*70)
    
    # Verificar configuración
    if not CloudinaryService.is_configured():
        print("\n❌ Cloudinary no está configurado")
        print("Configura las variables de entorno en .env")
        return
    
    print("\n✅ Cloudinary configurado correctamente\n")
    
    # Buscar presentaciones que NO están en Cloudinary
    local_only = Presentation.objects.filter(
        is_stored_in_cloud=False,
        video_file__isnull=False
    ).exclude(video_file='')
    
    if not local_only.exists():
        print("ℹ️  No hay presentaciones locales para migrar")
        print("Todas las presentaciones ya están en Cloudinary o no tienen video")
        return
    
    print(f"📋 Presentaciones disponibles para subir ({local_only.count()}):\n")
    
    # Mostrar lista de presentaciones
    for i, pres in enumerate(local_only[:10], 1):
        size_mb = pres.file_size / (1024*1024) if pres.file_size else 0
        print(f"{i}. ID: {pres.id} - {pres.title[:50]}")
        print(f"   Estudiante: {pres.student.username if pres.student else 'N/A'}")
        print(f"   Tamaño: {size_mb:.2f} MB")
        print(f"   Es grabación en vivo: {'✅ Sí' if pres.is_live_recording else '❌ No'}")
        print()
    
    if local_only.count() > 10:
        print(f"   ... y {local_only.count() - 10} más\n")
    
    # Preguntar qué hacer
    print("="*70)
    print("Opciones:")
    print("1. Subir una presentación específica por ID")
    print("2. Subir todas las grabaciones en vivo")
    print("3. Subir las primeras 5 presentaciones")
    print("4. Salir")
    print("="*70)
    
    choice = input("\nSelecciona una opción (1-4): ").strip()
    
    if choice == '1':
        # Subir una presentación específica
        pres_id = input("Ingresa el ID de la presentación: ").strip()
        try:
            pres = Presentation.objects.get(id=int(pres_id))
            upload_single_presentation(pres)
        except Presentation.DoesNotExist:
            print(f"❌ No se encontró la presentación con ID {pres_id}")
        except ValueError:
            print("❌ ID inválido")
    
    elif choice == '2':
        # Subir todas las grabaciones en vivo
        live_recordings = local_only.filter(is_live_recording=True)
        if live_recordings.exists():
            confirm = input(f"¿Subir {live_recordings.count()} grabaciones en vivo? (s/n): ").lower()
            if confirm == 's':
                upload_multiple_presentations(live_recordings)
        else:
            print("ℹ️  No hay grabaciones en vivo sin subir")
    
    elif choice == '3':
        # Subir las primeras 5
        presentations = local_only[:5]
        confirm = input(f"¿Subir las primeras {presentations.count()} presentaciones? (s/n): ").lower()
        if confirm == 's':
            upload_multiple_presentations(presentations)
    
    elif choice == '4':
        print("👋 Saliendo...")
    
    else:
        print("❌ Opción inválida")

def upload_single_presentation(presentation):
    """Subir una presentación a Cloudinary"""
    print("\n" + "="*70)
    print(f"📤 Subiendo presentación: {presentation.title}")
    print("="*70)
    
    if not presentation.video_file or not os.path.exists(presentation.video_file.path):
        print("❌ El archivo de video no existe")
        return
    
    print(f"\nℹ️  Información de la presentación:")
    print(f"   • ID: {presentation.id}")
    print(f"   • Título: {presentation.title}")
    print(f"   • Estudiante: {presentation.student.username if presentation.student else 'N/A'}")
    print(f"   • Tamaño: {presentation.file_size / (1024*1024):.2f} MB")
    print(f"   • Es grabación en vivo: {'Sí' if presentation.is_live_recording else 'No'}")
    print(f"   • Ruta: {presentation.video_file.path}")
    
    print("\n⏳ Iniciando subida a Cloudinary...")
    
    try:
        result = presentation.upload_to_cloudinary()
        
        if result:
            print("\n✅ ¡Subida exitosa!")
            print(f"\n📊 Detalles:")
            print(f"   • Public ID: {presentation.cloudinary_public_id}")
            print(f"   • URL: {presentation.cloudinary_url}")
            
            if presentation.cloudinary_thumbnail_url:
                print(f"   • Thumbnail: {presentation.cloudinary_thumbnail_url}")
            
            print(f"\n🔗 Puedes ver el video en:")
            print(f"   {presentation.get_video_url()}")
            
        else:
            print("\n❌ Falló la subida a Cloudinary")
            print("Revisa los logs para más detalles")
    
    except Exception as e:
        print(f"\n❌ Error durante la subida: {e}")
        import traceback
        traceback.print_exc()

def upload_multiple_presentations(presentations):
    """Subir múltiples presentaciones a Cloudinary"""
    total = presentations.count()
    successful = 0
    failed = 0
    
    print("\n" + "="*70)
    print(f"📤 Subiendo {total} presentaciones a Cloudinary")
    print("="*70)
    
    for i, pres in enumerate(presentations, 1):
        print(f"\n[{i}/{total}] Procesando: {pres.title[:50]}")
        
        if not pres.video_file or not os.path.exists(pres.video_file.path):
            print(f"   ⚠️  Archivo de video no existe, omitiendo...")
            failed += 1
            continue
        
        try:
            result = pres.upload_to_cloudinary()
            
            if result:
                print(f"   ✅ Subido exitosamente")
                print(f"   • Public ID: {pres.cloudinary_public_id}")
                successful += 1
            else:
                print(f"   ❌ Falló la subida")
                failed += 1
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            failed += 1
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE SUBIDA")
    print("="*70)
    print(f"Total procesadas: {total}")
    print(f"✅ Exitosas: {successful}")
    print(f"❌ Fallidas: {failed}")
    print(f"📈 Tasa de éxito: {(successful/total*100) if total > 0 else 0:.1f}%")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
