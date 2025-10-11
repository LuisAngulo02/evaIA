"""
Servicio de Detección de Liveness (Video en Vivo vs Pregrabado)
================================================================

Este servicio analiza videos para determinar si fueron grabados en vivo
o corresponden a material previamente grabado.

Métodos de detección:
1. Análisis de ruido de cámara (videos en vivo tienen más ruido)
2. Variaciones de brillo y luz natural
3. Análisis de metadatos del archivo
4. Patrones de compresión de video
5. Análisis temporal de frames

Utiliza:
- OpenCV para análisis de frames
- NumPy para cálculos estadísticos
- Análisis de metadatos de video
"""

import cv2
import numpy as np
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class LivenessDetectionService:
    """
    Servicio para detectar si un video es grabación en vivo o pregrabado
    """
    
    def __init__(self):
        """
        Inicializa el servicio de detección de liveness
        """
        self.max_frames_to_analyze = 300  # Analizar primeros 10 segundos (a 30fps)
        
    def analyze_video(self, video_path):
        """
        Analiza un video para determinar si es en vivo o pregrabado
        
        Args:
            video_path (str): Ruta al archivo de video
            
        Returns:
            dict: Resultados del análisis de liveness
        """
        logger.info(f"🔍 Iniciando análisis de liveness para: {video_path}")
        
        try:
            # 1. Análisis de metadatos del archivo
            metadata_score = self._analyze_metadata(video_path)
            
            # 2. Análisis de características del video
            video_features = self._analyze_video_features(video_path)
            
            # 3. Calcular score final y determinar tipo
            final_score = self._calculate_liveness_score(metadata_score, video_features)
            
            # Determinar si es en vivo
            is_live = final_score >= 50  # Umbral: 50%
            confidence = final_score if is_live else (100 - final_score)
            
            # Determinar tipo de grabación
            if final_score >= 75:
                recording_type = 'LIVE'
                type_display = 'En Vivo'
            elif final_score >= 50:
                recording_type = 'LIKELY_LIVE'
                type_display = 'Probablemente en Vivo'
            elif final_score >= 25:
                recording_type = 'LIKELY_RECORDED'
                type_display = 'Probablemente Pregrabado'
            else:
                recording_type = 'RECORDED'
                type_display = 'Pregrabado'
            
            result = {
                'success': True,
                'is_live': is_live,
                'liveness_score': round(final_score, 2),
                'confidence': round(confidence, 2),
                'recording_type': recording_type,
                'type_display': type_display,
                'details': {
                    'metadata_score': round(metadata_score, 2),
                    'noise_level': round(video_features['noise_level'], 2),
                    'brightness_variation': round(video_features['brightness_variation'], 2),
                    'motion_consistency': round(video_features['motion_consistency'], 2),
                    'temporal_consistency': round(video_features['temporal_consistency'], 2)
                }
            }
            
            logger.info(f"✅ Liveness análisis completado: {type_display} ({final_score:.1f}%)")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en análisis de liveness: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'is_live': False,
                'liveness_score': 0,
                'confidence': 0,
                'recording_type': 'UNKNOWN',
                'type_display': 'Desconocido'
            }
    
    def _analyze_metadata(self, video_path):
        """
        Analiza metadatos del archivo para detectar indicios de grabación en vivo
        
        Args:
            video_path (str): Ruta al archivo
            
        Returns:
            float: Score de 0-100 (mayor = más probable en vivo)
        """
        score = 50  # Score base neutral
        
        try:
            # Obtener información del archivo
            file_stat = os.stat(video_path)
            creation_time = datetime.fromtimestamp(file_stat.st_ctime)
            modification_time = datetime.fromtimestamp(file_stat.st_mtime)
            
            # Si el archivo fue creado y modificado casi al mismo tiempo,
            # es más probable que sea grabación en vivo
            time_diff = abs((modification_time - creation_time).total_seconds())
            
            if time_diff < 5:  # Menos de 5 segundos de diferencia
                score += 20
            elif time_diff < 30:  # Menos de 30 segundos
                score += 10
            elif time_diff > 300:  # Más de 5 minutos
                score -= 20
            
            # Obtener propiedades del video con OpenCV
            cap = cv2.VideoCapture(video_path)
            
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = frame_count / fps if fps > 0 else 0
                
                # Videos en vivo suelen tener FPS estándar (30, 60)
                if fps in [30, 60, 25, 50]:
                    score += 10
                
                # Videos muy cortos o muy largos son sospechosos
                if duration < 30:  # Menos de 30 segundos
                    score -= 10
                elif 60 <= duration <= 600:  # 1-10 minutos (rango normal)
                    score += 5
                
                cap.release()
            
        except Exception as e:
            logger.warning(f"⚠️ Error analizando metadatos: {str(e)}")
        
        return max(0, min(100, score))
    
    def _analyze_video_features(self, video_path):
        """
        Analiza características visuales del video
        
        Args:
            video_path (str): Ruta al video
            
        Returns:
            dict: Características analizadas
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise Exception(f"No se pudo abrir el video: {video_path}")
        
        noise_levels = []
        brightness_variations = []
        motion_variations = []
        
        prev_frame = None
        prev_gray = None
        frame_count = 0
        
        logger.info("📊 Analizando características del video...")
        
        while cap.isOpened() and frame_count < self.max_frames_to_analyze:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 1. Calcular nivel de ruido
            noise = self._calculate_noise_level(gray)
            noise_levels.append(noise)
            
            # 2. Calcular variación de brillo
            if prev_gray is not None:
                brightness_diff = np.mean(np.abs(gray.astype(float) - prev_gray.astype(float)))
                brightness_variations.append(brightness_diff)
            
            # 3. Calcular variación de movimiento (flujo óptico simplificado)
            if prev_gray is not None:
                motion = self._calculate_motion_variation(gray, prev_gray)
                motion_variations.append(motion)
            
            prev_frame = frame
            prev_gray = gray
            frame_count += 1
            
            # Log de progreso cada 100 frames
            if frame_count % 100 == 0:
                logger.info(f"⏳ Analizados {frame_count} frames...")
        
        cap.release()
        
        # Calcular promedios y estadísticas
        avg_noise = np.mean(noise_levels) if noise_levels else 0
        std_noise = np.std(noise_levels) if noise_levels else 0
        
        avg_brightness_var = np.mean(brightness_variations) if brightness_variations else 0
        std_brightness = np.std(brightness_variations) if brightness_variations else 0
        
        avg_motion = np.mean(motion_variations) if motion_variations else 0
        std_motion = np.std(motion_variations) if motion_variations else 0
        
        logger.info(f"✅ Análisis completado: {frame_count} frames procesados")
        
        return {
            'noise_level': avg_noise,
            'noise_std': std_noise,
            'brightness_variation': avg_brightness_var,
            'brightness_std': std_brightness,
            'motion_consistency': avg_motion,
            'motion_std': std_motion,
            'temporal_consistency': self._calculate_temporal_consistency(
                noise_levels, brightness_variations, motion_variations
            )
        }
    
    def _calculate_noise_level(self, image):
        """
        Calcula el nivel de ruido en una imagen usando Laplacian
        Videos en vivo tienden a tener más ruido que videos pregrabados comprimidos
        
        Args:
            image: Imagen en escala de grises
            
        Returns:
            float: Nivel de ruido normalizado (0-100)
        """
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        variance = laplacian.var()
        
        # Normalizar a escala 0-100
        # Valores típicos: 50-500 para video en vivo, 10-100 para pregrabado
        normalized = min(100, (variance / 5))
        
        return normalized
    
    def _calculate_motion_variation(self, current_gray, prev_gray):
        """
        Calcula la variación de movimiento entre frames
        
        Args:
            current_gray: Frame actual en escala de grises
            prev_gray: Frame anterior en escala de grises
            
        Returns:
            float: Variación de movimiento
        """
        # Calcular diferencia absoluta
        diff = cv2.absdiff(current_gray, prev_gray)
        motion_score = np.mean(diff)
        
        return motion_score
    
    def _calculate_temporal_consistency(self, noise_levels, brightness_variations, motion_variations):
        """
        Calcula la consistencia temporal de las características
        Videos en vivo tienen más variabilidad natural
        
        Args:
            noise_levels: Lista de niveles de ruido
            brightness_variations: Lista de variaciones de brillo
            motion_variations: Lista de variaciones de movimiento
            
        Returns:
            float: Score de consistencia temporal (0-100)
        """
        score = 50  # Base neutral
        
        try:
            # Videos en vivo tienen más variabilidad
            if noise_levels:
                noise_variability = np.std(noise_levels) / (np.mean(noise_levels) + 1e-6)
                if noise_variability > 0.2:  # Alta variabilidad
                    score += 15
                elif noise_variability < 0.05:  # Muy constante (sospechoso)
                    score -= 15
            
            if brightness_variations:
                brightness_variability = np.std(brightness_variations) / (np.mean(brightness_variations) + 1e-6)
                if brightness_variability > 0.3:
                    score += 10
                elif brightness_variability < 0.1:
                    score -= 10
            
            if motion_variations:
                motion_variability = np.std(motion_variations) / (np.mean(motion_variations) + 1e-6)
                if motion_variability > 0.4:
                    score += 10
        
        except Exception as e:
            logger.warning(f"⚠️ Error calculando consistencia temporal: {str(e)}")
        
        return max(0, min(100, score))
    
    def _calculate_liveness_score(self, metadata_score, video_features):
        """
        Calcula el score final de liveness combinando todas las métricas
        
        Args:
            metadata_score: Score de metadatos (0-100)
            video_features: Diccionario con características del video
            
        Returns:
            float: Score final (0-100)
        """
        # Pesos para cada factor
        weights = {
            'metadata': 0.20,
            'noise': 0.25,
            'brightness': 0.20,
            'motion': 0.15,
            'temporal': 0.20
        }
        
        # Normalizar características a escala 0-100
        noise_score = min(100, video_features['noise_level'] * 2)  # Mayor ruido = más probable en vivo
        brightness_score = min(100, video_features['brightness_variation'] * 1.5)
        motion_score = min(100, video_features['motion_consistency'] * 1.2)
        temporal_score = video_features['temporal_consistency']
        
        # Calcular score ponderado
        final_score = (
            metadata_score * weights['metadata'] +
            noise_score * weights['noise'] +
            brightness_score * weights['brightness'] +
            motion_score * weights['motion'] +
            temporal_score * weights['temporal']
        )
        
        return max(0, min(100, final_score))
    
    def get_liveness_summary(self, result):
        """
        Genera un resumen textual del análisis de liveness
        
        Args:
            result (dict): Resultado del análisis
            
        Returns:
            str: Resumen formateado
        """
        if not result['success']:
            return f"❌ Error en análisis: {result.get('error', 'Unknown')}"
        
        summary = f"🎥 **Análisis de Autenticidad de Grabación**\n\n"
        summary += f"**Tipo detectado:** {result['type_display']}\n"
        summary += f"**Score de Liveness:** {result['liveness_score']:.1f}/100\n"
        summary += f"**Confianza:** {result['confidence']:.1f}%\n\n"
        
        # Emoji según el tipo
        if result['recording_type'] == 'LIVE':
            summary += "✅ El video muestra características consistentes con grabación en vivo\n\n"
        elif result['recording_type'] == 'LIKELY_LIVE':
            summary += "⚠️ El video probablemente fue grabado en vivo, pero hay algunas inconsistencias\n\n"
        elif result['recording_type'] == 'LIKELY_RECORDED':
            summary += "⚠️ El video probablemente fue pregrabado y editado\n\n"
        else:
            summary += "❌ El video muestra características de material pregrabado\n\n"
        
        # Detalles técnicos
        if 'details' in result:
            details = result['details']
            summary += "**Detalles del análisis:**\n"
            summary += f"• Nivel de ruido: {details['noise_level']:.1f}/100\n"
            summary += f"• Variación de brillo: {details['brightness_variation']:.1f}/100\n"
            summary += f"• Consistencia de movimiento: {details['motion_consistency']:.1f}/100\n"
            summary += f"• Consistencia temporal: {details['temporal_consistency']:.1f}/100\n"
        
        return summary
