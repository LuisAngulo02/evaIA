from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.presentaciones.models import Presentation, Assignment
from .services import NotificationService
from .models import NotificationSettings


@receiver(post_save, sender=User)
def create_notification_settings(sender, instance, created, **kwargs):
    """Crear configuración de notificaciones para nuevos usuarios"""
    if created:
        NotificationSettings.objects.get_or_create(user=instance)
        # Crear notificación de bienvenida
        NotificationService.notify_welcome_user(instance)


@receiver(post_save, sender=Presentation)
def handle_presentation_updates(sender, instance, created, **kwargs):
    """Manejar actualizaciones de presentaciones"""
    
    # Nueva presentación creada - notificar al profesor
    if created:
        NotificationService.notify_new_submission(instance)
    
    # Presentación calificada - notificar al estudiante
    if not created and instance.final_score and instance.graded_at:
        from .models import Notification
        existing_notification = Notification.objects.filter(
            recipient=instance.student,
            notification_type='PRESENTATION_GRADED',
            related_presentation=instance
        ).exists()
        
        if not existing_notification:
            NotificationService.notify_presentation_graded(instance)
    
    # Análisis de IA completado
    elif not created and instance.status == 'ANALYZED':
        from .models import Notification
        
        # Notificar al estudiante
        existing_student_notification = Notification.objects.filter(
            recipient=instance.student,
            notification_type='PRESENTATION_ANALYZED',
            related_presentation=instance
        ).exists()
        
        if not existing_student_notification:
            NotificationService.notify_presentation_analyzed(instance)
        
        # Notificar al profesor que está lista para calificar
        if instance.assignment:
            teacher = instance.assignment.course.teacher
            existing_teacher_notification = Notification.objects.filter(
                recipient=teacher,
                notification_type='SUBMISSION_READY_TO_GRADE',
                related_presentation=instance
            ).exists()
            
            if not existing_teacher_notification:
                NotificationService.notify_submission_ready_to_grade(instance)


@receiver(post_save, sender=Assignment)
def handle_new_assignment(sender, instance, created, **kwargs):
    """Notificar sobre nuevas asignaciones"""
    if created and instance.is_active:
        # Obtener estudiantes inscritos en el curso
        from django.contrib.auth.models import User
        
        # Obtener estudiantes que están inscritos en este curso
        students = User.objects.filter(
            groups__name='Estudiante',
            enrolled_courses=instance.course
        ).distinct()
        
        if not students.exists():
            # Si no hay estudiantes específicos en el curso, notificar a todos los estudiantes
            students = User.objects.filter(groups__name='Estudiante')
        
        NotificationService.notify_new_assignment(instance, students)