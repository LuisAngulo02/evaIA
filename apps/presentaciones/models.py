from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import os

def upload_to_presentations(instance, filename):
    """Función para definir la ruta de upload de videos"""
    return f'presentations/{instance.student.username}/{timezone.now().year}/{timezone.now().month}/{filename}'

class Course(models.Model):
    """Modelo para los cursos"""
    name = models.CharField(max_length=200, verbose_name="Nombre del curso")
    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'groups__name': 'Docente'}, 
        verbose_name="Docente",
        related_name='courses'  
    )
    description = models.TextField(blank=True, verbose_name="Descripción")
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)  # Mantener campo existente
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def total_assignments(self):
        return self.assignment_set.count()
    
    @property
    def active_assignments(self):
        return self.assignment_set.filter(is_active=True, due_date__gte=timezone.now()).count()

class Assignment(models.Model):
    """Modelo para las asignaciones de presentaciones"""
    ASSIGNMENT_TYPES = [
        ('PRESENTATION', 'Presentación Individual'),
        ('GROUP_PRESENTATION', 'Presentación Grupal'),
        ('DEBATE', 'Debate'),
        ('CONFERENCE', 'Conferencia'),
        ('PITCH', 'Pitch de Negocio'),
        ('SEMINAR', 'Seminario'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso")
    assignment_type = models.CharField(
        max_length=20, 
        choices=ASSIGNMENT_TYPES, 
        default='PRESENTATION', 
        verbose_name="Tipo"
    )
    max_duration = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        help_text="Duración máxima en minutos", 
        verbose_name="Duración máxima (min)"
    )
    due_date = models.DateTimeField(verbose_name="Fecha límite")
    max_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=100.00,
        validators=[MinValueValidator(0.01), MaxValueValidator(999.99)],
        verbose_name="Puntaje máximo"
    )
    instructions = models.TextField(blank=True, verbose_name="Instrucciones")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Asignación"
        verbose_name_plural = "Asignaciones"
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"
    
    @property
    def is_expired(self):
        return timezone.now() > self.due_date
    
    @property
    def days_remaining(self):
        if self.is_expired:
            return 0
        delta = self.due_date - timezone.now()
        return delta.days
    
    @property
    def status_badge_class(self):
        if self.is_expired:
            return 'bg-danger'
        elif self.days_remaining <= 1:
            return 'bg-warning'
        elif self.days_remaining <= 7:
            return 'bg-info'
        else:
            return 'bg-success'

class Presentation(models.Model):
    """Modelo principal para las presentaciones"""
    STATUS_CHOICES = [
        ('UPLOADED', 'Subida'),
        ('PROCESSING', 'Procesando'),
        ('ANALYZED', 'Analizada por IA'),
        ('GRADED', 'Calificada'),
        ('FAILED', 'Error en procesamiento'),
        ('REJECTED', 'Rechazada'),
    ]
    

    title = models.CharField(max_length=200, verbose_name="Título de la presentación")
    description = models.TextField(blank=True, verbose_name="Descripción")  # Renombrar a 'notes' en views
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'groups__name': 'Estudiante'}, 
        verbose_name="Estudiante",
        related_name='presentations' 
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name="Asignación", null=True, blank=True)
    
    # Archivo de video
    video_file = models.FileField(
        upload_to=upload_to_presentations, 
        verbose_name="Archivo de video",
        null=True, blank=True  # Temporal hasta migrar datos existentes
    )
    transcript = models.TextField(blank=True, verbose_name="Transcripción automática")
    
    # Metadatos del archivo
    duration = models.DurationField(null=True, blank=True, verbose_name="Duración")
    file_size = models.BigIntegerField(null=True, blank=True, verbose_name="Tamaño del archivo (bytes)")
    
    # Estado y timestamps
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='UPLOADED', 
        verbose_name="Estado"
    )
    uploaded_at = models.DateTimeField(null=True, blank=True, verbose_name="Subida el")  # Usar created_at si es null
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="Procesada el")
    
    # Análisis de IA - Puntajes principales
    ai_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Puntaje IA general"
    )
    content_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Puntaje contenido"
    )
    fluency_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Puntaje fluidez"
    )
    body_language_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Puntaje lenguaje corporal"
    )
    voice_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Puntaje voz y dicción"
    )
    
    # Retroalimentación de IA
    ai_feedback = models.JSONField(
        default=dict, 
        blank=True, 
        verbose_name="Retroalimentación detallada IA"
    )
    
    # Calificación final del docente
    final_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00)],
        verbose_name="Puntaje final"
    )
    teacher_feedback = models.TextField(blank=True, verbose_name="Retroalimentación del docente")
    graded_at = models.DateTimeField(null=True, blank=True, verbose_name="Calificada el")
    graded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='graded_presentations',
        limit_choices_to={'groups__name': 'Docente'},
        verbose_name="Calificada por"
    )
    

    transcription_text = models.TextField(blank=True, null=True, help_text="Transcripción completa del video")
    transcription_segments = models.JSONField(blank=True, null=True, help_text="Segmentos de transcripción con timestamps")
    transcription_completed_at = models.DateTimeField(blank=True, null=True)
    audio_duration = models.FloatField(blank=True, null=True, help_text="Duración del audio en segundos")
    
    class Meta:
        verbose_name = 'Presentación'
        verbose_name_plural = 'Presentaciones'
        ordering = ['-created_at']  # Usar created_at por compatibilidad
    
    def __str__(self):
        return f"{self.title} - {self.student.get_full_name() or self.student.username}"
    
    @property
    def notes(self):
        """Alias para compatibilidad con vistas"""
        return self.description
    
    @property
    def uploaded_at_display(self):
        """Mostrar uploaded_at o created_at como fallback"""
        return self.uploaded_at or self.created_at
    
    @property
    def is_late(self):
        """Verifica si la presentación fue subida después de la fecha límite"""
        if hasattr(self, 'assignment') and self.assignment:
            return self.uploaded_at_display > self.assignment.due_date
        return False
    
    @property
    def status_display(self):
        """Devuelve el estado con icono HTML"""
        status_icons = {
            'UPLOADED': '<i class="fas fa-upload text-primary"></i> Subida',
            'PROCESSING': '<i class="fas fa-cogs text-warning"></i> Procesando',
            'ANALYZED': '<i class="fas fa-robot text-info"></i> Analizada por IA',
            'GRADED': '<i class="fas fa-star text-success"></i> Calificada',
            'FAILED': '<i class="fas fa-exclamation-triangle text-danger"></i> Error',
            'REJECTED': '<i class="fas fa-times-circle text-danger"></i> Rechazada',
        }
        return status_icons.get(self.status, self.get_status_display())
    
    @property
    def status_badge_class(self):
        """Devuelve la clase CSS para el badge del estado"""
        status_classes = {
            'UPLOADED': 'bg-primary',
            'PROCESSING': 'bg-warning',
            'ANALYZED': 'bg-info',
            'GRADED': 'bg-success',
            'FAILED': 'bg-danger',
            'REJECTED': 'bg-danger',
        }
        return status_classes.get(self.status, 'bg-secondary')
    
    @property
    def file_size_mb(self):
        """Devuelve el tamaño del archivo en MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
    
    @property
    def overall_ai_score(self):
        """Calcula el puntaje promedio de IA"""
        scores = [
            self.content_score,
            self.fluency_score,
            self.body_language_score,
            self.voice_score
        ]
        valid_scores = [score for score in scores if score is not None]
        if valid_scores:
            return round(sum(valid_scores) / len(valid_scores), 2)
        return None
    
    def delete(self, *args, **kwargs):
        """Override delete para eliminar el archivo físico"""
        if self.video_file:
            if os.path.isfile(self.video_file.path):
                os.remove(self.video_file.path)
        super().delete(*args, **kwargs)

class AIAnalysis(models.Model):
    """Modelo para almacenar análisis detallados de IA"""
    presentation = models.OneToOneField(
        Presentation, 
        on_delete=models.CASCADE, 
        related_name='ai_analysis'
    )
    
    # Análisis de contenido (usando IA para validar tema)
    content_keywords = models.JSONField(default=list, blank=True, verbose_name="Palabras clave detectadas")
    content_relevance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Relevancia del contenido"
    )
    content_depth = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Profundidad del contenido"
    )
    topic_coverage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Cobertura del tema asignado"
    )
    
    # Análisis de audio/voz (usando SpeechRecognition)
    speech_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Velocidad del habla (palabras/minuto)"
    )
    pause_frequency = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Frecuencia de pausas"
    )
    volume_variation = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Variación de volumen"
    )
    pronunciation_clarity = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Claridad de pronunciación"
    )
    
    # Análisis visual (usando OpenCV)
    eye_contact_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Porcentaje de contacto visual"
    )
    gesture_frequency = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Frecuencia de gestos por minuto"
    )
    posture_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Puntaje de postura"
    )
    movement_naturalness = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Naturalidad del movimiento"
    )
    
    # Timestamps del análisis
    analyzed_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Tiempo de procesamiento (segundos)"
    )
    
    # Datos brutos del análisis (para debugging y mejoras futuras)
    raw_data = models.JSONField(default=dict, blank=True, verbose_name="Datos brutos del análisis")
    
    # Recomendaciones generadas por IA
    recommendations = models.JSONField(
        default=list, 
        blank=True, 
        verbose_name="Recomendaciones de mejora"
    )
    
    class Meta:
        verbose_name = "Análisis de IA"
        verbose_name_plural = "Análisis de IA"
        ordering = ['-analyzed_at']
    
    def __str__(self):
        return f"Análisis IA - {self.presentation}"
