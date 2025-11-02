from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def has_group(user, group_name):
    """
    Verifica si un usuario pertenece a un grupo específico
    Uso: {% if user|has_group:"Estudiante" %}
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()

@register.filter
def is_student(user):
    """
    Verifica si el usuario es estudiante
    Uso: {% if user|is_student %}
    """
    return has_group(user, 'Estudiante')

@register.filter
def is_teacher(user):
    """
    Verifica si el usuario es docente
    Uso: {% if user|is_teacher %}
    """
    return has_group(user, 'Docente')

@register.filter
def is_admin(user):
    """
    Verifica si el usuario es administrador
    Uso: {% if user|is_admin %}
    """
    return has_group(user, 'Administrador')

@register.filter
def user_role(user):
    """
    Obtiene el rol principal del usuario
    Uso: {{ user|user_role }}
    """
    if not user.is_authenticated:
        return 'Sin autenticar'
    
    user_group = user.groups.filter(name__in=['Administrador', 'Docente', 'Estudiante']).first()
    return user_group.name if user_group else 'Sin rol'