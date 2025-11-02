from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services import NotificationService


@login_required
def notification_dropdown_simple(request):
    """Vista simple para el dropdown de notificaciones"""
    try:
        notifications = NotificationService.get_user_notifications(request.user, limit=5)
        unread_count = NotificationService.get_unread_count(request.user)
        
        # Crear HTML mejorado
        html = f"""
        <div class="dropdown-header d-flex justify-content-between align-items-center px-3 py-2">
            <span class="fw-bold">
                <i class="fas fa-bell me-2"></i>Notificaciones
            </span>
            {f'<span class="badge bg-primary rounded-pill">{unread_count}</span>' if unread_count > 0 else ''}
        </div>
        """
        
        if notifications.exists():
            for notification in notifications:
                unread_class = 'unread' if not notification.is_read else ''
                action_url = notification.get_action_url()
                
                # Escapar comillas en el mensaje para evitar problemas con HTML
                title_safe = notification.title.replace('"', '&quot;').replace("'", '&#39;')
                message_safe = notification.message.replace('"', '&quot;').replace("'", '&#39;')
                
                html += f"""
                <a href="{action_url}" class="dropdown-item notification-item {unread_class} cursor-pointer" 
                   data-notification-id="{notification.id}"
                   onclick="handleNotificationClick(event, {notification.id})">
                    <div class="d-flex align-items-start">
                        <div class="notification-icon me-3">
                            <i class="{notification.icon_class}"></i>
                        </div>
                        <div class="flex-grow-1">
                            <h6 class="mb-1 notification-title">{title_safe}</h6>
                            <p class="mb-1 small notification-message">{message_safe}</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <small class="text-muted notification-time">
                                    <i class="far fa-clock me-1"></i>{notification.time_since_created}
                                </small>
                                {f'<span class="badge badge-sm bg-primary">Nuevo</span>' if not notification.is_read else ''}
                            </div>
                        </div>
                    </div>
                </a>
                """
        else:
            html += """
            <div class="dropdown-item text-center py-4">
                <i class="fas fa-bell-slash fa-2x text-muted mb-2"></i>
                <p class="mb-0 text-muted">No hay notificaciones</p>
            </div>
            """
        
        html += f"""
        <div class="dropdown-divider m-0"></div>
        <div class="dropdown-item text-center py-2">
            <a href="/notifications/" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-list me-1"></i>Ver todas las notificaciones
            </a>
        </div>
        """
        
        return JsonResponse({
            'success': True,
            'html': html,
            'unread_count': unread_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def api_unread_count(request):
    """API endpoint para obtener el conteo de notificaciones no leídas"""
    try:
        unread_count = NotificationService.get_unread_count(request.user)
        return JsonResponse({
            'success': True,
            'unread_count': unread_count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)