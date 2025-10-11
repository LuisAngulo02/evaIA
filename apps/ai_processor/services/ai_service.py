# apps/ai_processor/services/ai_service.py
import logging
from django.utils import timezone
from .transcription_service import TranscriptionService
from .face_detection_service import FaceDetectionService
from .liveness_detection_service import LivenessDetectionService

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.transcription_service = TranscriptionService()
        self.face_detection_service = FaceDetectionService(
            tolerance=0.6,  # Sensibilidad de comparación de rostros
            sample_rate=30  # Analizar 1 frame por segundo (asumiendo 30 FPS)
        )
        self.liveness_detection_service = LivenessDetectionService()
    
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
            
            # 3. Análisis de liveness (video en vivo vs pregrabado)
            logger.info(f"Iniciando análisis de liveness para presentación {presentation.id}")
            liveness_result = self.liveness_detection_service.analyze_video(video_path)
            
            # Guardar resultados de liveness
            if liveness_result['success']:
                presentation.is_live_recording = liveness_result['is_live']
                presentation.liveness_score = liveness_result['liveness_score']
                presentation.liveness_confidence = liveness_result['confidence']
                presentation.recording_type = liveness_result['recording_type']
            
            # 4. Análisis de participación (con detección de rostros)
            participation_data = self.analyze_participation(video_path)
            
            # Guardar datos de participación en el modelo
            presentation.participation_data = participation_data
            
            # Calcular puntuación IA
            presentation.ai_score = (coherence_score + participation_data['score']) / 2
            
            # Generar feedback
            presentation.ai_feedback = self.generate_feedback(
                transcription_result,
                coherence_score,
                participation_data,
                liveness_result
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
        Análisis REAL de participación mediante detección de rostros
        
        Detecta y compara rostros en el video para:
        - Identificar participantes únicos (Persona 1, Persona 2, etc.)
        - Medir tiempo de pantalla de cada participante
        - Calcular porcentajes de participación
        - Evaluar equidad en la distribución del tiempo
        
        Returns:
            dict: Datos de participación con score de equidad
        """
        logger.info(f"🎭 Iniciando análisis de participación con detección de rostros")
        
        try:
            # Usar el servicio de detección de rostros
            result = self.face_detection_service.process_video(video_path)
            
            if not result['success']:
                logger.error(f"Error en detección de rostros: {result.get('error', 'Unknown error')}")
                # Fallback a datos básicos en caso de error
                return {
                    'score': 0,
                    'participants': [],
                    'error': result.get('error', 'Error en detección de rostros'),
                    'total_participants': 0
                }
            
            # Formatear participantes para compatibilidad con código existente
            formatted_participants = []
            for p in result['participants']:
                formatted_participants.append({
                    'id': p['id'],
                    'percentage': round(p['percentage'], 1),
                    'time': p['time_formatted'],
                    'time_seconds': p['time_seconds'],
                    'appearances': p['appearances_count']
                })
            
            logger.info(f"✅ Participación analizada: {result['total_participants']} participantes, Score: {result['score']:.1f}")
            
            return {
                'score': result['score'],
                'participants': formatted_participants,
                'total_participants': result['total_participants'],
                'frames_analyzed': result.get('frames_analyzed', 0),
                'faces_detected': result.get('faces_detected', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ Error crítico en análisis de participación: {str(e)}", exc_info=True)
            # Retornar estructura de error
            return {
                'score': 0,
                'participants': [],
                'error': str(e),
                'total_participants': 0
            }
    
    def generate_feedback(self, transcription_result, coherence_score, participation_data, liveness_result):
        """
        Genera feedback automático basado en el análisis
        Incluye información detallada de detección de rostros y liveness
        """
        feedback = f"""
🤖 **Análisis Automático Completado**

"""
        
        # Información de autenticidad (liveness)
        if liveness_result.get('success', False):
            feedback += f"""🎥 **Autenticidad de la Grabación:**
- Tipo: {liveness_result['type_display']}
- Score de Liveness: {liveness_result['liveness_score']:.1f}/100
- Confianza: {liveness_result['confidence']:.1f}%

"""
            if liveness_result['recording_type'] == 'LIVE':
                feedback += "✅ Video grabado en vivo detectado\n\n"
            elif liveness_result['recording_type'] == 'LIKELY_LIVE':
                feedback += "⚠️ Video probablemente grabado en vivo\n\n"
            elif liveness_result['recording_type'] == 'LIKELY_RECORDED':
                feedback += "⚠️ Video probablemente pregrabado\n\n"
            else:
                feedback += "❌ Video pregrabado detectado\n\n"
        
        feedback += f"""📝 **Transcripción:**
- Texto transcrito: {len(transcription_result['full_text'])} caracteres
- Duración total: {transcription_result['duration']:.1f} segundos
- Segmentos identificados: {len(transcription_result['segments'])}

📊 **Coherencia Temática: {coherence_score:.1f}/100**
{" ✅ Excelente coherencia con el tema" if coherence_score >= 80 else
 " ⚠️ Coherencia moderada con el tema" if coherence_score >= 60 else
 " ❌ Baja coherencia con el tema asignado"}

"""
        
        # Información de participación con detección de rostros
        total_participants = participation_data.get('total_participants', 0)
        
        if total_participants > 0:
            feedback += f"""🎭 **Participación de Integrantes: {total_participants} participante(s) detectado(s)**

"""
            
            for participant in participation_data['participants']:
                feedback += f"**{participant['id']}:**\n"
                feedback += f"  • Tiempo en pantalla: {participant['time']} ({participant['percentage']:.1f}%)\n"
                if 'appearances' in participant:
                    feedback += f"  • Apariciones detectadas: {participant['appearances']}\n"
                feedback += "\n"
            
            # Análisis de equidad
            if total_participants > 1:
                percentages = [p['percentage'] for p in participation_data['participants']]
                max_diff = max(percentages) - min(percentages)
                
                feedback += "**Análisis de Equidad:**\n"
                if max_diff < 15:
                    feedback += "✅ Participación muy equilibrada entre los integrantes\n"
                elif max_diff < 30:
                    feedback += "⚠️ Participación moderadamente equilibrada\n"
                else:
                    feedback += "❌ Participación desigual - se recomienda mayor equidad\n"
                feedback += f"   (Diferencia máxima: {max_diff:.1f}%)\n\n"
            
            # Información técnica de la detección
            if 'frames_analyzed' in participation_data:
                feedback += f"**Detalles técnicos:**\n"
                feedback += f"  • Frames analizados: {participation_data['frames_analyzed']}\n"
                feedback += f"  • Rostros detectados: {participation_data.get('faces_detected', 0)}\n\n"
        else:
            feedback += "⚠️ **No se detectaron rostros en el video**\n"
            feedback += "Esto puede deberse a:\n"
            feedback += "  • Cámara apagada durante la grabación\n"
            feedback += "  • Personas fuera del encuadre\n"
            feedback += "  • Calidad de video muy baja\n\n"
        
        feedback += f"""📈 **Puntuación de Participación: {participation_data['score']:.1f}/100**

💡 **Recomendaciones:**
"""
        
        # Generar recomendaciones basadas en los resultados
        if coherence_score < 70:
            feedback += "• Enfócate más en el tema asignado durante la presentación\n"
        
        if participation_data['score'] < 80 and total_participants > 1:
            feedback += "• Busca una distribución más equitativa del tiempo entre integrantes\n"
        
        if total_participants == 0:
            feedback += "• Asegúrate de que la cámara esté encendida y los participantes visibles\n"
        
        if transcription_result['duration'] < 60:
            feedback += "• Considera extender la duración de la presentación\n"
        elif transcription_result['duration'] > 600:
            feedback += "• La presentación es muy larga, intenta ser más conciso\n"
        
        if coherence_score >= 80 and participation_data['score'] >= 80:
            feedback += "• ¡Excelente trabajo! Mantén este nivel de calidad\n"
        
        return feedback