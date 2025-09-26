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
        empty_label="Selecciona tu rol",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Tu rol actual en el sistema."
    )

    class Meta:
        model = Profile
        fields = ['institution', 'phone']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
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

    def save(self, commit=True):
        profile = super().save(commit=False)
        
        if commit:
            # Actualizar datos del usuario
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            
            # Actualizar grupos
            # Primero remover grupos de rol existentes
            user.groups.filter(name__in=['Estudiante', 'Docente', 'Administrador']).delete()
            # Añadir el nuevo grupo
            selected_group = self.cleaned_data['role']
            user.groups.add(selected_group)
            
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