"""
Comando de gestión para migrar videos existentes a Cloudinary
"""
from django.core.management.base import BaseCommand, CommandError
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Migra videos existentes a Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Migrar todos los videos, no solo los no migrados',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular la migración sin hacer cambios reales',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limitar el número de videos a migrar',
        )

    def handle(self, *args, **options):
        # Importar aquí para evitar imports pesados al inicio
        from apps.presentaciones.models import Presentation
        from apps.ai_processor.services.cloudinary_service import CloudinaryService
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('  📤 MIGRACIÓN DE VIDEOS A CLOUDINARY'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        # Verificar configuración de Cloudinary
        if not CloudinaryService.is_configured():
            raise CommandError('❌ Cloudinary no está configurado. Verifica el archivo .env')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Cloudinary está configurado correctamente'))
        
        # Verificar conexión
        if not CloudinaryService.test_connection():
            raise CommandError('❌ No se pudo conectar con Cloudinary')
        
        self.stdout.write(self.style.SUCCESS('✅ Conexión con Cloudinary exitosa\n'))
        
        # Filtrar presentaciones
        if options['all']:
            presentations = Presentation.objects.filter(video_file__isnull=False)
            self.stdout.write(f"📊 Migrando TODOS los videos ({presentations.count()} encontrados)")
        else:
            presentations = Presentation.objects.filter(
                video_file__isnull=False,
                is_stored_in_cloud=False
            )
            self.stdout.write(f"📊 Migrando videos NO migrados ({presentations.count()} encontrados)")
        
        # Aplicar límite si se especificó
        if options['limit']:
            presentations = presentations[:options['limit']]
            self.stdout.write(f"   Limitado a {options['limit']} videos\n")
        
        if not presentations.exists():
            self.stdout.write(self.style.WARNING('⚠️  No hay videos para migrar'))
            return
        
        # Estadísticas
        total = presentations.count()
        migrated = 0
        failed = 0
        skipped = 0
        
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write('  🔄 INICIANDO MIGRACIÓN')
        self.stdout.write('=' * 70 + '\n')
        
        for i, presentation in enumerate(presentations, 1):
            self.stdout.write(f"\n[{i}/{total}] Procesando: {presentation.title}")
            self.stdout.write(f"   Estudiante: {presentation.student.get_full_name() or presentation.student.username}")
            self.stdout.write(f"   ID: {presentation.id}")
            
            # Verificar si ya está en Cloudinary
            if presentation.is_stored_in_cloud and not options['all']:
                self.stdout.write(self.style.WARNING('   ⏭️  Ya está en Cloudinary, omitiendo...'))
                skipped += 1
                continue
            
            # Verificar que el archivo existe
            try:
                if not presentation.video_file.path:
                    self.stdout.write(self.style.ERROR('   ❌ No se encontró la ruta del archivo'))
                    failed += 1
                    continue
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Error accediendo al archivo: {e}'))
                failed += 1
                continue
            
            if options['dry_run']:
                self.stdout.write(self.style.WARNING('   🧪 DRY RUN: No se realizarán cambios'))
                migrated += 1
                continue
            
            # Migrar a Cloudinary
            try:
                result = presentation.upload_to_cloudinary()
                
                if result:
                    self.stdout.write(self.style.SUCCESS('   ✅ Migrado exitosamente'))
                    self.stdout.write(f'      Public ID: {presentation.cloudinary_public_id}')
                    self.stdout.write(f'      URL: {presentation.cloudinary_url[:80]}...')
                    migrated += 1
                else:
                    self.stdout.write(self.style.ERROR('   ❌ Error en la migración'))
                    failed += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Error: {e}'))
                failed += 1
        
        # Resumen final
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write('  📊 RESUMEN DE MIGRACIÓN')
        self.stdout.write('=' * 70)
        self.stdout.write(f'\n📝 Total de videos procesados: {total}')
        self.stdout.write(self.style.SUCCESS(f'✅ Migrados exitosamente: {migrated}'))
        if skipped > 0:
            self.stdout.write(self.style.WARNING(f'⏭️  Omitidos (ya migrados): {skipped}'))
        if failed > 0:
            self.stdout.write(self.style.ERROR(f'❌ Fallidos: {failed}'))
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING('\n🧪 NOTA: Esta fue una ejecución de prueba (--dry-run)'))
            self.stdout.write('   No se realizaron cambios reales')
        
        self.stdout.write('\n' + '=' * 70)
        
        if migrated > 0 and not options['dry_run']:
            self.stdout.write(self.style.SUCCESS('✅ MIGRACIÓN COMPLETADA'))
        elif failed == total:
            self.stdout.write(self.style.ERROR('❌ MIGRACIÓN FALLIDA'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  MIGRACIÓN COMPLETADA CON ADVERTENCIAS'))
        
        self.stdout.write('=' * 70 + '\n')
