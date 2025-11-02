from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.presentaciones.models import Presentation, Assignment, Course
from authentication.models import Profile

class Command(BaseCommand):
    help = 'Debug teacher dashboard for presentations to grade'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Teacher username to debug')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            profile = getattr(user, 'profile', None)
            
            self.stdout.write(f"=== DEBUG DASHBOARD DOCENTE: {username} ===")
            self.stdout.write(f"ID: {user.id}")
            self.stdout.write(f"Email: {user.email}")
            self.stdout.write(f"Activo: {user.is_active}")
            
            if profile:
                self.stdout.write(f"Rol: {profile.get_role()}")
                self.stdout.write(f"Es docente: {profile.is_teacher()}")
            else:
                self.stdout.write("¡NO TIENE PERFIL!")
                
            # Verificar cursos del docente
            teacher_courses = Course.objects.filter(teacher=user, is_active=True)
            self.stdout.write(f"\n=== CURSOS DEL DOCENTE ({teacher_courses.count()}) ===")
            for course in teacher_courses:
                self.stdout.write(f"- {course.name} ({course.code}) - {course.students.count()} estudiantes")
                
            # Verificar asignaciones del docente
            teacher_assignments = Assignment.objects.filter(
                course__teacher=user,
                is_active=True
            )
            self.stdout.write(f"\n=== ASIGNACIONES DEL DOCENTE ({teacher_assignments.count()}) ===")
            for assignment in teacher_assignments:
                presentations_count = Presentation.objects.filter(assignment=assignment).count()
                self.stdout.write(f"- {assignment.title} ({assignment.course.code}) - {presentations_count} presentaciones")
                
            # Verificar presentaciones por calificar
            pending_presentations = Presentation.objects.filter(
                assignment__course__teacher=user,
                status__in=['UPLOADED', 'ANALYZED']
            ).select_related('student', 'assignment', 'assignment__course')
            
            self.stdout.write(f"\n=== PRESENTACIONES POR CALIFICAR ({pending_presentations.count()}) ===")
            for presentation in pending_presentations:
                self.stdout.write(f"- '{presentation.title}' por {presentation.student.username}")
                self.stdout.write(f"  Curso: {presentation.assignment.course.name}")
                self.stdout.write(f"  Status: {presentation.status}")
                self.stdout.write(f"  Subida: {presentation.uploaded_at}")
                self.stdout.write(f"  AI Score: {presentation.ai_score}")
                self.stdout.write("  ---")
                
            # Estadísticas generales
            all_presentations = Presentation.objects.filter(
                assignment__course__teacher=user
            )
            graded_presentations = all_presentations.filter(status='GRADED')
            
            self.stdout.write(f"\n=== ESTADÍSTICAS GENERALES ===")
            self.stdout.write(f"Total presentaciones: {all_presentations.count()}")
            self.stdout.write(f"Presentaciones calificadas: {graded_presentations.count()}")
            self.stdout.write(f"Presentaciones pendientes: {pending_presentations.count()}")
            
            if graded_presentations.exists():
                avg_score = graded_presentations.aggregate(
                    avg=models.Avg('final_score')
                )['avg']
                self.stdout.write(f"Promedio general: {avg_score:.1f}%" if avg_score else "No hay promedio")
                
        except User.DoesNotExist:
            self.stdout.write(f"Usuario '{username}' no encontrado")
        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")
            import traceback
            self.stdout.write(traceback.format_exc())