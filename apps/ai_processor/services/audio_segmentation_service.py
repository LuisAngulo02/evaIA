"""
Servicio de Segmentación de Audio por Participante
==================================================
Utiliza diarización de hablantes para determinar quién habla cuándo
y asigna transcripciones exactas a cada participante.

Métodos disponibles:
1. Pyannote.audio (RECOMENDADO): Gratuito, preciso, funciona offline
2. Simple VAD: Detección de actividad de voz básica con Whisper timestamps
"""

import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import numpy as np


class AudioSegmentationService:
    """
    Servicio para segmentar audio por hablante y asignar transcripciones exactas.
    
    Estrategias:
    - PYANNOTE: Usa pyannote.audio para diarización profesional (requiere instalación)
    - VAD_WHISPER: Usa timestamps de Whisper + heurística de asignación
    - SIMPLE: Distribución proporcional por tiempo de aparición (método actual)
    """
    
    STRATEGY_PYANNOTE = "pyannote"
    STRATEGY_VAD_WHISPER = "vad_whisper"
    STRATEGY_SIMPLE = "simple"
    
    def __init__(self, strategy: str = STRATEGY_VAD_WHISPER):
        """
        Inicializa el servicio de segmentación.
        
        Args:
            strategy: Estrategia de segmentación a usar
        """
        self.strategy = strategy
        self._pyannote_pipeline = None
    
    def segment_audio_by_participants(
        self,
        video_path: str,
        participants: List[Dict[str, Any]],
        transcription_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Segmenta el audio y asigna transcripciones exactas a cada participante.
        
        Args:
            video_path: Ruta al archivo de video
            participants: Lista de participantes detectados con sus apariciones
            transcription_data: Datos de transcripción de Whisper (con timestamps)
        
        Returns:
            Lista de participantes con sus transcripciones asignadas:
            [
                {
                    'participant_id': int,
                    'name': str,
                    'appearances': [...],
                    'transcription': str,
                    'speech_segments': [
                        {'start': float, 'end': float, 'text': str}
                    ]
                }
            ]
        """
        if self.strategy == self.STRATEGY_PYANNOTE:
            return self._segment_with_pyannote(video_path, participants, transcription_data)
        elif self.strategy == self.STRATEGY_VAD_WHISPER:
            return self._segment_with_vad_whisper(video_path, participants, transcription_data)
        else:
            return self._segment_simple(participants, transcription_data)
    
    def _segment_with_pyannote(
        self,
        video_path: str,
        participants: List[Dict[str, Any]],
        transcription_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Segmentación usando pyannote.audio (método más preciso).
        
        Requiere instalación:
        pip install pyannote.audio
        
        También necesita token de Hugging Face para el modelo.
        """
        try:
            from pyannote.audio import Pipeline
            
            # Cargar pipeline de diarización (lazy loading)
            if self._pyannote_pipeline is None:
                # Nota: Requiere token de Hugging Face
                # Usuario debe configurar: HF_TOKEN en settings o variable de entorno
                self._pyannote_pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=self._get_huggingface_token()
                )
            
            # Ejecutar diarización
            num_speakers = len(participants)
            diarization = self._pyannote_pipeline(
                video_path,
                num_speakers=num_speakers if num_speakers > 0 else None
            )
            
            # Convertir diarización a segmentos de tiempo
            speaker_segments = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                speaker_segments.append({
                    'start': turn.start,
                    'end': turn.end,
                    'speaker': speaker
                })
            
            # Asignar speakers a participantes usando solapamiento temporal
            return self._assign_speakers_to_participants(
                participants,
                speaker_segments,
                transcription_data
            )
            
        except ImportError:
            print("⚠️ pyannote.audio no instalado. Usando método alternativo...")
            return self._segment_with_vad_whisper(video_path, participants, transcription_data)
        except Exception as e:
            print(f"⚠️ Error en pyannote: {str(e)}. Usando método alternativo...")
            return self._segment_with_vad_whisper(video_path, participants, transcription_data)
    
    def _segment_with_vad_whisper(
        self,
        video_path: str,
        participants: List[Dict[str, Any]],
        transcription_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Segmentación usando timestamps de Whisper + heurística de asignación.
        
        Estrategia:
        1. Whisper devuelve transcripción con timestamps de cada segmento
        2. Para cada segmento de habla, determinar qué participante está visible
        3. Asignar el texto al participante más visible en ese momento
        """
        # Extraer segmentos de Whisper con timestamps
        whisper_segments = transcription_data.get('segments', [])
        
        if not whisper_segments:
            # Si Whisper no tiene segments, usar método simple
            return self._segment_simple(participants, transcription_data)
        
        # Inicializar transcripciones para cada participante
        for participant in participants:
            participant['speech_segments'] = []
            participant['transcription'] = ''
        
        # Asignar cada segmento de Whisper al participante más visible
        for segment in whisper_segments:
            start_time = segment.get('start', 0)
            end_time = segment.get('end', 0)
            text = segment.get('text', '').strip()
            
            if not text:
                continue
            
            # Encontrar participante más visible en este intervalo
            best_participant = self._find_most_visible_participant(
                participants,
                start_time,
                end_time
            )
            
            if best_participant:
                best_participant['speech_segments'].append({
                    'start': start_time,
                    'end': end_time,
                    'text': text
                })
        
        # Construir transcripción completa para cada participante
        for participant in participants:
            segments = participant['speech_segments']
            participant['transcription'] = ' '.join(
                seg['text'] for seg in segments
            )
        
        return participants
    
    def _segment_simple(
        self,
        participants: List[Dict[str, Any]],
        transcription_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Método simple: distribuir texto proporcionalmente por tiempo de aparición.
        (Este es el método actual del sistema)
        """
        full_text = transcription_data.get('text', '')
        words = full_text.split()
        total_words = len(words)
        
        if total_words == 0:
            for participant in participants:
                participant['transcription'] = ''
                participant['speech_segments'] = []
            return participants
        
        # Calcular tiempo total de aparición
        total_time = sum(
            p.get('total_participation_time', 0) for p in participants
        )
        
        if total_time == 0:
            # Distribuir equitativamente
            words_per_participant = total_words // len(participants)
            word_idx = 0
            for participant in participants:
                participant['transcription'] = ' '.join(
                    words[word_idx:word_idx + words_per_participant]
                )
                participant['speech_segments'] = []
                word_idx += words_per_participant
        else:
            # Distribuir proporcionalmente
            word_idx = 0
            for participant in participants:
                participation_time = participant.get('total_participation_time', 0)
                proportion = participation_time / total_time
                words_for_participant = int(total_words * proportion)
                
                participant['transcription'] = ' '.join(
                    words[word_idx:word_idx + words_for_participant]
                )
                participant['speech_segments'] = []
                word_idx += words_for_participant
        
        return participants
    
    def _find_most_visible_participant(
        self,
        participants: List[Dict[str, Any]],
        start_time: float,
        end_time: float
    ) -> Optional[Dict[str, Any]]:
        """
        Encuentra el participante más visible durante un intervalo de tiempo.
        
        Args:
            participants: Lista de participantes con sus apariciones
            start_time: Inicio del intervalo (segundos)
            end_time: Fin del intervalo (segundos)
        
        Returns:
            El participante más visible o None
        """
        best_participant = None
        max_overlap = 0
        
        for participant in participants:
            overlap = 0
            appearances = participant.get('appearances', [])
            
            for appearance in appearances:
                app_start = appearance.get('start_time', 0)
                app_end = appearance.get('end_time', 0)
                
                # Calcular solapamiento
                overlap_start = max(start_time, app_start)
                overlap_end = min(end_time, app_end)
                
                if overlap_end > overlap_start:
                    overlap += (overlap_end - overlap_start)
            
            if overlap > max_overlap:
                max_overlap = overlap
                best_participant = participant
        
        return best_participant
    
    def _assign_speakers_to_participants(
        self,
        participants: List[Dict[str, Any]],
        speaker_segments: List[Dict[str, Any]],
        transcription_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Asigna speakers detectados por pyannote a participantes detectados por MediaPipe.
        
        Estrategia:
        - Para cada speaker, calcular solapamiento temporal con apariciones de participantes
        - Asignar speaker al participante con mayor solapamiento
        """
        whisper_segments = transcription_data.get('segments', [])
        
        # Mapear speakers a participantes
        speaker_to_participant = {}
        
        for speaker_label in set(seg['speaker'] for seg in speaker_segments):
            # Obtener todos los segmentos de este speaker
            speaker_times = [
                seg for seg in speaker_segments if seg['speaker'] == speaker_label
            ]
            
            # Calcular solapamiento con cada participante
            best_participant = None
            max_overlap = 0
            
            for participant in participants:
                overlap = 0
                appearances = participant.get('appearances', [])
                
                for speaker_seg in speaker_times:
                    for appearance in appearances:
                        app_start = appearance.get('start_time', 0)
                        app_end = appearance.get('end_time', 0)
                        
                        overlap_start = max(speaker_seg['start'], app_start)
                        overlap_end = min(speaker_seg['end'], app_end)
                        
                        if overlap_end > overlap_start:
                            overlap += (overlap_end - overlap_start)
                
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_participant = participant
            
            if best_participant:
                speaker_to_participant[speaker_label] = best_participant
        
        # Inicializar transcripciones
        for participant in participants:
            participant['speech_segments'] = []
            participant['transcription'] = ''
        
        # Asignar texto de Whisper según speakers
        for segment in whisper_segments:
            start_time = segment.get('start', 0)
            end_time = segment.get('end', 0)
            text = segment.get('text', '').strip()
            
            if not text:
                continue
            
            # Encontrar speaker activo en este momento
            active_speaker = None
            for speaker_seg in speaker_segments:
                if (speaker_seg['start'] <= start_time <= speaker_seg['end'] or
                    speaker_seg['start'] <= end_time <= speaker_seg['end']):
                    active_speaker = speaker_seg['speaker']
                    break
            
            if active_speaker and active_speaker in speaker_to_participant:
                participant = speaker_to_participant[active_speaker]
                participant['speech_segments'].append({
                    'start': start_time,
                    'end': end_time,
                    'text': text
                })
        
        # Construir transcripción completa
        for participant in participants:
            segments = participant['speech_segments']
            participant['transcription'] = ' '.join(
                seg['text'] for seg in segments
            )
        
        return participants
    
    def _get_huggingface_token(self) -> Optional[str]:
        """
        Obtiene el token de Hugging Face desde settings o variable de entorno.
        
        Para usar pyannote.audio, el usuario debe:
        1. Crear cuenta en huggingface.co
        2. Aceptar términos del modelo: huggingface.co/pyannote/speaker-diarization-3.1
        3. Generar token en: huggingface.co/settings/tokens
        4. Configurar en settings.py: HUGGINGFACE_TOKEN = "hf_xxx..."
           O como variable de entorno: HF_TOKEN=hf_xxx...
        """
        try:
            from django.conf import settings
            token = getattr(settings, 'HUGGINGFACE_TOKEN', None)
            if token:
                return token
        except:
            pass
        
        # Intentar desde variable de entorno
        return os.getenv('HF_TOKEN')
    
    @staticmethod
    def get_recommended_strategy() -> str:
        """
        Determina la mejor estrategia disponible en el sistema.
        
        Returns:
            Nombre de la estrategia recomendada
        """
        try:
            import pyannote.audio
            # Si pyannote está instalado, verificar token
            service = AudioSegmentationService()
            if service._get_huggingface_token():
                return AudioSegmentationService.STRATEGY_PYANNOTE
            else:
                print("⚠️ pyannote.audio instalado pero falta HF_TOKEN")
                return AudioSegmentationService.STRATEGY_VAD_WHISPER
        except ImportError:
            return AudioSegmentationService.STRATEGY_VAD_WHISPER
    
    @staticmethod
    def install_pyannote_instructions() -> str:
        """
        Retorna instrucciones para instalar pyannote.audio.
        """
        return """
📦 Para instalar pyannote.audio (diarización profesional):

1. Instalar dependencias:
   pip install pyannote.audio

2. Crear cuenta en Hugging Face:
   https://huggingface.co/join

3. Aceptar términos del modelo:
   https://huggingface.co/pyannote/speaker-diarization-3.1

4. Generar token de acceso:
   https://huggingface.co/settings/tokens

5. Configurar token en settings.py:
   HUGGINGFACE_TOKEN = "hf_xxxxxxxxxxxxx"
   
   O como variable de entorno:
   export HF_TOKEN="hf_xxxxxxxxxxxxx"  (Linux/Mac)
   $env:HF_TOKEN="hf_xxxxxxxxxxxxx"  (Windows PowerShell)

✅ Listo! El sistema usará pyannote automáticamente.
"""
