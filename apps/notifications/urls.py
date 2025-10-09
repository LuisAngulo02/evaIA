from django.urls import path
from . import views
from . import views_simple

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('dropdown/', views.notification_dropdown, name='dropdown'),
    path('dropdown-simple/', views_simple.notification_dropdown_simple, name='dropdown_simple'),
    path('mark-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('settings/', views.notification_settings, name='settings'),
]