"""
Formularios para calificación y edición de participantes
"""
from django import forms
from .models import Participant


class ParticipantGradingForm(forms.ModelForm):
    """
    Formulario para que el profesor edite la calificación de un participante.
    
    El formulario viene pre-llenado con:
    - ai_grade: Calificación generada por IA (solo lectura)
    - ai_feedback: Retroalimentación de IA (solo lectura)
    - manual_grade: Campo editable para el profesor
    - teacher_feedback: Campo editable para comentarios adicionales
    """
    
    class Meta:
        model = Participant
        fields = ['manual_grade', 'teacher_feedback']
        widgets = {
            'manual_grade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.1',
                'placeholder': 'Calificación'
            }),
            'teacher_feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Comentarios adicionales del profesor (opcional)...'
            })
        }
        labels = {
            'manual_grade': 'Calificación Manual',
            'teacher_feedback': 'Comentarios del Profesor'
        }
        help_texts = {
            'manual_grade': 'Edita la calificación si deseas ajustar la evaluación de IA.',
            'teacher_feedback': 'Añade comentarios adicionales que complementen el análisis de IA.'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Obtener max_score de la asignación
        max_score = 20.0  # Valor por defecto
        if self.instance and self.instance.presentation and self.instance.presentation.assignment:
            max_score = float(self.instance.presentation.assignment.max_score)
        
        # Configurar el widget con el max_score dinámico
        self.fields['manual_grade'].widget.attrs['max'] = str(max_score)
        self.fields['manual_grade'].widget.attrs['placeholder'] = f'Calificación sobre {max_score}'
        self.fields['manual_grade'].label = f'Calificación Manual (sobre {max_score})'
        self.fields['manual_grade'].help_text = f'Edita la calificación si deseas ajustar la evaluación de IA (0-{max_score}).'
        
        # Si no hay calificación manual, pre-llenar con la de IA
        if self.instance and self.instance.manual_grade is None:
            if self.instance.ai_grade is not None:
                self.initial['manual_grade'] = self.instance.ai_grade
    
    def clean_manual_grade(self):
        """Valida que la calificación esté en el rango correcto según max_score de la asignación"""
        grade = self.cleaned_data.get('manual_grade')
        
        if grade is not None and self.instance:
            # Obtener max_score de la asignación
            max_score = 20.0
            if self.instance.presentation and self.instance.presentation.assignment:
                max_score = float(self.instance.presentation.assignment.max_score)
            
            if grade < 0 or grade > max_score:
                raise forms.ValidationError(f'La calificación debe estar entre 0 y {max_score}.')
        
        return grade


class BulkGradingForm(forms.Form):
    """
    Formulario para calificar múltiples participantes de una presentación
    """
    
    def __init__(self, *args, **kwargs):
        participants = kwargs.pop('participants', [])
        super().__init__(*args, **kwargs)
        
        # Crear campos dinámicamente para cada participante
        for participant in participants:
            # Campo de calificación
            self.fields[f'grade_{participant.id}'] = forms.FloatField(
                required=False,
                initial=participant.ai_grade,
                min_value=0,
                max_value=20,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control form-control-sm',
                    'step': '0.1',
                    'placeholder': 'Nota'
                }),
                label=f'{participant.label}'
            )
            
            # Campo de comentario
            self.fields[f'feedback_{participant.id}'] = forms.CharField(
                required=False,
                widget=forms.Textarea(attrs={
                    'class': 'form-control form-control-sm',
                    'rows': 2,
                    'placeholder': 'Comentario opcional'
                }),
                label=f'Comentario para {participant.label}'
            )
