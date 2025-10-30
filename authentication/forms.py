from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres'
        })
    )
    
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    

    role = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Estudiante', 'Docente', 'Administrador']),
        required=True,
        empty_label="Selecciona tu rol",
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Selecciona el rol que corresponde a tu función."
    )
    
    institution = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Universidad o Institución'
        })
    )
    
    phone = forms.CharField(
        max_length=15, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar widgets para los campos de contraseña
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # Asignar el grupo seleccionado al usuario
            selected_group = self.cleaned_data['role']
            user.groups.add(selected_group)
            
            # Actualizar perfil con datos adicionales
            if hasattr(user, 'profile'):
                profile = user.profile
            else:
                profile = Profile.objects.create(user=user)
                
            profile.institution = self.cleaned_data['institution']
            profile.phone = self.cleaned_data['phone']
            profile.save()
            
        return user

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    

    role = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Estudiante', 'Docente', 'Administrador']),
        required=True,
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        help_text="Tu rol actual en el sistema (no editable)."
    )

    class Meta:
        model = Profile
        fields = ['institution', 'phone', 'avatar']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Universidad o Institución'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'institution': 'Institución',
            'phone': 'Teléfono',
            'avatar': 'Foto de Perfil',
        }
        help_texts = {
            'avatar': 'Formatos permitidos: JPG, PNG, GIF. Tamaño máximo: 5MB',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            # Prellenar campos del usuario
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            
            # Prellenar el grupo actual
            user_groups = self.instance.user.groups.filter(name__in=['Estudiante', 'Docente', 'Administrador'])
            if user_groups.exists():
                self.fields['role'].initial = user_groups.first()

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Solo validar si es un archivo nuevo (no el archivo existente)
            if hasattr(avatar, 'content_type'):
                # Verificar tamaño del archivo (5MB máximo)
                if avatar.size > 5 * 1024 * 1024:
                    raise forms.ValidationError('El archivo es demasiado grande. Tamaño máximo: 5MB')
                
                # Verificar tipo de archivo
                if not avatar.content_type.startswith('image/'):
                    raise forms.ValidationError('El archivo debe ser una imagen (JPG, PNG, GIF)')
        
        return avatar

    def save(self, commit=True):
        profile = super().save(commit=False)
        
        if commit:
            # Actualizar datos del usuario
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            
            # NO actualizar grupos (campo deshabilitado para evitar errores)
            # Los grupos deben ser asignados por administradores
            
            profile.save()
            
        return profile

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password'
        })
    )


class PasswordResetForm(forms.Form):
    """Formulario para solicitar recuperación de contraseña"""
    email = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingresa tu correo electrónico',
            'autocomplete': 'email'
        }),
        help_text="Te enviaremos un enlace para restablecer tu contraseña."
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'No existe una cuenta con este correo electrónico.'
            )
        return email


class SetPasswordForm(forms.Form):
    """Formulario para establecer nueva contraseña"""
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Nueva contraseña',
            'autocomplete': 'new-password'
        }),
        help_text="Tu contraseña debe tener al menos 8 caracteres."
    )
    
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirma tu nueva contraseña',
            'autocomplete': 'new-password'
        })
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden.')
            if len(password1) < 8:
                raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        return password2