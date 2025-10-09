from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.views.decorators.http import require_http_methods
import json
import os

from authentication.models import Profile
from authentication.decoradores import student_required, teacher_required, admin_required
from .models import Presentation, Assignment, Course, AIAnalysis
from .forms import PresentationUploadForm, CourseForm, AssignmentForm

# =====================================================
# VISTAS PARA ESTUDIANTES
# =====================================================

@student_required
def upload_presentation_view(request):
    """Vista para que los estudiantes suban presentaciones"""
    if request.method == 'POST':
        form = PresentationUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.student = request.user
            
            # Calcular tamaño del archivo
            if presentation.video_file:
                presentation.file_size = presentation.video_file.size
            
            try:
                presentation.save()
                
                # Agregar placeholder para transcripción si no existe
                if not presentation.transcription_text and presentation.video_file:
                    presentation.transcription_text = ""  # Placeholder vacío para que aparezca el botón
                    presentation.save()
                
                # Aquí se integraría con OpenCV, SpeechRecognition y IA para análisis
                # process_presentation_async.delay(presentation.id)
                
                messages.success(
                    request, 
                    f'¡Presentación "{presentation.title}" subida exitosamente! '
                    f'Puedes transcribir el audio usando el botón "Transcribir Audio" en los detalles.'
                )
                return redirect('presentations:my_presentations')
                
            except Exception as e:
                messages.error(request, f'Error al guardar la presentación: {str(e)}')
                # Recargar la página con el mensaje de error
                form = PresentationUploadForm(user=request.user)
        else:
            # Mostrar errores del formulario como mensajes flotantes amigables
            error_messages = []
            
            for field, error_list in form.errors.items():
                for error in error_list:
                    if field == 'title':
                        error_messages.append(f' {error}')
                    elif field == 'video_file':
                        error_messages.append(f' {error}')
                    elif field == 'assignment':
                        error_messages.append(f' {error}')
                    elif field == 'description':
                        error_messages.append(f' {error}')
                    elif field == '__all__':
                        error_messages.append(f' {error}')
                    else:
                        field_name = field.replace('_', ' ').title()
                        error_messages.append(f' {field_name}: {error}')
            
            # Mostrar todos los errores
            for msg in error_messages:
                messages.error(request, msg)
            
            # Si no se capturaron errores específicos
            if not error_messages:
                messages.error(request, ' Por favor revisa la información ingresada y corrige los errores.')
    else:
        form = PresentationUploadForm(user=request.user)
    
    # Obtener asignaciones disponibles para el contexto
    available_assignments = Assignment.objects.filter(
        is_active=True,
        due_date__gte=timezone.now()
    ).select_related('course', 'course__teacher').order_by('due_date')
    
    context = {
        'form': form,
        'available_assignments': available_assignments,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'presentations/presentations_upload.html', context)

@student_required
def my_presentations_view(request):
    """Vista para que los estudiantes vean sus presentaciones"""
    presentations = Presentation.objects.filter(
        student=request.user
    ).select_related(
        'assignment', 
        'assignment__course', 
        'graded_by'
    ).prefetch_related(
        'ai_analysis'
    ).order_by('-uploaded_at')
    
    # Paginación
    paginator = Paginator(presentations, 10)
    page_number = request.GET.get('page')
    presentations_page = paginator.get_page(page_number)
    
    # Estadísticas del estudiante
    stats = {
        'total': presentations.count(),
        'pending': presentations.filter(status__in=['UPLOADED', 'PROCESSING']).count(),
        'analyzed': presentations.filter(status='ANALYZED').count(),
        'graded': presentations.filter(status='GRADED').count(),
        'avg_score': presentations.filter(final_score__isnull=False).aggregate(
            avg=Avg('final_score')
        )['avg'] or 0
    }
    
    context = {
        'presentations': presentations_page,
        'stats': stats,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'presentations/my_presentations.html', context)

@student_required
def presentation_detail_view(request, presentation_id):
    """Vista detallada de una presentación específica"""
    presentation = get_object_or_404(
        Presentation.objects.select_related(
            'assignment', 
            'assignment__course', 
            'graded_by'
        ).prefetch_related('ai_analysis'),
        id=presentation_id,
        student=request.user  # Solo puede ver sus propias presentaciones
    )
    
    context = {
        'presentation': presentation,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'presentations/presentation_detail.html', context)

@student_required
def delete_presentation_view(request, presentation_id):
    """Vista para eliminar una presentación (solo si no ha sido calificada)"""
    presentation = get_object_or_404(
        Presentation,
        id=presentation_id,
        student=request.user
    )
    
    # Solo se puede eliminar si no ha sido calificada
    if presentation.status == 'GRADED' or presentation.final_score is not None:
        messages.error(request, 'No puedes eliminar una presentación que ya ha sido calificada.')
        return redirect('presentations:my_presentations')
    
    if request.method == 'POST':
        title = presentation.title
        presentation.delete()  # El método delete del modelo se encarga de eliminar el archivo
        messages.success(request, f'Presentación "{title}" eliminada exitosamente.')
        return redirect('presentations:my_presentations')
    
    context = {
        'presentation': presentation,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'presentations/confirm_delete.html', context)

@student_required
def edit_presentation_view(request, presentation_id):
    """Vista para editar una presentación (solo si no ha sido calificada)"""
    presentation = get_object_or_404(
        Presentation,
        id=presentation_id,
        student=request.user
    )
    
    # Solo se puede editar si no ha sido calificada
    if presentation.status == 'GRADED' or presentation.final_score is not None:
        messages.error(request, 'No puedes editar una presentación que ya ha sido calificada.')
        return redirect('presentations:presentation_detail', presentation_id=presentation.id)
    
    if request.method == 'POST':
        form = PresentationUploadForm(request.POST, request.FILES, instance=presentation, user=request.user)
        if form.is_valid():
            # Guardar el video anterior para comparación
            old_video_file = presentation.video_file
            
            # Guardar la presentación
            updated_presentation = form.save(commit=False)
            
            # Si se subió un nuevo video, actualizar el tamaño y limpiar el anterior
            new_video_file = form.cleaned_data.get('video_file')
            if new_video_file and new_video_file != old_video_file:
                # Calcular nuevo tamaño del archivo
                updated_presentation.file_size = new_video_file.size
                updated_presentation.status = 'UPLOADED'  # Resetear estado para nuevo análisis
                
                # Eliminar archivo anterior si existe y es diferente
                if old_video_file:
                    try:
                        import os
                        if os.path.isfile(old_video_file.path):
                            os.remove(old_video_file.path)
                    except Exception as e:
                        print(f"Error eliminando archivo anterior: {e}")
            
            updated_presentation.save()
            
            messages.success(request, f'Presentación "{updated_presentation.title}" actualizada exitosamente.')
            return redirect('presentations:presentation_detail', presentation_id=updated_presentation.id)
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PresentationUploadForm(instance=presentation, user=request.user)
    
    # Obtener asignaciones disponibles para el contexto
    available_assignments = Assignment.objects.filter(
        is_active=True,
        due_date__gte=timezone.now()
    ).select_related('course', 'course__teacher').order_by('due_date')
    
    context = {
        'form': form,
        'presentation': presentation,
        'available_assignments': available_assignments,
        'user': request.user,
        'profile': request.user.profile,
        'is_editing': True,
    }
    
    return render(request, 'presentations/edit_presentation.html', context)

# =====================================================
# VISTAS PARA DOCENTES
# =====================================================

@teacher_required
def manage_courses_view(request):
    """Vista para gestionar cursos del docente"""
    courses = Course.objects.filter(
        teacher=request.user
    ).annotate(
        assignments_count=Count('assignment'),
        presentations_count=Count('assignment__presentation')
    ).order_by('-created_at')
    
    context = {
        'courses': courses,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'courses/manage_courses.html', context)

@teacher_required
def create_course_view(request):
    """Vista para crear un nuevo curso"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, f'Curso "{course.name}" creado exitosamente.')
            return redirect('presentations:manage_courses')
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'title': 'Crear Nuevo Curso',
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'courses/course_form.html', context)

@teacher_required
def manage_assignments_view(request):
    """Vista para gestionar asignaciones del docente"""
    assignments = Assignment.objects.filter(
        course__teacher=request.user
    ).select_related('course').annotate(
        presentations_count=Count('presentation')
    ).order_by('-created_at')
    
    # Filtros
    course_filter = request.GET.get('course')
    status_filter = request.GET.get('status')
    
    if course_filter:
        assignments = assignments.filter(course_id=course_filter)
    
    if status_filter == 'active':
        assignments = assignments.filter(is_active=True, due_date__gte=timezone.now())
    elif status_filter == 'expired':
        assignments = assignments.filter(due_date__lt=timezone.now())
    elif status_filter == 'inactive':
        assignments = assignments.filter(is_active=False)
    
    # Paginación
    paginator = Paginator(assignments, 15)
    page_number = request.GET.get('page')
    assignments_page = paginator.get_page(page_number)
    
    # Cursos para el filtro
    courses = Course.objects.filter(teacher=request.user, is_active=True)
    
    context = {
        'assignments': assignments_page,
        'courses': courses,
        'current_course_filter': course_filter,
        'current_status_filter': status_filter,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'assignments/manage_assignments.html', context)

@teacher_required
def create_assignment_view(request):
    """Vista para crear una nueva asignación"""
    if request.method == 'POST':
        form = AssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            assignment = form.save()
            messages.success(request, f'Asignación "{assignment.title}" creada exitosamente.')
            return redirect('presentations:manage_assignments')
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = AssignmentForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Crear Nueva Asignación',
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'assignments/assignment_form.html', context)

@teacher_required
def grade_presentations_view(request):
    """Vista para calificar presentaciones"""
    presentations = Presentation.objects.filter(
        assignment__course__teacher=request.user,
        status__in=['UPLOADED', 'PROCESSING', 'ANALYZED', 'GRADED']
    ).select_related(
        'student', 
        'assignment', 
        'assignment__course'
    ).prefetch_related('ai_analysis').order_by('-uploaded_at')
    
    # Filtros
    course_filter = request.GET.get('course')
    assignment_filter = request.GET.get('assignment')
    
    if course_filter:
        presentations = presentations.filter(assignment__course_id=course_filter)
    
    if assignment_filter:
        presentations = presentations.filter(assignment_id=assignment_filter)
    
    # Paginación
    paginator = Paginator(presentations, 10)
    page_number = request.GET.get('page')
    presentations_page = paginator.get_page(page_number)
    
    # Datos para filtros
    courses = Course.objects.filter(teacher=request.user, is_active=True)
    assignments = Assignment.objects.filter(course__teacher=request.user, is_active=True)
    
    context = {
        'presentations': presentations_page,
        'courses': courses,
        'assignments': assignments,
        'current_course_filter': course_filter,
        'current_assignment_filter': assignment_filter,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'presentations/grade_presentations.html', context)

@teacher_required
def grade_presentation_detail_view(request, presentation_id):
    """Vista para calificar una presentación específica"""
    presentation = get_object_or_404(
        Presentation.objects.select_related(
            'student', 'assignment', 'assignment__course', 'graded_by'
        ).prefetch_related('ai_analysis'),
        id=presentation_id,
        assignment__course__teacher=request.user
    )
    
    if request.method == 'POST':
        final_score = request.POST.get('final_score')
        teacher_feedback = request.POST.get('teacher_feedback')
        
        try:
            final_score = float(final_score)
            if final_score < 0 or final_score > presentation.assignment.max_score:
                messages.error(request, f'La puntuación debe estar entre 0 y {presentation.assignment.max_score}')
            else:
                presentation.final_score = final_score
                presentation.teacher_feedback = teacher_feedback
                presentation.status = 'GRADED'
                presentation.graded_by = request.user
                presentation.graded_at = timezone.now()
                presentation.save()
                
                messages.success(request, f'Presentación "{presentation.title}" calificada exitosamente.')
                return redirect('presentations:grade_presentations')
        except ValueError:
            messages.error(request, 'Puntuación inválida')
    
    context = {
        'presentation': presentation,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'presentations/grade_presentation_detail.html', context)

@teacher_required
def edit_course_view(request, course_id):
    """Vista para editar un curso"""
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Curso "{course.name}" actualizado exitosamente.')
            return redirect('presentations:manage_courses')
    else:
        form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'course': course,
        'title': f'Editar Curso - {course.name}',
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'courses/course_form.html', context)

@teacher_required
def delete_course_view(request, course_id):
    """Vista para eliminar un curso"""
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    
    if request.method == 'POST':
        course_name = course.name
        course.is_active = False  # Soft delete
        course.save()
        messages.success(request, f'Curso "{course_name}" eliminado exitosamente.')
        return redirect('presentations:manage_courses')
    
    context = {
        'course': course,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'courses/confirm_delete_course.html', context)

@teacher_required
def edit_assignment_view(request, assignment_id):
    """Vista para editar una asignación"""
    assignment = get_object_or_404(
        Assignment.objects.select_related('course'),
        id=assignment_id,
        course__teacher=request.user
    )
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Asignación "{assignment.title}" actualizada exitosamente.')
            return redirect('presentations:manage_assignments')
    else:
        form = AssignmentForm(instance=assignment, user=request.user)
    
    context = {
        'form': form,
        'assignment': assignment,
        'title': f'Editar Asignación - {assignment.title}',
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'assignments/assignment_form.html', context)

@teacher_required
def delete_assignment_view(request, assignment_id):
    """Vista para eliminar una asignación"""
    assignment = get_object_or_404(
        Assignment.objects.select_related('course'),
        id=assignment_id,
        course__teacher=request.user
    )
    
    if request.method == 'POST':
        assignment_title = assignment.title
        assignment.is_active = False  # Soft delete
        assignment.save()
        messages.success(request, f'Asignación "{assignment_title}" eliminada exitosamente.')
        return redirect('presentations:manage_assignments')
    
    context = {
        'assignment': assignment,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'assignments/confirm_delete_assignment.html', context)

@teacher_required
def teacher_dashboard_view(request):
    """Dashboard principal para docentes con estadísticas"""
    from django.db.models import Avg
    
    # Obtener cursos del docente
    courses = Course.objects.filter(teacher=request.user, is_active=True)
    
    # Estadísticas básicas
    stats = {
        'total_courses': courses.count(),
        'total_assignments': Assignment.objects.filter(course__teacher=request.user, is_active=True).count(),
        'pending_grading': Presentation.objects.filter(
            assignment__course__teacher=request.user,
            status='ANALYZED'
        ).count(),
        'total_presentations': Presentation.objects.filter(
            assignment__course__teacher=request.user
        ).count(),
        'graded_presentations': Presentation.objects.filter(
            assignment__course__teacher=request.user,
            status='GRADED'
        ).count()
    }
    
    # Presentaciones recientes por calificar
    pending_presentations = Presentation.objects.filter(
        assignment__course__teacher=request.user,
        status='ANALYZED'
    ).select_related('student', 'assignment', 'assignment__course').order_by('-uploaded_at')[:5]
    
    # Cursos recientes
    recent_courses = courses.order_by('-created_at')[:4]
    
    # Cálculos de rendimiento
    if stats['total_presentations'] > 0:
        stats['completion_rate'] = (stats['graded_presentations'] / stats['total_presentations']) * 100
        
        # Promedio de calificaciones
        avg_score = Presentation.objects.filter(
            assignment__course__teacher=request.user,
            status='GRADED',
            final_score__isnull=False
        ).aggregate(Avg('final_score'))['final_score__avg']
        stats['average_score'] = avg_score if avg_score else 0
        
        # Promedio IA
        avg_ai_score = Presentation.objects.filter(
            assignment__course__teacher=request.user,
            ai_score__isnull=False
        ).aggregate(Avg('ai_score'))['ai_score__avg']
        stats['ai_average'] = avg_ai_score if avg_ai_score else 0
    else:
        stats['completion_rate'] = 0
        stats['average_score'] = 0
        stats['ai_average'] = 0
    
    context = {
        'stats': stats,
        'pending_presentations': pending_presentations,
        'recent_courses': recent_courses,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'dashboard/docentes.html', context)

# =====================================================
# VISTAS DE ADMINISTRADOR
# =====================================================

@admin_required
def admin_presentations_view(request):
    """Vista de administración de todas las presentaciones"""
    presentations = Presentation.objects.all().select_related(
        'student', 
        'assignment', 
        'assignment__course', 
        'graded_by'
    ).order_by('-uploaded_at')
    
    # Filtros
    status_filter = request.GET.get('status')
    course_filter = request.GET.get('course')
    search = request.GET.get('search')
    
    if status_filter:
        presentations = presentations.filter(status=status_filter)
    
    if course_filter:
        presentations = presentations.filter(assignment__course_id=course_filter)
    
    if search:
        presentations = presentations.filter(
            Q(title__icontains=search) |
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(student__username__icontains=search) |
            Q(assignment__title__icontains=search)
        )
    
    # Paginación
    paginator = Paginator(presentations, 20)
    page_number = request.GET.get('page')
    presentations_page = paginator.get_page(page_number)
    
    # Datos para filtros
    courses = Course.objects.filter(is_active=True)
    status_choices = Presentation.STATUS_CHOICES
    
    # Estadísticas generales
    stats = {
        'total': Presentation.objects.count(),
        'uploaded': Presentation.objects.filter(status='UPLOADED').count(),
        'processing': Presentation.objects.filter(status='PROCESSING').count(),
        'analyzed': Presentation.objects.filter(status='ANALYZED').count(),
        'graded': Presentation.objects.filter(status='GRADED').count(),
        'failed': Presentation.objects.filter(status='FAILED').count(),
    }
    
    context = {
        'presentations': presentations_page,
        'courses': courses,
        'status_choices': status_choices,
        'current_status_filter': status_filter,
        'current_course_filter': course_filter,
        'current_search': search,
        'stats': stats,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'admin/presentations_admin.html', context)

# =====================================================
# VISTAS AJAX Y API
# =====================================================

@require_http_methods(["GET"])
def get_assignment_details(request):
    """API para obtener detalles de una asignación (AJAX)"""
    assignment_id = request.GET.get('assignment_id')
    
    if not assignment_id:
        return JsonResponse({'error': 'No assignment ID provided'}, status=400)
    
    try:
        assignment = Assignment.objects.select_related(
            'course', 'course__teacher'
        ).get(id=assignment_id, is_active=True)
        
        data = {
            'id': assignment.id,
            'title': assignment.title,
            'description': assignment.description,
            'course': f"{assignment.course.code} - {assignment.course.name}",
            'teacher': assignment.course.teacher.get_full_name() or assignment.course.teacher.username,
            'type': assignment.get_assignment_type_display(),
            'max_duration': assignment.max_duration,
            'due_date': assignment.due_date.strftime('%Y-%m-%d %H:%M'),
            'max_score': float(assignment.max_score),
            'instructions': assignment.instructions,
            'is_expired': assignment.is_expired,
            'days_remaining': assignment.days_remaining
        }
        
        return JsonResponse(data)
        
    except Assignment.DoesNotExist:
        return JsonResponse({'error': 'Assignment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def presentation_transcription(request, presentation_id):
    """
    Muestra la transcripción de una presentación y permite transcripción real
    """
    presentation = get_object_or_404(Presentation, id=presentation_id)
    
    # Verificar permisos
    if request.user != presentation.student and request.user != presentation.assignment.course.instructor:
        messages.error(request, "No tienes permiso para ver esta transcripción.")
        return redirect('presentations:my_presentations')
    
    # Procesar transcripción real si se solicita
    if request.method == 'POST' and 'transcribe_real' in request.POST:
        try:
            # Importar librerías necesarias
            import whisper
            import numpy as np
            import tempfile
            import os
            
            messages.info(request, "Iniciando transcripción real del audio...")
            
            # Cargar modelo Whisper
            model = whisper.load_model("base")
            
            # Configurar FFmpeg para que Whisper lo encuentre
            try:
                import imageio_ffmpeg as ffmpeg
                import shutil
                from pathlib import Path
                
                ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
                
                # Crear directorio local para FFmpeg si no existe
                local_bin = Path("local_bin")
                local_bin.mkdir(exist_ok=True)
                
                # Copiar FFmpeg al directorio local
                local_ffmpeg = local_bin / "ffmpeg.exe"
                if not local_ffmpeg.exists():
                    shutil.copy2(ffmpeg_exe, local_ffmpeg)
                
                # Agregar al PATH
                local_bin_abs = str(local_bin.absolute())
                current_path = os.environ.get('PATH', '')
                if local_bin_abs not in current_path:
                    os.environ['PATH'] = f"{local_bin_abs};{current_path}"
                
                messages.info(request, "FFmpeg configurado correctamente para Whisper")
            except Exception as e:
                messages.warning(request, f"Advertencia configurando FFmpeg: {str(e)}")
            
            # Verificar si el video tiene audio primero
            try:
                from moviepy.editor import VideoFileClip
                video = VideoFileClip(presentation.video_file.path)
                
                if video.audio is None:
                    video.close()
                    messages.error(request, "❌ Este video no contiene audio para transcribir. Sube un video que incluya audio/voz.")
                    return redirect(request.path)
                else:
                    video.close()
                    messages.info(request, "✅ Video con audio detectado, procediendo con la transcripción...")
            except:
                # Si no puede verificar, continuar
                pass
            
            # Método 1: Intentar con Whisper directamente
            try:
                # Whisper puede manejar MP4 directamente
                result = model.transcribe(
                    presentation.video_file.path,
                    language='es',
                    task='transcribe',
                    verbose=False
                )
                
                if result and result.get('text') and len(result['text'].strip()) > 5:
                    # Guardar transcripción real
                    presentation.transcription_text = result['text'].strip()
                    
                    # Procesar segmentos
                    segments = []
                    if 'segments' in result:
                        for segment in result['segments']:
                            if segment['text'].strip():
                                segments.append({
                                    'start_time': round(segment['start'], 2),
                                    'end_time': round(segment['end'], 2),
                                    'text': segment['text'].strip()
                                })
                    
                    presentation.transcription_segments = segments
                    
                    # Calcular duración
                    if segments:
                        presentation.audio_duration = max(seg['end_time'] for seg in segments)
                    
                    presentation.save()
                    
                    messages.success(request, f"¡Transcripción real completada! Se transcribieron {len(result['text'])} caracteres de audio real.")
                    
                else:
                    messages.warning(request, "No se detectó texto en el audio del video.")
                    
            except Exception as whisper_error:
                # Método 2: Usar MoviePy como fallback
                try:
                    from moviepy.editor import VideoFileClip
                    
                    video = VideoFileClip(presentation.video_file.path)
                    
                    if video.audio is not None:
                        # Crear archivo temporal
                        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                        temp_audio_path = temp_audio.name
                        temp_audio.close()
                        
                        try:
                            # Extraer audio con configuración más robusta
                            audio = video.audio
                            
                            # Configurar FFmpeg con imageio
                            import imageio_ffmpeg as ffmpeg
                            ffmpeg_path = ffmpeg.get_ffmpeg_exe()
                            
                            # Usar el ejecutable de FFmpeg de imageio
                            import subprocess
                            cmd = [
                                ffmpeg_path,
                                '-i', presentation.video_file.path,
                                '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                                '-y', temp_audio_path
                            ]
                            
                            subprocess.run(cmd, check=True, capture_output=True)
                            
                            # Transcribir con Whisper
                            result = model.transcribe(
                                temp_audio_path,
                                language='es',
                                task='transcribe'
                            )
                            
                            if result and result.get('text') and len(result['text'].strip()) > 5:
                                # Guardar transcripción real
                                presentation.transcription_text = result['text'].strip()
                                
                                # Procesar segmentos
                                segments = []
                                if 'segments' in result:
                                    for segment in result['segments']:
                                        if segment['text'].strip():
                                            segments.append({
                                                'start_time': round(segment['start'], 2),
                                                'end_time': round(segment['end'], 2),
                                                'text': segment['text'].strip()
                                            })
                                
                                presentation.transcription_segments = segments
                                
                                # Calcular duración
                                if segments:
                                    presentation.audio_duration = max(seg['end_time'] for seg in segments)
                                
                                presentation.save()
                                
                                messages.success(request, "¡Transcripción real completada con método alternativo!")
                            else:
                                messages.warning(request, "No se detectó texto en el audio extraído.")
                                
                        finally:
                            # Limpiar recursos
                            if 'audio' in locals():
                                audio.close()
                            if 'video' in locals():
                                video.close()
                            if os.path.exists(temp_audio_path):
                                os.unlink(temp_audio_path)
                    else:
                        messages.error(request, "El video no contiene pista de audio.")
                        
                except Exception as moviepy_error:
                    messages.error(request, f"Error con ambos métodos. Whisper: {str(whisper_error)[:100]}, MoviePy: {str(moviepy_error)[:100]}")
                
        except ImportError as e:
            messages.error(request, f"Librerías no disponibles: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error general: {str(e)}")
    
    # Preparar contexto
    context = {
        'presentation': presentation,
        'has_transcription': bool(presentation.transcription_text),
        'formatted_transcription': None
    }
    
    # Formatear transcripción si existe
    if presentation.transcription_segments:
        try:
            from apps.ai_processor.services.transcription_service import TranscriptionService
            service = TranscriptionService()
            context['formatted_transcription'] = service.format_transcription_for_display(
                presentation.transcription_segments
            )
        except ImportError:
            # Fallback cuando MoviePy no está disponible
            formatted_text = ""
            for segment in presentation.transcription_segments:
                start_min = int(segment['start_time'] // 60)
                start_sec = int(segment['start_time'] % 60)
                formatted_text += f"[{start_min:02d}:{start_sec:02d}] {segment['text']}\n"
            context['formatted_transcription'] = formatted_text
    
    return render(request, 'presentations/transcription_detail.html', context)