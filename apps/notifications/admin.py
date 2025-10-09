from django.contrib import admin
from .models import Notification, NotificationSettings


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'notification_type', 'priority', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username', 'recipient__email']
    readonly_fields = ['created_at', 'read_at']
    list_per_page = 20
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('recipient', 'title', 'message', 'notification_type', 'priority')
        }),
        ('Estado', {
            'fields': ('is_read', 'read_at', 'created_at', 'expires_at')
        }),
        ('Acciones', {
            'fields': ('action_url', 'action_text'),
            'classes': ('collapse',)
        }),
        ('Relaciones', {
            'fields': ('related_presentation', 'related_assignment', 'related_course'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'related_presentation', 'related_assignment', 'related_course')


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'receive_grade_notifications', 'receive_assignment_notifications', 
                    'email_notifications', 'digest_frequency']
    list_filter = ['receive_grade_notifications', 'receive_assignment_notifications', 
                   'email_notifications', 'digest_frequency']
    search_fields = ['user__username', 'user__email']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Notificaciones Web', {
            'fields': ('receive_grade_notifications', 'receive_assignment_notifications', 
                      'receive_course_notifications', 'receive_system_notifications')
        }),
        ('Notificaciones por Email', {
            'fields': ('email_notifications', 'digest_frequency')
        }),
    )