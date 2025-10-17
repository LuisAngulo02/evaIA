# apps/ai_processor/services/face_detection_mediapipe.py
"""
Servicio de Detección de Rostros con MediaPipe
===============================================

Usa MediaPipe Face Detection de Google para:
1. Detectar múltiples rostros en video
2. Rastrear rostros únicos a lo largo del tiempo
3. Calcular tiempo de participación individual
4. Asignar etiquetas anónimas (Persona 1, 2, 3...)

"""

import cv2
import numpy as np
import mediapipe as mp
from collections import defaultdict
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class MediaPipeFaceDetection:
    """
    Servicio de detección de rostros con MediaPipe
    """
    
    def __init__(self, min_detection_confidence=0.5, sample_rate=15):
        """
        Inicializa MediaPipe Face Detection
        
        Args:
            min_detection_confidence (float): Confianza mínima para detectar rostro (0.5 = 50%)
            sample_rate (int): Procesar 1 frame cada N frames (15 = ~2 frames por segundo)
        """
        self.min_detection_confidence = min_detection_confidence
        self.sample_rate = sample_rate
        
        # Inicializar MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=min_detection_confidence,
            model_selection=1  # 0: corto alcance, 1: largo alcance (mejor para video)
        )
        
        # Inicializar MediaPipe Face Mesh para verificación adicional
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=5,
            refine_landmarks=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Tracking de rostros
        self.face_tracks = []  # Lista de tracks de rostros únicos
        self.next_face_id = 1
        
    def process_video(self, video_path):
        """
        Procesa el video y detecta participantes únicos
        
        Returns:
            dict: Información de participantes con tiempos y porcentajes
        """
        logger.info(f"🎥 Iniciando detección MediaPipe en: {video_path}")
        
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
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Procesar cada N frames
                if frame_count % self.sample_rate == 0:
                    timestamp = frame_count / fps
                    self._process_frame(frame, timestamp)
                    processed_frames += 1
                
                frame_count += 1
            
            cap.release()
            
            # Analizar resultados
            result = self._analyze_tracks(duration)
            result['frames_analyzed'] = processed_frames
            result['total_frames'] = total_frames
            result['detection_method'] = 'mediapipe'
            
            logger.info(f"✅ Detección completada: {result['total_participants']} participantes únicos")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en detección MediaPipe: {str(e)}", exc_info=True)
            return {
                'success': False,
                'participants': [],
                'total_participants': 0,
                'score': 0,
                'error': str(e),
                'detection_method': 'mediapipe'
            }
    
    def _process_frame(self, frame, timestamp):
        """
        Procesa un frame individual detectando rostros
        """
        # Convertir a RGB (MediaPipe usa RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detectar rostros
        results = self.face_detection.process(frame_rgb)
        
        if not results.detections:
            return
        
        # Extraer información de cada rostro detectado
        current_faces = []
        for detection in results.detections:
            # Verificar score de confianza
            confidence = detection.score[0]
            if confidence < 0.5:  # Umbral moderado de confianza
                continue
            
            # Obtener bounding box
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            
            # Convertir a coordenadas absolutas
            x = int(bboxC.xmin * iw)
            y = int(bboxC.ymin * ih)
            w = int(bboxC.width * iw)
            h = int(bboxC.height * ih)
            
            # Filtro principal: Solo verificar que sea un rostro humano real
            # Permitir rostros de cualquier tamaño y en cualquier posición
            
            # Verificación con Face Mesh (detecta características faciales humanas)
            # Extraer región del rostro para verificación
            face_roi = frame_rgb[max(0, y):min(ih, y+h), max(0, x):min(iw, x+w)]
            if face_roi.size > 0:
                face_mesh_results = self.face_mesh.process(face_roi)
                # Si Face Mesh no detecta landmarks faciales, probablemente no es un rostro humano
                if not face_mesh_results.multi_face_landmarks:
                    continue
            
            # Centro del rostro (para tracking)
            center_x = x + w // 2
            center_y = y + h // 2
            
            current_faces.append({
                'bbox': (x, y, w, h),
                'center': (center_x, center_y),
                'confidence': confidence,
                'timestamp': timestamp
            })
        
        # Asignar rostros a tracks existentes o crear nuevos
        self._update_tracks(current_faces)
    
    def _update_tracks(self, current_faces):
        """
        Actualiza tracks de rostros usando distancia euclidiana
        """
        # Si no hay tracks, crear nuevos para cada rostro
        if not self.face_tracks:
            for face in current_faces:
                self.face_tracks.append({
                    'id': self.next_face_id,
                    'label': f'Persona {self.next_face_id}',
                    'appearances': [face],
                    'last_seen': face['timestamp']
                })
                self.next_face_id += 1
            return
        
        # Matching: asignar rostros actuales a tracks existentes
        used_tracks = set()
        threshold = 150  # Píxeles de distancia máxima para considerar el mismo rostro
        
        for face in current_faces:
            best_match = None
            min_distance = float('inf')
            
            # Buscar el track más cercano
            for i, track in enumerate(self.face_tracks):
                if i in used_tracks:
                    continue
                
                # Calcular distancia al último centro conocido
                last_appearance = track['appearances'][-1]
                last_center = last_appearance['center']
                
                distance = np.sqrt(
                    (face['center'][0] - last_center[0])**2 + 
                    (face['center'][1] - last_center[1])**2
                )
                
                if distance < min_distance and distance < threshold:
                    min_distance = distance
                    best_match = i
            
            # Asignar a track existente o crear nuevo
            if best_match is not None:
                self.face_tracks[best_match]['appearances'].append(face)
                self.face_tracks[best_match]['last_seen'] = face['timestamp']
                used_tracks.add(best_match)
            else:
                # Nuevo rostro
                self.face_tracks.append({
                    'id': self.next_face_id,
                    'label': f'Persona {self.next_face_id}',
                    'appearances': [face],
                    'last_seen': face['timestamp']
                })
                self.next_face_id += 1
    
    def _analyze_tracks(self, total_duration):
        """
        Analiza los tracks y genera estadísticas de participación
        """
        if not self.face_tracks:
            return {
                'success': True,
                'participants': [],
                'total_participants': 0,
                'score': 0
            }
        
        participants = []
        
        for track in self.face_tracks:
            # Calcular tiempo de participación
            appearances_count = len(track['appearances'])
            
            # Estimar tiempo (cada aparición representa sample_rate frames)
            # Asumiendo fps ~30
            time_seconds = (appearances_count * self.sample_rate) / 30.0
            
            # Calcular porcentaje
            percentage = (time_seconds / total_duration * 100) if total_duration > 0 else 0
            
            # Formatear tiempo
            minutes = int(time_seconds // 60)
            seconds = int(time_seconds % 60)
            time_formatted = f"{minutes}:{seconds:02d}"
            
            # Primera y última aparición
            first_seen = track['appearances'][0]['timestamp']
            last_seen = track['appearances'][-1]['timestamp']
            
            # Crear segmentos de tiempo
            time_segments = self._create_time_segments(track['appearances'])
            
            participants.append({
                'id': track['label'],
                'time_formatted': time_formatted,
                'time_seconds': time_seconds,
                'percentage': round(percentage, 1),
                'appearances_count': appearances_count,
                'first_seen': round(first_seen, 1),
                'last_seen': round(last_seen, 1),
                'time_segments': time_segments
            })
        
        # Ordenar por tiempo de participación (mayor a menor)
        participants.sort(key=lambda x: x['time_seconds'], reverse=True)
        
        # Calcular score de equidad
        if len(participants) > 1:
            percentages = [p['percentage'] for p in participants]
            max_diff = max(percentages) - min(percentages)
            score = max(0, 100 - max_diff * 2)  # Penalizar desigualdad
        else:
            score = participants[0]['percentage'] if participants else 0
        
        return {
            'success': True,
            'participants': participants,
            'total_participants': len(participants),
            'score': round(score, 1)
        }
    
    def _create_time_segments(self, appearances):
        """
        Crea segmentos de tiempo continuos
        """
        if not appearances:
            return []
        
        segments = []
        current_segment_start = appearances[0]['timestamp']
        last_timestamp = current_segment_start
        
        for appearance in appearances[1:]:
            # Si hay un gap grande (>5s), iniciar nuevo segmento
            if appearance['timestamp'] - last_timestamp > 5:
                segments.append({
                    'start': round(current_segment_start, 1),
                    'end': round(last_timestamp, 1)
                })
                current_segment_start = appearance['timestamp']
            
            last_timestamp = appearance['timestamp']
        
        # Agregar último segmento
        segments.append({
            'start': round(current_segment_start, 1),
            'end': round(last_timestamp, 1)
        })
        
        return segments
    
    def __del__(self):
        """Limpiar recursos de MediaPipe"""
        if hasattr(self, 'face_detection'):
            self.face_detection.close()
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()
