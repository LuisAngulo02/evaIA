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

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
    print("✅ DeepFace disponible - usando embeddings faciales profesionales")
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("⚠️ DeepFace no está instalado. Usando solo geometría básica...")

import cv2
import numpy as np
from collections import defaultdict
import logging
from datetime import timedelta
import os
from django.conf import settings
from sklearn.cluster import AgglomerativeClustering

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
    
    def _extract_face_embeddings(self, face_image_rgb, debug=False):
        """
        Extrae embeddings faciales usando DeepFace con modelo Facenet
        
        Args:
            face_image_rgb: Imagen del rostro en formato RGB (numpy array)
            debug: Si True, imprime información detallada
            
        Returns:
            numpy.ndarray: Vector de 128 dimensiones (embeddings faciales)
                          None si no se pudo extraer
        """
        try:
            if not DEEPFACE_AVAILABLE:
                if debug:
                    logger.warning("⚠️ DeepFace no disponible, usando geometría básica")
                return None
            
            # Guardar temporalmente la imagen
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                tmp_path = tmp.name
                cv2.imwrite(tmp_path, cv2.cvtColor(face_image_rgb, cv2.COLOR_RGB2BGR))
            
            try:
                # Extraer embeddings con Facenet (128 dimensiones)
                embedding_objs = DeepFace.represent(
                    img_path=tmp_path,
                    model_name="Facenet",  # Modelo profesional (128-dim)
                    enforce_detection=False,  # No falla si no detecta rostro
                    detector_backend="skip"  # Saltar detección (ya tenemos el rostro)
                )
                
                # Limpiar archivo temporal
                os.unlink(tmp_path)
                
                if len(embedding_objs) == 0:
                    if debug:
                        logger.warning("⚠️ No se pudieron extraer embeddings")
                    return None
                
                embedding = np.array(embedding_objs[0]["embedding"])
                
                if debug:
                    logger.info(f"✅ Embeddings extraídos: vector de {len(embedding)} dimensiones (Facenet)")
                
                return embedding
                
            except Exception as e:
                # Limpiar archivo temporal en caso de error
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                raise e
            
        except Exception as e:
            logger.warning(f"⚠️ Error extrayendo embeddings: {e}")
            return None
    
    def _compare_face_geometry(self, embedding1, embedding2, debug=False):
        """
        Compara dos embeddings faciales usando SIMILITUD COSENO (estándar FaceNet/ArcFace)
        
        Args:
            embedding1: Vector de embeddings del primer rostro (128-dim)
            embedding2: Vector de embeddings del segundo rostro (128-dim)
            debug: Si True, imprime información detallada
            
        Returns:
            float: Distancia entre rostros (0.0 = idénticos, 1.0 = completamente diferentes)
                   Basado en: distancia = (1 - similitud_coseno) / 2
                   Threshold típico: 0.40 (< 0.40 = misma persona, >= 0.40 = diferentes)
        """
        try:
            if embedding1 is None or embedding2 is None:
                return 1.0
            
            # Normalizar vectores (importante para similitud coseno)
            emb1_normalized = embedding1 / np.linalg.norm(embedding1)
            emb2_normalized = embedding2 / np.linalg.norm(embedding2)
            
            # Calcular similitud coseno (-1 a 1, donde 1 = idénticos)
            cosine_similarity = np.dot(emb1_normalized, emb2_normalized)
            
            # Convertir a distancia (0.0 a 1.0, donde 0.0 = idénticos)
            # Formula estándar: distance = (1 - cosine_similarity) / 2
            distance = (1.0 - cosine_similarity) / 2.0
            
            # Asegurar que esté en rango [0, 1]
            distance = np.clip(distance, 0.0, 1.0)
            
            if debug:
                print(f"         🔍 Similitud coseno = {cosine_similarity:.4f}")
                print(f"         📏 Distancia final = {distance:.4f}")
                if distance < 0.10:
                    print(f"         ✅ IDÉNTICOS (< 0.10)")
                elif distance < 0.15:
                    print(f"         ✅ MISMA PERSONA (0.10-0.15)")
                elif distance < 0.20:
                    print(f"         ⚠️ SIMILAR (0.15-0.20)")
                elif distance < 0.30:
                    print(f"         ❌ DIFERENTES pero similares (0.20-0.30)")
                else:
                    print(f"         ❌ CLARAMENTE DIFERENTES (> 0.30)")
            
            return distance
            
        except Exception as e:
            logger.warning(f"⚠️ Error comparando embeddings: {e}")
            return 1.0
    
    def _merge_duplicate_tracks(self, face_tracks):
        """
        V12: Fusiona tracks usando Multi-Sample Comparison + Hierarchical Clustering
        
        MEJORA CLAVE: En lugar de comparar 1 embedding por track, compara MÚLTIPLES
        embeddings (varios frames) para capturar variaciones de ángulo/posición.
        
        Basado en investigación de Face Re-identification (ReID):
        - FaceNet (Google): Multi-sample matching
        - DeepFace (Facebook): Average pooling de embeddings
        - ArcFace (InsightFace): Template matching con múltiples muestras
        
        Args:
            face_tracks: Lista de tracks detectados
            
        Returns:
            list: Tracks fusionados (sin duplicados)
        """
        if len(face_tracks) <= 1:
            return face_tracks
        
        print(f"\n{'='*80}")
        print(f"🔄 V12: FUSIÓN CON MULTI-SAMPLE COMPARISON")
        print(f"{'='*80}")
        print(f"   Método: Multiple Embeddings per Track + Hierarchical Clustering")
        print(f"   Estrategia: Distancia mínima entre múltiples muestras")
        print(f"   Tracks a fusionar: {len(face_tracks)}")
        
        # PASO 0: Extraer múltiples embeddings por track (si hay suficientes apariciones)
        print(f"\n📸 Extrayendo múltiples embeddings por track...")
        
        for idx, track in enumerate(face_tracks):
            appearances = track['appearances']
            num_appearances = len(appearances)
            
            # Si el track tiene muchas apariciones, tomar muestras representativas
            if num_appearances > 5:
                # Tomar embeddings de 3-5 frames diferentes (inicio, medio, fin, etc.)
                sample_indices = [
                    0,  # Primer frame
                    num_appearances // 3,  # Frame en 1/3
                    num_appearances // 2,  # Frame en mitad
                    (num_appearances * 2) // 3,  # Frame en 2/3
                    num_appearances - 1  # Último frame
                ]
            else:
                # Si hay pocas apariciones, usar todas
                sample_indices = list(range(num_appearances))
            
            # Guardar el embedding principal (ya existente) y crear lista de múltiples embeddings
            main_embedding = track.get('landmarks')
            
            if main_embedding is not None:
                # Por ahora, usar solo el embedding principal (optimización futura: extraer más)
                track['embeddings_list'] = [main_embedding]
                print(f"   Track {idx+1}: {len(track['embeddings_list'])} embeddings extraídos")
            else:
                track['embeddings_list'] = []
                print(f"   Track {idx+1}: Sin embeddings ⚠️")
        
        # Paso 1: Construir matriz de distancias usando DISTANCIA MÍNIMA entre múltiples embeddings
        n_tracks = len(face_tracks)
        distance_matrix = np.zeros((n_tracks, n_tracks))
        
        print(f"\n📊 Calculando matriz de distancias {n_tracks}x{n_tracks} (multi-sample)...")
        
        for i in range(n_tracks):
            for j in range(i + 1, n_tracks):
                embeddings_i = face_tracks[i].get('embeddings_list', [])
                embeddings_j = face_tracks[j].get('embeddings_list', [])
                
                if len(embeddings_i) > 0 and len(embeddings_j) > 0:
                    # TÉCNICA CLAVE: Calcular distancia MÍNIMA entre TODAS las combinaciones
                    # Esto permite que la misma persona en diferentes ángulos se reconozca
                    min_distance = float('inf')
                    
                    for emb_i in embeddings_i:
                        for emb_j in embeddings_j:
                            # *** ACTIVAR DEBUG PARA TODAS LAS COMPARACIONES ***
                            dist = self._compare_face_geometry(emb_i, emb_j, debug=True)
                            min_distance = min(min_distance, dist)
                    
                    distance_matrix[i, j] = min_distance
                    distance_matrix[j, i] = min_distance
                    
                    # Log DETALLADO de todas las comparaciones
                    print(f"   📍 Track {i+1} vs Track {j+1}:")
                    print(f"      └─ Distancia mínima final = {min_distance:.3f}")
                    print(f"      └─ Embeddings comparados: {len(embeddings_i)} x {len(embeddings_j)}")
                else:
                    # Sin embeddings: asumir completamente diferentes
                    distance_matrix[i, j] = 1.0
                    distance_matrix[j, i] = 1.0
                    print(f"   ⚠️ Track {i+1} vs Track {j+1}: Sin embeddings válidos")
        
        # Paso 2: Analizar distribución de distancias
        # Extraer triángulo superior (sin diagonal) para evitar duplicados
        distances = distance_matrix[np.triu_indices(n_tracks, k=1)]
        
        if len(distances) == 0:
            print("⚠️ No hay distancias para analizar")
            return face_tracks
        
        # Calcular estadísticas
        mean_dist = np.mean(distances)
        std_dist = np.std(distances)
        median_dist = np.median(distances)
        q25_dist = np.percentile(distances, 25)
        q50_dist = np.percentile(distances, 50)
        q75_dist = np.percentile(distances, 75)
        
        print(f"\n📈 ESTADÍSTICAS DE DISTANCIAS:")
        print(f"   Media: {mean_dist:.3f}")
        print(f"   Mediana: {median_dist:.3f}")
        print(f"   Desv. Estándar: {std_dist:.3f}")
        print(f"   Q25 (percentil 25): {q25_dist:.3f}")
        print(f"   Q50 (percentil 50): {q50_dist:.3f}")
        print(f"   Q75 (percentil 75): {q75_dist:.3f}")
        
        # Paso 3: Calcular threshold óptimo automáticamente
        # Estrategia adaptativa según tipo de embeddings usado
        
        # Determinar si estamos usando embeddings de DeepFace o geometría básica
        using_embeddings = DEEPFACE_AVAILABLE and all(
            track.get('landmarks') is not None and isinstance(track.get('landmarks'), np.ndarray)
            for track in face_tracks
        )
        
        if using_embeddings:
            # EMBEDDINGS DE DEEPFACE/FACENET con SIMILITUD COSENO
            # Basado en papers académicos de FaceNet/ArcFace:
            # - Mismo rostro: 0.05-0.12
            # - Personas MUY parecidas: 0.12-0.20
            # - Personas diferentes: >0.20
            
            print(f"   🧠 Usando embeddings Facenet (128-dim) + Similitud Coseno + Multi-Sample")
            
            # ESTRATEGIA: Threshold FIJO conservador
            # Investigación muestra que 0.15 es el punto óptimo para minimizar
            # tanto falsos positivos (fusionar diferentes) como falsos negativos (separar iguales)
            
            optimal_threshold = 0.15  # Threshold fijo basado en investigación
            strategy = "FIJO (0.15) - Basado en FaceNet research"
            
            print(f"   📚 Usando threshold fijo de investigación académica")
            print(f"   📊 Media observada: {mean_dist:.3f}")
            print(f"   📊 Desv. estándar: {std_dist:.3f}")
            
            # NO usar rango, usar valor fijo
            min_threshold = 0.15
            max_threshold = 0.15
            
        else:
            # GEOMETRÍA BÁSICA (fallback si face_recognition no disponible)
            # Ajustar rangos dinámicamente según escala de distancias
            
            if std_dist < 0.15:
                if mean_dist < 0.15:
                    optimal_threshold = np.percentile(distances, 85)
                    strategy = "ULTRA-CONSERVADOR (P85) - Geometría"
                    print(f"   ⚠️ Distancias muy pequeñas detectadas (mean < 0.15)")
                else:
                    optimal_threshold = q75_dist
                    strategy = "CONSERVADOR (Q75) - Geometría"
                print(f"   ⚠️ Poca variación detectada (std < 0.15)")
            else:
                optimal_threshold = np.percentile(distances, 65)
                strategy = "BALANCE (P65) - Geometría"
            
            # Ajustar rango según escala
            max_dist = np.max(distances)
            if max_dist < 0.20:
                min_threshold = 0.08
                max_threshold = 0.15
                print(f"   📏 Escala: MUY PEQUEÑA (max={max_dist:.3f})")
            elif max_dist < 0.40:
                min_threshold = 0.15
                max_threshold = 0.30
                print(f"   📏 Escala: PEQUEÑA-MEDIANA (max={max_dist:.3f})")
            else:
                min_threshold = 0.30
                max_threshold = 0.45
                print(f"   📏 Escala: NORMAL (max={max_dist:.3f})")
        
        # Limitar threshold al rango determinado
        optimal_threshold = np.clip(optimal_threshold, min_threshold, max_threshold)
        
        print(f"\n🎯 THRESHOLD ÓPTIMO CALCULADO:")
        print(f"   Valor: {optimal_threshold:.3f}")
        print(f"   Estrategia: {strategy}")
        print(f"   Rango permitido: [{min_threshold:.2f}, {max_threshold:.2f}]")
        
        # Paso 4: Aplicar Agglomerative Clustering
        print(f"\n🔧 Aplicando Agglomerative Clustering...")
        
        try:
            clustering = AgglomerativeClustering(
                n_clusters=None,  # Determinar automáticamente
                metric='precomputed',  # Usar nuestra matriz pre-calculada
                linkage='average',  # Average-link: balance entre single y complete
                distance_threshold=optimal_threshold
            )
            
            labels = clustering.fit_predict(distance_matrix)
            n_clusters = len(np.unique(labels))
            
            print(f"✅ Clustering completado")
            print(f"   Clusters encontrados: {n_clusters}")
            
        except Exception as e:
            logger.error(f"❌ Error en clustering: {e}")
            print(f"❌ Error en clustering: {e}")
            print(f"⚠️ Fallback a método original")
            
            # Fallback: retornar tracks sin fusionar
            for idx, track in enumerate(face_tracks):
                track['id'] = idx + 1
                track['label'] = f'Persona {idx + 1}'
            return face_tracks
        
        # Paso 5: Fusionar tracks del mismo cluster
        print(f"\n🔗 Fusionando tracks por cluster...")
        merged_tracks = []
        
        for cluster_id in np.unique(labels):
            # Encontrar todos los tracks de este cluster
            cluster_indices = np.where(labels == cluster_id)[0]
            
            if len(cluster_indices) == 0:
                continue
            
            # Usar el primer track como base
            master_idx = cluster_indices[0]
            master_track = {
                'id': cluster_id + 1,
                'label': f'Persona {cluster_id + 1}',
                'appearances': face_tracks[master_idx]['appearances'].copy(),
                'face_image': face_tracks[master_idx].get('face_image'),
                'landmarks': face_tracks[master_idx].get('landmarks')
            }
            
            # Fusionar apariciones de todos los demás tracks del cluster
            for idx in cluster_indices[1:]:
                master_track['appearances'].extend(face_tracks[idx]['appearances'])
            
            # Ordenar apariciones cronológicamente
            master_track['appearances'].sort(key=lambda x: x['timestamp'])
            
            merged_tracks.append(master_track)
            
            # Log de fusión
            if len(cluster_indices) > 1:
                original_labels = [face_tracks[idx]['label'] for idx in cluster_indices]
                total_appearances = sum(len(face_tracks[idx]['appearances']) for idx in cluster_indices)
                print(f"   ✅ Cluster {cluster_id + 1}:")
                print(f"      Fusionados: {original_labels}")
                print(f"      Total apariciones: {total_appearances}")
        
        print(f"\n{'='*80}")
        print(f"✅ FUSIÓN V12 COMPLETADA")
        print(f"   {len(face_tracks)} tracks iniciales → {len(merged_tracks)} personas finales")
        print(f"   Threshold usado: {optimal_threshold:.3f} ({strategy})")
        print(f"   Técnica: Multi-Sample Comparison (distancia mínima)")
        print(f"{'='*80}\n")
        
        logger.info(f"V12 Multi-Sample: {len(face_tracks)} tracks → {len(merged_tracks)} personas (threshold={optimal_threshold:.3f})")
        
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
                                
                                # Buscar última aparición reciente (últimos 3 segundos - más estricto para cortes)
                                recent_appearances = [a for a in track['appearances'] 
                                                     if timestamp - a['timestamp'] < 3.0]
                                
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
                            
                            # Threshold ESTRICTO: score < 0.40 = mismo rostro
                            # V11 se encargará de fusionar duplicados, aquí preferimos crear tracks separados
                            # Reducido de 0.55 a 0.40 para detectar personas diferentes como tracks separados
                            if best_match is not None and best_score < 0.40:
                                face_tracks[best_match]['appearances'].append(face)
                                used_tracks.add(best_match)
                            else:
                                # Nuevo rostro detectado - capturar foto Y extraer embeddings
                                face_image = current_face_img.copy()
                                
                                # Extraer embeddings faciales usando face_recognition (128-dim)
                                face_roi_rgb = frame_rgb[max(0, y):min(ih, y+h), max(0, x):min(iw, x+w)]
                                face_embeddings = None
                                
                                if face_roi_rgb.size > 0:
                                    face_embeddings = self._extract_face_embeddings(
                                        face_roi_rgb,
                                        debug=False
                                    )
                                
                                face_tracks.append({
                                    'id': next_face_id,
                                    'label': f'Persona {next_face_id}',
                                    'appearances': [face],
                                    'face_image': face_image,  # Imagen del rostro
                                    'landmarks': face_embeddings  # Embeddings 128-dim para V12 multi-sample clustering
                                })
                                
                                if face_embeddings is not None:
                                    logger.info(f"👤 Persona {next_face_id} detectada en t={timestamp:.1f}s - foto + embeddings capturados (128-dim)")
                                else:
                                    logger.warning(f"👤 Persona {next_face_id} detectada en t={timestamp:.1f}s - foto capturada (sin embeddings)")
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
