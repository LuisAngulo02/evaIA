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
    
    # URLs para exportación
    path('export/grades/excel/', views.export_grades_excel, name='export_grades_excel'),
    path('export/grades/pdf/', views.export_grades_pdf, name='export_grades_pdf'),
    path('export/course/<int:course_id>/', views.export_course_grades, name='export_course_grades'),
    path('export/student/grades/', views.export_student_grades, name='export_student_grades'),
    path('no-data/', views.no_data_view, name='no_data'),
]