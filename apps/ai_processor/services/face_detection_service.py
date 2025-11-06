"""
Servicio de Detección y Comparación de Rostros Anónimos
========================================================

Este servicio procesa videos para:
1. Detectar rostros en cada frame con MediaPipe
2. Comparar rostros para identificar participantes únicos
3. Asignar etiquetas genéricas (Persona 1, Persona 2, etc.)
4. Calcular tiempo de participación de cada persona
5. NO almacenar información biométrica ni identificar personas

Utiliza:
- MediaPipe para detección facial avanzada (optimizado para tiempo real)
- OpenCV para procesamiento de video
- Clustering para agrupar rostros similares
"""

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
    print("✅ MediaPipe disponible - usando detección avanzada")
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️ MediaPipe no está instalado. Usando OpenCV básico...")

import cv2
import numpy as np
from collections import defaultdict
import logging
from datetime import timedelta
import os
from django.conf import settings

logger = logging.getLogger(__name__)


class FaceDetectionService:
    """
    Servicio de detección de rostros anónima para medir participación
    """
    
    def __init__(self, tolerance=0.6, sample_rate=30, teacher=None):
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
        
        # Configuración personalizada del docente
        if teacher:
            self._load_teacher_config(teacher)
    
    def _load_teacher_config(self, teacher):
        """Carga la configuración personalizada del docente"""
        try:
            from apps.presentaciones.models import AIConfiguration
            config = AIConfiguration.get_config_for_teacher(teacher)
            
            # Usar confianza personalizada (convertir a tolerance - inversamente proporcional)
            # confidence 0.7 -> tolerance 0.3, confidence 0.3 -> tolerance 0.7
            self.tolerance = 1.0 - config.face_detection_confidence
            
            logger.info(f"✅ Configuración personalizada cargada para {teacher.username}")
            logger.info(f"   - Confianza: {config.face_detection_confidence}")
            logger.info(f"   - Tolerance: {self.tolerance}")
            
        except Exception as e:
            logger.warning(f"⚠️ No se pudo cargar configuración para {teacher.username}: {e}")
            # Mantener valores por defecto
        
    def process_video(self, video_path, presentation_id=None):
        """
        Procesa el video completo y detecta participantes
        
        Args:
            video_path (str): Ruta al archivo de video
            presentation_id (int): ID de la presentación para guardar fotos
            
        Returns:
            dict: Información de participantes con tiempos y porcentajes
        """
        # Usar MediaPipe (detección avanzada optimizada)
        if MEDIAPIPE_AVAILABLE:
            logger.info("✅ Usando MediaPipe para detección facial")
            return self._process_video_mediapipe(video_path, presentation_id)
        else:
            logger.warning("⚠️ Usando OpenCV básico (detección simple)")
            return self._process_video_opencv_fallback(video_path)
    
    def _process_video_mediapipe(self, video_path, presentation_id=None):
        """
        Método con MediaPipe - detecta múltiples rostros en tiempo real (mejor opción)
        """
        logger.info(f"🎥 Iniciando detección de rostros con MediaPipe: {video_path}")
        logger.info(f"🔧 Parámetros de detección:")
        logger.info(f"   - Tolerance: {self.tolerance}")
        logger.info(f"   - Sample rate: {self.sample_rate}")
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception(f"No se pudo abrir el video: {video_path}")
            
            # Obtener información del video
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            logger.info(f"📊 Video: {total_frames} frames, {fps:.2f} FPS, {duration:.2f}s duración")
            
            if fps <= 0:
                logger.error(f"❌ FPS inválido: {fps}. No se puede procesar el video.")
                raise Exception(f"FPS inválido: {fps}")            # Procesar frames
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
    
    def _calculate_visual_similarity(self, face1, face2):
        """
        Calcula la similitud visual entre dos imágenes de rostros
        Usa histogramas de color y estructura para comparar
        
        Args:
            face1: Primera imagen del rostro (numpy array)
            face2: Segunda imagen del rostro (numpy array)
            
        Returns:
            float: Score de diferencia (0.0 = idénticos, 1.0 = muy diferentes)
        """
        try:
            # Redimensionar ambas imágenes al mismo tamaño
            target_size = (64, 64)
            face1_resized = cv2.resize(face1, target_size)
            face2_resized = cv2.resize(face2, target_size)
            
            # 1. Comparación por histograma de color (HSV)
            face1_hsv = cv2.cvtColor(face1_resized, cv2.COLOR_BGR2HSV)
            face2_hsv = cv2.cvtColor(face2_resized, cv2.COLOR_BGR2HSV)
            
            hist1 = cv2.calcHist([face1_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
            hist2 = cv2.calcHist([face2_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
            
            hist1 = cv2.normalize(hist1, hist1).flatten()
            hist2 = cv2.normalize(hist2, hist2).flatten()
            
            # Correlación de histogramas (1.0 = idénticos, 0.0 = diferentes)
            hist_correlation = cv2.compareHist(
                hist1.reshape(-1, 1), 
                hist2.reshape(-1, 1), 
                cv2.HISTCMP_CORREL
            )
            
            # 2. Comparación estructural (similitud de patrones)
            gray1 = cv2.cvtColor(face1_resized, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(face2_resized, cv2.COLOR_BGR2GRAY)
            
            # Diferencia absoluta media
            diff = cv2.absdiff(gray1, gray2)
            structural_diff = np.mean(diff) / 255.0  # Normalizar 0-1
            
            # 3. Score combinado
            # hist_correlation: 1.0 = idénticos → convertir a 0.0
            # structural_diff: 0.0 = idénticos
            hist_score = 1.0 - max(0.0, hist_correlation)  # Invertir: 0 = iguales
            structural_score = structural_diff
            
            # Promedio ponderado: 70% histograma + 30% estructura
            combined_score = (0.7 * hist_score) + (0.3 * structural_score)
            
            return combined_score
            
        except Exception as e:
            logger.warning(f"⚠️ Error en comparación visual: {str(e)}")
            return 1.0  # En caso de error, asumir diferentes
    
    def _merge_duplicate_tracks(self, face_tracks):
        """
        Fusiona tracks que corresponden a la misma persona
        Compara rostros de diferentes tracks usando similitud visual
        
        Args:
            face_tracks: Lista de tracks detectados
            
        Returns:
            list: Tracks fusionados (sin duplicados)
        """
        if len(face_tracks) <= 1:
            return face_tracks
        
        merged_tracks = []
        used_indices = set()
        
        for i, track_i in enumerate(face_tracks):
            if i in used_indices:
                continue
            
            # Este track será el "master" al que fusionaremos otros
            master_track = {
                'id': track_i['id'],
                'label': track_i['label'],
                'appearances': track_i['appearances'].copy(),
                'face_image': track_i.get('face_image')
            }
            
            # Buscar tracks similares para fusionar
            for j, track_j in enumerate(face_tracks):
                if j <= i or j in used_indices:
                    continue
                
                # Comparar rostros de referencia
                face_i = track_i.get('face_image')
                face_j = track_j.get('face_image')
                
                if face_i is None or face_j is None:
                    continue
                
                if face_i.size == 0 or face_j.size == 0:
                    continue
                
                try:
                    # Calcular similitud visual
                    similarity_score = self._calculate_visual_similarity(face_i, face_j)
                    
                    # Threshold MUY permisivo para fusionar duplicados (0.50)
                    # Aumentado de 0.38 a 0.50 para fusionar rostros con mayor variación
                    # Score < 0.50 = mismo rostro (50% de similitud)
                    if similarity_score < 0.50:
                        logger.info(f"🔗 Fusionando {track_i['label']} y {track_j['label']} (similitud: {similarity_score:.3f})")
                        
                        # Agregar apariciones del track duplicado al master
                        master_track['appearances'].extend(track_j['appearances'])
                        
                        # Marcar como usado
                        used_indices.add(j)
                    elif similarity_score < 0.60:
                        # Log de advertencia para similitudes cercanas al threshold
                        logger.warning(f"⚠️ {track_i['label']} y {track_j['label']} son similares (score: {similarity_score:.3f}) pero no fusionados")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Error comparando tracks {i} y {j}: {str(e)}")
                    continue
            
            # Ordenar apariciones por timestamp
            master_track['appearances'].sort(key=lambda x: x['timestamp'])
            
            merged_tracks.append(master_track)
            used_indices.add(i)
        
        # Re-etiquetar tracks fusionados
        for idx, track in enumerate(merged_tracks):
            track['id'] = idx + 1
            track['label'] = f'Persona {idx + 1}'
        
        return merged_tracks
    
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

    def _process_video_opencv_fallback(self, video_path):
        """
        Método fallback que usa solo OpenCV para detectar rostros (sin comparación)
        Asume 1 participante si detecta rostros
        """
        logger.info(f"🎥 Usando detección básica OpenCV (fallback mode)")
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception(f"No se pudo abrir el video: {video_path}")
            
            # Obtener información del video
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            # Cargar clasificador de rostros de OpenCV
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(cascade_path)
            
            frames_with_faces = 0
            frame_count = 0
            processed_frames = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Procesar cada 30 frames
                if frame_count % 30 == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                    
                    if len(faces) > 0:
                        frames_with_faces += 1
                    
                    processed_frames += 1
                
                frame_count += 1
            
            cap.release()
            
            # Calcular tiempo con rostros
            time_with_faces = (frames_with_faces / processed_frames) * duration if processed_frames > 0 else 0
            percentage = (time_with_faces / duration * 100) if duration > 0 else 0
            
            logger.info(f" Detección básica completada: {frames_with_faces}/{processed_frames} frames con rostros")
            
            # Retornar resultado asumiendo 1 participante
            return {
                'success': True,
                'participants': [{
                    'id': 'Participante 1',
                    'time_formatted': f"{int(time_with_faces // 60)}:{int(time_with_faces % 60):02d}",
                    'time_seconds': time_with_faces,
                    'percentage': percentage,
                    'appearances_count': frames_with_faces,
                    'first_seen': 0,
                    'last_seen': duration
                }],
                'total_participants': 1,
                'score': percentage,
                'frames_analyzed': processed_frames,
                'faces_detected': frames_with_faces,
                'detection_method': 'opencv_basic'
            }
            
        except Exception as e:
            logger.error(f" Error en detección OpenCV: {str(e)}")
            return {
                'success': False,
                'participants': [],
                'total_participants': 0,
                'score': 0,
                'error': str(e),
                'detection_method': 'opencv_basic'
            }

    def _process_video_mediapipe(self, video_path, presentation_id=None):
        """
        Método con MediaPipe - detecta múltiples rostros y los rastrea
        """
        logger.info(f" Usando detección MediaPipe para múltiples participantes")
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception(f"No se pudo abrir el video: {video_path}")
            
            # Obtener información del video
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            logger.info(f"📊 Video: {duration:.1f}s, {fps:.1f} FPS, {total_frames} frames")
            
            # Inicializar MediaPipe con parámetros MUY permisivos
            mp_face_detection = mp.solutions.face_detection
            face_detection = mp_face_detection.FaceDetection(
                min_detection_confidence=0.40,  # MUY permisivo - detecta rostros con poca confianza
                model_selection=1  # Modelo de largo alcance
            )
            
            # Inicializar Face Mesh para verificación adicional
            mp_face_mesh = mp.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=5,
                refine_landmarks=False,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            
            # Tracking de rostros
            face_tracks = []
            next_face_id = 1
            
            frame_count = 0
            processed_frames = 0
            frames_with_detections = 0  # Contador de frames con rostros detectados
            sample_rate = 3  # Procesar cada 3 frames (máxima frecuencia razonable)
            
            logger.info(f"🔍 Iniciando detección ULTRA-SENSIBLE... (procesando 1/{sample_rate} frames)")
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Procesar cada N frames
                if frame_count % sample_rate == 0:
                    timestamp = frame_count / fps
                    
                    # Convertir a RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Detectar rostros
                    results = face_detection.process(frame_rgb)
                    
                    if results.detections:
                        current_faces = []
                        frames_with_detections += 1  # Incrementar contador
                        
                        # Log detallado de detecciones (primeros 50 frames para no saturar)
                        if processed_frames < 50:
                            logger.info(f"⭐ Frame {frame_count} (t={timestamp:.1f}s): {len(results.detections)} rostro(s) DETECTADO(S) por MediaPipe")
                        
                        for detection in results.detections:
                            # Verificar score de confianza
                            confidence = detection.score[0]
                            if processed_frames < 50:
                                logger.info(f"   📊 Confianza del rostro: {confidence:.3f}")
                            
                            if confidence < 0.40:  # Umbral MUY permisivo de confianza
                                if processed_frames < 50:
                                    logger.warning(f"   🚫 DESCARTADO por baja confianza: {confidence:.3f} < 0.40")
                                continue
                            
                            # Obtener bounding box
                            bboxC = detection.location_data.relative_bounding_box
                            ih, iw, _ = frame.shape
                            
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
                                face_mesh_results = face_mesh.process(face_roi)
                                # Si Face Mesh no detecta landmarks faciales, probablemente no es un rostro humano
                                if not face_mesh_results.multi_face_landmarks:
                                    if processed_frames < 50:
                                        logger.warning(f"   🚫 DESCARTADO: Sin características faciales humanas (Face Mesh)")
                                    continue
                                elif processed_frames < 50:
                                    logger.info(f"   ✅ Face Mesh: Rostro humano confirmado")
                            
                            center_x = x + w // 2
                            center_y = y + h // 2
                            
                            # ✅ Rostro humano real detectado
                            if processed_frames < 50:
                                logger.info(f"   ✅ ACEPTADO: Rostro humano válido - conf={confidence:.3f}, size={w}x{h}, pos=({x},{y})")
                            
                            current_faces.append({
                                'center': (center_x, center_y),
                                'bbox': (x, y, w, h),
                                'timestamp': timestamp,
                                'frame': frame_count,
                                'confidence': confidence
                            })
                        
                        # Log de rostros aceptados en este frame
                        if processed_frames < 50:
                            logger.info(f"   🎯 Total rostros aceptados en este frame: {len(current_faces)}")
                        
                        # Actualizar tracks con algoritmo mejorado (distancia + similitud visual)
                        frame_diagonal = np.sqrt(iw**2 + ih**2)
                        spatial_threshold = frame_diagonal * 0.20  # Threshold espacial MUY permisivo
                        
                        used_tracks = set()
                        
                        for face in current_faces:
                            # Extraer imagen del rostro para comparación visual
                            x, y, w, h = face['bbox']
                            x = max(0, x)
                            y = max(0, y)
                            w = min(w, iw - x)
                            h = min(h, ih - y)
                            
                            # Extraer rostro con padding
                            padding = int(w * 0.2)
                            x1 = max(0, x - padding)
                            y1 = max(0, y - padding)
                            x2 = min(iw, x + w + padding)
                            y2 = min(ih, y + h + padding)
                            
                            current_face_img = frame[y1:y2, x1:x2]
                            
                            if current_face_img.size == 0:
                                continue
                            
                            best_match = None
                            best_score = float('inf')  # Menor es mejor
                            
                            for i, track in enumerate(face_tracks):
                                if i in used_tracks:
                                    continue
                                
                                # Buscar última aparición reciente (últimos 7 segundos - más permisivo)
                                recent_appearances = [a for a in track['appearances'] 
                                                     if timestamp - a['timestamp'] < 7.0]
                                
                                if not recent_appearances:
                                    continue
                                
                                last_appearance = recent_appearances[-1]
                                last_center = last_appearance['center']
                                
                                # 1. Calcular distancia espacial (normalizada 0-1)
                                spatial_distance = np.sqrt(
                                    (face['center'][0] - last_center[0])**2 + 
                                    (face['center'][1] - last_center[1])**2
                                )
                                spatial_score = min(1.0, spatial_distance / spatial_threshold)
                                
                                # 2. Calcular similitud visual usando histograma de color
                                try:
                                    reference_img = track.get('face_image')
                                    if reference_img is not None and reference_img.size > 0:
                                        visual_score = self._calculate_visual_similarity(
                                            reference_img, 
                                            current_face_img
                                        )
                                    else:
                                        visual_score = 1.0  # Asignar score neutro si no hay referencia
                                except Exception as e:
                                    visual_score = 1.0
                                
                                # 3. Score combinado: 60% visual + 40% espacial
                                # Menor score = mejor match
                                combined_score = (0.6 * visual_score) + (0.4 * spatial_score)
                                
                                if combined_score < best_score:
                                    best_score = combined_score
                                    best_match = i
                            
                            # Threshold MUY permisivo: score < 0.55 = mismo rostro
                            # Aumentado de 0.45 a 0.55 para evitar crear duplicados
                            if best_match is not None and best_score < 0.55:
                                face_tracks[best_match]['appearances'].append(face)
                                used_tracks.add(best_match)
                            else:
                                # Nuevo rostro detectado - capturar foto
                                face_image = current_face_img.copy()
                                
                                face_tracks.append({
                                    'id': next_face_id,
                                    'label': f'Persona {next_face_id}',
                                    'appearances': [face],
                                    'face_image': face_image  # Guardar imagen del rostro
                                })
                                logger.info(f"👤 Persona {next_face_id} detectada en t={timestamp:.1f}s - foto capturada")
                                next_face_id += 1
                    else:
                        # NO se detectaron rostros en este frame
                        if processed_frames < 50:
                            logger.warning(f"❌ Frame {frame_count} (t={timestamp:.1f}s): MediaPipe NO detectó ningún rostro")
                    
                    processed_frames += 1
                    
                    # Log de progreso más frecuente
                    if processed_frames % 30 == 0:
                        progress = (frame_count / total_frames) * 100
                        logger.info(f"⏳ Progreso: {progress:.1f}% ({frame_count}/{total_frames} frames) - {len(face_tracks)} persona(s) detectada(s)")
                
                frame_count += 1
            
            cap.release()
            face_detection.close()
            face_mesh.close()
            
            logger.info(f"")
            logger.info(f"=" * 80)
            logger.info(f"✅ DETECCIÓN FINALIZADA: {len(face_tracks)} tracks encontrados")
            logger.info(f"📹 Frames procesados: {processed_frames}")
            logger.info(f"✅ Frames CON rostros: {frames_with_detections} ({frames_with_detections/processed_frames*100:.1f}%)")
            logger.info(f"❌ Frames SIN rostros: {processed_frames - frames_with_detections} ({(processed_frames - frames_with_detections)/processed_frames*100:.1f}%)")
            logger.info(f"=" * 80)
            
            # Mostrar detalles de cada track ANTES de fusionar
            for idx, track in enumerate(face_tracks):
                logger.info(f"Track {idx+1}: {len(track['appearances'])} apariciones")
            
            # POST-PROCESAMIENTO: Fusionar tracks duplicados
            logger.info(f"")
            logger.info(f"🔄 Iniciando fusión de tracks duplicados...")
            face_tracks = self._merge_duplicate_tracks(face_tracks)
            logger.info(f"✅ Después de fusión: {len(face_tracks)} tracks únicos")
            logger.info(f"")
            
            # Mostrar TODOS los tracks detectados (incluso con pocas apariciones)
            logger.info(f"=" * 80)
            logger.info(f"📊 RESUMEN DE DETECCIONES:")
            logger.info(f"=" * 80)
            total_appearances = 0
            for track in face_tracks:
                appearances = len(track['appearances'])
                total_appearances += appearances
                time_seconds = (appearances * sample_rate) / fps
                logger.info(f"   🔍 {track['label']}: {appearances} apariciones ({time_seconds:.1f}s)")
            
            logger.info(f"")
            logger.info(f"📈 Total de apariciones registradas: {total_appearances}")
            logger.info(f"📹 Total de frames procesados: {processed_frames}")
            if processed_frames > 0:
                logger.info(f"📊 Promedio de rostros por frame procesado: {total_appearances / processed_frames:.2f}")
            logger.info(f"")
            
            # Filtrar tracks con muy pocas apariciones o tiempo muy corto (ruido)
            # MÍNIMO 0.3 SEGUNDOS de tiempo en pantalla para ser considerado participante válido
            min_time_seconds = 0.3  # Reducido de 0.5 a 0.3 para detectar apariciones MUY breves
            valid_tracks = []
            
            logger.info(f"=" * 80)
            logger.info(f"🔍 FILTRADO DE TRACKS (mínimo {min_time_seconds}s):")
            logger.info(f"🎬 FPS del video: {fps:.2f}")
            logger.info(f"📊 Sample rate: {sample_rate} (procesa 1 de cada {sample_rate} frames)")
            logger.info(f"=" * 80)
            
            for track in face_tracks:
                appearances = len(track['appearances'])
                time_seconds = (appearances * sample_rate) / fps
                
                logger.info(f"")
                logger.info(f"🔍 Evaluando {track['label']}:")
                logger.info(f"   📊 Apariciones: {appearances}")
                logger.info(f"   🧮 Cálculo: ({appearances} × {sample_rate}) / {fps:.2f} = {time_seconds:.3f}s")
                logger.info(f"   ⚖️  Comparación: {time_seconds:.3f}s >= {min_time_seconds}s? {time_seconds >= min_time_seconds}")
                
                if time_seconds >= min_time_seconds:
                    valid_tracks.append(track)
                    logger.info(f"   ✅ ACEPTADO")
                else:
                    logger.info(f"   🚫 DESCARTADO (tiempo insuficiente)")
            
            logger.info(f"")
            logger.info(f"✅ Participantes válidos totales: {len(valid_tracks)}")
            logger.info(f"")
            
            # Crear directorio para fotos si no existe
            if presentation_id:
                photos_dir = os.path.join(settings.MEDIA_ROOT, 'participant_photos', str(presentation_id))
                os.makedirs(photos_dir, exist_ok=True)
                logger.info(f"📁 Directorio de fotos: {photos_dir}")
            
            # Analizar resultados
            participants = []
            
            for idx, track in enumerate(valid_tracks):
                appearances_count = len(track['appearances'])
                time_seconds = (appearances_count * sample_rate) / fps
                percentage = (time_seconds / duration * 100) if duration > 0 else 0
                
                minutes = int(time_seconds // 60)
                seconds = int(time_seconds % 60)
                
                # Guardar foto del participante
                photo_filename = None
                if presentation_id and 'face_image' in track and track['face_image'] is not None:
                    photo_filename = f"participant_{idx + 1}.jpg"
                    photo_path = os.path.join(photos_dir, photo_filename)
                    
                    # Redimensionar foto a tamaño razonable (150x150)
                    face_img = track['face_image']
                    if face_img.size > 0:
                        try:
                            # Redimensionar manteniendo aspecto
                            h, w = face_img.shape[:2]
                            size = 150
                            if h > w:
                                new_h = size
                                new_w = int(w * (size / h))
                            else:
                                new_w = size
                                new_h = int(h * (size / w))
                            
                            face_img_resized = cv2.resize(face_img, (new_w, new_h))
                            
                            # Guardar
                            cv2.imwrite(photo_path, face_img_resized)
                            logger.info(f"📸 Foto guardada: {photo_filename}")
                        except Exception as e:
                            logger.error(f"❌ Error guardando foto: {e}")
                            photo_filename = None
                
                # Crear segmentos de tiempo
                appearances = track['appearances']
                segments = []
                appearances_with_intervals = []  # Para audio segmentation
                
                if appearances:
                    current_start = appearances[0]['timestamp']
                    last_time = current_start
                    time_per_frame = sample_rate / fps
                    
                    for app in appearances:
                        # Crear intervalo para cada aparición (para audio segmentation)
                        appearances_with_intervals.append({
                            'start_time': app['timestamp'],
                            'end_time': app['timestamp'] + time_per_frame,
                            'timestamp': app['timestamp']  # Mantener original
                        })
                    
                    # Crear segmentos continuos para visualización
                    current_start = appearances[0]['timestamp']
                    last_time = current_start
                    
                    for app in appearances[1:]:
                        # Nuevo segmento si hay más de 5 segundos de gap
                        if app['timestamp'] - last_time > 5:
                            segments.append({
                                'start': round(current_start, 1), 
                                'end': round(last_time + time_per_frame, 1)
                            })
                            current_start = app['timestamp']
                        last_time = app['timestamp']
                    
                    # Último segmento
                    segments.append({
                        'start': round(current_start, 1), 
                        'end': round(last_time + time_per_frame, 1)
                    })
                
                participants.append({
                    'id': track['label'],
                    'time_formatted': f"{minutes}:{seconds:02d}",
                    'time_seconds': round(time_seconds, 1),
                    'percentage': round(percentage, 1),
                    'appearances_count': appearances_count,
                    'first_seen': round(appearances[0]['timestamp'], 1) if appearances else 0,
                    'last_seen': round(appearances[-1]['timestamp'], 1) if appearances else 0,
                    'time_segments': segments,
                    'appearances': appearances_with_intervals,  # Para audio segmentation
                    'photo': f'participant_photos/{presentation_id}/{photo_filename}' if photo_filename else None
                })
                
                logger.info(f"📊 {track['label']}: {time_seconds:.1f}s ({percentage:.1f}%), {appearances_count} apariciones")
            
            # Ordenar por orden de aparición en el video (primera aparición = Persona 1)
            participants.sort(key=lambda x: x['first_seen'])
            
            # Re-etiquetar según orden de aparición en el video
            for idx, participant in enumerate(participants):
                old_id = participant['id']
                participant['id'] = f'Persona {idx + 1}'
                logger.info(f"🏷️  {old_id} → {participant['id']} (primera aparición: {participant['first_seen']:.1f}s)")
            
            # Calcular score de equidad
            if len(participants) > 1:
                percentages = [p['percentage'] for p in participants]
                max_diff = max(percentages) - min(percentages)
                score = max(0, 100 - max_diff * 2)
            else:
                score = participants[0]['percentage'] if participants else 0
            
            logger.info(f"🎯 Análisis completado: {len(participants)} participantes, Score: {score:.1f}/100")
            
            return {
                'success': True,
                'participants': participants,
                'total_participants': len(participants),
                'score': round(score, 1),
                'frames_analyzed': processed_frames,
                'faces_detected': sum(p['appearances_count'] for p in participants),
                'video_duration': duration,
                'detection_method': 'mediapipe'
            }
            
        except Exception as e:
            logger.error(f"❌ Error en MediaPipe: {str(e)}", exc_info=True)
            return {
                'success': False,
                'participants': [],
                'total_participants': 0,
                'score': 0,
                'error': str(e),
                'detection_method': 'mediapipe'
            }
