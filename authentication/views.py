from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, LoginForm, PasswordResetForm, SetPasswordForm
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
                return redirect('auth:login')  
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
            return redirect('auth:profile')  
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'auth/profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('auth:login')  

@login_required
def dashboard_view(request):
    """Dashboard principal que redirige según el rol del usuario"""
    # Crear perfil si no existe
    if not hasattr(request.user, 'profile') or not request.user.profile:
        from .models import Profile
        Profile.objects.create(user=request.user)
        messages.info(request, 'Se ha creado tu perfil automáticamente.')
    
    profile = request.user.profile
    
    # Redirigir según el grupo del usuario
    if request.user.groups.filter(name='Docente').exists():
        return redirect('presentations:teacher_dashboard')
    elif request.user.groups.filter(name='Estudiante').exists():
        return redirect('auth:student_dashboard')
    elif request.user.groups.filter(name='Administrador').exists():
        return render(request, 'dashboard/admin.html', {
            'user': request.user,
            'profile': profile,
        })
    else:
        # Usuario sin rol asignado
        messages.warning(request, 'Tu cuenta no tiene un rol asignado. Contacta al administrador.')
        return redirect('auth:login')

@login_required
@student_required
def student_dashboard_view(request):
    """Dashboard para estudiantes con estadísticas """
    from django.db.models import Avg, Count
    from django.utils import timezone
    from apps.presentaciones.models import Presentation, Assignment
    
    # Obtener presentaciones del estudiante
    user_presentations = Presentation.objects.filter(student=request.user)
    
    # Estadísticas del estudiante
    stats = {
        'total_presentations': user_presentations.count(),
        'completed_presentations': user_presentations.filter(status='GRADED').count(),
        'pending_presentations': user_presentations.filter(status__in=['UPLOADED', 'PROCESSING', 'ANALYZED']).count(),
        'average_score': 0.0
    }
    
    # Calcular promedio general
    if stats['completed_presentations'] > 0:
        avg_score = user_presentations.filter(
            status='GRADED',
            final_score__isnull=False
        ).aggregate(Avg('final_score'))['final_score__avg']
        stats['average_score'] = round(avg_score, 1) if avg_score else 0.0
    
    # Asignaciones pendientes
    # Obtener todos los cursos donde el usuario está inscrito
    user_courses = request.user.enrolled_courses.filter(is_active=True)
    
    # Obtener todas las asignaciones activas de esos cursos
    all_assignments = Assignment.objects.filter(
        course__in=user_courses,
        is_active=True,
        due_date__gte=timezone.now()
    ).select_related('course')
    
    # Filtrar asignaciones que el usuario ya completó
    # Solo excluir si tiene presentaciones activas (las borradas ya no están en la BD)
    completed_assignment_ids = user_presentations.values_list('assignment_id', flat=True)
    
    pending_assignments = all_assignments.exclude(
        id__in=completed_assignment_ids
    ).order_by('due_date')[:10]  # Aumentado a 10 para mostrar más tareas
    
    # Presentaciones recientes
    recent_presentations = user_presentations.select_related(
        'assignment', 'assignment__course'
    ).order_by('-uploaded_at')[:5]
    
    # Progreso académico
    progress = {
        'completion_percentage': 0,
        'quality_percentage': 0
    }
    
    if stats['total_presentations'] > 0:
        progress['completion_percentage'] = (stats['completed_presentations'] / stats['total_presentations']) * 100
        
        # Calcular calidad promedio basada en score IA
        avg_ai_score = user_presentations.filter(
            ai_score__isnull=False
        ).aggregate(Avg('ai_score'))['ai_score__avg']
        progress['quality_percentage'] = avg_ai_score if avg_ai_score else 0
    
    context = {
        'user': request.user,
        'profile': request.user.profile,
        'stats': stats,
        'progress': progress,
        'pending_assignments': pending_assignments,
        'recent_presentations': recent_presentations,
    }
    
    return render(request, 'dashboard/estudiantes.html', context)

def check_username(request):
    """Vista AJAX para verificar si un nombre de usuario está disponible"""
    username = request.GET.get('username')
    if username:
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': True})



# VISTAS DE RECUPERACIÓN DE CONTRASEÑA


@csrf_protect
def password_reset_view(request):
    """Vista para solicitar recuperación de contraseña"""
    if request.user.is_authenticated:
        return redirect('auth:dashboard')
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Generar token y enlace de recuperación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Crear el enlace de recuperación
            reset_url = request.build_absolute_uri(
                f'/auth/password-reset-confirm/{uid}/{token}/'
            )
            
            # Preparar el contenido del email
            context = {
                'user': user,
                'reset_url': reset_url,
                'site_name': 'EvalExpo AI'
            }
            
            subject = 'Recuperación de contraseña - EvalExpo AI'
            html_message = render_to_string('auth/password_reset_email.html', context)
            plain_message = render_to_string('auth/password_reset_email.txt', context)
            
            try:
                # Enviar email
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                messages.success(
                    request, 
                    f'Se ha enviado un enlace de recuperación a {email}. '
                    'Revisa tu bandeja de entrada y carpeta de spam.'
                )
                return redirect('auth:password_reset_sent')
                
            except Exception as e:
                messages.error(
                    request,
                    'Error al enviar el correo. Inténtalo de nuevo más tarde.'
                )
    else:
        form = PasswordResetForm()
    
    return render(request, 'auth/password_reset.html', {'form': form})


def password_reset_sent_view(request):
    """Vista que confirma que se envió el email de recuperación"""
    return render(request, 'auth/password_reset_sent.html')


@csrf_protect
def password_reset_confirm_view(request, uidb64, token):
    """Vista para confirmar y establecer nueva contraseña"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                
                messages.success(
                    request,
                    '¡Contraseña actualizada exitosamente! Ahora puedes iniciar sesión.'
                )
                return redirect('auth:password_reset_complete')
        else:
            form = SetPasswordForm()
        
        return render(request, 'auth/password_reset_confirm.html', {
            'form': form,
            'validlink': True,
            'user': user
        })
    else:
        return render(request, 'auth/password_reset_confirm.html', {
            'validlink': False
        })


def password_reset_complete_view(request):
    """Vista que confirma que la contraseña fue restablecida"""
    return render(request, 'auth/password_reset_complete.html')
