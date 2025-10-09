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
    if not created and instance.final_score and instance.graded_at:
        # La presentación fue calificada
        # Verificar si ya se envió esta notificación
        from .models import Notification
        existing_notification = Notification.objects.filter(
            recipient=instance.student,
            notification_type='PRESENTATION_GRADED',
            related_presentation=instance
        ).exists()
        
        if not existing_notification:
            NotificationService.notify_presentation_graded(instance)
    
    elif not created and instance.status == 'ANALYZED':
        # El análisis de IA fue completado
        from .models import Notification
        existing_notification = Notification.objects.filter(
            recipient=instance.student,
            notification_type='PRESENTATION_ANALYZED',
            related_presentation=instance
        ).exists()
        
        if not existing_notification:
            NotificationService.notify_presentation_analyzed(instance)


@receiver(post_save, sender=Assignment)
def handle_new_assignment(sender, instance, created, **kwargs):
    """Notificar sobre nuevas asignaciones"""
    if created and instance.is_active:
        # Obtener estudiantes del curso
        from django.contrib.auth.models import User
        students = User.objects.filter(
            groups__name='Estudiante',
            presentation__assignment__course=instance.course
        ).distinct()
        
        if not students.exists():
            # Si no hay estudiantes específicos, notificar a todos los estudiantes
            students = User.objects.filter(groups__name='Estudiante')
        
        NotificationService.notify_new_assignment(instance, students)