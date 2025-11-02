"""
Template tags personalizados para presentaciones
"""
from django import template

register = template.Library()

@register.simple_tag
def get_video_url(presentation):
    """
    Obtiene la URL del video, priorizando Cloudinary sobre almacenamiento local
    
    Usage: {% get_video_url presentation %}
    """
    return presentation.get_video_url()

@register.simple_tag
def get_thumbnail_url(presentation):
    """
    Obtiene la URL de la miniatura, priorizando Cloudinary sobre almacenamiento local
    
    Usage: {% get_thumbnail_url presentation %}
    """
    return presentation.get_thumbnail_url()

@register.filter
def is_in_cloud(presentation):
    """
    Verifica si el video está almacenado en Cloudinary
    
    Usage: {% if presentation|is_in_cloud %}
    """
    return presentation.is_stored_in_cloud

@register.inclusion_tag('presentations/tags/cloud_badge.html')
def cloud_storage_badge(presentation):
    """
    Muestra un badge indicando dónde está almacenado el video
    
    Usage: {% cloud_storage_badge presentation %}
    """
    return {
        'is_in_cloud': presentation.is_stored_in_cloud,
        'cloudinary_url': presentation.cloudinary_url,
    }

@register.filter
def lookup(dictionary, key):
    """
    Permite acceder a valores de diccionarios en templates
    
    Usage: {{ dict|lookup:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)
