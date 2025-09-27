from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # URLs para estudiantes
    path('my-grades/', views.student_reports_view, name='student_reports'),
    
    # URLs para docentes
    path('teacher-reports/', views.teacher_reports_view, name='teacher_reports'),
    
    # URLs para administradores
    path('admin-reports/', views.admin_reports_view, name='admin_reports'),
]