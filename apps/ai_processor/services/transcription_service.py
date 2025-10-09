# apps/ai_processor/services/transcription_service.py
import whisper
import os
import tempfile
import logging
from django.conf import settings

try:
    from moviepy.editor import VideoFileClip
    import moviepy.config as mp_config
    import imageio_ffmpeg
    # Configurar FFmpeg para MoviePy
    mp_config.FFMPEG_BINARY = imageio_ffmpeg.get_ffmpeg_exe()
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self):
        # Usar modelo base (balance entre velocidad y precisión)
        self.model = whisper.load_model("base")
    
    def extract_audio_from_video(self, video_path):
        """
        Extrae el audio de un video y lo guarda como archivo temporal
        """
        if not MOVIEPY_AVAILABLE:
            raise Exception("MoviePy no está disponible. No se puede extraer audio del video.")
        
        try:
            # Crear archivo temporal para el audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio_path = temp_audio.name
            
            # Extraer audio del video
            video = VideoFileClip(video_path)
            
            # Verificar que el video tenga audio
            if video.audio is None:
                video.close()
                raise Exception(f"El video {video_path} no contiene audio")
            
            audio = video.audio
            audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
            
            # Limpiar memoria
            audio.close()
            video.close()
            
            return temp_audio_path
            
        except Exception as e:
            logger.error(f"Error extrayendo audio: {str(e)}")
            raise Exception(f"No se pudo extraer audio del video: {str(e)}")
    
    def transcribe_audio(self, audio_path):
        """
        Transcribe un archivo de audio usando Whisper
        """
        try:
            # Transcribir con Whisper
            result = self.model.transcribe(
                audio_path,
                language="es",  # Español
                word_timestamps=True,  # Timestamps por palabra
                verbose=False
            )
            
            return {
                'text': result['text'],
                'segments': result['segments'],
                'language': result['language']
            }
            
        except Exception as e:
            logger.error(f"Error en transcripción: {str(e)}")
            raise Exception(f"Error transcribiendo audio: {str(e)}")
    
    def transcribe_video(self, video_path):
        """
        Transcribe un video completo (extrae audio + transcribe)
        """
        audio_path = None
        try:
            # 1. Extraer audio del video
            logger.info(f"Extrayendo audio de: {video_path}")
            audio_path = self.extract_audio_from_video(video_path)
            
            # 2. Transcribir audio
            logger.info("Iniciando transcripción...")
            transcription = self.transcribe_audio(audio_path)
            
            # 3. Procesar segmentos para mejor formato
            processed_segments = []
            for segment in transcription['segments']:
                processed_segments.append({
                    'start_time': segment['start'],
                    'end_time': segment['end'],
                    'text': segment['text'].strip(),
                    'speaker': None  # Se asignará más tarde con detección de hablantes
                })
            
            return {
                'full_text': transcription['text'],
                'segments': processed_segments,
                'language': transcription['language'],
                'duration': processed_segments[-1]['end_time'] if processed_segments else 0
            }
            
        except Exception as e:
            logger.error(f"Error transcribiendo video: {str(e)}")
            raise e
        
        finally:
            # Limpiar archivo temporal de audio
            if audio_path and os.path.exists(audio_path):
                try:
                    os.unlink(audio_path)
                except:
                    pass

    def format_transcription_for_display(self, segments):
        """
        Formatea la transcripción para mostrar en la interfaz
        """
        formatted_text = ""
        for segment in segments:
            start_min = int(segment['start_time'] // 60)
            start_sec = int(segment['start_time'] % 60)
            
            formatted_text += f"[{start_min:02d}:{start_sec:02d}] {segment['text']}\n"
        
        return formatted_text