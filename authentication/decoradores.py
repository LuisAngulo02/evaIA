from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def group_required(*group_names):
    """
    Decorador para verificar que el usuario pertenezca a uno de los grupos especificados
    Usa directamente los grupos nativos de Django
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario pertenece a alguno de los grupos permitidos
            user_groups = request.user.groups.filter(name__in=group_names)
            
            if not user_groups.exists():
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('auth:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def student_required(view_func):
    """Decorador específico para estudiantes"""
    return group_required('Estudiante')(view_func)

def teacher_required(view_func):
    """Decorador específico para docentes"""
    return group_required('Docente')(view_func)

def admin_required(view_func):
    """Decorador específico para administradores"""
    return group_required('Administrador')(view_func)

def teacher_or_admin_required(view_func):
    """Decorador para docentes y administradores"""
    return group_required('Docente', 'Administrador')(view_func)

def staff_required(view_func):
    """Decorador para personal (docentes y administradores)"""
    return group_required('Docente', 'Administrador')(view_func)