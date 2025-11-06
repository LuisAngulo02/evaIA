"""
Script de diagnóstico para depurar problemas de segmentación de audio
Uso: python debug_presentation.py <presentation_id>
"""
import sys
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sist_evaluacion_expo.settings')
django.setup()

import logging
from apps.ai_processor.services.ai_service import AIService
from apps.presentaciones.models import Presentation

# Configurar logging para ver TODO
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def debug_presentation(presentation_id):
    """Reprocesa una presentación con logs ultra-detallados"""
    
    print("=" * 80)
    print(f"🔍 DIAGNÓSTICO DE PRESENTACIÓN {presentation_id}")
    print("=" * 80)
    print()
    
    try:
        # Obtener presentación
        presentation = Presentation.objects.get(pk=presentation_id)
        print(f"✅ Presentación encontrada: {presentation.assignment.title if presentation.assignment else 'Sin título'}")
        print(f"   Usuario: {presentation.user.username}")
        print(f"   Video: {presentation.video_file.name}")
        print()
        
        # Crear servicio de IA
        ai_service = AIService()
        
        print("🚀 Iniciando análisis...")
        print("=" * 80)
        print()
        
        # Analizar
        result = ai_service.analyze_presentation(presentation)
        
        print()
        print("=" * 80)
        if result:
            print(f"✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        else:
            print(f"❌ ANÁLISIS FALLÓ")
        print("=" * 80)
        print()
        
        # Mostrar resultados
        presentation.refresh_from_db()
        
        print("📊 RESULTADOS:")
        print(f"   Estado: {presentation.status}")
        print(f"   Score IA: {presentation.ai_score}")
        print(f"   Participantes detectados: {presentation.participants.count()}")
        print()
        
        for p in presentation.participants.all():
            print(f"👤 {p.name}:")
            print(f"   Tiempo: {p.participation_time}s")
            print(f"   Transcripción: {len(p.transcription_text)} caracteres")
            print(f"   Preview: {p.transcription_text[:100]}...")
            print()
        
        return True
        
    except Presentation.DoesNotExist:
        print(f"❌ ERROR: No existe presentación con ID {presentation_id}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python debug_presentation.py <presentation_id>")
        print()
        print("Ejemplos:")
        print("  python debug_presentation.py 12")
        print("  python debug_presentation.py 10")
        sys.exit(1)
    
    try:
        presentation_id = int(sys.argv[1])
    except ValueError:
        print(f"❌ ERROR: '{sys.argv[1]}' no es un ID válido")
        sys.exit(1)
    
    success = debug_presentation(presentation_id)
    sys.exit(0 if success else 1)
