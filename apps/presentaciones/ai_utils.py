"""
Utilidades para configuración de IA
"""

def get_ai_config_for_teacher(teacher):
    """
    Obtiene la configuración de IA personalizada para un docente
    
    Args:
        teacher (User): Usuario docente
        
    Returns:
        dict: Configuración de IA con todos los parámetros
    """
    try:
        from apps.presentaciones.models import AIConfiguration
        config = AIConfiguration.get_config_for_teacher(teacher)
        
        return {
            'model': config.ai_model,
            'temperature': config.ai_temperature,
            'face_detection_confidence': config.face_detection_confidence,
            'weights': {
                'coherence': config.coherence_weight / 100.0,  # Convertir a decimal
                'face_detection': config.face_detection_weight / 100.0,
                'duration': config.duration_weight / 100.0,
                'manual': config.manual_weight / 100.0,
            }
        }
    except Exception as e:
        # Valores por defecto si hay algún error
        return {
            'model': 'llama-3.3-70b-versatile',
            'temperature': 0.3,
            'face_detection_confidence': 0.7,
            'weights': {
                'coherence': 0.4,
                'face_detection': 0.2,
                'duration': 0.2,
                'manual': 0.2,
            }
        }


def calculate_final_grade(ai_grade, face_score, duration_score, manual_grade, teacher):
    """
    Calcula la calificación final usando los pesos configurados por el docente
    
    Args:
        ai_grade (float): Calificación de coherencia por IA
        face_score (float): Puntuación de detección facial
        duration_score (float): Puntuación de duración
        manual_grade (float): Calificación manual del docente
        teacher (User): Usuario docente
        
    Returns:
        float: Calificación final calculada
    """
    config = get_ai_config_for_teacher(teacher)
    weights = config['weights']
    
    final_grade = (
        (ai_grade or 0) * weights['coherence'] +
        (face_score or 0) * weights['face_detection'] +
        (duration_score or 0) * weights['duration'] +
        (manual_grade or 0) * weights['manual']
    )
    
    return min(100.0, max(0.0, final_grade))  # Asegurar que esté entre 0 y 100