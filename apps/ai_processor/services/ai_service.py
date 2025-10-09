# apps/ai_processor/services/ai_service.py
import logging
from django.utils import timezone
from .transcription_service import TranscriptionService

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.transcription_service = TranscriptionService()
    
    def analyze_presentation(self, presentation):
        """
        Análisis completo de una presentación
        """
        try:
            # Actualizar estado a procesando
            presentation.status = 'PROCESSING'
            presentation.save()
            
            # 1. Transcripción automática
            logger.info(f"Iniciando transcripción para presentación {presentation.id}")
            
            video_path = presentation.video_file.path
            transcription_result = self.transcription_service.transcribe_video(video_path)
            
            # Guardar transcripción en la base de datos
            presentation.transcription_text = transcription_result['full_text']
            presentation.transcription_segments = transcription_result['segments']
            presentation.audio_duration = transcription_result['duration']
            presentation.transcription_completed_at = timezone.now()
            
            # 2. Análisis de coherencia (básico por ahora)
            coherence_score = self.analyze_coherence(
                transcription_result['full_text'], 
                presentation.assignment.description
            )
            
            # 3. Análisis de participación (simulado por ahora)
            participation_data = self.analyze_participation(video_path)
            
            # Calcular puntuación IA
            presentation.ai_score = (coherence_score + participation_data['score']) / 2
            
            # Generar feedback
            presentation.ai_feedback = self.generate_feedback(
                transcription_result,
                coherence_score,
                participation_data
            )
            
            # Actualizar estado
            presentation.status = 'ANALYZED'
            presentation.analyzed_at = timezone.now()
            presentation.save()
            
            logger.info(f"Análisis completado para presentación {presentation.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error en análisis IA: {str(e)}")
            presentation.ai_feedback = f"Error en análisis: {str(e)}"
            presentation.status = 'FAILED'
            presentation.save()
            return False
    
    def analyze_coherence(self, transcription, topic_description):
        """
        Análisis básico de coherencia temática
        """
        if not transcription or not topic_description:
            return 0
        
        # Convertir a minúsculas y dividir en palabras
        topic_words = set(topic_description.lower().split())
        transcription_words = set(transcription.lower().split())
        
        # Calcular intersección
        common_words = topic_words.intersection(transcription_words)
        
        if len(topic_words) == 0:
            return 0
        
        # Calcular porcentaje de coincidencia
        coherence_score = (len(common_words) / len(topic_words)) * 100
        
        # Limitar a 100%
        return min(100, coherence_score)
    
    def analyze_participation(self, video_path):
        """
        Análisis básico de participación (implementaremos detección real después)
        """
        # Por ahora, retornamos datos simulados
        return {
            'score': 85.0,
            'participants': [
                {'id': 'Persona 1', 'percentage': 60.0, 'time': '3.2 min'},
                {'id': 'Persona 2', 'percentage': 40.0, 'time': '2.1 min'}
            ]
        }
    
    def generate_feedback(self, transcription_result, coherence_score, participation_data):
        """
        Genera feedback automático basado en el análisis
        """
        feedback = f"""
🤖 **Análisis Automático Completado**

📝 **Transcripción:**
- Texto transcrito: {len(transcription_result['full_text'])} caracteres
- Duración total: {transcription_result['duration']:.1f} segundos
- Segmentos identificados: {len(transcription_result['segments'])}

 **Coherencia Temática: {coherence_score:.1f}/100**
{" Excelente coherencia con el tema" if coherence_score >= 80 else
 " Coherencia moderada con el tema" if coherence_score >= 60 else
 " Baja coherencia con el tema asignado"}

 **Participación de Integrantes:**
"""
        
        for participant in participation_data['participants']:
            feedback += f"- {participant['id']}: {participant['percentage']:.1f}% ({participant['time']})\n"
        
        feedback += f"""
**Puntuación de Participación: {participation_data['score']:.1f}/100**

 **Recomendaciones:**
"""
        
        # Generar recomendaciones basadas en los resultados
        if coherence_score < 70:
            feedback += "- Enfócate más en el tema asignado durante la presentación\n"
        
        if participation_data['score'] < 80:
            feedback += "- Busca una distribución más equitativa del tiempo entre integrantes\n"
        
        if transcription_result['duration'] < 60:
            feedback += "- Considera extender la duración de la presentación\n"
        elif transcription_result['duration'] > 600:
            feedback += "- La presentación es muy larga, intenta ser más conciso\n"
        
        return feedback