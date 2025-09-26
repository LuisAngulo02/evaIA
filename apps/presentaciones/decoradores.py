from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def role_required(*allowed_roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles permitidos
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if not hasattr(request.user, 'profile'):
                messages.error(request, 'Tu cuenta no tiene un perfil asociado. Contacta al administrador.')
                return redirect('login')
            
            user_role = request.user.profile.get_role()
            
            if user_role not in allowed_roles:
                messages.error(request, f'No tienes permisos para acceder a esta sección.')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def student_required(view_func):
    """Decorador específico para estudiantes"""
    return role_required('ESTUDIANTE')(view_func)

def teacher_required(view_func):
    """Decorador específico para docentes"""
    return role_required('DOCENTE')(view_func)

def admin_required(view_func):
    """Decorador específico para administradores"""
    return role_required('ADMIN')(view_func)

def teacher_or_admin_required(view_func):
    """Decorador para docentes y administradores"""
    return role_required('DOCENTE', 'ADMIN')(view_func)