# apps/ai_processor/services/ai_service.py
import logging
from django.utils import timezone
from .transcription_service import TranscriptionService
from .face_detection_service import FaceDetectionService
from .liveness_detection_service import LivenessDetectionService
from .coherence_analyzer import CoherenceAnalyzer
from .audio_segmentation_service import AudioSegmentationService

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.transcription_service = TranscriptionService()
        self.face_detection_service = FaceDetectionService(
            tolerance=0.6,  # Sensibilidad de comparación de rostros
            sample_rate=30  # Analizar 1 frame por segundo (asumiendo 30 FPS)
        )
        self.liveness_detection_service = LivenessDetectionService()
        self.coherence_analyzer = CoherenceAnalyzer()  # NUEVO
        
        # Servicio de segmentación de audio
        recommended_strategy = AudioSegmentationService.get_recommended_strategy()
        self.audio_segmentation_service = AudioSegmentationService(strategy=recommended_strategy)
        logger.info(f"🎤 Audio segmentation strategy: {recommended_strategy}")
    
    def analyze_presentation(self, presentation):
        """
        Análisis completo de una presentación con evaluación individual
        """
        try:
            # Actualizar estado a procesando
            presentation.status = 'PROCESSING'
            presentation.save()
            
            # Función helper para reportar progreso
            def report_progress(progress, step):
                from django.core.cache import cache
                cache.set(f'presentation_progress_{presentation.id}', {
                    'status': 'PROCESSING',
                    'progress': progress,
                    'step': step
                }, timeout=3600)
            
            video_path = presentation.video_file.path
            
            # 1. Análisis de liveness (video en vivo vs pregrabado)
            report_progress(15, 'Analizando autenticidad del video...')
            logger.info(f"🎥 Iniciando análisis de liveness para presentación {presentation.id}")
            liveness_result = self.liveness_detection_service.analyze_video(video_path)
            
            # Guardar resultados de liveness
            if liveness_result['success']:
                presentation.is_live_recording = liveness_result['is_live']
                presentation.liveness_score = liveness_result['liveness_score']
                presentation.liveness_confidence = liveness_result['confidence']
                presentation.recording_type = liveness_result['recording_type']
            
            # 2. Detección de rostros y análisis de participación
            report_progress(30, 'Detectando rostros y participantes...')
            logger.info(f"👥 Iniciando detección de rostros para presentación {presentation.id}")
            face_analysis = self.face_detection_service.process_video(video_path, presentation_id=presentation.id)
            
            # Guardar datos de participación básicos
            presentation.participation_data = face_analysis
            
            # 3. Transcripción completa del video
            report_progress(50, 'Transcribiendo audio con Whisper...')
            logger.info(f"🎤 Iniciando transcripción completa para presentación {presentation.id}")
            transcription_result = self.transcription_service.transcribe_video(video_path)
            
            # Guardar transcripción completa
            presentation.transcription_text = transcription_result['full_text']
            presentation.transcription_segments = transcription_result['segments']
            presentation.audio_duration = transcription_result['duration']
            presentation.transcription_completed_at = timezone.now()
            
            # ===== VALIDACIONES CRÍTICAS =====
            # Verificar si hay audio
            has_audio = bool(transcription_result['full_text'] and transcription_result['full_text'].strip())
            has_face = face_analysis['success'] and face_analysis.get('total_participants', 0) > 0
            
            # CASO 1: No hay audio - ERROR CRÍTICO
            if not has_audio:
                error_msg = "❌ No se detectó audio en el video. Por favor, verifica que tu micrófono esté funcionando y graba nuevamente."
                logger.error(f"Sin audio detectado en presentación {presentation.id}")
                presentation.status = 'FAILED'
                presentation.ai_feedback = error_msg
                presentation.save()
                
                from django.core.cache import cache
                cache.set(f'presentation_progress_{presentation.id}', {
                    'status': 'FAILED',
                    'progress': 0,
                    'step': 'Sin audio detectado',
                    'error': error_msg
                }, timeout=3600)
                
                return False
            
            # CASO 2: No hay cara - ERROR CRÍTICO (solo si tampoco hay audio)
            # Pero si hay audio sin cara, continuar con análisis de audio únicamente
            if not has_face:
                logger.warning(f"⚠️ No se detectaron rostros en presentación {presentation.id}")
                # Marcar que no hay rostros pero continuar procesamiento
                presentation.participation_data['no_face_detected'] = True
                presentation.participation_data['warning'] = "No se detectaron rostros en el video"
            
            # 4. ANÁLISIS INDIVIDUAL DE COHERENCIA
            report_progress(70, 'Analizando coherencia individual...')
            logger.info(f"🧠 Iniciando análisis individual de coherencia")
            
            # Determinar si hay rostros detectados
            has_participants = face_analysis['success'] and face_analysis.get('participants') and len(face_analysis['participants']) > 0
            
            if has_participants:
                # CASO NORMAL: Hay rostros detectados
                logger.info(f"✅ {len(face_analysis['participants'])} participante(s) detectado(s)")
                
                # Preparar tema y descripción
                tema = presentation.assignment.title if presentation.assignment else "Tema general"
                descripcion_tema = presentation.assignment.description if presentation.assignment else ""
                
                # Asignar transcripción completa si solo hay 1 participante
                # Para múltiples, idealmente se debería segmentar por tiempo
                participants_data = self._prepare_participants_data(
                    face_analysis['participants'],
                    transcription_result,
                    video_path
                )
                
                # Obtener puntaje máximo de la asignación (default 20)
                max_score = float(presentation.assignment.max_score) if presentation.assignment else 20.0
                
                # Obtener assignment para configuración de IA
                assignment = presentation.assignment
                if assignment:
                    logger.info(f"� Assignment identificado: {assignment.title}")
                
                # Analizar coherencia individual con assignment
                coherence_results = self.coherence_analyzer.analizar_grupo(
                    participants_data,
                    tema,
                    descripcion_tema,
                    max_score=max_score,  # Pasar puntaje máximo
                    assignment=assignment  # Pasar assignment completo para configuración de estrictez
                )
                
                # Guardar participantes individuales en la BD
                self._save_participants(presentation, coherence_results)
                
                # Calcular score promedio de coherencia
                avg_coherence = sum(r['nota_coherencia'] for r in coherence_results) / len(coherence_results)
                presentation.ai_score = avg_coherence
                
            else:
                # CASO ESPECIAL: No hay rostros pero hay audio
                # Análisis solo por audio (voz en off)
                logger.warning("⚠️ No se detectaron rostros - Análisis solo por audio")
                
                # Preparar tema y descripción
                tema = presentation.assignment.title if presentation.assignment else "Tema general"
                descripcion_tema = presentation.assignment.description if presentation.assignment else ""
                max_score = float(presentation.assignment.max_score) if presentation.assignment else 20.0
                
                # Obtener assignment para configuración de IA
                assignment = presentation.assignment
                
                # Crear un participante virtual "Sin Rostro Detectado"
                participants_data = [{
                    'etiqueta': 'Sin Rostro Detectado',
                    'texto_transcrito': transcription_result['full_text'],
                    'tiempo_participacion': transcription_result['duration'],
                    'foto_url': None
                }]
                
                # Analizar coherencia del audio con assignment
                coherence_results = self.coherence_analyzer.analizar_grupo(
                    participants_data,
                    tema,
                    descripcion_tema,
                    max_score=max_score,
                    assignment=assignment
                )
                
                # Marcar que no hay rostro en el resultado
                coherence_results[0]['sin_rostro'] = True
                coherence_results[0]['observacion'] += " ⚠️ NOTA: No se detectó ningún rostro en el video, calificación basada únicamente en el análisis de audio."
                
                # Guardar participante virtual en la BD
                self._save_participants(presentation, coherence_results)
                
                # Calcular score
                avg_coherence = coherence_results[0]['nota_coherencia']
                presentation.ai_score = avg_coherence
            
            # 5. Generar feedback detallado
            report_progress(90, 'Generando retroalimentación...')
            presentation.ai_feedback = self.generate_feedback(
                transcription_result,
                avg_coherence if face_analysis['participants'] else presentation.ai_score,
                face_analysis,
                liveness_result,
                coherence_results
            )
            
            # Actualizar estado
            presentation.status = 'ANALYZED'
            presentation.analyzed_at = timezone.now()
            presentation.save()
            
            report_progress(100, 'Análisis completado ✅')
            logger.info(f"✅ Análisis completado para presentación {presentation.id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en análisis IA: {str(e)}", exc_info=True)
            presentation.ai_feedback = f"Error en análisis: {str(e)}"
            presentation.status = 'FAILED'
            presentation.save()
            return False
    
    def analyze_coherence(self, transcription, topic_description):
        """
        Análisis básico de coherencia temática (fallback)
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
    
    def _prepare_participants_data(self, participants, transcription_result, video_path):
        """
        Prepara datos de participantes para análisis de coherencia.
        
        Utiliza segmentación de audio para asignar transcripciones exactas
        a cada participante según quién habla cuándo.
        """
        full_text = transcription_result['full_text']
        total_duration = transcription_result['duration']
        
        # Si no hay transcripción, retornar datos básicos
        if not full_text or not full_text.strip():
            return [{
                'etiqueta': p['id'],
                'texto_transcrito': '',
                'tiempo_participacion': p['time_seconds'],
                'foto_url': p.get('photo')
            } for p in participants]
        
        # Si solo hay 1 participante, darle toda la transcripción
        if len(participants) == 1:
            return [{
                'etiqueta': participants[0]['id'],
                'texto_transcrito': full_text,
                'tiempo_participacion': participants[0]['time_seconds'],
                'foto_url': participants[0].get('photo')
            }]
        
        # Para múltiples participantes: segmentar audio por hablante
        logger.info(f"🎤 Segmentando audio para {len(participants)} participantes")
        
        try:
            # Crear estructura de datos compatible con AudioSegmentationService
            participants_for_segmentation = []
            for p in participants:
                participants_for_segmentation.append({
                    'participant_id': p['id'],
                    'name': p['id'],  # Usar 'id' como nombre (ej: "Persona 1")
                    'appearances': p.get('appearances', []),
                    'total_participation_time': p['time_seconds']
                })
            
            # Ejecutar segmentación
            segmented_participants = self.audio_segmentation_service.segment_audio_by_participants(
                video_path,
                participants_for_segmentation,
                transcription_result
            )
            
            # Convertir a formato esperado por coherence_analyzer
            participants_data = []
            for seg_participant in segmented_participants:
                # Buscar participante original para obtener foto
                original_participant = next(
                    (p for p in participants if p['id'] == seg_participant['participant_id']),
                    None
                )
                
                participants_data.append({
                    'etiqueta': seg_participant['participant_id'],
                    'texto_transcrito': seg_participant.get('transcription', ''),
                    'tiempo_participacion': seg_participant.get('total_participation_time', 0),
                    'foto_url': original_participant.get('photo') if original_participant else None,
                    'speech_segments': seg_participant.get('speech_segments', []),
                    'time_segments': original_participant.get('time_segments', []) if original_participant else []
                })
            
            logger.info(f"✅ Segmentación completada: {len(participants_data)} participantes con transcripciones asignadas")
            return participants_data
            
        except Exception as e:
            logger.warning(f"⚠️ Error en segmentación de audio: {str(e)}. Usando método proporcional.")
            
            # Fallback: distribución proporcional (método antiguo)
            participants_data = []
            palabras = full_text.split()
            
            for participant in participants:
                tiempo_porcentaje = participant['percentage'] / 100
                num_palabras = int(len(palabras) * tiempo_porcentaje)
                texto = ' '.join(palabras[:max(num_palabras, 20)])  # Mínimo 20 palabras
                
                participants_data.append({
                    'etiqueta': participant['id'],
                    'texto_transcrito': texto,
                    'tiempo_participacion': participant['time_seconds'],
                    'foto_url': participant.get('photo'),
                    'time_segments': participant.get('time_segments', [])
                })
            
            return participants_data
    
    def _save_participants(self, presentation, coherence_results):
        """
        Guarda los resultados individuales de participantes en la BD
        """
        from apps.presentaciones.models import Participant
        
        # Eliminar participantes anteriores si existen
        presentation.participants.all().delete()
        
        # Crear nuevos participantes
        for resultado in coherence_results:
            # Buscar la foto si existe
            photo_path = resultado.get('foto_url')
            
            # Preparar feedback de IA
            ai_feedback_text = f"""**Análisis de Coherencia:**
{resultado['observacion']}

**Métricas Detectadas:**
- Coherencia semántica: {resultado['coherencia_semantica']}%
- Palabras clave encontradas: {resultado['puntaje_palabras_clave']}%
- Profundidad del contenido: {resultado['puntaje_profundidad']}%
- Tiempo de participación: {resultado['tiempo_participacion']}s ({resultado['porcentaje_tiempo']}%)

**Palabras clave identificadas:** {', '.join(resultado['palabras_clave_encontradas'][:10]) if resultado['palabras_clave_encontradas'] else 'Ninguna'}

**Nivel de coherencia:** {resultado['nivel']}
"""
            
            # Si hay feedback avanzado de IA (Groq), usarlo
            if 'feedback_ia_avanzada' in resultado:
                ai_feedback_text = resultado['feedback_ia_avanzada']
            
            Participant.objects.create(
                presentation=presentation,
                label=resultado['etiqueta'],
                photo=photo_path,  # Guardar ruta de la foto
                participation_time=resultado['tiempo_participacion'],
                time_percentage=resultado['porcentaje_tiempo'],
                time_segments=resultado.get('time_segments', []),  # Guardar segmentos de tiempo
                transcription=resultado['texto_transcrito'],
                word_count=resultado['palabras_totales'],
                semantic_coherence=resultado['coherencia_semantica'],
                keywords_score=resultado['puntaje_palabras_clave'],
                depth_score=resultado['puntaje_profundidad'],
                coherence_score=resultado['nota_coherencia'],
                contribution_percentage=resultado['porcentaje_aporte_normalizado'],
                ai_grade=resultado['calificacion_final'],  # Calificación de IA
                ai_feedback=ai_feedback_text,  # Feedback de IA
                coherence_level=resultado['nivel'],
                observations=resultado['observacion'],
                keywords_found=resultado['palabras_clave_encontradas']
            )
        
        logger.info(f"💾 Guardados {len(coherence_results)} participantes en la BD")
    
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
    
    def generate_feedback(self, transcription_result, coherence_score, participation_data, liveness_result, coherence_results=[]):
        """
        Genera feedback automático basado en el análisis
        Incluye información detallada individual de cada participante
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

"""
        
        # NUEVO: Evaluación individual de participantes
        if coherence_results:
            # Verificar si es caso sin rostro
            is_no_face_case = len(coherence_results) == 1 and coherence_results[0].get('sin_rostro', False)
            
            if is_no_face_case:
                feedback += f"""⚠️ **ANÁLISIS SIN ROSTRO DETECTADO**\n\n"""
                feedback += f"""**IMPORTANTE:** No se detectó ningún rostro en el video. La calificación está basada únicamente en el análisis del audio transcrito.\n\n"""
            else:
                feedback += f"""📊 **EVALUACIÓN INDIVIDUAL - {len(coherence_results)} Participantes**\n\n"""
            
            # Ordenar por calificación (mayor a menor)
            coherence_results_sorted = sorted(coherence_results, key=lambda x: x['calificacion_final'], reverse=True)
            
            for idx, resultado in enumerate(coherence_results_sorted, 1):
                # Icono diferente si no hay rostro
                icon = "🎤" if resultado.get('sin_rostro', False) else "👤"
                
                feedback += f"""**{idx}. {icon} {resultado['etiqueta']}** - {resultado['nivel']}
   📝 Calificación: **{resultado['calificacion_final']}/20**
   ⏱️  Tiempo: {resultado['porcentaje_tiempo']:.1f}%
   📈 Aporte: {resultado['porcentaje_aporte_normalizado']:.1f}%
   🎯 Coherencia: {resultado['nota_coherencia']:.1f}/100
   💬 Palabras: {resultado['palabras_totales']}
   
   **Desglose:**
   • Coherencia semántica: {resultado['coherencia_semantica']:.1f}/100
   • Palabras clave: {resultado['puntaje_palabras_clave']:.1f}/100
   • Profundidad: {resultado['puntaje_profundidad']:.1f}/100
   
   **Observación:** {resultado['observacion']}
   
"""
                if resultado['palabras_clave_encontradas']:
                    palabras = ', '.join(resultado['palabras_clave_encontradas'][:5])
                    feedback += f"   🔑 Palabras clave: {palabras}\n\n"
            
            # Estadísticas del grupo
            import numpy as np
            promedio_coherencia = np.mean([r['nota_coherencia'] for r in coherence_results])
            promedio_calificacion = np.mean([r['calificacion_final'] for r in coherence_results])
            
            feedback += f"""**📊 Estadísticas del Grupo:**
   • Coherencia promedio: {promedio_coherencia:.1f}/100
   • Calificación promedio: {promedio_calificacion:.1f}/20
   • Participantes detectados: {len(coherence_results)}
   
"""
            
            # Análisis de equidad
            desviacion_tiempo = np.std([r['porcentaje_tiempo'] for r in coherence_results])
            if desviacion_tiempo < 10:
                feedback += "   • ✅ Participación muy equilibrada en tiempo\n"
            elif desviacion_tiempo < 20:
                feedback += "   • ⚠️  Participación moderadamente equilibrada\n"
            else:
                feedback += "   • ❌ Participación desigual - revisar distribución\n"
            
            feedback += "\n"
        
        else:
            # Si no hay análisis individual, usar el global
            feedback += f"""📊 **Coherencia Temática General: {coherence_score:.1f}/100**
{" ✅ Excelente coherencia con el tema" if coherence_score >= 80 else
 " ⚠️ Coherencia moderada con el tema" if coherence_score >= 60 else
 " ❌ Baja coherencia con el tema asignado"}

"""
        
        # Información de participación (resumen)
        total_participants = participation_data.get('total_participants', 0)
        no_face_detected = participation_data.get('no_face_detected', False)
        
        if total_participants > 0:
            feedback += f"""🎭 **Detección de Rostros:**
- Participantes únicos: {total_participants}
- Frames analizados: {participation_data.get('frames_analyzed', 0)}
- Rostros detectados: {participation_data.get('faces_detected', 0)}

"""
        else:
            feedback += """⚠️ **No se detectaron rostros en el video**

**Posibles causas:**
• Cámara apagada o cubierta
• Participante fuera del cuadro
• Iluminación muy baja
• Calidad de video muy baja

**Recomendación:** Para una evaluación completa, asegúrate de que tu rostro sea visible durante la grabación.

"""
        
        # Recomendaciones generales
        feedback += f"""💡 **Recomendaciones Generales:**
"""
        
        if coherence_results:
            # Recomendaciones basadas en análisis individual
            notas_bajas = [r for r in coherence_results if r['calificacion_final'] < 11]
            if notas_bajas:
                feedback += f"• {len(notas_bajas)} participante(s) necesita(n) mejorar la coherencia con el tema\n"
            
            max_diff_tiempo = max([r['porcentaje_tiempo'] for r in coherence_results]) - min([r['porcentaje_tiempo'] for r in coherence_results])
            if max_diff_tiempo > 30:
                feedback += "• Buscar mayor equidad en la distribución del tiempo entre participantes\n"
        
        if transcription_result['duration'] < 60:
            feedback += "• Considerar extender la duración de la presentación\n"
        elif transcription_result['duration'] > 600:
            feedback += "• La presentación es muy larga, intenta ser más conciso\n"
        
        if total_participants == 0:
            feedback += "• Asegúrate de que la cámara esté encendida y los participantes visibles\n"
        
        return feedback
