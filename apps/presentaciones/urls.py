from django.urls import path
from . import views

app_name = 'presentations'

urlpatterns = [
    # URLs para estudiantes
    path('upload/', views.upload_presentation_view, name='upload_presentation'),
    path('my-presentations/', views.my_presentations_view, name='my_presentations'),
    path('presentation/<int:presentation_id>/', views.presentation_detail_view, name='presentation_detail'),
    path('presentation/<int:presentation_id>/edit/', views.edit_presentation_view, name='edit_presentation'),
    path('presentation/<int:presentation_id>/delete/', views.delete_presentation_view, name='delete_presentation'),
    
    # URLs para docentes
    path('teacher-dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('courses/', views.manage_courses_view, name='manage_courses'),
    path('courses/create/', views.create_course_view, name='create_course'),
    path('courses/<int:course_id>/edit/', views.edit_course_view, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course_view, name='delete_course'),
    path('assignments/', views.manage_assignments_view, name='manage_assignments'),
    path('assignments/create/', views.create_assignment_view, name='create_assignment'),
    path('assignments/<int:assignment_id>/edit/', views.edit_assignment_view, name='edit_assignment'),
    path('assignments/<int:assignment_id>/delete/', views.delete_assignment_view, name='delete_assignment'),
    path('grade/', views.grade_presentations_view, name='grade_presentations'),
    path('grade/<int:presentation_id>/', views.grade_presentation_detail_view, name='grade_presentation_detail'),
    
    # APIs AJAX
    path('api/assignment-details/', views.get_assignment_details, name='get_assignment_details'),

    # URL para transcripciones
    path('transcription/<int:presentation_id>/', views.presentation_transcription, name='presentation_transcription'),
]