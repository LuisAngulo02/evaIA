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
        verbose_name="Duración máxima (max)"
    )
    due_date = models.DateTimeField(verbose_name="Fecha límite")
    max_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=100.00,
        validators=[MinValueValidator(0.01), MaxValueValidator(999.99)],
        verbose_name="Puntaje máximo"
    )
    strictness_level = models.CharField(
        max_length=20,
        choices=[
            ('strict', 'Estricto - Evaluación rigurosa'),
            ('moderate', 'Moderado - Evaluación balanceada (Recomendado)'),
            ('lenient', 'Permisivo - Evaluación flexible')
        ],
        null=True,
        blank=True,
        verbose_name="Nivel de Rigurosidad de IA",
        help_text="Nivel de exigencia en la evaluación con IA. Si no se especifica, se usará la configuración global del docente."
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
    video_thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True,
        verbose_name="Miniatura del video"
    )
    
    # Campos de Cloudinary
    cloudinary_public_id = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="ID público en Cloudinary",
        help_text="ID del video almacenado en Cloudinary"
    )
    cloudinary_url = models.URLField(
        blank=True, 
        null=True,
        verbose_name="URL de Cloudinary",
        help_text="URL segura del video en Cloudinary"
    )
    cloudinary_thumbnail_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL miniatura Cloudinary",
        help_text="URL de la miniatura del video en Cloudinary"
    )
    is_stored_in_cloud = models.BooleanField(
        default=False,
        verbose_name="Almacenado en la nube",
        help_text="Indica si el video está en Cloudinary"
    )
    
    transcript = models.TextField(blank=True, verbose_name="Transcripción automática")
    
    # Metadatos del archivo
    duration = models.DurationField(null=True, blank=True, verbose_name="Duración")
    duration_seconds = models.FloatField(null=True, blank=True, verbose_name="Duración en segundos")
    video_width = models.IntegerField(null=True, blank=True, verbose_name="Ancho del video")
    video_height = models.IntegerField(null=True, blank=True, verbose_name="Alto del video")
    video_fps = models.FloatField(null=True, blank=True, verbose_name="FPS del video")
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
    
    # Análisis de participación con detección de rostros
    participation_data = models.JSONField(
        blank=True, 
        null=True, 
        help_text="Datos de participación detectados mediante análisis de rostros (Persona 1, Persona 2, etc.)"
    )
    analyzed_at = models.DateTimeField(blank=True, null=True, help_text="Fecha de análisis completo de IA")
    
    # Análisis de liveness (video en vivo vs pregrabado)
    is_live_recording = models.BooleanField(
        default=False,
        help_text="Indica si el video fue grabado en vivo"
    )
    liveness_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        help_text="Score de liveness (0-100, mayor = más probable en vivo)"
    )
    liveness_confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        help_text="Confianza del análisis de liveness"
    )
    recording_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('LIVE', 'En Vivo'),
            ('LIKELY_LIVE', 'Probablemente en Vivo'),
            ('LIKELY_RECORDED', 'Probablemente Pregrabado'),
            ('RECORDED', 'Pregrabado'),
            ('UNKNOWN', 'Desconocido'),
        ],
        help_text="Tipo de grabación detectado"
    )
    
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
    
    def get_video_url(self):
        """
        Obtener URL del video (Cloudinary o local)
        Prioriza Cloudinary si está disponible
        """
        if self.is_stored_in_cloud and self.cloudinary_url:
            return self.cloudinary_url
        elif self.video_file:
            return self.video_file.url
        return None
    
    def get_thumbnail_url(self):
        """
        Obtener URL de la miniatura (Cloudinary o local)
        """
        if self.cloudinary_thumbnail_url:
            return self.cloudinary_thumbnail_url
        elif self.video_thumbnail:
            return self.video_thumbnail.url
        return None
    
    def upload_to_cloudinary(self):
        """
        Subir video a Cloudinary si no está ya subido
        Returns: dict con resultado o None si falla
        """
        from apps.ai_processor.services import CloudinaryService
        import logging
        
        logger = logging.getLogger(__name__)
        
        if self.is_stored_in_cloud:
            logger.info(f"Video ya está en Cloudinary: {self.cloudinary_public_id}")
            return {'success': True, 'message': 'Ya está en Cloudinary', 'url': self.cloudinary_url}
        
        if not self.video_file:
            logger.error("No hay archivo de video para subir")
            return None
        
        try:
            logger.info(f"Subiendo video a Cloudinary: {self.title}")
            
            # Crear carpeta específica para el estudiante
            folder = f'presentations/{self.student.username}'
            
            # Subir video
            result = CloudinaryService.upload_video(
                self.video_file.path,
                folder=folder,
                public_id=f"{self.id}_{self.title[:50]}"  # ID único
            )
            
            if result:
                # Guardar información de Cloudinary
                self.cloudinary_public_id = result['public_id']
                self.cloudinary_url = result['secure_url']
                self.is_stored_in_cloud = True
                
                # Generar URL de miniatura automática
                self.cloudinary_thumbnail_url = CloudinaryService.get_video_url(
                    result['public_id']
                ).replace('/video/', '/video/so_0/')  # Primer frame como thumbnail
                
                self.save(update_fields=['cloudinary_public_id', 'cloudinary_url', 
                                        'cloudinary_thumbnail_url', 'is_stored_in_cloud'])
                
                logger.info(f"✅ Video subido a Cloudinary: {result['public_id']}")
                return result
            else:
                logger.error("Error subiendo video a Cloudinary")
                return None
                
        except Exception as e:
            logger.error(f"Error en upload_to_cloudinary: {e}")
            return None
    
    def delete_from_cloudinary(self):
        """
        Eliminar video de Cloudinary
        Returns: bool indicando éxito
        """
        from apps.ai_processor.services import CloudinaryService
        import logging
        
        logger = logging.getLogger(__name__)
        
        if not self.cloudinary_public_id:
            logger.warning("No hay public_id de Cloudinary para eliminar")
            return False
        
        try:
            success = CloudinaryService.delete_file(
                self.cloudinary_public_id,
                resource_type='video'
            )
            
            if success:
                # Limpiar campos de Cloudinary
                self.cloudinary_public_id = None
                self.cloudinary_url = None
                self.cloudinary_thumbnail_url = None
                self.is_stored_in_cloud = False
                self.save(update_fields=['cloudinary_public_id', 'cloudinary_url',
                                        'cloudinary_thumbnail_url', 'is_stored_in_cloud'])
                
                logger.info(f"✅ Video eliminado de Cloudinary")
                return True
            else:
                logger.warning("No se pudo eliminar de Cloudinary")
                return False
                
        except Exception as e:
            logger.error(f"Error eliminando de Cloudinary: {e}")
            return False
    
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
        """Override delete para eliminar archivos físicos y de Cloudinary"""
        import logging
        logger = logging.getLogger(__name__)
        
        # Eliminar de Cloudinary si está almacenado allí
        if self.is_stored_in_cloud and self.cloudinary_public_id:
            logger.info(f"Eliminando video de Cloudinary: {self.cloudinary_public_id}")
            self.delete_from_cloudinary()
        
        # Eliminar archivo local si existe
        if self.video_file:
            try:
                if os.path.isfile(self.video_file.path):
                    os.remove(self.video_file.path)
                    logger.info(f"Archivo local eliminado: {self.video_file.path}")
            except Exception as e:
                logger.error(f"Error eliminando archivo local: {e}")
        
        # Eliminar miniatura local si existe
        if self.video_thumbnail:
            try:
                if os.path.isfile(self.video_thumbnail.path):
                    os.remove(self.video_thumbnail.path)
                    logger.info(f"Miniatura eliminada: {self.video_thumbnail.path}")
            except Exception as e:
                logger.error(f"Error eliminando miniatura: {e}")
        
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


class Participant(models.Model):
    """
    Modelo para almacenar evaluación individual de cada participante
    en exposiciones grupales
    """
    presentation = models.ForeignKey(
        Presentation, 
        on_delete=models.CASCADE, 
        related_name='participants',
        verbose_name="Presentación"
    )
    label = models.CharField(
        max_length=50,
        verbose_name="Etiqueta",
        help_text="Persona 1, Persona 2, etc."
    )
    
    # Foto del participante
    photo = models.ImageField(
        upload_to='participant_photos/',
        null=True,
        blank=True,
        verbose_name="Foto del rostro",
        help_text="Captura del rostro detectado"
    )
    
    # Tiempo de participación
    participation_time = models.FloatField(
        verbose_name="Tiempo de participación (segundos)",
        help_text="Tiempo total que estuvo visible/hablando"
    )
    time_percentage = models.FloatField(
        verbose_name="Porcentaje de tiempo",
        help_text="% del tiempo total de la exposición"
    )
    
    # Segmentos de tiempo (intervalos de participación)
    time_segments = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Segmentos de tiempo",
        help_text="Intervalos de tiempo donde aparece (formato: [{'start': 10.5, 'end': 25.3}, ...])"
    )
    
    # Transcripción individual
    transcription = models.TextField(
        verbose_name="Transcripción",
        help_text="Texto transcrito de esta persona"
    )
    word_count = models.IntegerField(
        default=0,
        verbose_name="Cantidad de palabras"
    )
    
    # Evaluación de coherencia
    semantic_coherence = models.FloatField(
        default=0,
        verbose_name="Coherencia semántica",
        help_text="Similitud semántica con el tema (0-100)"
    )
    keywords_score = models.FloatField(
        default=0,
        verbose_name="Puntaje de palabras clave",
        help_text="Score basado en palabras clave del tema (0-100)"
    )
    depth_score = models.FloatField(
        default=0,
        verbose_name="Puntaje de profundidad",
        help_text="Evaluación de profundidad del contenido (0-100)"
    )
    
    # Calificación final
    coherence_score = models.FloatField(
        default=0,
        verbose_name="Nota de coherencia",
        help_text="Puntaje ponderado de coherencia (0-100)"
    )
    contribution_percentage = models.FloatField(
        default=0,
        verbose_name="Porcentaje de aporte",
        help_text="Aporte ponderado considerando tiempo y coherencia"
    )
    
    # Calificación de IA (automática)
    ai_grade = models.FloatField(
        default=0,
        verbose_name="Calificación IA",
        help_text="Calificación automática generada por IA (sobre 20)"
    )
    ai_feedback = models.TextField(
        blank=True,
        verbose_name="Retroalimentación IA",
        help_text="Feedback detallado generado por IA (150-250 palabras)"
    )
    
    # Calificación del profesor (manual, opcional)
    manual_grade = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Calificación manual",
        help_text="Calificación editada por el profesor (sobre 20)"
    )
    teacher_feedback = models.TextField(
        blank=True,
        verbose_name="Retroalimentación del profesor",
        help_text="Comentarios adicionales del profesor"
    )
    grade_modified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='modified_grades',
        verbose_name="Calificación modificada por"
    )
    grade_modified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de modificación"
    )
    
    @property
    def final_grade(self):
        """
        Retorna la calificación final:
        - Si el profesor editó manualmente, retorna manual_grade
        - Si no, retorna ai_grade (generada automáticamente)
        """
        return self.manual_grade if self.manual_grade is not None else self.ai_grade
    
    @property
    def final_feedback(self):
        """
        Retorna el feedback final:
        - Si hay feedback del profesor, lo combina con el de IA
        - Si no, solo retorna el de IA
        """
        if self.teacher_feedback:
            return f"**Retroalimentación del Profesor:**\n{self.teacher_feedback}\n\n**Análisis de IA:**\n{self.ai_feedback}"
        return self.ai_feedback
    
    @property
    def is_manually_graded(self):
        """Indica si la calificación fue modificada manualmente"""
        return self.manual_grade is not None
    
    # Nivel y observaciones
    coherence_level = models.CharField(
        max_length=20,
        default="Regular",
        verbose_name="Nivel de coherencia",
        help_text="Excelente, Muy Buena, Buena, Regular, Baja, Insuficiente"
    )
    observations = models.TextField(
        blank=True,
        verbose_name="Observaciones",
        help_text="Retroalimentación automática"
    )
    
    # Palabras clave encontradas
    keywords_found = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Palabras clave encontradas"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        ordering = ['-ai_grade']  # Ordenar por calificación de IA
        unique_together = ['presentation', 'label']
    
    def __str__(self):
        return f"{self.label} - {self.presentation} ({self.ai_grade}/20)"
    
    @property
    def grade_badge_class(self):
        """Retorna clase CSS según la calificación"""
        grade = self.final_grade  # Usa la propiedad que ya maneja manual vs IA
        if grade >= 18:
            return 'bg-success'
        elif grade >= 14:
            return 'bg-info'
        elif grade >= 11:
            return 'bg-warning'
        else:
            return 'bg-danger'
    
    @property
    def level_badge_class(self):
        """Retorna clase CSS según el nivel"""
        level_classes = {
            'Excelente': 'bg-success',
            'Muy Buena': 'bg-info',
            'Buena': 'bg-primary',
            'Regular': 'bg-warning',
            'Baja': 'bg-danger',
            'Insuficiente': 'bg-secondary'
        }
        return level_classes.get(self.coherence_level, 'bg-secondary')


class AIConfiguration(models.Model):
    """Configuración de IA personalizada por docente"""
    
    AI_MODELS = [
        ('llama-3.3-70b-versatile', 'Llama 3.3 70B (Recomendado)'),
        ('llama-3.1-70b-versatile', 'Llama 3.1 70B'),
        ('mixtral-8x7b-32768', 'Mixtral 8x7B'),
    ]
    
    STRICTNESS_LEVELS = [
        ('strict', 'Estricto'),
        ('moderate', 'Moderado'),
        ('lenient', 'Suave'),
    ]
    
    teacher = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'groups__name': 'Docente'},
        verbose_name="Docente",
        related_name='ai_configuration'
    )
    
    # Nivel de estrictez para evaluación de coherencia
    strictness_level = models.CharField(
        max_length=20,
        choices=STRICTNESS_LEVELS,
        default='moderate',
        verbose_name="Nivel de Estrictez"
    )
    
    # Configuración del modelo de IA
    ai_model = models.CharField(
        max_length=50,
        choices=AI_MODELS,
        default='llama-3.3-70b-versatile',
        verbose_name="Modelo de IA"
    )
    
    ai_temperature = models.FloatField(
        default=0.3,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        verbose_name="Temperatura del modelo"
    )
    
    # Configuración de detección facial
    face_detection_confidence = models.FloatField(
        default=0.7,
        validators=[MinValueValidator(0.1), MaxValueValidator(1.0)],
        verbose_name="Confianza de detección facial"
    )
    
    # Pesos de evaluación (deben sumar 100)
    coherence_weight = models.FloatField(
        default=40.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name="Peso de coherencia (%)"
    )
    
    face_detection_weight = models.FloatField(
        default=20.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name="Peso de detección facial (%)"
    )
    
    duration_weight = models.FloatField(
        default=20.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name="Peso de duración (%)"
    )
    
    manual_weight = models.FloatField(
        default=20.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name="Peso de calificación manual (%)"
    )
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de IA"
        verbose_name_plural = "Configuraciones de IA"
        
    def __str__(self):
        return f"Config IA - {self.teacher.get_full_name() or self.teacher.username}"
    
    def clean(self):
        """Validar que los pesos sumen 100%"""
        from django.core.exceptions import ValidationError
        
        total_weight = (
            self.coherence_weight + 
            self.face_detection_weight + 
            self.duration_weight + 
            self.manual_weight
        )
        
        if abs(total_weight - 100.0) > 0.1:
            raise ValidationError(
                f'Los pesos deben sumar exactamente 100%. Suma actual: {total_weight}%'
            )
    
    def save(self, *args, **kwargs):
        """Validar antes de guardar"""
        self.clean()
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config_for_teacher(cls, teacher):
        """Obtener o crear configuración para un docente"""
        config, created = cls.objects.get_or_create(
            teacher=teacher,
            defaults={
                'strictness_level': 'moderate',
                'ai_model': 'llama-3.3-70b-versatile',
                'ai_temperature': 0.3,
                'face_detection_confidence': 0.7,
                'coherence_weight': 40.0,
                'face_detection_weight': 20.0,
                'duration_weight': 20.0,
                'manual_weight': 20.0,
            }
        )
        return config
    
    def get_strictness_description(self):
        """Obtener descripción del nivel de estrictez"""
        descriptions = {
            'strict': {
                'title': 'Estricto',
                'items': [
                    'Requiere dominio completo del tema',
                    'Penaliza imprecisiones y falta de profundidad',
                    'Exige estructura clara y ejemplos concretos'
                ]
            },
            'moderate': {
                'title': 'Moderado',
                'items': [
                    '70-95% para presentaciones bien desarrolladas',
                    '85-95% para presentaciones sobresalientes',
                    'Balance entre exigencia y comprensión',
                    'Valora profundidad y relevancia del contenido'
                ]
            },
            'lenient': {
                'title': 'Suave',
                'items': [
                    '70-80% con comprensión básica del tema',
                    '85-95% si el contenido es relevante',
                    'Valora el esfuerzo y participación',
                    'Enfoque en reforzar lo positivo'
                ]
            }
        }
        return descriptions.get(self.strictness_level, descriptions['moderate'])
