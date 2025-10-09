from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import datetime, timedelta
import random
from decimal import Decimal

from apps.presentaciones.models import Course, Assignment, Presentation
from authentication.models import Profile


class Command(BaseCommand):
    help = 'Crea datos de ejemplo para probar la funcionalidad de exportación'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando datos de ejemplo...'))

        # Crear grupos si no existen
        teacher_group, created = Group.objects.get_or_create(name='Docente')
        student_group, created = Group.objects.get_or_create(name='Estudiante')

        # Crear docente de ejemplo
        teacher, created = User.objects.get_or_create(
            username='docente1',
            defaults={
                'first_name': 'María',
                'last_name': 'González',
                'email': 'maria.gonzalez@ejemplo.com',
                'is_staff': True
            }
        )
        if created:
            teacher.set_password('123456')
            teacher.save()
            teacher.groups.add(teacher_group)
            Profile.objects.get_or_create(user=teacher)
            self.stdout.write(f'Docente creado: {teacher.username}')

        # Crear estudiantes de ejemplo
        students_data = [
            {'username': 'estudiante1', 'first_name': 'Carlos', 'last_name': 'Rodríguez'},
            {'username': 'estudiante2', 'first_name': 'Ana', 'last_name': 'Martínez'},
            {'username': 'estudiante3', 'first_name': 'Luis', 'last_name': 'López'},
            {'username': 'estudiante4', 'first_name': 'Sofia', 'last_name': 'García'},
            {'username': 'estudiante5', 'first_name': 'Diego', 'last_name': 'Hernández'},
        ]

        students = []
        for student_data in students_data:
            student, created = User.objects.get_or_create(
                username=student_data['username'],
                defaults={
                    'first_name': student_data['first_name'],
                    'last_name': student_data['last_name'],
                    'email': f"{student_data['username']}@ejemplo.com"
                }
            )
            if created:
                student.set_password('123456')
                student.save()
                student.groups.add(student_group)
                Profile.objects.get_or_create(user=student)
                self.stdout.write(f'Estudiante creado: {student.username}')
            students.append(student)

        # Crear cursos de ejemplo
        courses_data = [
            {'code': 'PROG101', 'name': 'Programación I', 'description': 'Introducción a la programación'},
            {'code': 'WEB201', 'name': 'Desarrollo Web', 'description': 'Desarrollo de aplicaciones web'},
            {'code': 'BD301', 'name': 'Bases de Datos', 'description': 'Diseño y gestión de bases de datos'},
        ]

        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                code=course_data['code'],
                defaults={
                    'name': course_data['name'],
                    'description': course_data['description'],
                    'teacher': teacher,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Curso creado: {course.code} - {course.name}')
            courses.append(course)

        # Crear asignaciones de ejemplo
        assignments_data = [
            {'title': 'Presentación Final del Proyecto', 'type': 'PRESENTATION'},
            {'title': 'Exposición de Conceptos Básicos', 'type': 'SEMINAR'},
            {'title': 'Defensa de Tesis', 'type': 'PRESENTATION'},
            {'title': 'Pitch de Startup', 'type': 'PITCH'},
        ]

        assignments = []
        for course in courses:
            for i, assignment_data in enumerate(assignments_data[:2]):  # 2 asignaciones por curso
                assignment, created = Assignment.objects.get_or_create(
                    title=f"{assignment_data['title']} - {course.code}",
                    course=course,
                    defaults={
                        'description': f'Descripción de la asignación: {assignment_data["title"]}',
                        'assignment_type': assignment_data['type'],
                        'max_duration': random.randint(10, 30),
                        'due_date': timezone.now() + timedelta(days=random.randint(1, 30)),
                        'max_score': Decimal('100.00'),
                        'instructions': 'Instrucciones detalladas de la presentación.',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'Asignación creada: {assignment.title}')
                assignments.append(assignment)

        # Crear presentaciones de ejemplo con calificaciones
        presentation_titles = [
            'Sistema de Gestión de Inventarios',
            'Análisis de Datos con Python',
            'Aplicación Móvil de E-commerce',
            'Implementación de API REST',
            'Machine Learning en la Medicina',
            'Blockchain y Criptomonedas',
            'Desarrollo de Juegos con Unity',
            'Análisis de Redes Sociales',
        ]

        for assignment in assignments:
            # Crear 2-4 presentaciones por asignación
            num_presentations = random.randint(2, min(4, len(students)))
            selected_students = random.sample(students, num_presentations)
            
            for student in selected_students:
                presentation_title = random.choice(presentation_titles)
                
                presentation, created = Presentation.objects.get_or_create(
                    title=f"{presentation_title} - {student.first_name}",
                    student=student,
                    assignment=assignment,
                    defaults={
                        'description': f'Presentación desarrollada por {student.get_full_name()} sobre {presentation_title}',
                        'status': 'GRADED',
                        'file_size': random.randint(1000000, 50000000),  # 1MB a 50MB
                        'duration': timezone.timedelta(seconds=random.randint(300, 1800)),  # 5 a 30 minutos
                        
                        # Calificaciones de IA simuladas
                        'ai_score': Decimal(str(round(random.uniform(70, 95), 2))),
                        'content_score': Decimal(str(round(random.uniform(65, 98), 2))),
                        'fluency_score': Decimal(str(round(random.uniform(60, 95), 2))),
                        'body_language_score': Decimal(str(round(random.uniform(70, 90), 2))),
                        'voice_score': Decimal(str(round(random.uniform(75, 95), 2))),
                        
                        # Calificación final del docente
                        'final_score': Decimal(str(round(random.uniform(70, 100), 2))),
                        'teacher_feedback': self._get_random_feedback(),
                        'graded_by': teacher,
                        'graded_at': timezone.now() - timedelta(days=random.randint(1, 15)),
                        'uploaded_at': timezone.now() - timedelta(days=random.randint(2, 20)),
                        'processed_at': timezone.now() - timedelta(days=random.randint(1, 18)),
                    }
                )
                
                if created:
                    # Agregar feedback de IA simulado
                    presentation.ai_feedback = {
                        'overall_analysis': 'La presentación muestra un buen dominio del tema con oportunidades de mejora en algunos aspectos.',
                        'content_analysis': 'El contenido es relevante y está bien estructurado.',
                        'fluency_analysis': 'La fluidez es adecuada con algunas pausas menores.',
                        'body_language_analysis': 'El lenguaje corporal es apropiado para el contexto.',
                        'voice_analysis': 'La voz es clara y audible.',
                        'recommendations': [
                            'Mantener mayor contacto visual con la audiencia',
                            'Reducir el uso de muletillas',
                            'Agregar más ejemplos prácticos'
                        ]
                    }
                    presentation.save()
                    self.stdout.write(f'Presentación creada: {presentation.title}')

        self.stdout.write(
            self.style.SUCCESS(
                '\n¡Datos de ejemplo creados exitosamente!'
                '\n\nCredenciales de acceso:'
                '\nDocente: usuario=docente1, contraseña=123456'
                '\nEstudiantes: usuario=estudiante1-5, contraseña=123456'
                '\n\nAhora puedes probar la funcionalidad de exportación de calificaciones.'
            )
        )

    def _get_random_feedback(self):
        """Genera retroalimentación aleatoria realista"""
        positive_comments = [
            'Excelente presentación con contenido muy bien estructurado.',
            'Demostró un buen dominio del tema y claridad en la exposición.',
            'La presentación fue informativa y bien organizada.',
            'Buen uso de ejemplos y explicaciones claras.',
            'Se notó preparación y conocimiento del tema.',
        ]
        
        improvement_comments = [
            'Para futuras presentaciones, recomiendo mantener más contacto visual.',
            'Sería beneficioso reducir el ritmo de habla para mayor claridad.',
            'Considerar agregar más ejemplos prácticos.',
            'Trabajar en la gesticulación para complementar el discurso.',
            'Mejorar la transición entre temas.',
        ]
        
        feedback_parts = [
            random.choice(positive_comments),
            random.choice(improvement_comments)
        ]
        
        return ' '.join(feedback_parts)