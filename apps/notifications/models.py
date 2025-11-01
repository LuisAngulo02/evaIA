from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Notification(models.Model):
    """Modelo para las notificaciones del sistema"""
    
    NOTIFICATION_TYPES = [
        ('PRESENTATION_GRADED', 'Presentación calificada'),
        ('NEW_ASSIGNMENT', 'Nueva asignación'),
        ('ASSIGNMENT_DUE_SOON', 'Asignación próxima a vencer'),
        ('ASSIGNMENT_OVERDUE', 'Asignación vencida'),
        ('PRESENTATION_ANALYZED', 'Análisis de IA completado'),
        ('COURSE_UPDATE', 'Actualización de curso'),
        ('SYSTEM_UPDATE', 'Actualización del sistema'),
        ('WELCOME', 'Bienvenida'),
    ]
    
    PRIORITY_LEVELS = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('URGENT', 'Urgente'),
    ]
    
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        verbose_name="Destinatario"
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    message = models.TextField(verbose_name="Mensaje")
    notification_type = models.CharField(
        max_length=30, 
        choices=NOTIFICATION_TYPES,
        verbose_name="Tipo de notificación"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_LEVELS,
        default='MEDIUM',
        verbose_name="Prioridad"
    )
    
    # Estado de la notificación
    is_read = models.BooleanField(default=False, verbose_name="Leída")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Leída el")
    
    # Enlaces opcionales
    action_url = models.URLField(blank=True, null=True, verbose_name="URL de acción")
    action_text = models.CharField(max_length=100, blank=True, null=True, verbose_name="Texto del botón")
    
    # Relaciones opcionales con otros modelos
    related_presentation = models.ForeignKey(
        'presentaciones.Presentation',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Presentación relacionada"
    )
    related_assignment = models.ForeignKey(
        'presentaciones.Assignment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Asignación relacionada"
    )
    related_course = models.ForeignKey(
        'presentaciones.Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Curso relacionado"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creada el")
    expires_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Expira el",
        help_text="Fecha después de la cual la notificación se considerará obsoleta"
    )
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Marcar la notificación como leída"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def get_action_url(self):
        """Obtener la URL de acción, generándola automáticamente si es necesario"""
        if self.action_url:
            return self.action_url
        
        # Generar URL basada en relaciones
        from django.urls import reverse
        
        if self.related_presentation:
            return reverse('presentations:presentation_detail', args=[self.related_presentation.id])
        elif self.related_assignment:
            # Incluir el ID de la asignación como parámetro GET para pre-seleccionarla
            base_url = reverse('presentations:upload_presentation')
            return f"{base_url}?assignment={self.related_assignment.id}"
        elif self.related_course:
            return reverse('presentations:manage_courses')
        
        # URL por defecto
        return reverse('notifications:list')
    
    def is_expired(self):
        """Verificar si la notificación ha expirado"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def icon_class(self):
        """Obtener la clase de ícono basada en el tipo"""
        icon_map = {
            'PRESENTATION_GRADED': 'fas fa-star text-success',
            'NEW_ASSIGNMENT': 'fas fa-tasks text-info',
            'ASSIGNMENT_DUE_SOON': 'fas fa-clock text-warning',
            'ASSIGNMENT_OVERDUE': 'fas fa-exclamation-triangle text-danger',
            'PRESENTATION_ANALYZED': 'fas fa-robot text-primary',
            'COURSE_UPDATE': 'fas fa-book text-info',
            'SYSTEM_UPDATE': 'fas fa-cog text-secondary',
            'WELCOME': 'fas fa-hand-wave text-success',
        }
        return icon_map.get(self.notification_type, 'fas fa-bell text-info')
    
    @property
    def badge_class(self):
        """Obtener la clase del badge basada en la prioridad"""
        badge_map = {
            'LOW': 'bg-secondary',
            'MEDIUM': 'bg-info',
            'HIGH': 'bg-warning',
            'URGENT': 'bg-danger',
        }
        return badge_map.get(self.priority, 'bg-info')
    
    @property
    def time_since_created(self):
        """Obtener tiempo transcurrido desde la creación"""
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"hace {diff.days} día{'s' if diff.days > 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"hace {hours} hora{'s' if hours > 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"hace {minutes} minuto{'s' if minutes > 1 else ''}"
        else:
            return "hace un momento"


class NotificationSettings(models.Model):
    """Configuración de notificaciones por usuario"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_settings',
        verbose_name="Usuario"
    )
    
    # Configuraciones por tipo
    receive_grade_notifications = models.BooleanField(
        default=True, 
        verbose_name="Recibir notificaciones de calificaciones"
    )
    receive_assignment_notifications = models.BooleanField(
        default=True,
        verbose_name="Recibir notificaciones de asignaciones"
    )
    receive_course_notifications = models.BooleanField(
        default=True,
        verbose_name="Recibir notificaciones de cursos"
    )
    receive_system_notifications = models.BooleanField(
        default=True,
        verbose_name="Recibir notificaciones del sistema"
    )
    
    # Configuraciones adicionales
    email_notifications = models.BooleanField(
        default=False,
        verbose_name="Enviar notificaciones por email"
    )
    digest_frequency = models.CharField(
        max_length=20,
        choices=[
            ('NEVER', 'Nunca'),
            ('DAILY', 'Diario'),
            ('WEEKLY', 'Semanal'),
        ],
        default='NEVER',
        verbose_name="Frecuencia de resumen por email"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de Notificaciones"
        verbose_name_plural = "Configuraciones de Notificaciones"
    
    def __str__(self):
        return f"Configuración de {self.user.username}"