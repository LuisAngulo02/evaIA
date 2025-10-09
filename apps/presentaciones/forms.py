from django import forms
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from .models import Presentation, Assignment, Course

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
                'accept': 'video/*',
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
        
        # Si es edición (instance existe), el video no es requerido
        if self.instance and self.instance.pk:
            self.fields['video_file'].required = False
            self.fields['video_file'].widget.attrs['required'] = False
        
        if user and user.groups.filter(name='Estudiante').exists():
            # Solo mostrar asignaciones activas y no vencidas
            self.fields['assignment'].queryset = Assignment.objects.filter(
                is_active=True,
                due_date__gte=timezone.now()
            ).select_related('course', 'course__teacher').order_by('due_date')
            
            # Personalizar el display de las asignaciones
            self.fields['assignment'].empty_label = "Selecciona una asignación..."
        else:
            self.fields['assignment'].queryset = Assignment.objects.none()
    
    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if video:
            # Validar tamaño (máximo 500MB)
            max_size = 500 * 1024 * 1024  # 500MB en bytes
            if video.size > max_size:
                raise forms.ValidationError('El archivo es demasiado grande. Máximo 500MB.')
            
            # Validar extensión
            valid_extensions = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'm4v']
            ext = video.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    f'Formato no válido. Formatos permitidos: {", ".join(valid_extensions).upper()}'
                )
        
        return video
    
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 5:
            raise forms.ValidationError('El título debe tener al menos 5 caracteres.')
        if len(title) > 200:
            raise forms.ValidationError('El título no puede exceder 200 caracteres.')
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        assignment = cleaned_data.get('assignment')
        
        if assignment:
            # Verificar que la asignación no esté vencida
            if assignment.due_date < timezone.now():
                raise forms.ValidationError('No puedes subir presentaciones a asignaciones vencidas.')
        
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
            'max_duration', 'due_date', 'max_score', 'instructions', 'is_active'
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