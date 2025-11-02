"""
Comando para generar miniaturas de videos que no las tienen
"""
from django.core.management.base import BaseCommand
from apps.presentaciones.models import Presentation
import os
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Genera miniaturas para videos que no las tienen'

    def handle(self, *args, **options):
        presentations = Presentation.objects.filter(
            video_file__isnull=False
        ).exclude(
            video_file=''
        )
        
        total = presentations.count()
        self.stdout.write(f'Encontradas {total} presentaciones con video')
        
        generated = 0
        skipped = 0
        errors = 0
        
        for presentation in presentations:
            # Verificar si ya tiene thumbnail
            has_thumbnail = (
                presentation.cloudinary_thumbnail_url or 
                (presentation.video_thumbnail and presentation.video_thumbnail.name)
            )
            
            if has_thumbnail:
                skipped += 1
                continue
            
            try:
                # Intentar generar thumbnail
                self.stdout.write(f'Generando thumbnail para: {presentation.title}')
                
                # Verificar que el archivo existe
                if not os.path.exists(presentation.video_file.path):
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠️ Archivo no existe: {presentation.video_file.path}'
                        )
                    )
                    errors += 1
                    continue
                
                # Generar thumbnail usando moviepy
                try:
                    from moviepy.editor import VideoFileClip
                    from django.core.files import File
                    import tempfile
                    
                    # Cargar video
                    clip = VideoFileClip(presentation.video_file.path)
                    
                    # Obtener frame del segundo 1 (o 0 si el video es muy corto)
                    time_position = min(1.0, clip.duration / 2)
                    frame = clip.get_frame(time_position)
                    
                    # Convertir a imagen PIL
                    img = Image.fromarray(frame)
                    
                    # Redimensionar a tamaño de thumbnail
                    img.thumbnail((320, 240), Image.Resampling.LANCZOS)
                    
                    # Guardar en archivo temporal
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                        img.save(tmp_file.name, 'JPEG', quality=85)
                        tmp_path = tmp_file.name
                    
                    # Guardar en el modelo
                    with open(tmp_path, 'rb') as f:
                        filename = f'thumb_{presentation.id}.jpg'
                        presentation.video_thumbnail.save(
                            filename,
                            File(f),
                            save=True
                        )
                    
                    # Limpiar
                    clip.close()
                    os.remove(tmp_path)
                    
                    generated += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✅ Thumbnail generado exitosamente'
                        )
                    )
                    
                except ImportError:
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠️ moviepy no está instalado. Instalalo con: pip install moviepy'
                        )
                    )
                    errors += 1
                    break
                    
            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'  ❌ Error generando thumbnail: {str(e)}'
                    )
                )
        
        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'✅ Generados: {generated}'))
        self.stdout.write(self.style.WARNING(f'⏭️  Omitidos (ya tenían): {skipped}'))
        self.stdout.write(self.style.ERROR(f'❌ Errores: {errors}'))
        self.stdout.write('='*50)
