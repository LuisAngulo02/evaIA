from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.decoradores import student_required, admin_required, teacher_required

@student_required
def student_reports_view(request):
    """Vista para que los estudiantes vean sus calificaciones y reportes"""
    context = {
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'reportes/student_reports.html', context)

@teacher_required
def teacher_reports_view(request):
    """Vista para que los docentes vean reportes de sus estudiantes"""
    from apps.presentaciones.models import Course, Assignment, Presentation
    from django.db.models import Count, Avg, Q
    from django.utils import timezone
    
    # Obtener cursos del docente
    teacher_courses = Course.objects.filter(teacher=request.user, is_active=True)
    
    # Obtener asignaciones del docente
    teacher_assignments = Assignment.objects.filter(
        course__teacher=request.user, 
        is_active=True
    )
    
    # Obtener presentaciones de los estudiantes del docente
    teacher_presentations = Presentation.objects.filter(
        assignment__course__teacher=request.user
    ).select_related('student', 'assignment', 'assignment__course')
    
    # Estadísticas generales
    stats = {
        'total_courses': teacher_courses.count(),
        'total_assignments': teacher_assignments.count(),
        'total_presentations': teacher_presentations.count(),
        'pending_grading': teacher_presentations.filter(
            Q(status='ANALYZED') | Q(status='UPLOADED')
        ).count(),
        'graded_presentations': teacher_presentations.filter(status='GRADED').count(),
        'average_score': teacher_presentations.filter(
            final_score__isnull=False
        ).aggregate(avg_score=Avg('final_score'))['avg_score'] or 0,
        'ai_average': teacher_presentations.filter(
            ai_score__isnull=False
        ).aggregate(avg_ai=Avg('ai_score'))['avg_ai'] or 0,
    }
    
    # Estadísticas por curso
    course_stats = []
    for course in teacher_courses:
        course_presentations = teacher_presentations.filter(assignment__course=course)
        course_stats.append({
            'course': course,
            'presentations_count': course_presentations.count(),
            'average_score': course_presentations.filter(
                final_score__isnull=False
            ).aggregate(avg=Avg('final_score'))['avg'] or 0,
            'pending_count': course_presentations.filter(
                Q(status='ANALYZED') | Q(status='UPLOADED')
            ).count(),
        })
    
    # Presentaciones recientes
    recent_presentations = teacher_presentations.order_by('-uploaded_at')[:10]
    
    context = {
        'user': request.user,
        'stats': stats,
        'course_stats': course_stats,
        'recent_presentations': recent_presentations,
        'teacher_courses': teacher_courses,
        'teacher_assignments': teacher_assignments,
    }
    return render(request, 'reportes/teacher_reports.html', context)

@admin_required
def admin_reports_view(request):
    """Vista para que los administradores vean reportes del sistema"""
    context = {
        'user': request.user,
    }
    return render(request, 'reportes/admin_reports.html', context)
