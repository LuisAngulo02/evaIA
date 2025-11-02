"""
Servicio de Cloudinary para gestión de archivos multimedia
Ubicación: apps/ai_processor/services/cloudinary_service.py
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)

class CloudinaryService:
    """
    Servicio para gestionar la subida, descarga y eliminación de archivos en Cloudinary
    """
    
    @staticmethod
    def is_configured():
        """Verificar si Cloudinary está configurado"""
        return all([
            os.getenv('CLOUDINARY_CLOUD_NAME'),
            os.getenv('CLOUDINARY_API_KEY'),
            os.getenv('CLOUDINARY_API_SECRET')
        ])
    
    @staticmethod
    def upload_video(video_file, folder='presentations', public_id=None):
        """
        Subir video a Cloudinary
        
        Args:
            video_file: Archivo de video (File object o ruta)
            folder: Carpeta destino en Cloudinary (default: 'presentations')
            public_id: ID público personalizado (opcional)
            
        Returns:
            dict: Información del video subido con keys:
                - public_id: ID único en Cloudinary
                - url: URL segura del video
                - secure_url: URL HTTPS
                - format: Formato del video
                - duration: Duración en segundos
                - size: Tamaño en bytes
                - width: Ancho del video
                - height: Alto del video
            None: Si falla la subida
        """
        if not CloudinaryService.is_configured():
            logger.error("❌ Cloudinary no está configurado")
            return None
        
        try:
            logger.info(f"📤 Subiendo video a Cloudinary...")
            
            upload_params = {
                'resource_type': 'video',
                'folder': folder,
                'chunk_size': 6000000,  # 6MB chunks para videos grandes
                'eager': [
                    {
                        'width': 1280,
                        'height': 720,
                        'crop': 'limit',
                        'quality': 'auto',
                        'fetch_format': 'auto'
                    }
                ],
                'eager_async': True,  # Procesamiento asíncrono
                'overwrite': True,
                'invalidate': True,
            }
            
            if public_id:
                upload_params['public_id'] = public_id
            
            result = cloudinary.uploader.upload(video_file, **upload_params)
            
            logger.info(f"✅ Video subido exitosamente: {result.get('public_id')}")
            
            return {
                'public_id': result.get('public_id'),
                'url': result.get('url'),
                'secure_url': result.get('secure_url'),
                'format': result.get('format'),
                'duration': result.get('duration'),
                'size': result.get('bytes'),
                'width': result.get('width'),
                'height': result.get('height'),
                'created_at': result.get('created_at'),
            }
            
        except cloudinary.exceptions.Error as e:
            logger.error(f"❌ Error de Cloudinary subiendo video: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error inesperado subiendo video: {e}")
            return None
    
    @staticmethod
    def upload_image(image_file, folder='participant_photos', public_id=None):
        """
        Subir imagen a Cloudinary
        
        Args:
            image_file: Archivo de imagen (File object o ruta)
            folder: Carpeta destino en Cloudinary (default: 'participant_photos')
            public_id: ID público personalizado (opcional)
            
        Returns:
            dict: Información de la imagen subida
            None: Si falla la subida
        """
        if not CloudinaryService.is_configured():
            logger.error("❌ Cloudinary no está configurado")
            return None
        
        try:
            logger.info(f"📤 Subiendo imagen a Cloudinary...")
            
            upload_params = {
                'resource_type': 'image',
                'folder': folder,
                'transformation': [
                    {
                        'width': 800,
                        'height': 800,
                        'crop': 'limit',
                        'quality': 'auto',
                        'fetch_format': 'auto'
                    }
                ],
                'overwrite': True,
            }
            
            if public_id:
                upload_params['public_id'] = public_id
            
            result = cloudinary.uploader.upload(image_file, **upload_params)
            
            logger.info(f"✅ Imagen subida exitosamente: {result.get('public_id')}")
            
            return {
                'public_id': result.get('public_id'),
                'url': result.get('url'),
                'secure_url': result.get('secure_url'),
                'format': result.get('format'),
                'size': result.get('bytes'),
                'width': result.get('width'),
                'height': result.get('height'),
            }
            
        except cloudinary.exceptions.Error as e:
            logger.error(f"❌ Error de Cloudinary subiendo imagen: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error inesperado subiendo imagen: {e}")
            return None
    
    @staticmethod
    def delete_file(public_id, resource_type='video'):
        """
        Eliminar archivo de Cloudinary
        
        Args:
            public_id: ID del archivo en Cloudinary
            resource_type: Tipo de recurso ('video', 'image', 'raw')
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if not CloudinaryService.is_configured():
            logger.error("❌ Cloudinary no está configurado")
            return False
        
        try:
            result = cloudinary.uploader.destroy(
                public_id,
                resource_type=resource_type,
                invalidate=True
            )
            
            if result.get('result') == 'ok':
                logger.info(f"✅ Archivo eliminado de Cloudinary: {public_id}")
                return True
            elif result.get('result') == 'not found':
                logger.warning(f"⚠️ Archivo no encontrado en Cloudinary: {public_id}")
                return False
            else:
                logger.warning(f"⚠️ No se pudo eliminar el archivo: {public_id} - {result}")
                return False
                
        except cloudinary.exceptions.Error as e:
            logger.error(f"❌ Error de Cloudinary eliminando archivo: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado eliminando archivo: {e}")
            return False
    
    @staticmethod
    def get_video_thumbnail_url(public_id, transformation=None):
        """
        Obtener URL de thumbnail (miniatura) de un video en Cloudinary
        
        Args:
            public_id: ID público del video
            transformation: Diccionario con transformaciones adicionales opcionales
            
        Returns:
            str: URL del thumbnail o None si falla
        """
        if not CloudinaryService.is_configured():
            logger.error("❌ Cloudinary no está configurado")
            return None
        
        try:
            from cloudinary import CloudinaryVideo
            
            # Transformación por defecto para thumbnail: primer frame del video, 320x180
            default_transformation = {
                'start_offset': '0',  # Primer frame
                'width': 320,
                'height': 180,
                'crop': 'fill',
                'gravity': 'auto',
                'quality': 'auto',
                'fetch_format': 'jpg'  # Convertir a imagen JPG
            }
            
            # Combinar con transformaciones personalizadas si las hay
            if transformation:
                default_transformation.update(transformation)
            
            # Generar URL con formato de imagen (no video)
            url = CloudinaryVideo(public_id).build_url(
                transformation=default_transformation,
                format='jpg'  # Forzar formato de imagen
            )
            
            return url
                
        except Exception as e:
            logger.error(f"❌ Error obteniendo thumbnail del video: {e}")
            return None
    
    @staticmethod
    def get_video_url(public_id, transformation=None):
        """
        Obtener URL del video en Cloudinary con transformaciones opcionales
        
        Args:
            public_id: ID público del video
            transformation: Diccionario con transformaciones opcionales
                Ejemplo: {'width': 640, 'height': 480, 'crop': 'fill'}
            
        Returns:
            str: URL del video o None si falla
        """
        if not CloudinaryService.is_configured():
            logger.error("❌ Cloudinary no está configurado")
            return None
        
        try:
            from cloudinary import CloudinaryVideo
            
            if transformation:
                return CloudinaryVideo(public_id).build_url(transformation=transformation)
            else:
                return CloudinaryVideo(public_id).build_url()
                
        except Exception as e:
            logger.error(f"❌ Error obteniendo URL del video: {e}")
            return None
    
    @staticmethod
    def get_image_url(public_id, transformation=None):
        """
        Obtener URL de imagen en Cloudinary con transformaciones opcionales
        
        Args:
            public_id: ID público de la imagen
            transformation: Diccionario con transformaciones opcionales
                Ejemplo: {'width': 300, 'height': 300, 'crop': 'thumb', 'gravity': 'face'}
            
        Returns:
            str: URL de la imagen o None si falla
        """
        if not CloudinaryService.is_configured():
            logger.error("❌ Cloudinary no está configurado")
            return None
        
        try:
            from cloudinary import CloudinaryImage
            
            if transformation:
                return CloudinaryImage(public_id).build_url(transformation=transformation)
            else:
                return CloudinaryImage(public_id).build_url()
                
        except Exception as e:
            logger.error(f"❌ Error obteniendo URL de la imagen: {e}")
            return None
    
    @staticmethod
    def get_file_info(public_id, resource_type='video'):
        """
        Obtener información de un archivo en Cloudinary
        
        Args:
            public_id: ID del archivo
            resource_type: Tipo de recurso ('video', 'image', 'raw')
            
        Returns:
            dict: Información del archivo o None si no existe
        """
        if not CloudinaryService.is_configured():
            logger.error("❌ Cloudinary no está configurado")
            return None
        
        try:
            result = cloudinary.api.resource(public_id, resource_type=resource_type)
            
            return {
                'public_id': result.get('public_id'),
                'format': result.get('format'),
                'size': result.get('bytes'),
                'width': result.get('width'),
                'height': result.get('height'),
                'duration': result.get('duration'),
                'created_at': result.get('created_at'),
                'url': result.get('secure_url'),
            }
            
        except cloudinary.exceptions.NotFound:
            logger.warning(f"⚠️ Archivo no encontrado: {public_id}")
            return None
        except Exception as e:
            logger.error(f"❌ Error obteniendo información del archivo: {e}")
            return None
    
    @staticmethod
    def test_connection():
        """
        Probar conexión con Cloudinary
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        if not CloudinaryService.is_configured():
            logger.error("❌ Cloudinary no está configurado")
            return False
        
        try:
            result = cloudinary.api.ping()
            logger.info(f"✅ Conexión exitosa con Cloudinary: {result}")
            return True
        except Exception as e:
            logger.error(f"❌ Error conectando con Cloudinary: {e}")
            return False