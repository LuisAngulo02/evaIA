from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Notification, NotificationSettings
from .services import NotificationService


@login_required
def notification_list(request):
    """Vista para listar todas las notificaciones del usuario"""
    notifications = NotificationService.get_user_notifications(request.user)
    
    # Paginación
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'notifications': page_obj,
        'unread_count': NotificationService.get_unread_count(request.user),
    }
    
    return render(request, 'notifications/notification_list.html', context)


@login_required
def notification_dropdown(request):
    """Vista AJAX para el dropdown de notificaciones"""
    notifications = NotificationService.get_user_notifications(request.user, limit=5)
    unread_count = NotificationService.get_unread_count(request.user)
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    
    return render(request, 'notifications/notification_dropdown.html', context)


@login_required
def mark_as_read(request, notification_id):
    """Marcar una notificación específica como leída"""
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        recipient=request.user
    )
    
    # Solo marcar como leída si es POST o GET (para compatibilidad)
    if request.method in ['POST', 'GET']:
        notification.mark_as_read()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.method == 'POST':
            return JsonResponse({
                'success': True,
                'unread_count': NotificationService.get_unread_count(request.user)
            })
        
        # Si hay URL de acción, redirigir ahí
        if notification.action_url:
            return redirect(notification.action_url)
        
        return redirect('notifications:list')
    
    # Si no es GET o POST, devolver error
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


@login_required
@require_POST 
def mark_all_as_read(request):
    """Marcar todas las notificaciones como leídas"""
    count = NotificationService.mark_all_as_read(request.user)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'marked_count': count,
            'unread_count': 0
        })
    
    messages.success(request, f'Se marcaron {count} notificaciones como leídas.')
    return redirect('notifications:list')


@login_required
def notification_settings(request):
    """Vista para configurar las notificaciones"""
    settings, created = NotificationSettings.objects.get_or_create(
        user=request.user
    )
    
    if request.method == 'POST':
        # Actualizar configuraciones
        settings.receive_grade_notifications = request.POST.get('receive_grade_notifications') == 'on'
        settings.receive_assignment_notifications = request.POST.get('receive_assignment_notifications') == 'on'
        settings.receive_course_notifications = request.POST.get('receive_course_notifications') == 'on'
        settings.receive_system_notifications = request.POST.get('receive_system_notifications') == 'on'
        settings.email_notifications = request.POST.get('email_notifications') == 'on'
        settings.digest_frequency = request.POST.get('digest_frequency', 'NEVER')
        
        settings.save()
        
        messages.success(request, 'Configuración de notificaciones actualizada exitosamente.')
        return redirect('notifications:settings')
    
    context = {
        'settings': settings,
    }
    
    return render(request, 'notifications/settings.html', context)