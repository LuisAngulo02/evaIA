from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import Profile
from authentication.decoradores import student_required, teacher_required, admin_required

# Vistas específicas de presentaciones
@student_required
def mis_presentaciones_view(request):
    """Vista para que los estudiantes vean sus presentaciones"""
    context = {
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'presentations/student_list.html', context)

@teacher_required
def gestionar_cursos_view(request):
    """Vista para que los docentes gestionen sus cursos"""
    context = {
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'courses/teacher_list.html', context)

@teacher_required
def crear_asignacion_view(request):
    """Vista para que los docentes creen asignaciones"""
    context = {
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'assignments/create.html', context)

@admin_required
def admin_panel_view(request):
    """Vista del panel de administración"""
    context = {
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'admin/panel.html', context)