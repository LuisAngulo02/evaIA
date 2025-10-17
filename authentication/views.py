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
from .forms import CustomUserCreationForm, ProfileForm, LoginForm
from .decoradores import group_required, student_required, teacher_required, admin_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('auth:dashboard')
    
    if request.method == 'POST':
        # Si es solicitud de recuperación de contraseña
        if 'recover_password' in request.POST:
            email = request.POST.get('email')
            
            try:
                user = User.objects.get(email=email)
                
                # Generar token seguro
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Construir URL del enlace (usamos la misma página de login con parámetros)
                reset_url = request.build_absolute_uri(
                    f'/auth/login/?uid={uid}&token={token}'
                )
                
                # Preparar contenido del correo
                subject = 'Recuperación de Contraseña - EvalExpo AI'
                message = render_to_string('auth/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                    'valid_minutes': 10,
                })
                
                # Enviar correo
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=message,
                        fail_silently=False,
                    )
                    
                    # Limpiar la sesión después de enviar el email
                    request.session['show_recovery'] = False
                    request.session.modified = True
                    
                    # Si es AJAX, devolver JSON
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': True,
                            'message': 'Enlace de recuperación enviado exitosamente'
                        })
                    
                    messages.success(
                        request, 
                        'Se ha enviado un enlace de recuperación a tu correo. Revisa tu bandeja de entrada.'
                    )
                    return redirect('auth:login')
                except Exception as e:
                    # Si es AJAX, devolver error en JSON
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'error': 'Error al enviar el correo. Por favor, inténtalo más tarde.'
                        }, status=500)
                    
                    messages.error(
                        request,
                        'Error al enviar el correo. Por favor, inténtalo más tarde.'
                    )
                    print(f"Error sending email: {e}")
                    
            except User.DoesNotExist:
                # Por seguridad, no revelar si el correo existe o no
                # Limpiar la sesión
                request.session['show_recovery'] = False
                request.session.modified = True
                
                # Si es AJAX, devolver JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Si el correo está registrado, recibirás un enlace de recuperación.'
                    })
                
                messages.info(
                    request,
                    'Si el correo está registrado, recibirás un enlace de recuperación.'
                )
                return redirect('auth:login')
        
        # Si es cambio de contraseña (viene del enlace del correo)
        elif 'reset_password' in request.POST:
            uid = request.POST.get('uid')
            token = request.POST.get('token')
            password1 = request.POST.get('new_password1')
            password2 = request.POST.get('new_password2')
            
            try:
                user_id = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=user_id)
                
                if default_token_generator.check_token(user, token):
                    if password1 and password2 and password1 == password2:
                        if len(password1) >= 8:
                            user.set_password(password1)
                            user.save()
                            # Limpiar la sesión
                            request.session['show_recovery'] = False
                            request.session.modified = True
                            messages.success(request, '¡Contraseña actualizada exitosamente! Ahora puedes iniciar sesión.')
                            return redirect('auth:login')
                        else:
                            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                    else:
                        messages.error(request, 'Las contraseñas no coinciden.')
                else:
                    messages.error(request, 'El enlace de recuperación ha expirado o es inválido.')
                    return redirect('auth:login')
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                messages.error(request, 'El enlace de recuperación es inválido.')
                return redirect('auth:login')
        
        # Login normal
        else:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    # Limpiar la sesión después de login exitoso
                    request.session['show_recovery'] = False
                    request.session.modified = True
                    next_url = request.GET.get('next', 'auth:dashboard')
                    messages.success(request, f'¡Bienvenido, {user.first_name or user.username}!')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Credenciales inválidas.')
                    # SOLO aquí mostramos la opción de recuperación
                    request.session['show_recovery'] = True
                    request.session.modified = True
    else:
        form = LoginForm()
    
    # Verificar si viene con parámetros de reset
    uid = request.GET.get('uid')
    token = request.GET.get('token')
    show_reset_form = False
    
    if uid and token:
        # Si viene del enlace de reset, ocultar el formulario de recuperación
        request.session['show_recovery'] = False
        request.session.modified = True
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                show_reset_form = True
            else:
                messages.error(request, 'El enlace de recuperación ha expirado (10 minutos).')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'El enlace de recuperación es inválido.')
    else:
        # Si NO viene de un enlace de reset y es GET, asegurar que show_recovery esté en False
        # SOLO se pondrá en True cuando haya un error de login
        if request.method == 'GET' and 'show_recovery' not in request.session:
            request.session['show_recovery'] = False
            request.session.modified = True
    
    # Obtener el valor de show_recovery de la sesión
    show_recovery = request.session.get('show_recovery', False)
    
    context = {
        'form': form,
        'show_recovery': show_recovery,
        'show_reset_form': show_reset_form,
        'uid': uid,
        'token': token,
    }
    
    return render(request, 'auth/login.html', context)

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
    """Dashboard para estudiantes con estadísticas reales"""
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
    
    # Filtrar asignaciones que el usuario no ha completado
    completed_assignment_ids = user_presentations.values_list('assignment_id', flat=True)
    
    pending_assignments = all_assignments.exclude(
        id__in=completed_assignment_ids
    ).order_by('due_date')[:5]
    
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
