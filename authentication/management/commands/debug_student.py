from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.presentaciones.models import Course, Assignment, Presentation

class Command(BaseCommand):
    help = 'Verificar datos de estudiante para debugging'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='estudiante_test')
            self.stdout.write(f"Usuario encontrado: {user.username}")
            
            # Verificar cursos
            courses = user.enrolled_courses.all()
            self.stdout.write(f"Cursos inscritos: {courses.count()}")
            for course in courses:
                self.stdout.write(f"  - {course.code}: {course.name}")
            
            # Verificar asignaciones
            assignments = Assignment.objects.filter(course__students=user)
            self.stdout.write(f"Asignaciones totales: {assignments.count()}")
            for assignment in assignments:
                self.stdout.write(f"  - {assignment.title} (Curso: {assignment.course.code})")
            
            # Verificar asignaciones activas
            from django.utils import timezone
            active_assignments = Assignment.objects.filter(
                course__students=user,
                is_active=True,
                due_date__gte=timezone.now()
            )
            self.stdout.write(f"Asignaciones activas: {active_assignments.count()}")
            
            # Verificar presentaciones del usuario
            presentations = Presentation.objects.filter(student=user)
            self.stdout.write(f"Presentaciones del usuario: {presentations.count()}")
            for presentation in presentations:
                self.stdout.write(f"  - {presentation.title} (Assignment ID: {presentation.assignment_id})")
            
            # Calcular pendientes
            completed_ids = presentations.values_list('assignment_id', flat=True)
            pending = active_assignments.exclude(id__in=completed_ids)
            self.stdout.write(f"Asignaciones pendientes: {pending.count()}")
            for p in pending:
                self.stdout.write(f"  - {p.title}")
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Usuario estudiante_test no encontrado'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))