"""
Script de Diagnóstico - Detección de Rostros
=============================================

Este script prueba la detección de rostros en un video
y muestra información detallada del proceso.

Uso:
    python test_face_detection.py <ruta_al_video.mp4>

Ejemplo:
    python test_face_detection.py uploads/presentations/test_video.mp4
"""

import sys
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sist_evaluacion_expo.settings')
django.setup()

from apps.ai_processor.services.face_detection_service import FaceDetectionService
import logging

# Configurar logging detallado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def test_face_detection(video_path):
    """
    Prueba la detección de rostros en un video
    """
    print("=" * 80)
    print("🎬 PRUEBA DE DETECCIÓN DE ROSTROS")
    print("=" * 80)
    print(f"📁 Video: {video_path}")
    print()
    
    # Verificar que el archivo existe
    if not os.path.exists(video_path):
        print(f"❌ ERROR: El archivo no existe: {video_path}")
        return
    
    # Crear servicio de detección
    print("🔧 Inicializando servicio de detección...")
    service = FaceDetectionService(
        tolerance=0.6,  # Valor por defecto
        sample_rate=3   # Procesar 1 de cada 3 frames
    )
    
    print(f"   - Tolerance: {service.tolerance}")
    print(f"   - Sample rate: {service.sample_rate}")
    print()
    
    # Procesar video
    print("🎥 Procesando video...")
    print("-" * 80)
    result = service.process_video(video_path, presentation_id=None)
    print("-" * 80)
    print()
    
    # Mostrar resultados
    if result['success']:
        print("✅ PROCESAMIENTO EXITOSO")
        print("=" * 80)
        print()
        
        # Resumen general
        print("📊 RESUMEN GENERAL:")
        print(f"   - Participantes detectados: {result['total_participants']}")
        print(f"   - Score de equidad: {result['score']:.1f}/100")
        print(f"   - Duración del video: {result['video_duration']:.1f}s")
        print(f"   - Frames analizados: {result['frames_analyzed']}")
        print(f"   - Rostros detectados: {result['faces_detected']}")
        print(f"   - Método: {result.get('detection_method', 'N/A')}")
        print()
        
        # Detalles por participante
        if result['participants']:
            print("👥 PARTICIPANTES:")
            print("-" * 80)
            for i, participant in enumerate(result['participants'], 1):
                print(f"\n{i}. {participant['id']}")
                print(f"   ⏱️  Tiempo en pantalla: {participant['time_formatted']} ({participant['time_seconds']:.1f}s)")
                print(f"   📊 Porcentaje: {participant['percentage']:.1f}%")
                print(f"   🎬 Apariciones: {participant['appearances_count']}")
                print(f"   🕐 Primera aparición: {participant['first_seen']:.1f}s")
                print(f"   🕕 Última aparición: {participant['last_seen']:.1f}s")
                
                if 'time_segments' in participant and participant['time_segments']:
                    print(f"   📍 Segmentos de tiempo:")
                    for seg in participant['time_segments'][:5]:  # Mostrar máximo 5
                        print(f"      • {seg['start']:.1f}s - {seg['end']:.1f}s")
                    if len(participant['time_segments']) > 5:
                        print(f"      ... y {len(participant['time_segments']) - 5} segmentos más")
        
        print()
        print("=" * 80)
        
        # Análisis de equidad
        if result['total_participants'] > 1:
            percentages = [p['percentage'] for p in result['participants']]
            max_diff = max(percentages) - min(percentages)
            
            print("\n📈 ANÁLISIS DE EQUIDAD:")
            print(f"   - Diferencia máxima: {max_diff:.1f}%")
            
            if max_diff < 15:
                print("   ✅ Participación MUY equilibrada")
            elif max_diff < 30:
                print("   ⚠️ Participación moderadamente equilibrada")
            else:
                print("   ❌ Participación DESIGUAL")
        
        print()
        
        # Recomendaciones
        print("💡 RECOMENDACIONES:")
        if result['total_participants'] == 0:
            print("   ❌ No se detectaron rostros. Verifica:")
            print("      - Calidad del video")
            print("      - Iluminación")
            print("      - Que haya rostros visibles en el video")
        elif result['total_participants'] == 1:
            print("   ⚠️ Solo se detectó 1 participante. Si hay más:")
            print("      - Verifica los logs arriba para ver si se fusionaron tracks")
            print("      - Busca líneas con: '🔗 Fusionando...'")
            print("      - Si los fusionó incorrectamente, reduce el threshold")
        else:
            print(f"   ✅ Se detectaron {result['total_participants']} participantes correctamente")
        
        print()
        
    else:
        print("❌ ERROR EN EL PROCESAMIENTO")
        print("=" * 80)
        print(f"Error: {result.get('error', 'Desconocido')}")
        print()
    
    print("=" * 80)
    print("🏁 Prueba completada")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso: python test_face_detection.py <ruta_al_video>")
        print()
        print("Ejemplo:")
        print("   python test_face_detection.py uploads/presentations/test_video.mp4")
        print("   python test_face_detection.py C:\\Videos\\mi_presentacion.mp4")
        sys.exit(1)
    
    video_path = sys.argv[1]
    test_face_detection(video_path)
