import cloudinary
import cloudinary.uploader
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CloudinaryRotationService:
    """Servicio para rotar entre múltiples cuentas de Cloudinary"""
    
    _current_account_index = 0
    _upload_count = 0
    _uploads_per_account = 10  # Cambiar de cuenta cada 10 uploads
    
    @classmethod
    def get_current_account(cls):
        """Obtiene la cuenta actual de Cloudinary"""
        if not settings.CLOUDINARY_ACCOUNTS:
            return None
        return settings.CLOUDINARY_ACCOUNTS[cls._current_account_index]
    
    @classmethod
    def rotate_account(cls):
        """Rota a la siguiente cuenta de Cloudinary"""
        if len(settings.CLOUDINARY_ACCOUNTS) <= 1:
            return
        
        cls._current_account_index = (cls._current_account_index + 1) % len(settings.CLOUDINARY_ACCOUNTS)
        account = cls.get_current_account()
        
        # Reconfigurar Cloudinary con la nueva cuenta
        cloudinary.config(
            cloud_name=account['cloud_name'],
            api_key=account['api_key'],
            api_secret=account['api_secret'],
            secure=True
        )
        
        logger.info(f"Cloudinary rotado a cuenta: {account['name']} ({account['cloud_name']})")
    
    @classmethod
    def upload_with_rotation(cls, file, **options):
        """
        Sube un archivo a Cloudinary con rotación automática de cuentas
        
        Args:
            file: Archivo a subir
            **options: Opciones adicionales para cloudinary.uploader.upload
        
        Returns:
            Resultado del upload de Cloudinary
        """
        try:
            # Verificar si hay cuentas configuradas
            if not settings.CLOUDINARY_ACCOUNTS:
                raise Exception("No hay cuentas de Cloudinary configuradas")
            
            # Rotar cuenta si es necesario
            cls._upload_count += 1
            if cls._upload_count % cls._uploads_per_account == 0:
                cls.rotate_account()
            
            account = cls.get_current_account()
            logger.info(f"Subiendo archivo a Cloudinary ({account['name']})")
            
            # Subir archivo
            result = cloudinary.uploader.upload(file, **options)
            
            logger.info(f"Archivo subido exitosamente a {account['cloud_name']}")
            return result
            
        except Exception as e:
            logger.error(f"Error al subir archivo a Cloudinary: {str(e)}")
            
            # Intentar con la siguiente cuenta
            if len(settings.CLOUDINARY_ACCOUNTS) > 1:
                logger.info("Intentando con la siguiente cuenta...")
                cls.rotate_account()
                try:
                    result = cloudinary.uploader.upload(file, **options)
                    logger.info("Archivo subido en segundo intento")
                    return result
                except Exception as e2:
                    logger.error(f"Segundo intento fallido: {str(e2)}")
                    raise
            else:
                raise
    
    @classmethod
    def delete_with_rotation(cls, public_id, **options):
        """Elimina un archivo intentando con todas las cuentas"""
        for account in settings.CLOUDINARY_ACCOUNTS:
            try:
                cloudinary.config(
                    cloud_name=account['cloud_name'],
                    api_key=account['api_key'],
                    api_secret=account['api_secret'],
                    secure=True
                )
                result = cloudinary.uploader.destroy(public_id, **options)
                if result.get('result') == 'ok':
                    logger.info(f"Archivo eliminado de {account['cloud_name']}")
                    return result
            except Exception as e:
                logger.warning(f"No se pudo eliminar de {account['cloud_name']}: {str(e)}")
        
        logger.error(f"No se pudo eliminar el archivo {public_id} de ninguna cuenta")
        return {'result': 'not found'}