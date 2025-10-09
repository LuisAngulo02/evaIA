# apps/presentaciones/management/commands/test_transcription.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.presentaciones.models import Presentation
from apps.ai_processor.services.ai_service import AIService
import logging

class Command(BaseCommand):
    help = 'Prueba la transcripción de una presentación específica'

    def add_arguments(self, parser):
        parser.add_argument('presentation_id', type=int, help='ID de la presentación a transcribir')

    def handle(self, *args, **options):
        presentation_id = options['presentation_id']
        
        try:
            # Obtener la presentación
            presentation = Presentation.objects.get(id=presentation_id)
            self.stdout.write(f"📹 Procesando presentación: {presentation.title}")
            self.stdout.write(f"👤 Estudiante: {presentation.student.username}")
            self.stdout.write(f"📁 Archivo: {presentation.video_file.name}")
            
            # Verificar que el archivo existe
            if not presentation.video_file or not presentation.video_file.path:
                self.stdout.write(
                    self.style.ERROR('❌ No se encontró el archivo de video')
                )
                return
            
            # Inicializar servicio de IA
            ai_service = AIService()
            
            # Procesar presentación
            self.stdout.write("🤖 Iniciando análisis con IA...")
            success = ai_service.analyze_presentation(presentation)
            
            if success:
                # Recargar desde DB para obtener datos actualizados
                presentation.refresh_from_db()
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Transcripción completada exitosamente!')
                )
                self.stdout.write(f"📝 Texto transcrito: {len(presentation.transcription_text or '')} caracteres")
                self.stdout.write(f"⏱️ Duración: {presentation.audio_duration or 0:.1f} segundos")
                self.stdout.write(f"📊 Puntuación IA: {presentation.ai_score or 0:.1f}/100")
                
                if presentation.transcription_text:
                    # Mostrar muestra del texto
                    sample = presentation.transcription_text[:200]
                    self.stdout.write(f"📄 Muestra del texto: '{sample}...'")
                
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Error durante la transcripción')
                )
                self.stdout.write(f"🔍 Error: {presentation.ai_feedback}")
                
        except Presentation.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ No se encontró presentación con ID {presentation_id}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error inesperado: {str(e)}')
            )