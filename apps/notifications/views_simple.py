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
        
        # Crear HTML simple
        html = f"""
        <div class="dropdown-header">
            <span class="fw-bold">Notificaciones ({unread_count})</span>
        </div>
        """
        
        if notifications.exists():
            for notification in notifications:
                unread_class = 'unread' if not notification.is_read else ''
                html += f"""
                <div class="dropdown-item notification-item {unread_class}" data-notification-id="{notification.id}">
                    <div class="d-flex">
                        <div class="flex-grow-1">
                            <h6 class="mb-1">{notification.title}</h6>
                            <p class="mb-0 small text-muted">{notification.message[:80]}...</p>
                            <small class="text-muted">{notification.time_since_created}</small>
                        </div>
                        {f'<span class="badge bg-primary">Nuevo</span>' if not notification.is_read else ''}
                    </div>
                </div>
                """
        else:
            html += """
            <div class="dropdown-item text-center">
                <i class="fas fa-bell-slash text-muted"></i>
                <p class="mb-0">No hay notificaciones</p>
            </div>
            """
        
        html += f"""
        <div class="dropdown-divider"></div>
        <div class="dropdown-item text-center">
            <a href="/notifications/" class="btn btn-sm btn-primary">Ver todas</a>
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