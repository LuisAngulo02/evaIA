from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.notifications.services import NotificationService
from apps.presentaciones.models import Assignment, Course, Presentation
from apps.notifications.models import Notification


class Command(BaseCommand):
    help = 'Crea notificaciones de prueba para demostrar el sistema'
    
    def handle(self, *args, **options):
        # Limpiar notificaciones existentes de prueba
        Notification.objects.filter(
            notification_type__in=['WELCOME', 'SYSTEM_UPDATE']
        ).delete()
        
        # Obtener algunos usuarios para prueba
        students = User.objects.filter(groups__name='Estudiante')[:5]
        teachers = User.objects.filter(groups__name='Docente')[:2]
        
        notifications_created = 0
        
        # Crear notificaciones de bienvenida para estudiantes
        for student in students:
            NotificationService.create_notification(
                recipient=student,
                title="¡Bienvenido a EvalExpo AI!",
                message="Explora todas las funcionalidades disponibles. Sube tu primera presentación y recibe feedback personalizado con IA.",
                notification_type='WELCOME',
                priority='MEDIUM',
                action_url='/presentations/upload/',
                action_text="Subir presentación",
                expires_in_days=7
            )
            notifications_created += 1
        
        # Crear notificaciones de sistema para todos
        all_users = list(students) + list(teachers)
        for user in all_users:
            NotificationService.create_notification(
                recipient=user,
                title="Nuevas funciones disponibles",
                message="Se han agregado nuevas características al sistema de notificaciones. Ahora recibirás actualizaciones en tiempo real sobre tus presentaciones y asignaciones.",
                notification_type='SYSTEM_UPDATE',
                priority='LOW',
                expires_in_days=3
            )
            notifications_created += 1
        
        # Crear notificaciones de asignación próxima a vencer para estudiantes
        active_assignments = Assignment.objects.filter(is_active=True)[:2]
        for assignment in active_assignments:
            for student in students:
                # Solo si no tienen presentación para esta asignación
                if not Presentation.objects.filter(student=student, assignment=assignment).exists():
                    NotificationService.create_notification(
                        recipient=student,
                        title="Asignación próxima a vencer",
                        message=f"La asignación '{assignment.title}' vence pronto. ¡No olvides subir tu presentación!",
                        notification_type='ASSIGNMENT_DUE_SOON',
                        priority='HIGH',
                        action_url='/presentations/upload/',
                        action_text="Subir ahora",
                        related_assignment=assignment
                    )
                    notifications_created += 1
        
        # Crear notificaciones de presentaciones analizadas para estudiantes con presentaciones
        analyzed_presentations = Presentation.objects.filter(
            status='ANALYZED'
        )[:3]
        
        for presentation in analyzed_presentations:
            # Solo crear si no existe ya una notificación similar
            existing = Notification.objects.filter(
                recipient=presentation.student,
                notification_type='PRESENTATION_ANALYZED',
                related_presentation=presentation
            ).exists()
            
            if not existing:
                NotificationService.create_notification(
                    recipient=presentation.student,
                    title="Análisis de IA completado",
                    message=f"El análisis de tu presentación '{presentation.title}' está listo. Revisa los consejos para mejorar.",
                    notification_type='PRESENTATION_ANALYZED',
                    priority='MEDIUM',
                    action_url=f'/presentations/{presentation.id}/',
                    action_text="Ver análisis",
                    related_presentation=presentation,
                    expires_in_days=15
                )
                notifications_created += 1
        
        # Crear notificaciones de calificación para presentaciones calificadas
        graded_presentations = Presentation.objects.filter(
            final_score__isnull=False,
            graded_at__isnull=False
        )[:3]
        
        for presentation in graded_presentations:
            # Solo crear si no existe ya una notificación similar
            existing = Notification.objects.filter(
                recipient=presentation.student,
                notification_type='PRESENTATION_GRADED',
                related_presentation=presentation
            ).exists()
            
            if not existing:
                NotificationService.create_notification(
                    recipient=presentation.student,
                    title="¡Tu presentación ha sido calificada!",
                    message=f"Tu presentación '{presentation.title}' ha recibido {presentation.final_score} puntos. Revisa el feedback de tu profesor.",
                    notification_type='PRESENTATION_GRADED',
                    priority='HIGH',
                    action_url=f'/presentations/{presentation.id}/',
                    action_text="Ver calificación",
                    related_presentation=presentation,
                    expires_in_days=30
                )
                notifications_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Se crearon {notifications_created} notificaciones de prueba exitosamente!')
        )
        
        # Mostrar resumen por usuario
        for user in all_users:
            count = Notification.objects.filter(recipient=user, is_read=False).count()
            self.stdout.write(f'  - {user.username}: {count} notificaciones no leídas')
        
        self.stdout.write(
            self.style.WARNING('Recuerda que las notificaciones se actualizan automáticamente cada 30 segundos en el navegador.')
        )