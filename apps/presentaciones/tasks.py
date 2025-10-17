# apps/presentaciones/tasks.py
"""
Tareas asíncronas para procesamiento de presentaciones
Usando threading para evitar dependencia de Celery
"""
import threading
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

def process_presentation_async(presentation_id):
    """
    Procesa una presentación en segundo plano usando threading
    Actualiza el progreso en cache para mostrar en UI
    """
    from .models import Presentation
    from apps.ai_processor.services.ai_service import AIService
    
    def _process():
        try:
            presentation = Presentation.objects.get(id=presentation_id)
            
            # Actualizar progreso: 0%
            cache.set(f'presentation_progress_{presentation_id}', {
                'status': 'PROCESSING',
                'progress': 0,
                'step': 'Iniciando análisis...'
            }, timeout=3600)
            
            # Iniciar análisis
            ai_service = AIService()
            
            # Actualizar progreso: 10%
            cache.set(f'presentation_progress_{presentation_id}', {
                'status': 'PROCESSING',
                'progress': 10,
                'step': 'Analizando autenticidad (liveness)...'
            }, timeout=3600)
            
            # El análisis completo se hace en AIService
            # Podemos monitorear el progreso desde ahí
            success = ai_service.analyze_presentation(presentation)
            
            if success:
                # Actualizar progreso: 100%
                cache.set(f'presentation_progress_{presentation_id}', {
                    'status': 'ANALYZED',
                    'progress': 100,
                    'step': 'Análisis completado ✅'
                }, timeout=3600)
                
                logger.info(f"✅ Presentación {presentation_id} procesada exitosamente")
            else:
                # Recargar desde DB para ver error
                presentation.refresh_from_db()
                error_msg = presentation.ai_feedback if presentation.status == 'FAILED' else 'Error desconocido'
                
                cache.set(f'presentation_progress_{presentation_id}', {
                    'status': 'FAILED',
                    'progress': 0,
                    'step': f'Error: {error_msg[:50]}...'
                }, timeout=3600)
                
                logger.error(f"❌ Error al procesar presentación {presentation_id}: {error_msg}")
        
        except Exception as e:
            logger.error(f"❌ Error crítico en tarea asíncrona: {str(e)}", exc_info=True)
            cache.set(f'presentation_progress_{presentation_id}', {
                'status': 'FAILED',
                'progress': 0,
                'step': f'Error: {str(e)[:50]}...'
            }, timeout=3600)
            
            # Actualizar presentación en DB
            try:
                presentation = Presentation.objects.get(id=presentation_id)
                presentation.status = 'FAILED'
                presentation.ai_feedback = f"Error en análisis: {str(e)}"
                presentation.save()
            except:
                pass
    
    # Ejecutar en thread separado
    thread = threading.Thread(target=_process, daemon=True)
    thread.start()
    
    logger.info(f"🚀 Tarea asíncrona iniciada para presentación {presentation_id}")
    
    return True


def update_progress(presentation_id, progress, step):
    """
    Helper para actualizar el progreso desde AIService
    """
    cache.set(f'presentation_progress_{presentation_id}', {
        'status': 'PROCESSING',
        'progress': progress,
        'step': step
    }, timeout=3600)
