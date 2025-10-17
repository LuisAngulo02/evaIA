"""
Validadores avanzados para archivos de presentaciones
======================================================
"""
import os
import cv2
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class VideoValidator:
    """
    Validador completo para archivos de video
    """
    
    # Configuración
    ALLOWED_FORMATS = ['mp4', 'webm', 'mov', 'avi']
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
    MIN_FILE_SIZE = 100 * 1024  # 100 KB
    MAX_DURATION = 30 * 60  # 30 minutos en segundos
    MIN_DURATION = 10  # 10 segundos
    MIN_WIDTH = 320
    MIN_HEIGHT = 240
    
    @staticmethod
    def validate_format(video_file):
        """
        Valida que el formato del video sea permitido
        
        Args:
            video_file: UploadedFile object
            
        Raises:
            ValidationError: Si el formato no es válido
        """
        # Obtener extensión del archivo
        file_name = video_file.name.lower()
        file_ext = file_name.split('.')[-1] if '.' in file_name else ''
        
        if file_ext not in VideoValidator.ALLOWED_FORMATS:
            raise ValidationError(
                f'❌ Formato de video no permitido: {file_ext}. '
                f'Formatos aceptados: {", ".join(VideoValidator.ALLOWED_FORMATS)}'
            )
        
        # Validar MIME type si está disponible
        if hasattr(video_file, 'content_type'):
            valid_mime_types = [
                'video/mp4',
                'video/webm',
                'video/quicktime',  # .mov
                'video/x-msvideo',  # .avi
            ]
            
            if video_file.content_type not in valid_mime_types:
                logger.warning(
                    f"MIME type no esperado: {video_file.content_type} "
                    f"para archivo {file_name}"
                )
    
    @staticmethod
    def validate_size(video_file):
        """
        Valida el tamaño del archivo
        
        Args:
            video_file: UploadedFile object
            
        Raises:
            ValidationError: Si el tamaño no es válido
        """
        file_size = video_file.size
        
        # Validar tamaño mínimo
        if file_size < VideoValidator.MIN_FILE_SIZE:
            raise ValidationError(
                f'❌ El archivo es demasiado pequeño ({file_size / 1024:.1f} KB). '
                f'Tamaño mínimo: {VideoValidator.MIN_FILE_SIZE / 1024:.0f} KB'
            )
        
        # Validar tamaño máximo
        if file_size > VideoValidator.MAX_FILE_SIZE:
            size_mb = file_size / (1024 * 1024)
            max_mb = VideoValidator.MAX_FILE_SIZE / (1024 * 1024)
            raise ValidationError(
                f'❌ El archivo es demasiado grande ({size_mb:.1f} MB). '
                f'Tamaño máximo permitido: {max_mb:.0f} MB'
            )
    
    @staticmethod
    def validate_video_properties(video_path):
        """
        Valida propiedades del video usando OpenCV
        
        Args:
            video_path: Ruta al archivo de video
            
        Returns:
            dict: Propiedades del video validadas
            
        Raises:
            ValidationError: Si el video está corrupto o no cumple requisitos
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValidationError(
                    '❌ No se pudo abrir el archivo de video. '
                    'El archivo puede estar corrupto o en un formato no soportado.'
                )
            
            # Obtener propiedades
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Calcular duración
            duration = total_frames / fps if fps > 0 else 0
            
            cap.release()
            
            # Validar que se obtuvieron valores válidos
            if fps <= 0 or total_frames <= 0 or width <= 0 or height <= 0:
                raise ValidationError(
                    '❌ El archivo de video está corrupto o no contiene datos válidos.'
                )
            
            # Validar duración
            if duration < VideoValidator.MIN_DURATION:
                raise ValidationError(
                    f'❌ El video es demasiado corto ({duration:.1f}s). '
                    f'Duración mínima: {VideoValidator.MIN_DURATION}s'
                )
            
            if duration > VideoValidator.MAX_DURATION:
                minutes = duration / 60
                max_minutes = VideoValidator.MAX_DURATION / 60
                raise ValidationError(
                    f'❌ El video es demasiado largo ({minutes:.1f} min). '
                    f'Duración máxima: {max_minutes:.0f} minutos'
                )
            
            # Validar resolución mínima
            if width < VideoValidator.MIN_WIDTH or height < VideoValidator.MIN_HEIGHT:
                raise ValidationError(
                    f'❌ Resolución demasiado baja ({width}x{height}). '
                    f'Mínimo requerido: {VideoValidator.MIN_WIDTH}x{VideoValidator.MIN_HEIGHT}'
                )
            
            logger.info(
                f"Video validado: {duration:.1f}s, {width}x{height}, "
                f"{fps:.1f} FPS, {total_frames} frames"
            )
            
            return {
                'duration': duration,
                'fps': fps,
                'width': width,
                'height': height,
                'total_frames': total_frames,
                'is_valid': True
            }
            
        except cv2.error as e:
            logger.error(f"Error OpenCV validando video: {str(e)}")
            raise ValidationError(
                f'❌ Error al validar el video: {str(e)}. '
                'El archivo puede estar corrupto.'
            )
        except Exception as e:
            logger.error(f"Error inesperado validando video: {str(e)}")
            raise ValidationError(
                f'❌ Error al procesar el video: {str(e)}'
            )
    
    @staticmethod
    def validate_video_integrity(video_path):
        """
        Verifica la integridad del video intentando leer algunos frames
        
        Args:
            video_path: Ruta al archivo de video
            
        Raises:
            ValidationError: Si el video está corrupto
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValidationError('❌ Video corrupto: no se puede abrir')
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Intentar leer 5 frames distribuidos por el video
            test_frames = [0, total_frames // 4, total_frames // 2, 
                          3 * total_frames // 4, total_frames - 1]
            
            for frame_num in test_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                
                if not ret or frame is None:
                    cap.release()
                    raise ValidationError(
                        f'❌ Video corrupto: no se pudo leer el frame {frame_num}/{total_frames}'
                    )
            
            cap.release()
            logger.info("Integridad del video verificada correctamente")
            
        except cv2.error as e:
            raise ValidationError(f'❌ Video corrupto: {str(e)}')
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f'❌ Error validando integridad: {str(e)}')
    
    @staticmethod
    def generate_thumbnail(video_path, output_path=None, time_position=2.0):
        """
        Genera un thumbnail del video
        
        Args:
            video_path: Ruta al archivo de video
            output_path: Ruta donde guardar el thumbnail (opcional)
            time_position: Posición en segundos para extraer el frame
            
        Returns:
            str: Ruta al thumbnail generado o None si falla
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                logger.error("No se pudo abrir el video para generar thumbnail")
                return None
            
            # Posicionar en el tiempo especificado
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_num = int(time_position * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret or frame is None:
                logger.error("No se pudo leer el frame para thumbnail")
                return None
            
            # Redimensionar a tamaño thumbnail (mantener aspect ratio)
            height, width = frame.shape[:2]
            max_width = 320
            
            if width > max_width:
                ratio = max_width / width
                new_width = max_width
                new_height = int(height * ratio)
                frame = cv2.resize(frame, (new_width, new_height))
            
            # Si no se especifica output_path, usar temporal
            if output_path is None:
                video_dir = os.path.dirname(video_path)
                video_name = os.path.splitext(os.path.basename(video_path))[0]
                output_path = os.path.join(video_dir, f'{video_name}_thumb.jpg')
            
            # Guardar thumbnail
            cv2.imwrite(output_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            
            logger.info(f"Thumbnail generado: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generando thumbnail: {str(e)}")
            return None
    
    @classmethod
    def validate_all(cls, video_file, video_path=None):
        """
        Ejecuta todas las validaciones
        
        Args:
            video_file: UploadedFile object
            video_path: Ruta al archivo guardado (para validaciones avanzadas)
            
        Returns:
            dict: Resultado de las validaciones
            
        Raises:
            ValidationError: Si alguna validación falla
        """
        result = {
            'format_valid': False,
            'size_valid': False,
            'properties_valid': False,
            'integrity_valid': False,
            'thumbnail_generated': False,
            'video_properties': None,
            'thumbnail_path': None
        }
        
        # Validación 1: Formato
        cls.validate_format(video_file)
        result['format_valid'] = True
        
        # Validación 2: Tamaño
        cls.validate_size(video_file)
        result['size_valid'] = True
        
        # Validaciones avanzadas (requieren archivo guardado)
        if video_path and os.path.exists(video_path):
            # Validación 3: Propiedades
            properties = cls.validate_video_properties(video_path)
            result['properties_valid'] = True
            result['video_properties'] = properties
            
            # Validación 4: Integridad
            cls.validate_video_integrity(video_path)
            result['integrity_valid'] = True
            
            # Generación de thumbnail
            thumbnail_path = cls.generate_thumbnail(video_path)
            if thumbnail_path:
                result['thumbnail_generated'] = True
                result['thumbnail_path'] = thumbnail_path
        
        return result


def validate_video_file(video_file):
    """
    Función de validación para usar en forms.py
    
    Args:
        video_file: UploadedFile object
        
    Raises:
        ValidationError: Si el video no es válido
    """
    validator = VideoValidator()
    
    # Validar formato
    validator.validate_format(video_file)
    
    # Validar tamaño
    validator.validate_size(video_file)
