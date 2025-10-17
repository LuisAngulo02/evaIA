"""
Servicio de análisis de coherencia con IA avanzada usando Groq API
==================================================================
Utiliza Llama 3.1 70B para análisis semántico profundo de coherencia
en exposiciones académicas.

Analiza:
- Coherencia temática con las instrucciones de la asignación
- Relevancia del contenido transcrito
- Profundidad y calidad del análisis
- Estructura y organización del discurso
"""

from groq import Groq
from django.conf import settings
import logging
import json
import re

logger = logging.getLogger(__name__)


class AdvancedCoherenceService:
    """
    Análisis de coherencia con IA avanzada usando Groq API (Llama 3.1 70B)
    
    Proporciona evaluación detallada de la coherencia entre:
    - Las instrucciones/descripción de la asignación
    - El contenido transcrito por Whisper
    - El tema general de la exposición
    """
    
    def __init__(self):
        """Inicializa el servicio con la API key de Groq"""
        if not settings.GROQ_API_KEY:
            raise ValueError(
                "⚠️ GROQ_API_KEY no configurada en settings. "
                "Configura la variable de entorno GROQ_API_KEY"
            )
        
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.config = settings.COHERENCE_CONFIG
        
        logger.info("✅ AdvancedCoherenceService inicializado con Groq API")
    
    def analyze_participant_coherence(
        self,
        participant_name: str,
        transcribed_text: str,
        assignment_title: str,
        assignment_description: str
    ) -> dict:
        """
        Analiza la coherencia de un participante individual.
        
        Args:
            participant_name: Nombre/etiqueta del participante
            transcribed_text: Texto transcrito por Whisper de este participante
            assignment_title: Título de la asignación
            assignment_description: Descripción completa de la asignación
        
        Returns:
            dict con:
                - coherence_score: float (0-100)
                - feedback: str (retroalimentación detallada)
                - details: dict (desglose por criterios)
                - strengths: list (puntos fuertes)
                - improvements: list (áreas de mejora)
        """
        # Validar entrada
        if not transcribed_text or len(transcribed_text.strip()) < 20:
            return self._insufficient_text_response(participant_name)
        
        try:
            # Construir prompt optimizado
            prompt = self._build_evaluation_prompt(
                participant_name=participant_name,
                transcribed_text=transcribed_text,
                assignment_title=assignment_title,
                assignment_description=assignment_description
            )
            
            # Llamar a Groq API
            logger.info(f"🤖 Analizando coherencia con Groq para: {participant_name}")
            logger.info(f"📝 Texto a analizar: {len(transcribed_text)} caracteres")
            
            response = self.client.chat.completions.create(
                model=self.config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.config['temperature'],
                max_tokens=self.config['max_tokens']
            )
            
            # Parsear respuesta de la IA
            ai_response = response.choices[0].message.content
            result = self._parse_ai_response(ai_response, participant_name)
            
            logger.info(
                f"✅ Análisis completado para {participant_name}: "
                f"{result['coherence_score']:.1f}% de coherencia"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en análisis con Groq: {str(e)}", exc_info=True)
            return self._fallback_response(participant_name, str(e))
    
    def _get_system_prompt(self) -> str:
        """Prompt del sistema que define el rol de la IA"""
        return """Eres un evaluador académico experto especializado en:
- Análisis de coherencia y relevancia en exposiciones orales
- Evaluación de comprensión y profundidad de contenido
- Retroalimentación constructiva y específica para estudiantes

Tu objetivo es evaluar objetivamente si lo que el estudiante dijo (según la transcripción) 
es coherente con las instrucciones de la asignación que se le dio.

IMPORTANTE:
- Sé justo pero exigente
- Proporciona feedback específico y útil
- Detecta si el estudiante comprendió realmente el tema
- Identifica si el contenido es relevante o si divaga
- Reconoce tanto fortalezas como áreas de mejora"""
    
    def _build_evaluation_prompt(
        self,
        participant_name: str,
        transcribed_text: str,
        assignment_title: str,
        assignment_description: str
    ) -> str:
        """Construye el prompt de evaluación con toda la información"""
        
        # Truncar texto si es muy largo (para no exceder límites de tokens)
        max_text_length = 4000
        if len(transcribed_text) > max_text_length:
            transcribed_text = transcribed_text[:max_text_length] + "..."
            logger.warning(f"⚠️ Texto truncado a {max_text_length} caracteres")
        
        return f"""
Evalúa la coherencia entre lo que el estudiante dijo y las instrucciones de la asignación.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ASIGNACIÓN DADA AL ESTUDIANTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**TÍTULO:** {assignment_title}

**INSTRUCCIONES/DESCRIPCIÓN:**
{assignment_description if assignment_description else "No se proporcionó descripción específica"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎤 LO QUE EL ESTUDIANTE DIJO (Transcripción de Whisper)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**PARTICIPANTE:** {participant_name}

**TRANSCRIPCIÓN:**
"{transcribed_text}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 CRITERIOS DE EVALUACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evalúa de 0-100 cada criterio:

1. **COHERENCIA TEMÁTICA (40%):**
   - ¿Aborda el tema/instrucciones de la asignación?
   - ¿Se mantiene enfocado o divaga?
   - ¿El contenido es pertinente?

2. **COMPRENSIÓN Y PROFUNDIDAD (30%):**
   - ¿Demuestra comprensión del tema?
   - ¿Incluye detalles, ejemplos o datos?
   - ¿Es superficial o profundo?

3. **RELEVANCIA DEL CONTENIDO (20%):**
   - ¿La información aportada es valiosa?
   - ¿Responde a lo que se pedía?
   - ¿Evita contenido irrelevante?

4. **ESTRUCTURA Y CLARIDAD (10%):**
   - ¿El discurso tiene estructura lógica?
   - ¿Las ideas se expresan claramente?
   - ¿Hay fluidez en la exposición?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 FORMATO DE RESPUESTA REQUERIDO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Responde EXACTAMENTE en este formato JSON (sin texto adicional):

```json
{{
  "thematic_coherence": 85.0,
  "depth_understanding": 75.0,
  "content_relevance": 90.0,
  "structure_clarity": 80.0,
  "overall_coherence": 82.5,
  "feedback": "Análisis breve (150-250 palabras) que explique la calificación, destacando qué tan bien cumplió con las instrucciones de la asignación.",
  "strengths": [
    "Punto fuerte específico 1",
    "Punto fuerte específico 2",
    "Punto fuerte específico 3"
  ],
  "improvements": [
    "Sugerencia concreta 1",
    "Sugerencia concreta 2",
    "Sugerencia concreta 3"
  ],
  "key_concepts_covered": [
    "Concepto clave 1 mencionado",
    "Concepto clave 2 mencionado"
  ],
  "missing_elements": [
    "Elemento que faltó según las instrucciones",
    "Otro aspecto no abordado"
  ]
}}
```

IMPORTANTE: 
- Sé específico y objetivo
- Basa tu evaluación en la coherencia entre instrucciones y transcripción
- El feedback debe ser constructivo y útil para el estudiante
"""
    
    def _parse_ai_response(self, response_text: str, participant_name: str) -> dict:
        """
        Parsea la respuesta JSON de la IA y extrae las calificaciones.
        """
        try:
            # Intentar extraer JSON del texto
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            
            if not json_match:
                raise ValueError("No se encontró JSON en la respuesta")
            
            data = json.loads(json_match.group())
            
            # Extraer puntuaciones
            thematic = float(data.get('thematic_coherence', 70))
            depth = float(data.get('depth_understanding', 70))
            relevance = float(data.get('content_relevance', 70))
            structure = float(data.get('structure_clarity', 70))
            
            # Calcular score final ponderado
            overall_score = (
                thematic * 0.40 +
                depth * 0.30 +
                relevance * 0.20 +
                structure * 0.10
            )
            
            # Validar que esté en rango 0-100
            overall_score = max(0, min(100, overall_score))
            
            return {
                'coherence_score': round(overall_score, 1),
                'feedback': data.get('feedback', 'Análisis completado por IA'),
                'details': {
                    'thematic_coherence': thematic,
                    'depth_understanding': depth,
                    'content_relevance': relevance,
                    'structure_clarity': structure
                },
                'strengths': data.get('strengths', []),
                'improvements': data.get('improvements', []),
                'key_concepts_covered': data.get('key_concepts_covered', []),
                'missing_elements': data.get('missing_elements', []),
                'ai_powered': True,
                'participant_name': participant_name
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error parseando JSON: {e}")
            logger.debug(f"Respuesta recibida: {response_text[:500]}")
            
            # Intentar extraer score del texto plano
            score_match = re.search(r'(\d+\.?\d*)\s*[%/]', response_text)
            score = float(score_match.group(1)) if score_match else 70.0
            
            return {
                'coherence_score': min(100, score),
                'feedback': response_text[:500],
                'details': {
                    'thematic_coherence': score,
                    'depth_understanding': score,
                    'content_relevance': score,
                    'structure_clarity': score
                },
                'strengths': ['Análisis completado'],
                'improvements': ['Ver feedback para detalles'],
                'ai_powered': True,
                'participant_name': participant_name
            }
        
        except Exception as e:
            logger.error(f"❌ Error inesperado parseando respuesta: {e}")
            raise
    
    def _insufficient_text_response(self, participant_name: str) -> dict:
        """Respuesta cuando el texto es insuficiente para análisis"""
        return {
            'coherence_score': 0.0,
            'feedback': (
                f"⚠️ {participant_name} tiene texto insuficiente para análisis "
                f"(menos de 20 caracteres). Esto puede indicar que no participó "
                f"verbalmente o que la transcripción falló."
            ),
            'details': {
                'thematic_coherence': 0.0,
                'depth_understanding': 0.0,
                'content_relevance': 0.0,
                'structure_clarity': 0.0
            },
            'strengths': [],
            'improvements': ['Participar más activamente en la exposición oral'],
            'key_concepts_covered': [],
            'missing_elements': ['Contenido verbal'],
            'ai_powered': False,
            'participant_name': participant_name
        }
    
    def _fallback_response(self, participant_name: str, error_message: str) -> dict:
        """Respuesta de fallback cuando falla la API"""
        return {
            'coherence_score': 0.0,
            'feedback': (
                f"❌ No se pudo analizar la coherencia de {participant_name} "
                f"con IA avanzada. Error: {error_message}. "
                f"Por favor, revisa la configuración de GROQ_API_KEY."
            ),
            'details': {
                'thematic_coherence': 0.0,
                'depth_understanding': 0.0,
                'content_relevance': 0.0,
                'structure_clarity': 0.0
            },
            'strengths': [],
            'improvements': [],
            'key_concepts_covered': [],
            'missing_elements': [],
            'ai_powered': False,
            'participant_name': participant_name,
            'error': error_message
        }
    
    def batch_analyze(self, participants_data: list, assignment_info: dict) -> list:
        """
        Analiza múltiples participantes en batch.
        
        Args:
            participants_data: Lista de dicts con 'name' y 'transcription'
            assignment_info: Dict con 'title' y 'description'
        
        Returns:
            Lista de resultados de análisis
        """
        results = []
        
        assignment_title = assignment_info.get('title', 'Sin título')
        assignment_description = assignment_info.get('description', '')
        
        for participant in participants_data:
            result = self.analyze_participant_coherence(
                participant_name=participant['name'],
                transcribed_text=participant['transcription'],
                assignment_title=assignment_title,
                assignment_description=assignment_description
            )
            results.append(result)
        
        return results
    
    @staticmethod
    def is_available() -> bool:
        """Verifica si el servicio está disponible (API key configurada)"""
        return bool(settings.GROQ_API_KEY)
