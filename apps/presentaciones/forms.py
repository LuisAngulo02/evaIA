from django import forms
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from .models import Presentation, Assignment, Course
from .validators import validate_video_file

class PresentationUploadForm(forms.ModelForm):
    """Formulario para subir presentaciones"""
    
    class Meta:
        model = Presentation
        fields = ['assignment', 'title', 'video_file', 'description']  
        widgets = {
            'assignment': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': True,
                'id': 'assignment'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ej: Análisis de Límites en Funciones Trigonométricas',
                'required': True,
                'id': 'title'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'form-control d-none',
                'accept': 'video/mp4,video/webm,video/quicktime,video/x-msvideo',
                'id': 'id_video_file'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Agrega cualquier información adicional que consideres importante...',
                'id': 'notes'
            }),
        }
        labels = {
            'assignment': 'Asignación',
            'title': 'Título de la presentación',
            'video_file': 'Archivo de video',
            'description': 'Notas adicionales',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Guardar el usuario para usarlo en la validación
        self._user = user
        
        # Si es edición (instance existe), el video no es requerido
        if self.instance and self.instance.pk:
            self.fields['video_file'].required = False
            self.fields['video_file'].widget.attrs['required'] = False
            
            # En modo edición, el assignment no se debe validar/cambiar
            # El template mostrará la asignación como información estática
            self.fields['assignment'].required = False
        
        if user and user.groups.filter(name='Estudiante').exists():
            # Si es edición, mostrar solo la asignación actual
            if self.instance and self.instance.pk:
                self.fields['assignment'].queryset = Assignment.objects.filter(
                    id=self.instance.assignment_id
                )
            else:
                # Obtener IDs de asignaciones donde el estudiante ya subió presentación
                asignaciones_con_presentacion = Presentation.objects.filter(
                    student=user
                ).values_list('assignment_id', flat=True)
                
                # Solo mostrar asignaciones activas, no vencidas y SIN presentación previa
                self.fields['assignment'].queryset = Assignment.objects.filter(
                    is_active=True,
                    due_date__gte=timezone.now()
                ).exclude(
                    id__in=asignaciones_con_presentacion
                ).select_related('course', 'course__teacher').order_by('due_date')
                
                # Personalizar el display de las asignaciones
                self.fields['assignment'].empty_label = "Selecciona una asignación..."
        else:
            self.fields['assignment'].queryset = Assignment.objects.none()
    
    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        
        # Solo validar si no es edición o si se está subiendo un nuevo archivo
        if not video and not self.instance.pk:
            raise forms.ValidationError('Debes seleccionar un archivo de video.')
            
        if video:
            # Usar validador avanzado
            validate_video_file(video)
        
        return video
    
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('El título es obligatorio.')
        if len(title) < 5:
            raise forms.ValidationError('El título debe tener al menos 5 caracteres. Por ejemplo: "Análisis de Datos"')
        if len(title) > 200:
            raise forms.ValidationError('El título es demasiado largo. Máximo 200 caracteres.')
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        assignment = cleaned_data.get('assignment')
        
        if assignment:
            # Verificar que la asignación no esté vencida
            if assignment.due_date < timezone.now():
                raise forms.ValidationError('No puedes subir presentaciones a asignaciones vencidas.')
            
            # Verificar que el estudiante no haya subido ya una presentación para esta asignación
            # Solo aplica para nuevas presentaciones (no ediciones)
            if not self.instance.pk:
                user = getattr(self, '_user', None)
                if user:
                    existing_presentation = Presentation.objects.filter(
                        student=user,
                        assignment=assignment
                    ).exists()
                    
                    if existing_presentation:
                        raise forms.ValidationError(
                            f'Ya has subido una presentación para la asignación "{assignment.title}". '
                            'No puedes subir más de una presentación por asignación.'
                        )
        
        return cleaned_data

class CourseForm(forms.ModelForm):
    """Formulario para crear/editar cursos (solo docentes)"""
    
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Matemáticas I'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: MAT101'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del curso...'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

class AssignmentForm(forms.ModelForm):
    """Formulario para crear/editar asignaciones (solo docentes)"""
    
    class Meta:
        model = Assignment
        fields = [
            'title', 'description', 'course', 'assignment_type', 
            'max_duration', 'due_date', 'max_score', 'strictness_level', 'instructions', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Presentación Final - Límites y Derivadas'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe los objetivos y contenido de la asignación...'
            }),
            'course': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assignment_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'max_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 120,
                'placeholder': '15'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.01,
                'max': 999.99,
                'step': 0.01,
                'value': 100.00
            }),
            'strictness_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Instrucciones específicas para los estudiantes...'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Configurar queryset de cursos para el usuario
        if user and user.groups.filter(name='Docente').exists():
            self.fields['course'].queryset = Course.objects.filter(
                teacher=user,
                is_active=True
            ).order_by('name')
            self.fields['course'].empty_label = "Selecciona un curso..."
        else:
            self.fields['course'].queryset = Course.objects.none()
        
        # Configurar labels y help_text
        self.fields['title'].help_text = "Título descriptivo para la asignación"
        self.fields['max_duration'].help_text = "Duración máxima en minutos (1-120)"
        self.fields['due_date'].help_text = "Fecha y hora límite para entregar"
        self.fields['max_score'].help_text = "Puntaje máximo que se puede obtener"
        self.fields['strictness_level'].help_text = "Define cuán estricta será la evaluación con IA. Si no se especifica, se usará tu configuración global."
        self.fields['strictness_level'].empty_label = "Usar mi configuración global"
        
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date <= timezone.now():
            raise forms.ValidationError('La fecha límite debe ser futura.')
        return due_date
        
    def clean_max_duration(self):
        max_duration = self.cleaned_data.get('max_duration')
        if max_duration and (max_duration < 1 or max_duration > 120):
            raise forms.ValidationError('La duración debe estar entre 1 y 120 minutos.')
        return max_duration


class AIConfigurationForm(forms.Form):
    """Formulario para configurar parámetros de IA"""
    
    # Configuración de detección de rostros
    face_detection_confidence = forms.FloatField(
        label="Confianza de Detección de Rostros",
        initial=0.7,
        min_value=0.1,
        max_value=1.0,
        step_size=0.1,
        help_text="Umbral de confianza para detectar rostros (0.1 = más sensible, 1.0 = menos sensible)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1',
            'max': '1.0'
        })
    )
    
    # Configuración del modelo de IA
    ai_model = forms.ChoiceField(
        label="Modelo de IA",
        choices=[
            ('llama-3.3-70b-versatile', 'Llama 3.3 70B (Recomendado)'),
            ('llama-3.1-70b-versatile', 'Llama 3.1 70B'),
            ('mixtral-8x7b-32768', 'Mixtral 8x7B'),
        ],
        initial='llama-3.3-70b-versatile',
        help_text="Modelo de inteligencia artificial para análisis de coherencia",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Temperatura del modelo
    ai_temperature = forms.FloatField(
        label="Creatividad del Análisis",
        initial=0.3,
        min_value=0.0,
        max_value=1.0,
        step_size=0.1,
        help_text="Creatividad en el análisis (0.0 = muy conservador, 1.0 = muy creativo)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.0',
            'max': '1.0'
        })
    )
    
    # Pesos de evaluación
    coherence_weight = forms.FloatField(
        label="Peso de Coherencia (%)",
        initial=40,
        min_value=0,
        max_value=100,
        help_text="Porcentaje de la calificación basado en coherencia del discurso",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '100'
        })
    )
    
    face_detection_weight = forms.FloatField(
        label="Peso de Detección Facial (%)",
        initial=20,
        min_value=0,
        max_value=100,
        help_text="Porcentaje de la calificación basado en detección de rostro",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '100'
        })
    )
    
    duration_weight = forms.FloatField(
        label="Peso de Duración (%)",
        initial=20,
        min_value=0,
        max_value=100,
        help_text="Porcentaje de la calificación basado en duración apropiada",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '100'
        })
    )
    
    manual_weight = forms.FloatField(
        label="Peso de Calificación Manual (%)",
        initial=20,
        min_value=0,
        max_value=100,
        help_text="Porcentaje de la calificación basado en evaluación manual del docente",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '100'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que los pesos sumen 100%
        coherence = cleaned_data.get('coherence_weight', 0)
        face = cleaned_data.get('face_detection_weight', 0)
        duration = cleaned_data.get('duration_weight', 0)
        manual = cleaned_data.get('manual_weight', 0)
        
        total_weight = coherence + face + duration + manual
        
        if abs(total_weight - 100) > 0.1:  # Permitir pequeña tolerancia por decimales
            raise forms.ValidationError(
                f'Los pesos deben sumar exactamente 100%. Suma actual: {total_weight}%'
            )
        
        return cleaned_data
