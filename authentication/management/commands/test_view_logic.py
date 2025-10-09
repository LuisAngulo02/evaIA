from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils import timezone
from apps.presentaciones.models import Course, Assignment, Presentation

class Command(BaseCommand):
    help = 'Replicar exactamente la lógica de la vista student_dashboard_view'

    def handle(self, *args, **options):
        try:
            # Simular request.user
            user = User.objects.get(username='estudiante_test')
            self.stdout.write(f"=== SIMULANDO VISTA PARA: {user.username} ===")
            
            # Obtener presentaciones del estudiante
            user_presentations = Presentation.objects.filter(student=user)
            self.stdout.write(f"Presentaciones del usuario: {user_presentations.count()}")
            
            # Estadísticas del estudiante
            stats = {
                'total_presentations': user_presentations.count(),
                'completed_presentations': user_presentations.filter(status='GRADED').count(),
                'pending_presentations': user_presentations.filter(status__in=['UPLOADED', 'PROCESSING', 'ANALYZED']).count(),
                'average_score': 0.0
            }
            self.stdout.write(f"Stats: {stats}")
            
            # Calcular promedio general
            if stats['completed_presentations'] > 0:
                avg_score = user_presentations.filter(
                    status='GRADED',
                    final_score__isnull=False
                ).aggregate(Avg('final_score'))['final_score__avg']
                stats['average_score'] = round(avg_score, 1) if avg_score else 0.0
            
            # Asignaciones pendientes - LÓGICA EXACTA DE LA VISTA
            # Obtener todos los cursos donde el usuario está inscrito
            user_courses = user.enrolled_courses.filter(is_active=True)
            self.stdout.write(f"DEBUG: Usuario {user.username}")
            self.stdout.write(f"DEBUG: Cursos del usuario: {list(user_courses.values_list('name', flat=True))}")
            
            # Obtener todas las asignaciones activas de esos cursos
            all_assignments = Assignment.objects.filter(
                course__in=user_courses,
                is_active=True,
                due_date__gte=timezone.now()
            ).select_related('course')
            self.stdout.write(f"DEBUG: Asignaciones activas: {all_assignments.count()}")
            
            # Filtrar asignaciones que el usuario no ha completado
            completed_assignment_ids = user_presentations.values_list('assignment_id', flat=True)
            self.stdout.write(f"DEBUG: IDs de asignaciones completadas: {list(completed_assignment_ids)}")
            
            pending_assignments = all_assignments.exclude(
                id__in=completed_assignment_ids
            ).order_by('due_date')[:5]
            self.stdout.write(f"DEBUG: Asignaciones pendientes: {pending_assignments.count()}")
            
            for assignment in pending_assignments:
                self.stdout.write(f"  - {assignment.title} (ID: {assignment.id}, Curso: {assignment.course.code})")
            
            self.stdout.write("=== RESULTADO ===")
            self.stdout.write(f"Deberían mostrarse {pending_assignments.count()} asignaciones pendientes")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))