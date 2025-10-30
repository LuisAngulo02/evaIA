# apps/ai_processor/services/transcription_service.py
import whisper
import os
import tempfile
import logging
from django.conf import settings
# Reload trigger

logger = logging.getLogger(__name__)

try:
    from moviepy.editor import VideoFileClip
    import moviepy.config as mp_config
    import imageio_ffmpeg
    # Configurar FFmpeg para MoviePy
    mp_config.FFMPEG_BINARY = imageio_ffmpeg.get_ffmpeg_exe()
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

# ⚡ CONFIGURAR FFMPEG PARA WHISPER
try:
    import imageio_ffmpeg
    # Agregar el directorio de FFmpeg al PATH temporalmente
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_path)
    if ffmpeg_dir not in os.environ['PATH']:
        os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ['PATH']
    logger.info(f"✅ FFmpeg configurado para Whisper: {ffmpeg_path}")
    print(f"✅ FFmpeg configurado para Whisper: {ffmpeg_path}")
except Exception as e:
    logger.warning(f"⚠️ No se pudo configurar FFmpeg automáticamente: {e}")
    print(f"⚠️ No se pudo configurar FFmpeg automáticamente: {e}")

class TranscriptionService:
    def __init__(self):
        # Usar modelo pequeño (más rápido, menos preciso)
        # Especificar device explícitamente para evitar errores de meta tensor
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        try:
            self.model = whisper.load_model("small", device=device)
        except Exception as e:
            logger.warning(f"Error cargando modelo Whisper con device={device}: {e}")
            # Intentar con download_root explícito
            try:
                cache_dir = os.path.join(settings.BASE_DIR, '.whisper_cache')
                os.makedirs(cache_dir, exist_ok=True)
                self.model = whisper.load_model("small", device=device, download_root=cache_dir)
            except Exception as e2:
                logger.error(f"Error crítico cargando Whisper: {e2}")
                raise
    
    def extract_audio_from_video(self, video_path):
        """
        Extrae el audio de un video y lo guarda como archivo temporal
        Usa ffmpeg directamente para evitar problemas con WebM sin duración
        """
        import subprocess
        
        try:
            # Crear archivo temporal para el audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio_path = temp_audio.name
            
            # Obtener ffmpeg de imageio_ffmpeg (ya instalado)
            try:
                import imageio_ffmpeg
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                logger.info(f"✅ FFmpeg encontrado: {ffmpeg_path}")
            except Exception as e:
                logger.error(f"Error obteniendo ffmpeg: {str(e)}")
                raise Exception(f"FFmpeg no disponible. Instala: pip install imageio-ffmpeg")
            
            # Comando ffmpeg para extraer audio
            command = [
                ffmpeg_path,
                '-i', video_path,           # Input file
                '-vn',                       # No video
                '-acodec', 'pcm_s16le',     # Audio codec (WAV)
                '-ar', '16000',             # Sample rate (16kHz para Whisper)
                '-ac', '1',                  # Mono
                '-y',                        # Overwrite output
                temp_audio_path
            ]
            
            # Ejecutar comando
            logger.info(f"🎵 Extrayendo audio: {video_path} → {temp_audio_path}")
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300  # 5 minutos max
            )
            
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                raise Exception(f"FFmpeg falló al extraer audio: {result.stderr}")
            
            # Verificar que el archivo se creó
            if not os.path.exists(temp_audio_path) or os.path.getsize(temp_audio_path) == 0:
                raise Exception("El archivo de audio está vacío")
            
            logger.info(f"✅ Audio extraído exitosamente: {temp_audio_path}")
            return temp_audio_path
            
        except subprocess.TimeoutExpired:
            logger.error("Timeout al extraer audio")
            raise Exception("El proceso de extracción de audio tardó demasiado")
        except Exception as e:
            logger.error(f"Error extrayendo audio: {str(e)}")
            raise Exception(f"No se pudo extraer audio del video: {str(e)}")
    
    def transcribe_audio(self, audio_path):
        """
        Transcribe un archivo de audio usando Whisper
        Carga el audio manualmente para evitar problemas con FFmpeg en el PATH
        """
        import numpy as np
        import subprocess
        
        try:
            # Obtener FFmpeg path
            try:
                import imageio_ffmpeg
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            except:
                raise Exception("imageio-ffmpeg no disponible")
            
            # Cargar audio manualmente usando FFmpeg
            # Whisper espera audio en formato: numpy array float32, sample rate 16000Hz
            command = [
                ffmpeg_path,
                '-i', audio_path,
                '-f', 's16le',  # PCM signed 16-bit little-endian
                '-acodec', 'pcm_s16le',
                '-ar', '16000',  # Sample rate 16kHz
                '-ac', '1',      # Mono
                '-'              # Output to stdout
            ]
            
            logger.info("🎧 Cargando audio para Whisper...")
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            
            # Convertir bytes a numpy array
            audio_data = np.frombuffer(result.stdout, dtype=np.int16).astype(np.float32) / 32768.0
            logger.info(f"✅ Audio cargado: {len(audio_data)} samples")
            
            # Transcribir con Whisper usando el array numpy directamente
            logger.info("🤖 Iniciando transcripción con Whisper...")
            transcription_result = self.model.transcribe(
                audio_data,
                language="es",  # Español
                word_timestamps=True,  # Timestamps por palabra
                verbose=False
            )
            
            return {
                'text': transcription_result['text'],
                'segments': transcription_result['segments'],
                'language': transcription_result['language']
            }
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error en FFmpeg al cargar audio: {e.stderr.decode() if e.stderr else str(e)}")
            raise Exception(f"Error cargando audio con FFmpeg: {str(e)}")
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
                    'start': segment['start'],  # Cambio: 'start' en lugar de 'start_time'
                    'end': segment['end'],      # Cambio: 'end' en lugar de 'end_time'
                    'text': segment['text'].strip(),
                    'speaker': None  # Se asignará más tarde con detección de hablantes
                })
            
            return {
                'text': transcription['text'],  # Cambio: 'text' en lugar de 'full_text'
                'full_text': transcription['text'],  # Mantener compatibilidad
                'segments': processed_segments,
                'language': transcription['language'],
                'duration': processed_segments[-1]['end'] if processed_segments else 0
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
            start_time = segment.get('start', segment.get('start_time', 0))
            start_min = int(start_time // 60)
            start_sec = int(start_time % 60)
            
            formatted_text += f"[{start_min:02d}:{start_sec:02d}] {segment['text']}\n"
        
        return formatted_text