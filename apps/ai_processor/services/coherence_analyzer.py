"""
Servicio de Análisis de Coherencia Individual
==============================================

Evalúa la coherencia de cada estudiante individualmente en exposiciones grupales.

Funcionalidades:
1. Análisis de coherencia con IA avanzada (Groq API) si está disponible
2. Fallback a análisis semántico con Sentence Transformers
3. Detección de palabras clave del tema
4. Evaluación de profundidad del contenido
5. Cálculo de calificaciones individuales ponderadas
6. Generación de reportes individuales y grupales

Utiliza:
- Groq API (Llama 3.1 70B) para análisis avanzado
- sentence-transformers para análisis semántico (fallback)
- sklearn para cálculo de similitud
"""

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️ sentence-transformers no está instalado. El análisis de coherencia estará limitado.")

import numpy as np
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class CoherenceAnalyzer:
    """
    Analizador de coherencia individual para exposiciones grupales
    
    Prioridad de análisis:
    1. IA Avanzada (Groq) - Si está configurado GROQ_API_KEY
    2. Sentence Transformers - Fallback si no hay Groq
    3. Análisis básico - Último recurso
    """
    
    def __init__(self):
        """
        Inicializa el analizador con el modelo de embeddings y/o IA avanzada
        """
        # Intentar inicializar IA avanzada
        self.advanced_service = None
        if settings.USE_ADVANCED_COHERENCE:
            try:
                from .advanced_coherence_service import AdvancedCoherenceService
                self.advanced_service = AdvancedCoherenceService()
                logger.info("🚀 IA Avanzada (Groq) activada para análisis de coherencia")
            except Exception as e:
                logger.warning(f"⚠️ No se pudo activar IA avanzada: {e}")
        
        # Inicializar modelo de embeddings como fallback
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                # Modelo multilingüe optimizado para español
                logger.info("🤖 Cargando modelo de análisis semántico...")
                self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                self.model_loaded = True
                logger.info("✅ Modelo cargado exitosamente")
            except Exception as e:
                logger.error(f"❌ Error cargando modelo: {str(e)}")
                self.model_loaded = False
        else:
            self.model_loaded = False
            logger.warning("⚠️ Modelo de análisis semántico no disponible")
    
    def analizar_grupo(self, participaciones, tema, descripcion_tema="", max_score=20.0, assignment=None):
        """
        Analiza la coherencia de cada estudiante individualmente
        
        Usa IA avanzada (Groq) si está disponible, sino fallback a Sentence Transformers
        
        Args:
            participaciones: Lista de dict con estructura:
                [
                    {
                        'etiqueta': 'Persona 1',
                        'texto_transcrito': 'El cambio climático es...',
                        'tiempo_participacion': 120.5  # segundos
                    },
                    ...
                ]
            tema: Tema asignado de la exposición
            descripcion_tema: Descripción detallada del tema (instrucciones de la asignación)
            max_score: Puntaje máximo de la asignación (default 20.0)
            assignment: Objeto Assignment completo (opcional, para configuración de IA)
        
        Returns:
            Lista de resultados individuales con calificaciones
        """
        logger.info(f"📊 Analizando coherencia de {len(participaciones)} participantes (puntaje máximo: {max_score})")
        
        # PRIORIDAD 1: IA Avanzada (Groq)
        if self.advanced_service:
            try:
                logger.info("🚀 Usando IA Avanzada (Groq) para análisis de coherencia")
                return self._analizar_con_ia_avanzada(participaciones, tema, descripcion_tema, max_score, assignment)
            except Exception as e:
                logger.error(f"❌ Error con IA avanzada: {e}. Usando fallback...")
        
        # PRIORIDAD 2: Sentence Transformers
        if not self.model_loaded:
            logger.warning("⚠️ Usando análisis básico por falta de modelo")
            return self._analizar_grupo_basico(participaciones, tema, descripcion_tema, max_score)
        
        # Análisis con Sentence Transformers (método original)
        logger.info("🤖 Usando Sentence Transformers para análisis")
        
        resultados = []
        texto_tema = f"{tema}. {descripcion_tema}"
        
        try:
            # Generar embedding del tema una sola vez
            embedding_tema = self.model.encode([texto_tema])
            
            # Evaluar cada participante
            for idx, participacion in enumerate(participaciones, 1):
                logger.info(f"🔍 Evaluando {participacion['etiqueta']}...")
                resultado_individual = self._evaluar_estudiante(
                    participacion,
                    embedding_tema,
                    tema,
                    descripcion_tema
                )
                resultados.append(resultado_individual)
            
            # Calcular calificaciones finales proporcionales
            resultados = self._calcular_calificaciones_finales(resultados, max_score)
            
            logger.info(f"✅ Análisis completado para {len(resultados)} participantes")
            
        except Exception as e:
            logger.error(f"❌ Error en análisis de grupo: {str(e)}", exc_info=True)
            return self._analizar_grupo_basico(participaciones, tema, descripcion_tema, max_score)
        
        return resultados
    
    def _evaluar_estudiante(self, participacion, embedding_tema, tema, descripcion_tema):
        """Evalúa coherencia de un estudiante individual"""
        texto = participacion['texto_transcrito']
        etiqueta = participacion['etiqueta']
        
        # Validar texto mínimo
        if len(texto.strip()) < 20:
            return self._resultado_sin_contenido(participacion)
        
        try:
            # 1. COHERENCIA SEMÁNTICA (60% de la nota)
            coherencia_semantica = self._calcular_coherencia_semantica(texto, embedding_tema)
            
            # 2. PALABRAS CLAVE (20% de la nota)
            palabras_clave = self._analizar_palabras_clave(texto, tema, descripcion_tema)
            puntaje_palabras = palabras_clave['puntaje']
            
            # 3. LONGITUD Y PROFUNDIDAD (20% de la nota)
            puntaje_profundidad = self._analizar_profundidad(texto)
            
            # CALIFICACIÓN PONDERADA (sobre 100)
            nota_coherencia = (
                coherencia_semantica * 0.60 +  # 60%
                puntaje_palabras * 0.20 +       # 20%
                puntaje_profundidad * 0.20      # 20%
            )
            
            # Determinar nivel y observación (provisional, se recalculará después)
            nivel, observacion = self._clasificar_coherencia(nota_coherencia, coherencia_semantica)
            
            return {
                'etiqueta': etiqueta,
                'tiempo_participacion': participacion['tiempo_participacion'],
                'texto_transcrito': texto,
                'coherencia_semantica': round(coherencia_semantica, 2),
                'palabras_clave_encontradas': palabras_clave['palabras'],
                'puntaje_palabras_clave': round(puntaje_palabras, 2),
                'puntaje_profundidad': round(puntaje_profundidad, 2),
                'nota_coherencia': round(nota_coherencia, 2),
                'nivel': nivel,  # Se recalculará en _calcular_calificaciones_finales
                'observacion': observacion,
                'palabras_totales': len(texto.split()),
                'caracteres': len(texto),
                'foto_url': participacion.get('foto_url')  # Incluir URL de la foto
            }
            
        except Exception as e:
            logger.error(f"❌ Error evaluando {etiqueta}: {str(e)}")
            return self._resultado_error(participacion)
    
    def _calcular_coherencia_semantica(self, texto, embedding_tema):
        """Calcula similitud semántica entre texto y tema"""
        embedding_estudiante = self.model.encode([texto])
        similitud = cosine_similarity(embedding_estudiante, embedding_tema)[0][0]
        
        # Convertir a porcentaje (0-100)
        # Ajustar para que valores típicos (0.3-0.8) mapeen mejor a 0-100
        coherencia = float(similitud * 125)  # Factor de ajuste
        coherencia = min(100, max(0, coherencia))  # Limitar a 0-100
        
        return coherencia
    
    def _analizar_palabras_clave(self, texto, tema, descripcion):
        """Detecta palabras clave del tema en el texto del estudiante"""
        # Combinar tema y descripción para extraer más palabras clave
        texto_completo_tema = f"{tema} {descripcion}".lower()
        palabras_tema = set(texto_completo_tema.split())
        palabras_texto = set(texto.lower().split())
        
        # Filtrar palabras comunes sin valor (stop words)
        palabras_comunes = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'de', 'en', 'y', 'o', 'pero', 'por', 'para', 'con',
            'a', 'al', 'del', 'es', 'son', 'está', 'están',
            'que', 'cual', 'como', 'se', 'su', 'sus', 'mi', 'tu',
            'te', 'me', 'le', 'les', 'nos', 'lo', 'este', 'esta'
        }
        palabras_tema = palabras_tema - palabras_comunes
        
        # Filtrar palabras muy cortas (menos de 4 letras)
        palabras_tema = {p for p in palabras_tema if len(p) >= 4}
        
        # Encontrar coincidencias
        palabras_encontradas = list(palabras_tema.intersection(palabras_texto))
        
        # Calcular puntaje
        if len(palabras_tema) > 0:
            porcentaje = (len(palabras_encontradas) / len(palabras_tema)) * 100
            # Puntaje: 100 si encuentra al menos 40% de palabras clave
            puntaje = min(porcentaje * 2.5, 100)
        else:
            puntaje = 50  # Puntaje neutral si no hay palabras clave
        
        return {
            'palabras': palabras_encontradas[:10],  # Limitar a 10 para display
            'puntaje': puntaje,
            'total_encontradas': len(palabras_encontradas),
            'total_tema': len(palabras_tema)
        }
    
    def _analizar_profundidad(self, texto):
        """Evalúa la profundidad del contenido basado en longitud y estructura"""
        palabras = texto.split()
        num_palabras = len(palabras)
        
        # Palabras indicadoras de profundidad y análisis
        indicadores_profundidad = [
            'porque', 'debido', 'causa', 'consecuencia', 'resultado',
            'ejemplo', 'como', 'además', 'también', 'sin embargo',
            'por lo tanto', 'en conclusión', 'finalmente', 'así',
            'entonces', 'específicamente', 'particularmente',
            'significa', 'implica', 'demuestra', 'evidencia',
            'importante', 'fundamental', 'esencial', 'clave',
            'primero', 'segundo', 'tercero', 'finalmente'
        ]
        
        texto_lower = texto.lower()
        indicadores_encontrados = sum(
            1 for indicador in indicadores_profundidad 
            if indicador in texto_lower
        )
        
        # Puntaje basado en palabras (30-50% del total)
        if num_palabras < 20:
            puntaje_base = 10
        elif num_palabras < 40:
            puntaje_base = 30
        elif num_palabras < 80:
            puntaje_base = 50
        elif num_palabras < 150:
            puntaje_base = 70
        else:
            puntaje_base = 85
        
        # Bonus por uso de conectores y palabras de análisis (hasta 30% adicional)
        bonus_conectores = min(indicadores_encontrados * 3, 15)
        
        # Bonus por longitud de oraciones (señal de elaboración)
        oraciones = texto.count('.') + texto.count('?') + texto.count('!')
        if oraciones > 0:
            palabras_por_oracion = num_palabras / oraciones
            if 10 <= palabras_por_oracion <= 25:  # Rango ideal
                bonus_oraciones = 5
            else:
                bonus_oraciones = 0
        else:
            bonus_oraciones = 0
        
        puntaje_total = min(puntaje_base + bonus_conectores + bonus_oraciones, 100)
        
        return puntaje_total
    
    def _clasificar_coherencia(self, nota_coherencia, coherencia_semantica):
        """Determina nivel y observación según el puntaje"""
        if nota_coherencia >= 80:
            nivel = "Excelente"
            observacion = "Discurso altamente coherente y bien estructurado con el tema asignado"
        elif nota_coherencia >= 70:
            nivel = "Muy Buena"
            observacion = "Muy buena relación con el tema, aborda los puntos principales"
        elif nota_coherencia >= 60:
            nivel = "Buena"
            observacion = "Buena coherencia con el tema, cubre aspectos relevantes"
        elif nota_coherencia >= 50:
            nivel = "Regular"
            observacion = "Coherencia moderada, se desvía parcialmente del tema"
        elif nota_coherencia >= 40:
            nivel = "Baja"
            observacion = "Poca coherencia con el tema asignado, varios desvíos"
        else:
            nivel = "Insuficiente"
            observacion = "Contenido insuficiente o muy poco relacionado con el tema"
        
        return nivel, observacion
    
    def _calcular_calificaciones_finales(self, resultados, max_score=20.0):
        """
        Calcula el porcentaje de aporte de cada estudiante
        considerando tiempo Y coherencia
        """
        logger.info(f"📊 Calculando calificaciones finales con max_score={max_score}")
        
        # Calcular tiempo total
        tiempo_total = sum(r['tiempo_participacion'] for r in resultados)
        
        if tiempo_total == 0:
            logger.warning("⚠️ Tiempo total es 0, asignando valores predeterminados")
            for r in resultados:
                r['porcentaje_tiempo'] = 0
                r['porcentaje_aporte'] = 0
                r['calificacion_final'] = 0
            return resultados
        
        for resultado in resultados:
            # Porcentaje de tiempo
            porcentaje_tiempo = (resultado['tiempo_participacion'] / tiempo_total) * 100
            resultado['porcentaje_tiempo'] = round(porcentaje_tiempo, 2)
            
            # Porcentaje de aporte = tiempo × factor_coherencia
            # Si habló 33% del tiempo con 80% de coherencia → aporte ajustado
            factor_coherencia = resultado['nota_coherencia'] / 100
            aporte_ponderado = porcentaje_tiempo * factor_coherencia
            
            resultado['porcentaje_aporte'] = round(aporte_ponderado, 2)
            
            # Calificación final sobre max_score (dinámico según configuración de asignación)
            # Basada en coherencia ajustada por participación mínima
            if porcentaje_tiempo < 15:  # Menos del 15% es penalizado
                factor_penalizacion = porcentaje_tiempo / 15
            else:
                factor_penalizacion = 1.0
            
            calificacion = (resultado['nota_coherencia'] / 100) * max_score * factor_penalizacion
            resultado['calificacion_final'] = round(calificacion, 2)
            resultado['max_score'] = max_score  # Guardar max_score en el resultado
            
            # Recalcular nivel basándose en la calificación final (porcentaje sobre max_score)
            porcentaje_calificacion = (resultado['calificacion_final'] / max_score) * 100
            
            # LOG DETALLADO PARA DEBUG
            logger.info(f"🔍 DEBUG - {resultado['etiqueta']}: calificacion_final={resultado['calificacion_final']}, max_score={max_score}, porcentaje={porcentaje_calificacion:.2f}%")
            
            if porcentaje_calificacion >= 90:
                resultado['nivel'] = "Excelente"
                logger.info(f"  ✅ Nivel asignado: Excelente (>= 90%)")
            elif porcentaje_calificacion >= 80:
                resultado['nivel'] = "Muy Buena"
                logger.info(f"  ✅ Nivel asignado: Muy Buena (>= 80%)")
            elif porcentaje_calificacion >= 70:
                resultado['nivel'] = "Buena"
                logger.info(f"  ✅ Nivel asignado: Buena (>= 70%)")
            elif porcentaje_calificacion >= 60:
                resultado['nivel'] = "Regular"
                logger.info(f"  ✅ Nivel asignado: Regular (>= 60%)")
            elif porcentaje_calificacion >= 50:
                resultado['nivel'] = "Baja"
                logger.info(f"  ⚠️ Nivel asignado: Baja (>= 50%)")
            else:
                resultado['nivel'] = "Insuficiente"
                logger.info(f"  ❌ Nivel asignado: Insuficiente (< 50%)")
        
        # Normalizar porcentajes de aporte para que sumen 100%
        suma_aportes = sum(r['porcentaje_aporte'] for r in resultados)
        if suma_aportes > 0:
            for resultado in resultados:
                resultado['porcentaje_aporte_normalizado'] = round(
                    (resultado['porcentaje_aporte'] / suma_aportes) * 100, 2
                )
        else:
            for resultado in resultados:
                resultado['porcentaje_aporte_normalizado'] = 0
        
        return resultados
    
    def _analizar_grupo_basico(self, participaciones, tema, descripcion_tema, max_score=20.0):
        """Análisis básico sin modelo de embeddings (fallback)"""
        logger.info("📊 Usando análisis básico de coherencia")
        
        resultados = []
        for participacion in participaciones:
            texto = participacion['texto_transcrito']
            
            # Análisis básico por palabras clave
            palabras_clave = self._analizar_palabras_clave(texto, tema, descripcion_tema)
            puntaje_palabras = palabras_clave['puntaje']
            
            # Análisis de profundidad
            puntaje_profundidad = self._analizar_profundidad(texto)
            
            # Puntaje combinado (sin similitud semántica)
            nota_coherencia = (puntaje_palabras * 0.6 + puntaje_profundidad * 0.4)
            
            nivel, observacion = self._clasificar_coherencia(nota_coherencia, puntaje_palabras)
            
            resultados.append({
                'etiqueta': participacion['etiqueta'],
                'tiempo_participacion': participacion['tiempo_participacion'],
                'texto_transcrito': texto,
                'coherencia_semantica': puntaje_palabras,
                'palabras_clave_encontradas': palabras_clave['palabras'],
                'puntaje_palabras_clave': round(puntaje_palabras, 2),
                'puntaje_profundidad': round(puntaje_profundidad, 2),
                'nota_coherencia': round(nota_coherencia, 2),
                'nivel': nivel,
                'observacion': observacion + " (análisis básico)",
                'palabras_totales': len(texto.split()),
                'caracteres': len(texto)
            })
        
        return self._calcular_calificaciones_finales(resultados, max_score)
    
    def _resultado_sin_contenido(self, participacion):
        """Resultado para participante sin contenido suficiente"""
        return {
            'etiqueta': participacion['etiqueta'],
            'tiempo_participacion': participacion['tiempo_participacion'],
            'texto_transcrito': participacion['texto_transcrito'],
            'coherencia_semantica': 0,
            'palabras_clave_encontradas': [],
            'puntaje_palabras_clave': 0,
            'puntaje_profundidad': 0,
            'nota_coherencia': 0,
            'nivel': "Insuficiente",
            'observacion': "Participación muy breve o sin contenido relevante",
            'palabras_totales': len(participacion['texto_transcrito'].split()),
            'caracteres': len(participacion['texto_transcrito'])
        }
    
    def _resultado_error(self, participacion):
        """Resultado en caso de error de procesamiento"""
        return {
            'etiqueta': participacion['etiqueta'],
            'tiempo_participacion': participacion['tiempo_participacion'],
            'texto_transcrito': participacion['texto_transcrito'],
            'coherencia_semantica': 0,
            'palabras_clave_encontradas': [],
            'puntaje_palabras_clave': 0,
            'puntaje_profundidad': 0,
            'nota_coherencia': 0,
            'nivel': "Error",
            'observacion': "Error al procesar la participación",
            'palabras_totales': 0,
            'caracteres': 0
        }
    
    def generar_resumen_grupal(self, resultados):
        """
        Genera un resumen textual del análisis grupal
        
        Args:
            resultados: Lista de resultados individuales
        
        Returns:
            str: Resumen formateado en texto
        """
        if not resultados:
            return "No hay resultados para mostrar."
        
        resumen = f"📊 **EVALUACIÓN GRUPAL - {len(resultados)} Participantes**\n\n"
        
        # Ordenar por calificación (mayor a menor)
        resultados_ordenados = sorted(resultados, key=lambda x: x['calificacion_final'], reverse=True)
        
        for idx, r in enumerate(resultados_ordenados, 1):
            max_score_individual = r.get('max_score', 20.0)
            resumen += f"**{idx}. {r['etiqueta']}**\n"
            resumen += f"   📝 Calificación: {r['calificacion_final']}/{max_score_individual} ({r['nivel']})\n"
            resumen += f"   ⏱️  Tiempo: {r['porcentaje_tiempo']:.1f}%\n"
            resumen += f"   📈 Aporte: {r['porcentaje_aporte_normalizado']:.1f}%\n"
            resumen += f"   🎯 Coherencia: {r['nota_coherencia']:.1f}/100\n"
            resumen += f"   💬 {r['palabras_totales']} palabras\n\n"
        
        # Estadísticas generales
        promedio_coherencia = np.mean([r['nota_coherencia'] for r in resultados])
        promedio_calificacion = np.mean([r['calificacion_final'] for r in resultados])
        max_score_value = resultados[0].get('max_score', 20.0) if resultados else 20.0
        
        resumen += f"**📊 Estadísticas del Grupo:**\n"
        resumen += f"   • Coherencia promedio: {promedio_coherencia:.1f}/100\n"
        resumen += f"   • Calificación promedio: {promedio_calificacion:.1f}/{max_score_value}\n"
        
        # Análisis de equidad
        desviacion_tiempo = np.std([r['porcentaje_tiempo'] for r in resultados])
        if desviacion_tiempo < 10:
            resumen += f"   • ✅ Participación muy equilibrada\n"
        elif desviacion_tiempo < 20:
            resumen += f"   • ⚠️  Participación moderadamente equilibrada\n"
        else:
            resumen += f"   • ❌ Participación desigual\n"
        
        return resumen

    def _analizar_con_ia_avanzada(self, participaciones, tema, descripcion_tema, max_score=20.0, assignment=None):
        """
        Analiza coherencia usando IA avanzada (Groq API)
        
        Este método utiliza Llama 3.3 70B para análisis semántico profundo
        
        Args:
            assignment: Objeto Assignment para obtener configuración de estrictez
        """
        logger.info(f"📊 Análisis con IA avanzada - max_score={max_score}")
        resultados = []
        
        for participacion in participaciones:
            etiqueta = participacion['etiqueta']
            texto = participacion['texto_transcrito']
            tiempo = participacion['tiempo_participacion']
            
            logger.info(f"🤖 Analizando {etiqueta} con IA avanzada...")
            
            try:
                # Llamar al servicio de IA avanzada con assignment para configuración
                ai_result = self.advanced_service.analyze_participant_coherence(
                    participant_name=etiqueta,
                    transcribed_text=texto,
                    assignment_title=tema,
                    assignment_description=descripcion_tema,
                    assignment=assignment
                )
                
                # Convertir score de 0-100 a nota de 0-max_score (dinámico según asignación)
                coherence_score = ai_result['coherence_score']  # 0-100
                nota_sobre_max = (coherence_score / 100) * max_score  # 0-max_score
                
                # Construir resultado compatible con el formato existente
                resultado = {
                    'etiqueta': etiqueta,
                    'texto_transcrito': texto,
                    'nota_coherencia': coherence_score,  # 0-100
                    'calificacion_final': round(nota_sobre_max, 2),  # 0-max_score
                    'nivel': self._clasificar_nivel(nota_sobre_max),
                    'observacion': ai_result['feedback'][:200] + '...' if len(ai_result['feedback']) > 200 else ai_result['feedback'],  # Resumen corto
                    'feedback_ia_avanzada': ai_result['feedback'],  # Feedback completo de IA
                    'palabras_totales': len(texto.split()),
                    'tiempo_participacion': tiempo,
                    'porcentaje_tiempo': 0,  # Se calcula después
                    'porcentaje_aporte_normalizado': 0,  # Se calcula después
                    
                    # Compatibilidad con campos existentes
                    'coherencia_semantica': coherence_score,
                    'palabras_clave_encontradas': ai_result.get('key_concepts_covered', []),
                    'puntaje_palabras_clave': coherence_score,  # Aproximación
                    'puntaje_profundidad': coherence_score,  # Aproximación
                    'foto_url': participacion.get('foto_url'),
                    
                    # Detalles de IA avanzada
                    'ai_powered': True,
                    'details': ai_result['details'],
                    'strengths': ai_result.get('strengths', []),
                    'improvements': ai_result.get('improvements', []),
                    'key_concepts_covered': ai_result.get('key_concepts_covered', []),
                    'missing_elements': ai_result.get('missing_elements', [])
                }
                
                resultados.append(resultado)
                logger.info(f"✅ {etiqueta}: {coherence_score:.1f}% coherencia")
                
            except Exception as e:
                logger.error(f"❌ Error analizando {etiqueta} con IA: {e}")
                # Fallback a análisis básico para este participante
                resultado_basico = self._analizar_participante_basico(
                    participacion, tema, descripcion_tema
                )
                resultados.append(resultado_basico)
        
        # Calcular porcentajes relativos
        if resultados:
            tiempo_total = sum(r['tiempo_participacion'] for r in resultados)
            for resultado in resultados:
                resultado['porcentaje_tiempo'] = (
                    (resultado['tiempo_participacion'] / tiempo_total * 100) 
                    if tiempo_total > 0 else 0
                )
                resultado['porcentaje_aporte_normalizado'] = resultado['porcentaje_tiempo']
        
        return resultados
    
    def _clasificar_nivel(self, nota):
        """Clasifica el nivel de desempeño según la nota (0-20)"""
        if nota >= 18:
            return "Excelente"
        elif nota >= 15:
            return "Muy Bueno"
        elif nota >= 13:
            return "Bueno"
        elif nota >= 11:
            return "Regular"
        else:
            return "Insuficiente"
    
    def _analizar_participante_basico(self, participacion, tema, descripcion_tema):
        """Análisis básico de un participante (fallback)"""
        etiqueta = participacion['etiqueta']
        texto = participacion['texto_transcrito']
        tiempo = participacion['tiempo_participacion']
        
        # Análisis muy básico basado en longitud y palabras clave
        palabras = texto.lower().split()
        palabras_tema = tema.lower().split()
        
        coincidencias = sum(1 for p in palabras if p in palabras_tema)
        coherencia_basica = min(100, (coincidencias / max(len(palabras_tema), 1)) * 100)
        
        nota_20 = (coherencia_basica / 100) * 20
        
        return {
            'etiqueta': etiqueta,
            'nota_coherencia': coherencia_basica,
            'calificacion_final': round(nota_20, 2),
            'nivel': self._clasificar_nivel(nota_20),
            'feedback': f"Análisis básico: {coincidencias} coincidencias con el tema.",
            'palabras_totales': len(palabras),
            'tiempo_participacion': tiempo,
            'porcentaje_tiempo': 0,
            'porcentaje_aporte_normalizado': 0,
            'ai_powered': False
        }

    def generar_conclusion_grupal(self, resultados_participantes, tema, descripcion_tema, max_score=20.0):
        """
        Genera una conclusión grupal personalizada usando IA de GROQ
        
        Args:
            resultados_participantes: Lista de resultados de análisis individual
            tema: Título del tema
            descripcion_tema: Descripción detallada del tema
            max_score: Puntaje máximo de la asignación (default: 20.0)
            
        Returns:
            str: Conclusión grupal generada por IA o mensaje predeterminado
        """
        if not resultados_participantes:
            return "No se encontraron participantes para analizar."
        
        try:
            # Intentar usar GROQ para generar conclusión dinámica
            from apps.ai_processor.services.groq_key_manager import GroqKeyManager
            from groq import Groq
            
            key_manager = GroqKeyManager()
            groq_api_key = key_manager.get_current_key()
            
            if not groq_api_key:
                logger.warning("No hay API key de GROQ disponible, usando conclusión básica")
                return self._generar_conclusion_basica(resultados_participantes)
            
            # Preparar datos del grupo para el prompt
            num_participantes = len(resultados_participantes)
            coherencia_promedio = np.mean([r['nota_coherencia'] for r in resultados_participantes])
            calificacion_promedio = np.mean([r['calificacion_final'] for r in resultados_participantes])
            
            # Información de cada participante
            info_participantes = []
            for idx, r in enumerate(resultados_participantes, 1):
                info_participantes.append(
                    f"{idx}. {r['etiqueta']}: {r['calificacion_final']:.1f}/{max_score} pts "
                    f"(Coherencia: {r['nota_coherencia']:.1f}%, Tiempo: {r['porcentaje_tiempo']:.1f}%)"
                )
            
            participantes_texto = "\n".join(info_participantes)
            
            # Identificar puntos fuertes y débiles
            mejor_participante = max(resultados_participantes, key=lambda x: x['calificacion_final'])
            peor_participante = min(resultados_participantes, key=lambda x: x['calificacion_final'])
            participante_mas_tiempo = max(resultados_participantes, key=lambda x: x['porcentaje_tiempo'])
            
            # Calcular desviación estándar de coherencia para ver dispersión
            coherencias = [r['nota_coherencia'] for r in resultados_participantes]
            desviacion_coherencia = np.std(coherencias)
            
            # Determinar si la coherencia es baja, media o alta
            if coherencia_promedio < 50:
                nivel_comprension = "BAJA - El grupo NO logró demostrar comprensión adecuada del tema"
            elif coherencia_promedio < 70:
                nivel_comprension = "MEDIA - El grupo demostró comprensión parcial del tema"
            else:
                nivel_comprension = "ALTA - El grupo demostró buena comprensión del tema"
            
            # Analizar equilibrio de participación
            tiempos = [r['porcentaje_tiempo'] for r in resultados_participantes]
            desviacion_tiempo = np.std(tiempos)
            if desviacion_tiempo > 20:
                equilibrio_participacion = "DESIGUAL - Hay gran diferencia en el tiempo de participación"
            elif desviacion_tiempo > 10:
                equilibrio_participacion = "MODERADO - La participación está medianamente equilibrada"
            else:
                equilibrio_participacion = "EQUILIBRADO - Todos participaron de forma similar"
            
            # Construir prompt para GROQ con análisis crítico
            prompt = f"""Eres un evaluador académico OBJETIVO y CRÍTICO que analiza presentaciones grupales. Debes generar una conclusión REALISTA basada en las métricas.

**Tema asignado:** {tema}

**Descripción completa:** {descripcion_tema[:300]}

**Resultados de cada participante ({num_participantes}):**
{participantes_texto}

**ANÁLISIS CRÍTICO:**
- Coherencia promedio: {coherencia_promedio:.1f}% → {nivel_comprension}
- Calificación promedio: {calificacion_promedio:.1f}/{max_score}
- Dispersión en coherencia: {desviacion_coherencia:.1f}% ({"Alta variabilidad" if desviacion_coherencia > 15 else "Moderada" if desviacion_coherencia > 8 else "Baja variabilidad"})
- Distribución de tiempo: {equilibrio_participacion}
- Mejor participante: {mejor_participante['etiqueta']} ({mejor_participante['nota_coherencia']:.1f}% coherencia)
- Participante más débil: {peor_participante['etiqueta']} ({peor_participante['nota_coherencia']:.1f}% coherencia)

**INSTRUCCIONES IMPORTANTES:**
1. Si la coherencia promedio es MENOR a 50%, di claramente que el grupo NO cumplió adecuadamente con el tema
2. Si la coherencia promedio es 50-69%, di que cumplieron PARCIALMENTE pero necesitan mejorar
3. Si la coherencia promedio es 70% o más, di que cumplieron bien
4. Sé ESPECÍFICO sobre qué aspectos fallaron o destacaron
5. Si hay gran variabilidad (desviación >15%), menciona que algunos participantes estuvieron mejor que otros
6. Si la participación es muy desigual (desviación tiempo >20%), señálalo como área crítica de mejora
7. NO uses frases genéricas como "comprensión básica" cuando los datos muestran bajo rendimiento
8. Máximo 3-4 oraciones, directas y constructivas

Genera SOLO la conclusión grupal, sin títulos ni formato adicional:"""

            client = Groq(api_key=groq_api_key)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un evaluador académico EXPERTO y OBJETIVO. Tu trabajo es dar retroalimentación REALISTA basada en métricas concretas.

REGLAS IMPORTANTES:
- Si los datos muestran bajo rendimiento, sé HONESTO al señalarlo
- NO uses eufemismos vagos como "comprensión básica" cuando la coherencia es menor a 50%
- Sé ESPECÍFICO: menciona qué falló y qué se puede mejorar
- Mantén un tono profesional pero directo
- La retroalimentación debe ser CONSTRUCTIVA pero REALISTA
- NO infles los logros si las métricas no los respaldan"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6,  # Reducido para respuestas más consistentes y objetivas
                max_tokens=300,   # Aumentado para conclusiones más detalladas
                top_p=0.9,
                stream=False
            )
            
            conclusion = response.choices[0].message.content.strip()
            
            # Verificar que la conclusión no esté vacía
            if conclusion and len(conclusion) > 20:
                logger.info(f"✅ Conclusión grupal generada con GROQ ({len(conclusion)} caracteres)")
                return conclusion
            else:
                logger.warning("Conclusión de GROQ muy corta, usando básica")
                return self._generar_conclusion_basica(resultados_participantes)
                
        except Exception as e:
            logger.error(f"Error al generar conclusión con GROQ: {str(e)}")
            return self._generar_conclusion_basica(resultados_participantes)
    
    def _generar_conclusion_basica(self, resultados_participantes):
        """
        Genera una conclusión básica cuando GROQ no está disponible
        """
        if not resultados_participantes:
            return "No hay participantes para evaluar."
        
        coherencia_promedio = np.mean([r['nota_coherencia'] for r in resultados_participantes])
        calificacion_promedio = np.mean([r['calificacion_final'] for r in resultados_participantes])
        num_participantes = len(resultados_participantes)
        
        # Análisis de dispersión
        coherencias = [r['nota_coherencia'] for r in resultados_participantes]
        desviacion_coherencia = np.std(coherencias)
        
        # Análisis de equilibrio de tiempo
        tiempos = [r['porcentaje_tiempo'] for r in resultados_participantes]
        desviacion_tiempo = np.std(tiempos)
        
        # Generar conclusión basada en métricas reales
        if coherencia_promedio >= 80:
            conclusion = f"El grupo ({num_participantes} participantes) demostró excelente dominio del tema con {coherencia_promedio:.1f}% de coherencia promedio. "
            if desviacion_coherencia < 10:
                conclusion += "Todos los integrantes mantuvieron un nivel consistentemente alto. "
            else:
                conclusion += "Aunque algunos participantes destacaron más que otros, el nivel general fue sobresaliente. "
            conclusion += "Se recomienda mantener este nivel de preparación y profundización temática."
            
        elif coherencia_promedio >= 70:
            conclusion = f"El grupo logró cumplir adecuadamente con el tema asignado, alcanzando {coherencia_promedio:.1f}% de coherencia promedio. "
            if desviacion_coherencia > 15:
                conclusion += "Sin embargo, se observa variabilidad significativa entre participantes, lo que sugiere preparación desigual. "
            conclusion += "Se sugiere profundizar más en los conceptos clave y asegurar que todos los integrantes dominen el tema de forma equilibrada."
            
        elif coherencia_promedio >= 50:
            conclusion = f"El grupo cumplió parcialmente con el tema, obteniendo {coherencia_promedio:.1f}% de coherencia promedio. "
            if calificacion_promedio < 12:
                conclusion += "Las calificaciones individuales reflejan que varios participantes no lograron desarrollar el tema con suficiente profundidad. "
            if desviacion_tiempo > 20:
                conclusion += "Además, la participación fue muy desigual, lo cual afectó el desempeño grupal. "
            conclusion += "Se recomienda mejorar la preparación temática, estructurar mejor el contenido y equilibrar la participación de todos los miembros."
            
        else:
            conclusion = f"El grupo NO logró cumplir adecuadamente con el tema asignado, alcanzando solo {coherencia_promedio:.1f}% de coherencia promedio. "
            conclusion += "Los análisis individuales muestran falta de comprensión de los conceptos fundamentales y desarrollo insuficiente del contenido. "
            if desviacion_coherencia > 15:
                conclusion += "La gran variabilidad entre participantes indica preparación muy desigual. "
            conclusion += "Es crítico revisar los conceptos básicos del tema, mejorar la preparación grupal y asegurar que todos los integrantes comprendan y puedan explicar los puntos clave antes de la presentación."
        
        return conclusion
