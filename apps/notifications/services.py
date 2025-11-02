from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Notification, NotificationSettings


class NotificationService:
    """Servicio para manejar las notificaciones del sistema"""
    
    @staticmethod
    def create_notification(
        recipient, 
        title, 
        message, 
        notification_type, 
        priority='MEDIUM',
        action_url=None,
        action_text=None,
        related_presentation=None,
        related_assignment=None,
        related_course=None,
        expires_in_days=None
    ):
        """
        Crear una nueva notificación
        """
        # Verificar configuraciones del usuario
        try:
            settings = NotificationSettings.objects.get(user=recipient)
        except NotificationSettings.DoesNotExist:
            # Crear configuración por defecto
            settings = NotificationSettings.objects.create(user=recipient)
        
        # Verificar si el usuario quiere recibir este tipo de notificación
        should_create = True
        
        if notification_type in ['PRESENTATION_GRADED'] and not settings.receive_grade_notifications:
            should_create = False
        elif notification_type in ['NEW_ASSIGNMENT', 'ASSIGNMENT_DUE_SOON', 'ASSIGNMENT_OVERDUE'] and not settings.receive_assignment_notifications:
            should_create = False
        elif notification_type in ['COURSE_UPDATE'] and not settings.receive_course_notifications:
            should_create = False
        elif notification_type in ['SYSTEM_UPDATE', 'WELCOME'] and not settings.receive_system_notifications:
            should_create = False
        
        if not should_create:
            return None
        
        # Calcular fecha de expiración
        expires_at = None
        if expires_in_days:
            expires_at = timezone.now() + timedelta(days=expires_in_days)
        
        # Crear la notificación
        notification = Notification.objects.create(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            action_url=action_url,
            action_text=action_text,
            related_presentation=related_presentation,
            related_assignment=related_assignment,
            related_course=related_course,
            expires_at=expires_at
        )
        
        return notification
    
    @staticmethod
    def notify_presentation_graded(presentation):
        """Notificar cuando una presentación es calificada"""
        return NotificationService.create_notification(
            recipient=presentation.student,
            title="¡Tu presentación ha sido calificada!",
            message=f"Tu presentación '{presentation.title}' ha recibido una calificación de {presentation.final_score} puntos.",
            notification_type='PRESENTATION_GRADED',
            priority='HIGH',
            action_url=reverse('presentations:presentation_detail', args=[presentation.id]),
            action_text="Ver calificación",
            related_presentation=presentation,
            expires_in_days=30
        )
    
    @staticmethod
    def notify_new_assignment(assignment, students):
        """Notificar nueva asignación a estudiantes"""
        notifications = []
        
        # Calcular días hasta la fecha límite
        days_until_due = (assignment.due_date - timezone.now()).days
        expires_days = max(days_until_due, 7)  # Al menos 7 días o hasta la fecha límite
        
        for student in students:
            notification = NotificationService.create_notification(
                recipient=student,
                title="Nueva asignación disponible",
                message=f"Se ha creado una nueva asignación: '{assignment.title}' para el curso {assignment.course.name}. Fecha límite: {assignment.due_date.strftime('%d/%m/%Y')}",
                notification_type='NEW_ASSIGNMENT',
                priority='MEDIUM',
                action_url=reverse('presentations:upload_presentation'),
                action_text="Subir presentación",
                related_assignment=assignment,
                related_course=assignment.course,
                expires_in_days=expires_days
            )
            if notification:
                notifications.append(notification)
        return notifications
    
    @staticmethod
    def notify_assignment_due_soon(assignment, students, days_remaining):
        """Notificar que una asignación vence pronto"""
        notifications = []
        for student in students:
            # Verificar si el estudiante ya tiene una presentación para esta asignación
            from apps.presentaciones.models import Presentation
            has_presentation = Presentation.objects.filter(
                student=student,
                assignment=assignment
            ).exists()
            
            if not has_presentation:
                notification = NotificationService.create_notification(
                    recipient=student,
                    title=f"Asignación vence en {days_remaining} día{'s' if days_remaining > 1 else ''}",
                    message=f"La asignación '{assignment.title}' vence el {assignment.due_date.strftime('%d/%m/%Y')}. ¡No olvides subir tu presentación!",
                    notification_type='ASSIGNMENT_DUE_SOON',
                    priority='HIGH' if days_remaining <= 1 else 'MEDIUM',
                    action_url=reverse('presentations:upload_presentation'),
                    action_text="Subir ahora",
                    related_assignment=assignment,
                    expires_at=assignment.due_date
                )
                if notification:
                    notifications.append(notification)
        return notifications
    
    @staticmethod
    def notify_assignment_overdue(assignment, students):
        """Notificar que una asignación está vencida"""
        notifications = []
        for student in students:
            # Verificar si el estudiante ya tiene una presentación para esta asignación
            from apps.presentaciones.models import Presentation
            has_presentation = Presentation.objects.filter(
                student=student,
                assignment=assignment
            ).exists()
            
            if not has_presentation:
                notification = NotificationService.create_notification(
                    recipient=student,
                    title="Asignación vencida",
                    message=f"La asignación '{assignment.title}' venció el {assignment.due_date.strftime('%d/%m/%Y')}. Contacta a tu profesor para más información.",
                    notification_type='ASSIGNMENT_OVERDUE',
                    priority='URGENT',
                    related_assignment=assignment,
                    expires_in_days=7  # Mantener por una semana después del vencimiento
                )
                if notification:
                    notifications.append(notification)
        return notifications
    
    @staticmethod
    def notify_presentation_analyzed(presentation):
        """Notificar cuando el análisis de IA está completado"""
        return NotificationService.create_notification(
            recipient=presentation.student,
            title="Análisis de IA completado",
            message=f"El análisis automático de tu presentación '{presentation.title}' ha sido completado. Revisa los resultados y consejos para mejorar.",
            notification_type='PRESENTATION_ANALYZED',
            priority='MEDIUM',
            action_url=reverse('presentations:presentation_detail', args=[presentation.id]),
            action_text="Ver análisis",
            related_presentation=presentation,
            expires_in_days=15
        )
    
    @staticmethod
    def notify_welcome_user(user):
        """Notificación de bienvenida para nuevos usuarios"""
        role = "estudiante" if user.groups.filter(name='Estudiante').exists() else "docente"
        
        return NotificationService.create_notification(
            recipient=user,
            title=f"¡Bienvenido a EvalExpo AI!",
            message=f"Te damos la bienvenida como {role}. Explora todas las funcionalidades disponibles y comienza a mejorar tus presentaciones con IA.",
            notification_type='WELCOME',
            priority='MEDIUM',
            action_url=reverse('help:user_guide'),
            action_text="Ver guía",
            expires_in_days=7
        )
    
    @staticmethod
    def notify_new_submission(presentation):
        """Notificar al profesor cuando un estudiante sube una presentación"""
        # Obtener el profesor del curso/asignación
        teacher = presentation.assignment.course.teacher if presentation.assignment else None
        
        if not teacher:
            return None
        
        return NotificationService.create_notification(
            recipient=teacher,
            title="Nueva presentación enviada",
            message=f"{presentation.student.get_full_name() or presentation.student.username} ha enviado la presentación '{presentation.title}' para la asignación '{presentation.assignment.title}'.",
            notification_type='NEW_SUBMISSION',
            priority='MEDIUM',
            action_url=reverse('presentations:grade_presentation_detail', args=[presentation.id]),
            action_text="Ver presentación",
            related_presentation=presentation,
            related_assignment=presentation.assignment,
            expires_in_days=15
        )
    
    @staticmethod
    def notify_submission_ready_to_grade(presentation):
        """Notificar al profesor cuando una presentación está lista para calificar (análisis completado)"""
        teacher = presentation.assignment.course.teacher if presentation.assignment else None
        
        if not teacher:
            return None
        
        return NotificationService.create_notification(
            recipient=teacher,
            title="Presentación lista para calificar",
            message=f"El análisis de IA de la presentación '{presentation.title}' de {presentation.student.get_full_name() or presentation.student.username} ha finalizado y está lista para tu revisión.",
            notification_type='SUBMISSION_READY_TO_GRADE',
            priority='HIGH',
            action_url=reverse('presentations:grade_presentation_detail', args=[presentation.id]),
            action_text="Calificar ahora",
            related_presentation=presentation,
            expires_in_days=10
        )
    
    @staticmethod
    def notify_assignment_deadline_approaching_teacher(assignment, days_remaining):
        """Notificar al profesor que la fecha límite de una asignación se acerca"""
        teacher = assignment.course.teacher
        
        # Contar presentaciones pendientes
        from apps.presentaciones.models import Presentation
        pending_count = Presentation.objects.filter(
            assignment=assignment,
            final_score__isnull=True
        ).count()
        
        if pending_count == 0:
            return None  # No notificar si no hay nada pendiente
        
        return NotificationService.create_notification(
            recipient=teacher,
            title=f"Fecha límite próxima: {assignment.title}",
            message=f"La asignación '{assignment.title}' vence en {days_remaining} día{'s' if days_remaining > 1 else ''}. Tienes {pending_count} presentación{'es' if pending_count > 1 else ''} pendiente{'s' if pending_count > 1 else ''} por calificar.",
            notification_type='ASSIGNMENT_DEADLINE_APPROACHING',
            priority='HIGH' if days_remaining <= 2 else 'MEDIUM',
            action_url=reverse('presentations:grade_presentations'),
            action_text="Ver presentaciones",
            related_assignment=assignment,
            expires_at=assignment.due_date
        )
    
    @staticmethod
    def get_user_notifications(user, limit=None, unread_only=False):
        """Obtener notificaciones de un usuario"""
        queryset = Notification.objects.filter(recipient=user)
        
        if unread_only:
            queryset = queryset.filter(is_read=False)
        
        # Excluir notificaciones expiradas
        queryset = queryset.exclude(
            expires_at__lt=timezone.now()
        )
        
        if limit:
            queryset = queryset[:limit]
        
        return queryset
    
    @staticmethod
    def get_unread_count(user):
        """Obtener cantidad de notificaciones no leídas"""
        return Notification.objects.filter(
            recipient=user,
            is_read=False
        ).exclude(
            expires_at__lt=timezone.now()
        ).count()
    
    @staticmethod
    def mark_all_as_read(user):
        """Marcar todas las notificaciones como leídas"""
        return Notification.objects.filter(
            recipient=user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
    
    @staticmethod
    def cleanup_old_notifications(days=30):
        """Limpiar notificaciones antiguas (para uso en tareas programadas)"""
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Eliminar notificaciones leídas más antiguas que X días
        deleted_count = Notification.objects.filter(
            is_read=True,
            read_at__lt=cutoff_date
        ).delete()[0]
        
        # Eliminar notificaciones expiradas
        expired_count = Notification.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()[0]
        
        return deleted_count + expired_count