"""
Servicio de Detección y Comparación de Rostros Anónimos
========================================================

Este servicio procesa videos para:
1. Detectar rostros en cada frame
2. Comparar rostros para identificar participantes únicos
3. Asignar etiquetas genéricas (Persona 1, Persona 2, etc.)
4. Calcular tiempo de participación de cada persona
5. NO almacenar información biométrica ni identificar personas

Utiliza:
- face_recognition para detección y comparación de rostros
- OpenCV para procesamiento de video
- Clustering para agrupar rostros similares
"""

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("⚠️ face_recognition no está instalado. La detección de rostros estará deshabilitada.")

import cv2
import numpy as np
from collections import defaultdict
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class FaceDetectionService:
    """
    Servicio de detección de rostros anónima para medir participación
    """
    
    def __init__(self, tolerance=0.6, sample_rate=30):
        """
        Inicializa el servicio de detección de rostros
        
        Args:
            tolerance (float): Sensibilidad de comparación (0.6 es bueno, menor = más estricto)
            sample_rate (int): Procesar 1 frame cada N frames (30 = ~1 frame por segundo)
        """
        self.tolerance = tolerance
        self.sample_rate = sample_rate
        self.known_face_encodings = []
        self.participant_data = []
        
    def process_video(self, video_path):
        """
        Procesa el video completo y detecta participantes
        
        Args:
            video_path (str): Ruta al archivo de video
            
        Returns:
            dict: Información de participantes con tiempos y porcentajes
        """
        if not FACE_RECOGNITION_AVAILABLE:
            logger.warning("⚠️ face_recognition no está disponible. Retornando datos vacíos.")
            return {
                'participants': [],
                'total_unique_faces': 0,
                'main_presenter': None,
                'detection_method': 'disabled',
                'error': 'face_recognition module not installed'
            }
        
        logger.info(f"🎥 Iniciando detección de rostros en: {video_path}")
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception(f"No se pudo abrir el video: {video_path}")
            
            # Obtener información del video
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            logger.info(f"📊 Video: {total_frames} frames, {fps:.2f} FPS, {duration:.2f}s duración")
            
            # Procesar frames
            frame_count = 0
            processed_frames = 0
            face_detections = []
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Procesar solo cada N frames para optimizar
                if frame_count % self.sample_rate == 0:
                    timestamp = frame_count / fps
                    faces = self._detect_faces_in_frame(frame, timestamp)
                    
                    if faces:
                        face_detections.extend(faces)
                        processed_frames += 1
                    
                    # Log de progreso cada 100 frames procesados
                    if processed_frames % 100 == 0:
                        progress = (frame_count / total_frames) * 100
                        logger.info(f"⏳ Progreso: {progress:.1f}% ({processed_frames} frames procesados)")
                
                frame_count += 1
            
            cap.release()
            logger.info(f"✅ Detección completada: {len(face_detections)} rostros detectados en {processed_frames} frames")
            
            # Agrupar rostros similares en participantes
            participants = self._cluster_faces(face_detections, fps, duration)
            
            # Calcular estadísticas
            total_detection_time = sum(p['time_seconds'] for p in participants)
            
            for participant in participants:
                participant['percentage'] = (
                    (participant['time_seconds'] / total_detection_time * 100) 
                    if total_detection_time > 0 else 0
                )
            
            # Calcular score de equidad
            score = self._calculate_participation_score(participants)
            
            result = {
                'success': True,
                'participants': participants,
                'score': score,
                'total_participants': len(participants),
                'video_duration': duration,
                'frames_analyzed': processed_frames,
                'faces_detected': len(face_detections)
            }
            
            logger.info(f"🎯 Resultado: {len(participants)} participantes identificados, Score: {score:.1f}/100")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en detección de rostros: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'participants': [],
                'score': 0,
                'total_participants': 0
            }
    
    def _detect_faces_in_frame(self, frame, timestamp):
        """
        Detecta todos los rostros en un frame
        
        Args:
            frame: Frame de video (numpy array)
            timestamp (float): Tiempo en segundos
            
        Returns:
            list: Lista de rostros detectados con sus encodings
        """
        # Convertir BGR (OpenCV) a RGB (face_recognition)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Reducir tamaño para mayor velocidad (escalar a 1/4)
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
        
        # Detectar ubicaciones de rostros
        face_locations = face_recognition.face_locations(small_frame, model='hog')
        
        if not face_locations:
            return []
        
        # Obtener encodings de los rostros
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        
        faces = []
        for encoding, location in zip(face_encodings, face_locations):
            faces.append({
                'encoding': encoding,
                'location': location,
                'timestamp': timestamp
            })
        
        return faces
    
    def _cluster_faces(self, face_detections, fps, video_duration):
        """
        Agrupa rostros similares en participantes únicos
        Asigna etiquetas genéricas: Persona 1, Persona 2, etc.
        
        Args:
            face_detections (list): Lista de detecciones de rostros
            fps (float): Frames por segundo del video
            video_duration (float): Duración total del video
            
        Returns:
            list: Lista de participantes con estadísticas
        """
        if not face_detections:
            logger.warning("⚠️ No se detectaron rostros en el video")
            return []
        
        logger.info(f"🔍 Agrupando {len(face_detections)} detecciones en participantes únicos...")
        
        participants = []
        participant_encodings = []
        participant_appearances = defaultdict(list)
        
        for detection in face_detections:
            encoding = detection['encoding']
            timestamp = detection['timestamp']
            
            if not participant_encodings:
                # Primer participante encontrado
                participant_encodings.append(encoding)
                participant_appearances[0].append(timestamp)
                logger.info(f"👤 Persona 1 detectada por primera vez en t={timestamp:.2f}s")
            else:
                # Comparar con participantes existentes
                face_distances = face_recognition.face_distance(participant_encodings, encoding)
                best_match_index = np.argmin(face_distances)
                
                if face_distances[best_match_index] <= self.tolerance:
                    # Es un participante conocido
                    participant_appearances[best_match_index].append(timestamp)
                else:
                    # Nuevo participante
                    new_index = len(participant_encodings)
                    participant_encodings.append(encoding)
                    participant_appearances[new_index].append(timestamp)
                    logger.info(f"👤 Persona {new_index + 1} detectada por primera vez en t={timestamp:.2f}s")
        
        # Construir datos de participantes
        for idx, appearances in participant_appearances.items():
            # Calcular tiempo total (cada aparición representa sample_rate/fps segundos)
            time_per_detection = self.sample_rate / fps
            total_time_seconds = len(appearances) * time_per_detection
            
            # Formatear tiempo
            time_str = self._format_duration(total_time_seconds)
            
            # Calcular apariciones consecutivas para detectar intervalos
            appearances.sort()
            first_appearance = appearances[0]
            last_appearance = appearances[-1]
            
            participant = {
                'id': f'Persona {idx + 1}',
                'time_seconds': total_time_seconds,
                'time_formatted': time_str,
                'appearances_count': len(appearances),
                'first_seen': first_appearance,
                'last_seen': last_appearance,
                'percentage': 0  # Se calculará después
            }
            
            participants.append(participant)
        
        # Ordenar por tiempo de participación (mayor a menor)
        participants.sort(key=lambda x: x['time_seconds'], reverse=True)
        
        # Re-etiquetar según orden de participación
        for idx, participant in enumerate(participants):
            participant['id'] = f'Persona {idx + 1}'
        
        logger.info(f"✅ Identificados {len(participants)} participantes únicos")
        
        return participants
    
    def _calculate_participation_score(self, participants):
        """
        Calcula un score de equidad de participación
        100 = perfectamente equitativo
        0 = muy desigual
        
        Args:
            participants (list): Lista de participantes con porcentajes
            
        Returns:
            float: Score de 0-100
        """
        if not participants:
            return 0
        
        if len(participants) == 1:
            return 100  # Solo una persona = participación completa
        
        percentages = [p['percentage'] for p in participants]
        
        # Calcular desviación estándar
        mean_percentage = np.mean(percentages)
        std_dev = np.std(percentages)
        
        # Score inverso a la desviación
        # Perfectamente equitativo: std_dev = 0 → score = 100
        # Muy desigual: std_dev = alta → score = bajo
        
        # Normalizar: si todos participan igual, std_dev = 0
        # En el peor caso (1 persona 100%, resto 0%), std_dev ≈ mean_percentage
        
        if mean_percentage == 0:
            return 0
        
        # Normalizar std_dev respecto al promedio
        normalized_std = (std_dev / mean_percentage) * 100
        
        # Score: 100 - penalización por desigualdad
        score = max(0, 100 - normalized_std)
        
        return round(score, 2)
    
    def _format_duration(self, seconds):
        """
        Formatea segundos a formato legible
        
        Args:
            seconds (float): Duración en segundos
            
        Returns:
            str: Duración formateada (ej: "2 min 30 seg")
        """
        if seconds < 60:
            return f"{seconds:.1f} seg"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes} min {secs} seg"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}min"
    
    def get_participation_summary(self, participants):
        """
        Genera un resumen textual de la participación
        
        Args:
            participants (list): Lista de participantes
            
        Returns:
            str: Resumen formateado
        """
        if not participants:
            return "No se detectaron participantes en el video."
        
        summary = f"🎭 **Participantes Detectados: {len(participants)}**\n\n"
        
        for p in participants:
            summary += f"**{p['id']}**\n"
            summary += f"  • Tiempo de pantalla: {p['time_formatted']} ({p['percentage']:.1f}%)\n"
            summary += f"  • Apariciones: {p['appearances_count']} veces\n"
            summary += f"  • Primera aparición: {p['first_seen']:.1f}s\n"
            summary += f"  • Última aparición: {p['last_seen']:.1f}s\n\n"
        
        # Análisis de equidad
        if len(participants) > 1:
            percentages = [p['percentage'] for p in participants]
            max_diff = max(percentages) - min(percentages)
            
            if max_diff < 15:
                summary += "✅ **Participación muy equilibrada entre los integrantes**\n"
            elif max_diff < 30:
                summary += "⚠️ **Participación moderadamente equilibrada**\n"
            else:
                summary += "❌ **Participación desigual - se recomienda mayor equidad**\n"
        
        return summary
