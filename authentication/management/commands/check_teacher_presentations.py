from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.presentaciones.models import Presentation, Assignment, Course

class Command(BaseCommand):
    help = 'Verificar presentaciones por calificar para docente1'

    def handle(self, *args, **options):
        try:
            # Obtener el docente1
            docente = User.objects.get(username='docente1')
            self.stdout.write(f"=== VERIFICANDO DOCENTE: {docente.username} ===")
            
            # Obtener cursos del docente
            cursos_docente = Course.objects.filter(teacher=docente, is_active=True)
            self.stdout.write(f"Cursos del docente: {cursos_docente.count()}")
            
            for curso in cursos_docente:
                self.stdout.write(f"  - {curso.name} ({curso.code})")
                
                # Obtener assignments de este curso
                assignments_curso = Assignment.objects.filter(course=curso, is_active=True)
                self.stdout.write(f"    Assignments: {assignments_curso.count()}")
                
                # Obtener presentaciones para estos assignments
                presentaciones_curso = Presentation.objects.filter(
                    assignment__in=assignments_curso
                )
                self.stdout.write(f"    Presentaciones totales: {presentaciones_curso.count()}")
                
                # Presentaciones por calificar (ANALYZED pero no GRADED)
                por_calificar = presentaciones_curso.filter(
                    status='ANALYZED'
                ).select_related('student', 'assignment')
                
                self.stdout.write(f"    Por calificar: {por_calificar.count()}")
                
                for presentacion in por_calificar:
                    self.stdout.write(f"      * {presentacion.title} - {presentacion.student.username} - {presentacion.assignment.title}")
            
            # Total de presentaciones por calificar
            total_por_calificar = Presentation.objects.filter(
                assignment__course__teacher=docente,
                status='ANALYZED'
            ).count()
            
            self.stdout.write(f"\n=== RESUMEN ===")
            self.stdout.write(f"Total presentaciones por calificar: {total_por_calificar}")
            
            # Verificar si existen presentaciones con diferentes estados
            estados = Presentation.objects.filter(
                assignment__course__teacher=docente
            ).values_list('status', flat=True).distinct()
            
            self.stdout.write(f"Estados de presentaciones encontrados: {list(estados)}")
            
            # Si no hay presentaciones ANALYZED, crear algunas para testing
            if total_por_calificar == 0:
                self.stdout.write(f"\n=== CREANDO DATOS DE PRUEBA ===")
                
                # Buscar presentaciones UPLOADED para cambiar a ANALYZED
                uploaded_presentations = Presentation.objects.filter(
                    assignment__course__teacher=docente,
                    status='UPLOADED'
                )[:3]  # Tomar las primeras 3
                
                for pres in uploaded_presentations:
                    pres.status = 'ANALYZED'
                    pres.ai_score = 75.5  # Score de ejemplo
                    pres.save()
                    self.stdout.write(f"  Cambiado a ANALYZED: {pres.title}")
                
                self.stdout.write(f"Creadas {uploaded_presentations.count()} presentaciones para calificar")
            
        except User.DoesNotExist:
            self.stdout.write("ERROR: Usuario 'docente1' no encontrado")
        except Exception as e:
            self.stdout.write(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()