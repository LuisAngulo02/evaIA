"""
Servicio de análisis de coherencia con IA avanzada usando Groq API
==================================================================
Utiliza Llama 3.3 70B para análisis semántico profundo de coherencia
en exposiciones académicas.

Analiza:
- Coherencia temática con las instrucciones de la asignación
- Relevancia del contenido transcrito
- Profundidad y calidad del análisis
- Estructura y organización del discurso

Sistema de rotación automática de API keys incluido.
"""

from groq import Groq
from django.conf import settings
import logging
import json
import re

logger = logging.getLogger(__name__)


class AdvancedCoherenceService:
    """
    Análisis de coherencia con IA avanzada usando Groq API (Llama 3.3 70B)
    
    Proporciona evaluación detallada de la coherencia entre:
    - Las instrucciones/descripción de la asignación
    - El contenido transcrito por Whisper
    - El tema general de la exposición
    
    Incluye rotación automática de API keys para evitar rate limits.
    """
    
    def __init__(self):
        """Inicializa el servicio con el gestor de API keys de Groq"""
        from .groq_key_manager import get_groq_key_manager
        
        self.key_manager = get_groq_key_manager()
        self.config = settings.COHERENCE_CONFIG
        self.client = None  # Se inicializa dinámicamente
        
        # Verificar que hay al menos una key disponible
        current_key = self.key_manager.get_current_key()
        if not current_key:
            raise ValueError(
                "⚠️ No hay API keys de Groq configuradas. "
                "Configura GROQ_API_KEY_1, GROQ_API_KEY_2, etc. en .env"
            )
        
        logger.info(f"✅ AdvancedCoherenceService inicializado con {len(self.key_manager.keys)} API keys")
    
    def _get_client(self) -> Groq:
        """
        Obtiene un cliente de Groq con la API key actual.
        
        Se actualiza dinámicamente según la rotación de keys.
        """
        current_key = self.key_manager.get_current_key()
        if not current_key:
            raise ValueError("No hay API keys disponibles actualmente")
        
        # Crear nuevo cliente con la key actual
        return Groq(api_key=current_key)
    
    def analyze_participant_coherence(
        self,
        participant_name: str,
        transcribed_text: str,
        assignment_title: str,
        assignment_description: str,
        assignment=None
    ) -> dict:
        """
        Analiza la coherencia de un participante individual.
        
        Args:
            participant_name: Nombre/etiqueta del participante
            transcribed_text: Texto transcrito por Whisper de este participante
            assignment_title: Título de la asignación
            assignment_description: Descripción completa de la asignación
            assignment: Objeto Assignment completo (opcional, para obtener configuración de IA)
        
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
        
        # Obtener nivel de estrictez con orden de prioridad:
        # 1. Nivel específico del assignment (si está configurado)
        # 2. Nivel global del teacher (si está disponible)
        # 3. Default 'moderate'
        strictness_level = 'moderate'  # Default
        
        if assignment:
            # Prioridad 1: Nivel específico del assignment
            if assignment.strictness_level:
                strictness_level = assignment.strictness_level
                logger.info(f"📊 Usando nivel de estrictez del assignment: {strictness_level}")
            # Prioridad 2: Nivel global del teacher
            elif assignment.course and assignment.course.teacher:
                try:
                    from apps.presentaciones.models import AIConfiguration
                    config = AIConfiguration.objects.filter(teacher=assignment.course.teacher).first()
                    if config:
                        strictness_level = config.strictness_level
                        logger.info(f"📊 Usando nivel de estrictez global del teacher: {strictness_level}")
                except Exception as e:
                    logger.warning(f"⚠️ No se pudo obtener configuración de IA: {e}")
        
        # Intentar con rotación automática de keys
        max_retries = len(self.key_manager.keys)
        
        for attempt in range(max_retries):
            try:
                # Obtener cliente con key actual
                client = self._get_client()
                current_key = self.key_manager.get_current_key()
                
                # Construir prompt optimizado
                prompt = self._build_evaluation_prompt(
                    participant_name=participant_name,
                    transcribed_text=transcribed_text,
                    assignment_title=assignment_title,
                    assignment_description=assignment_description,
                    strictness_level=strictness_level
                )
                
                # Llamar a Groq API
                logger.info(f"🤖 Analizando coherencia con Groq para: {participant_name} (intento {attempt + 1}/{max_retries})")
                logger.info(f"📝 Texto a analizar: {len(transcribed_text)} caracteres")
                
                response = client.chat.completions.create(
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
                    max_tokens=self.config['max_tokens'],
                    timeout=self.config.get('timeout', 45)
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
                error_message = str(e).lower()
                
                # Detectar errores de rate limit
                if 'rate_limit' in error_message or 'quota' in error_message or '429' in error_message:
                    logger.warning(f"⚠️ Rate limit alcanzado: {e}")
                    self.key_manager.mark_key_as_failed(current_key, f"Rate limit: {e}")
                    
                    # Intentar con siguiente key
                    if attempt < max_retries - 1:
                        logger.info(f"🔄 Reintentando con siguiente API key...")
                        continue
                    
                # Otros errores
                logger.error(f"❌ Error en análisis con Groq: {str(e)}", exc_info=True)
                
                # Si es el último intento, devolver fallback
                if attempt == max_retries - 1:
                    return self._fallback_response(participant_name, str(e))
        
        # Si llegamos aquí, todas las keys fallaron
        return self._fallback_response(participant_name, "Todas las API keys agotadas")
    
    def _get_strictness_instructions(self, strictness_level: str) -> str:
        """
        Retorna las instrucciones de evaluación según el nivel de estrictez configurado.
        
        Args:
            strictness_level: 'strict', 'moderate', o 'lenient'
        
        Returns:
            str: Instrucciones específicas para la IA según el nivel
        """
        instructions = {
            'strict': """
🔴 NIVEL DE EVALUACIÓN: ESTRICTO

CRITERIOS DE CALIFICACIÓN:
- Requiere dominio COMPLETO y PROFUNDO del tema
- Penaliza fuertemente imprecisiones, falta de profundidad o contenido superficial
- Exige estructura clara, ejemplos concretos y datos específicos
- Solo calificaciones altas (85-100) para exposiciones EXCEPCIONALES con dominio total
- Calificaciones medias (70-84) para presentaciones correctas pero no excepcionales
- Calificaciones bajas (<70) si hay errores conceptuales o falta de profundidad

SÉ MUY EXIGENTE: El estudiante debe demostrar comprensión profunda y manejo experto del tema.""",
            
            'moderate': """
🟡 NIVEL DE EVALUACIÓN: MODERADO (RECOMENDADO)

CRITERIOS DE CALIFICACIÓN:
- Califica 70-95% para presentaciones bien desarrolladas que cubran el tema adecuadamente
- Califica 85-95% para presentaciones sobresalientes con buen dominio
- Busca un balance entre exigencia académica y comprensión razonable
- Valora la profundidad y relevancia del contenido
- Penaliza divagaciones importantes o errores conceptuales graves
- Reconoce el esfuerzo cuando hay comprensión básica sólida

SÉ JUSTO: Evalúa objetivamente el cumplimiento de las instrucciones con criterio balanceado.""",
            
            'lenient': """
🟢 NIVEL DE EVALUACIÓN: SUAVE

CRITERIOS DE CALIFICACIÓN:
- Califica 70-80% si demuestra comprensión BÁSICA del tema
- Califica 85-95% si el contenido es relevante y muestra esfuerzo
- Valora el esfuerzo, la participación y el intento de cumplir las instrucciones
- Enfócate en reforzar lo POSITIVO más que en señalar deficiencias
- Sé tolerante con imprecisiones menores si la idea general es correcta
- Reconoce cualquier conexión válida con el tema asignado

SÉ COMPRENSIVO: Busca aspectos positivos y da crédito por el esfuerzo demostrado."""
        }
        
        return instructions.get(strictness_level, instructions['moderate'])
    
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
        assignment_description: str,
        strictness_level: str = 'moderate'
    ) -> str:
        """Construye el prompt de evaluación con toda la información"""
        
        # Truncar texto si es muy largo (para no exceder límites de tokens)
        max_text_length = 4000
        if len(transcribed_text) > max_text_length:
            transcribed_text = transcribed_text[:max_text_length] + "..."
            logger.warning(f"⚠️ Texto truncado a {max_text_length} caracteres")
        
        # Definir instrucciones según nivel de estrictez
        strictness_instructions = self._get_strictness_instructions(strictness_level)
        
        return f"""
Evalúa la coherencia entre lo que el estudiante dijo y las instrucciones de la asignación.

{strictness_instructions}

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
