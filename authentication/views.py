from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, LoginForm
from .decoradores import group_required, student_required, teacher_required, admin_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('auth:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'auth:dashboard')
                messages.success(request, f'¡Bienvenido, {user.first_name or user.username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Credenciales inválidas.')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})

@csrf_protect
def register_view(request):
    if request.user.is_authenticated:
        return redirect('auth:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
                return redirect('auth:login')  # ← Usar namespace
            except Exception as e:
                messages.error(request, 'Error al crear la cuenta. Inténtalo de nuevo.')
        else:
            # Se muestran los errores del formulario de manera más amigable
            field_names = {
                'username': 'Nombre de usuario',
                'first_name': 'Nombres',
                'last_name': 'Apellidos', 
                'email': 'Correo electrónico',
                'password1': 'Contraseña',
                'password2': 'Confirmación de contraseña',
                'role': 'Rol',
                'institution': 'Institución',
                'phone': 'Teléfono'
            }
            
            for field, errors in form.errors.items():
                field_display = field_names.get(field, field.title())
                for error in errors:
                    messages.error(request, f'{field_display}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('auth:profile')  # ← Usar namespace
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'auth/profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('auth:login')  # ← Usar namespace

@login_required
def dashboard_view(request):
    """Dashboard principal que redirige según el rol del usuario"""
    # Crear perfil si no existe
    if not hasattr(request.user, 'profile') or not request.user.profile:
        from .models import Profile
        Profile.objects.create(user=request.user)
        messages.info(request, 'Se ha creado tu perfil automáticamente.')
    
    profile = request.user.profile
    context = {
        'user': request.user,
        'profile': profile,
    }
    
    # Redirigir según el grupo del usuario
    if request.user.groups.filter(name='Docente').exists():
        return redirect('presentations:teacher_dashboard')
    elif request.user.groups.filter(name='Estudiante').exists():
        return render(request, 'dashboard/estudiantes.html', context)
    elif request.user.groups.filter(name='Administrador').exists():
        return render(request, 'dashboard/admin.html', context)
    else:
        # Usuario sin rol asignado
        messages.warning(request, 'Tu cuenta no tiene un rol asignado. Contacta al administrador.')
        return redirect('auth:login')

def check_username(request):
    """Vista AJAX para verificar si un nombre de usuario está disponible"""
    username = request.GET.get('username')
    if username:
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': True})
