from .services import NotificationService


def notification_context(request):
    """
    Context processor para agregar información de notificaciones a todas las plantillas
    """
    if request.user.is_authenticated:
        unread_count = NotificationService.get_unread_count(request.user)
        return {
            'unread_notifications_count': unread_count,
        }
    return {
        'unread_notifications_count': 0,
    }