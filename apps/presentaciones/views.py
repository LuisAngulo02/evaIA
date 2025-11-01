from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import json
import os
import logging

from authentication.models import Profile
from authentication.decoradores import student_required, teacher_required, admin_required, group_required
from .models import Presentation, Assignment, Course, AIAnalysis, AIConfiguration
from .forms import PresentationUploadForm, CourseForm, AssignmentForm
from .validators import VideoValidator

# Configurar logger
logger = logging.getLogger(__name__)


# VISTAS PARA ESTUDIANTES


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
                
                # Ejecutar validaciones avanzadas después de guardar (necesitamos la ruta del archivo)
                try:
                    validator = VideoValidator()
                    validation_result = validator.validate_all(presentation.video_file.path)
                    
                    # Guardar metadatos del video
                    if validation_result['properties_valid']:
                        props = validation_result['video_properties']
                        presentation.duration_seconds = props.get('duration')
                        presentation.video_fps = props.get('fps')
                        presentation.video_width = props.get('width')
                        presentation.video_height = props.get('height')
                    
                    # Guardar miniatura si se generó
                    if validation_result['thumbnail_generated']:
                        from django.core.files import File
                        thumb_path = validation_result['thumbnail_path']
                        with open(thumb_path, 'rb') as f:
                            presentation.video_thumbnail.save(
                                os.path.basename(thumb_path),
                                File(f),
                                save=False
                            )
                    
                    presentation.save()
                    
                except Exception as val_error:
                    # Si falla la validación avanzada, no bloqueamos pero registramos
                    print(f"Validación avanzada falló (no crítico): {str(val_error)}")
                
                # Subir a Cloudinary automáticamente
                try:
                    from apps.ai_processor.services import CloudinaryService
                    if CloudinaryService.is_configured():
                        cloudinary_result = presentation.upload_to_cloudinary()
                        if cloudinary_result:
                            messages.info(request, '☁️ Video subido a Cloudinary exitosamente')
                        else:
                            messages.warning(request, '⚠️ No se pudo subir a Cloudinary, usando almacenamiento local')
                except Exception as cloud_error:
                    print(f"Error subiendo a Cloudinary (no crítico): {str(cloud_error)}")
                    messages.warning(request, '⚠️ No se pudo subir a Cloudinary, usando almacenamiento local')
                
                # Iniciar análisis asíncrono en segundo plano
                from .tasks import process_presentation_async
                process_presentation_async(presentation.id)
                
                messages.success(
                    request, 
                    f'✅ Presentación "{presentation.title}" subida exitosamente! '
                    f'El análisis de IA se está procesando en segundo plano.'
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
        # Verificar si viene el parámetro de asignación (cuando se elimina una presentación)
        assignment_id = request.GET.get('assignment')
        
        if assignment_id:
            # Pre-seleccionar la asignación en el formulario
            form = PresentationUploadForm(
                user=request.user,
                initial={'assignment': assignment_id}
            )
        else:
            form = PresentationUploadForm(user=request.user)
    
    # Obtener IDs de asignaciones donde el estudiante ya subió presentación
    asignaciones_con_presentacion = Presentation.objects.filter(
        student=request.user
    ).values_list('assignment_id', flat=True)
    
    # Filtrar asignaciones disponibles (activas, no vencidas y SIN presentación previa)
    available_assignments = Assignment.objects.filter(
        is_active=True,
        due_date__gte=timezone.now()
    ).exclude(
        id__in=asignaciones_con_presentacion
    ).select_related('course', 'course__teacher').order_by('due_date')
    
    # Agregar parámetros al contexto para el template
    context = {
        'form': form,
        'available_assignments': available_assignments,
        'user': request.user,
        'profile': request.user.profile,
        'preselected_assignment_id': request.GET.get('assignment'),
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

@login_required
def presentation_detail_view(request, presentation_id):
    """Vista detallada de una presentación específica con análisis individual"""
    # Verificar si el usuario es estudiante o profesor
    is_student = request.user.groups.filter(name='Estudiante').exists()
    is_teacher = request.user.groups.filter(name='Docente').exists() or request.user.is_superuser
    
    if not (is_student or is_teacher):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('auth:dashboard')
    
    # Construir el filtro según el tipo de usuario
    if is_student:
        # Los estudiantes solo pueden ver sus propias presentaciones
        presentation = get_object_or_404(
            Presentation.objects.select_related(
                'assignment', 
                'assignment__course', 
                'graded_by'
            ).prefetch_related('ai_analysis', 'participants'),
            id=presentation_id,
            student=request.user
        )
    else:
        # Los profesores pueden ver presentaciones de sus cursos
        presentation = get_object_or_404(
            Presentation.objects.select_related(
                'assignment', 
                'assignment__course', 
                'graded_by'
            ).prefetch_related('ai_analysis', 'participants'),
            id=presentation_id,
            assignment__course__teacher=request.user
        )
    
    # Obtener participantes
    participants_queryset = presentation.participants.all()
    
    # Ordenar por número de persona (Persona 1, Persona 2, etc.) para mostrar en orden de aparición
    participants = sorted(participants_queryset, key=lambda p: int(p.label.split()[-1]) if p.label.split()[-1].isdigit() else 0)
    
    # Calcular estadísticas grupales
    max_score = float(presentation.assignment.max_score) if presentation.assignment else 20.0
    average_coherence = 0
    topic_coverage = 0
    time_distribution_quality = "No disponible"
    group_feedback = None
    overall_ai_score = 0
    
    if participants_queryset.exists():
        # Coherencia promedio
        avg_coherence = participants_queryset.aggregate(avg=Avg('ai_grade'))['avg']
        if avg_coherence:
            average_coherence = (avg_coherence / max_score) * 100
            overall_ai_score = round(avg_coherence, 1)
        
        # Cobertura del tema (basada en coherencia promedio)
        topic_coverage = average_coherence
        
        # Calidad de distribución del tiempo (MENOS ESTRICTO)
        time_percentages = [p.time_percentage for p in participants if hasattr(p, 'time_percentage') and p.time_percentage]
        if time_percentages:
            max_diff = max(time_percentages) - min(time_percentages)
            # Umbrales más tolerantes
            if max_diff < 25:  # Antes era 15
                time_distribution_quality = "Equilibrada"
            elif max_diff < 40:  # Antes era 30
                time_distribution_quality = "Aceptable"
            else:
                time_distribution_quality = "Variable"  # Antes era "Desigual"
        
        # Generar conclusión grupal con IA de GROQ
        try:
            from apps.ai_processor.services.coherence_analyzer import CoherenceAnalyzer
            
            # Preparar datos de participantes
            resultados_participantes = []
            for p in participants:
                resultados_participantes.append({
                    'etiqueta': p.label,
                    'nota_coherencia': p.coherence_score or 0,
                    'calificacion_final': p.ai_grade or 0,
                    'porcentaje_tiempo': p.time_percentage or 0,
                    'tiempo_participacion': p.participation_time or 0
                })
            
            # Obtener tema y descripción
            tema = presentation.assignment.title if presentation.assignment else "Presentación"
            descripcion_tema = presentation.assignment.description if presentation.assignment else ""
            
            # Generar conclusión con IA
            analyzer = CoherenceAnalyzer()
            max_score = float(presentation.assignment.max_score) if presentation.assignment else 20.0
            group_feedback = analyzer.generar_conclusion_grupal(
                resultados_participantes, 
                tema, 
                descripcion_tema,
                max_score=max_score
            )
            
        except Exception as e:
            logger.error(f"Error al generar conclusión grupal en detail: {str(e)}")
            # Fallback básico
            group_feedback = None
    
    # Preparar datos de segmentos de tiempo para JavaScript
    import json
    from decimal import Decimal
    
    participants_segments = []
    current_time = 0
    
    # Si solo hay un participante, usar la duración completa del video
    single_participant = len(participants) == 1
    
    # Intentar obtener duración del video de varias fuentes
    video_duration = None
    if presentation.duration_seconds:
        video_duration = presentation.duration_seconds
    elif single_participant and participants[0].participation_time:
        # Si solo hay un participante, usar su participation_time como duración total
        video_duration = float(participants[0].participation_time)
    
    for p in participants:
        # Si tiene segmentos guardados, usarlos
        if p.time_segments and len(p.time_segments) > 0:
            segments = p.time_segments
        else:
            # Crear un segmento ficticio basado en participation_time
            # Esto es temporal hasta que el procesamiento guarde los segmentos reales
            if p.participation_time and p.participation_time > 0:
                # Convertir Decimal a float para evitar problemas de JSON
                participation_time_float = float(p.participation_time) if isinstance(p.participation_time, Decimal) else p.participation_time
                
                # Si es el único participante, el segmento debe cubrir todo el timeline
                if single_participant:
                    # Usar la duración del video o el participation_time (lo que sea mayor)
                    end_time = max(video_duration, participation_time_float) if video_duration else participation_time_float
                    segments = [{
                        'start': 0.0,
                        'end': float(end_time)
                    }]
                else:
                    # Múltiples participantes: distribuir secuencialmente
                    segments = [{
                        'start': float(current_time),
                        'end': float(current_time + participation_time_float)
                    }]
                    current_time += participation_time_float + 2  # +2 segundos de espacio
            else:
                segments = []
        
        participants_segments.append({
            'label': p.label,
            'segments': segments,
            'color': None  # Se asignará en JavaScript
        })
    
    participants_segments_json = json.dumps(participants_segments, ensure_ascii=False)
    
    context = {
        'presentation': presentation,
        'participants': participants,
        'has_individual_analysis': participants_queryset.exists(),
        'max_score': max_score,
        'overall_ai_score': overall_ai_score,
        'average_coherence': average_coherence,
        'topic_coverage': topic_coverage,
        'time_distribution_quality': time_distribution_quality,
        'group_feedback': group_feedback,
        'user': request.user,
        'profile': request.user.profile,
        'is_teacher': is_teacher,
        'is_student': is_student,
        'participants_segments_json': participants_segments_json,  # Datos para timeline del video
    }
    
    # Si es profesor, usar el template de calificación en modo solo lectura
    if is_teacher:
        context.update({
            'is_review_mode': True,  # Modo solo lectura
            'suggested_grade': 0,
            'suggested_feedback': '',
        })
        return render(request, 'presentations/grade_presentation_detail.html', context)
    else:
        # Si es estudiante, usar el template normal
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
@require_http_methods(["POST"])
def delete_presentation_video_view(request, presentation_id):
    """Vista para eliminar toda la presentación y redirigir a subir nueva (AJAX)"""
    try:
        presentation = get_object_or_404(
            Presentation,
            id=presentation_id,
            student=request.user
        )
        
        # Solo se puede eliminar si no ha sido calificada
        if presentation.status == 'GRADED' or presentation.final_score is not None:
            return JsonResponse({
                'success': False,
                'message': 'No puedes eliminar una presentación que ya ha sido calificada.'
            })
        
        # Guardar el ID de la asignación antes de eliminar
        assignment_id = presentation.assignment.id
        
        # Eliminar toda la presentación (el método delete del modelo se encarga de los archivos)
        presentation.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Presentación eliminada exitosamente.',
            'redirect_url': f'/presentations/upload/?assignment={assignment_id}'
        })
        
    except Exception as e:
        logger.error(f"Error en delete_presentation_video_view: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error al eliminar la presentación: {str(e)}'
        })

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
    """Vista para calificar una presentación específica con análisis individual"""
    presentation = get_object_or_404(
        Presentation.objects.select_related(
            'student', 'assignment', 'assignment__course', 'graded_by'
        ).prefetch_related('ai_analysis', 'participants'),  # Agregar participants
        id=presentation_id,
        assignment__course__teacher=request.user
    )
    
    # Obtener participantes
    participants_queryset = presentation.participants.all()
    
    # Ordenar por número de persona (Persona 1, Persona 2, etc.) para mostrar en orden de aparición
    participants_list = sorted(participants_queryset, key=lambda p: int(p.label.split()[-1]) if p.label.split()[-1].isdigit() else 0)
    
    # Calcular calificación grupal sugerida por IA
    suggested_grade = 0
    suggested_feedback = ""
    
    if participants_queryset.exists():
        # Calificación sugerida = promedio de las calificaciones individuales
        avg_grade = participants_queryset.aggregate(avg=Avg('ai_grade'))['avg']
        if avg_grade:
            suggested_grade = round(avg_grade, 1)
        
        # Generar conclusión grupal dinámica con IA de GROQ
        try:
            from apps.ai_processor.services.coherence_analyzer import CoherenceAnalyzer
            
            # Preparar datos de participantes para el análisis
            resultados_participantes = []
            for p in participants_list:  # Usar la lista ordenada
                resultados_participantes.append({
                    'etiqueta': p.label,
                    'nota_coherencia': p.coherence_score or 0,
                    'calificacion_final': p.ai_grade or 0,
                    'porcentaje_tiempo': p.time_percentage or 0,
                    'tiempo_participacion': p.participation_time or 0
                })
            
            # Obtener tema y descripción
            tema = presentation.assignment.title if presentation.assignment else "Presentación"
            descripcion_tema = presentation.assignment.description if presentation.assignment else ""
            max_score = float(presentation.assignment.max_score) if presentation.assignment else 20.0
            
            # Generar conclusión con IA
            analyzer = CoherenceAnalyzer()
            suggested_feedback = analyzer.generar_conclusion_grupal(
                resultados_participantes, 
                tema, 
                descripcion_tema,
                max_score=max_score
            )
            
        except Exception as e:
            logger.error(f"Error al generar conclusión grupal: {str(e)}")
            # Fallback a mensaje básico
            avg_coherence = sum([p.coherence_score for p in participants_list]) / len(participants_list)
            suggested_feedback = f"La presentación demuestra un nivel adecuado de comprensión del tema con {avg_coherence:.1f}% de coherencia promedio."
    
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
    
    # Esta vista siempre es editable (para Calificar/Revisar)
    is_review_mode = False  # Modo editable
    is_already_graded = presentation.status == 'GRADED'
    
    # Preparar datos de segmentos de tiempo para JavaScript (timeline)
    import json
    from decimal import Decimal
    
    participants_segments = []
    current_time = 0
    
    # Si solo hay un participante, usar la duración completa del video
    single_participant = len(participants_list) == 1
    
    # Intentar obtener duración del video de varias fuentes
    video_duration = None
    if presentation.duration_seconds:
        video_duration = presentation.duration_seconds
    elif single_participant and participants_list[0].participation_time:
        # Si solo hay un participante, usar su participation_time como duración total
        video_duration = float(participants_list[0].participation_time)
    
    for p in participants_list:
        # Si tiene segmentos guardados, usarlos
        if p.time_segments and len(p.time_segments) > 0:
            segments = p.time_segments
        else:
            # Crear un segmento ficticio basado en participation_time
            if p.participation_time and p.participation_time > 0:
                # Convertir Decimal a float para evitar problemas de JSON
                participation_time_float = float(p.participation_time) if isinstance(p.participation_time, Decimal) else p.participation_time
                
                # Si es el único participante, el segmento debe cubrir todo el timeline
                if single_participant:
                    # Usar la duración del video o el participation_time (lo que sea mayor)
                    end_time = max(video_duration, participation_time_float) if video_duration else participation_time_float
                    segments = [{
                        'start': 0.0,
                        'end': float(end_time)
                    }]
                else:
                    # Múltiples participantes: distribuir secuencialmente
                    segments = [{
                        'start': float(current_time),
                        'end': float(current_time + participation_time_float)
                    }]
                    current_time += participation_time_float + 2  # +2 segundos de espacio
            else:
                segments = []
        
        participants_segments.append({
            'label': p.label,
            'segments': segments,
            'color': None  # Se asignará en JavaScript
        })
    
    participants_segments_json = json.dumps(participants_segments, ensure_ascii=False)
    
    context = {
        'presentation': presentation,
        'participants': participants_list,  # Usar lista ordenada
        'has_individual_analysis': participants_queryset.exists(),
        'suggested_grade': suggested_grade,
        'suggested_feedback': suggested_feedback,
        'is_review_mode': is_review_mode,  # Siempre False (editable)
        'is_already_graded': is_already_graded,
        'participants_segments_json': participants_segments_json,  # Datos para timeline
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
def manage_course_students_view(request, course_id):
    """Vista para gestionar estudiantes de un curso"""
    from django.contrib.auth.models import User
    from django.db.models import Q, Count
    from django.http import JsonResponse
    
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    
    # API para búsqueda AJAX de estudiantes disponibles
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        search_query = request.GET.get('search', '')
        
        # Obtener estudiantes disponibles (no matriculados)
        available_students = User.objects.filter(
            groups__name='Estudiante'
        ).exclude(
            id__in=course.students.values_list('id', flat=True)
        )
        
        # Aplicar búsqueda
        if search_query:
            available_students = available_students.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        available_students = available_students.order_by('last_name', 'first_name')[:50]  # Limitar a 50
        
        # Serializar datos
        students_data = [{
            'id': student.id,
            'username': student.username,
            'full_name': student.get_full_name() or student.username,
            'email': student.email,
        } for student in available_students]
        
        return JsonResponse({'students': students_data})
    
    # Manejar acciones POST
    if request.method == 'POST':
        action = request.POST.get('action')
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if action == 'add_student':
            student_id = request.POST.get('student_id')
            try:
                student = User.objects.get(id=student_id, groups__name='Estudiante')
                if course.students.filter(id=student_id).exists():
                    message = f'{student.get_full_name()} ya está matriculado en este curso.'
                    if is_ajax:
                        return JsonResponse({'success': False, 'message': message})
                    messages.warning(request, message)
                else:
                    course.students.add(student)
                    message = f'{student.get_full_name()} ha sido matriculado exitosamente.'
                    if is_ajax:
                        return JsonResponse({'success': True, 'message': message})
                    messages.success(request, message)
            except User.DoesNotExist:
                message = 'Estudiante no encontrado.'
                if is_ajax:
                    return JsonResponse({'success': False, 'message': message})
                messages.error(request, message)
        
        elif action == 'remove_student':
            student_id = request.POST.get('student_id')
            try:
                student = User.objects.get(id=student_id)
                course.students.remove(student)
                message = f'{student.get_full_name()} ha sido desmatriculado del curso.'
                if is_ajax:
                    return JsonResponse({'success': True, 'message': message})
                messages.success(request, message)
            except User.DoesNotExist:
                message = 'Estudiante no encontrado.'
                if is_ajax:
                    return JsonResponse({'success': False, 'message': message})
                messages.error(request, message)
        
        if not is_ajax:
            return redirect('presentations:manage_course_students', course_id=course_id)
        return JsonResponse({'success': False, 'message': 'Acción no válida'})
    
    # Obtener estudiantes matriculados con estadísticas
    enrolled_students = course.students.all().annotate(
        presentations_count=Count(
            'presentations',
            filter=Q(presentations__assignment__course=course)
        )
    ).order_by('last_name', 'first_name')
    
    # Obtener estudiantes disponibles para matricular (no están en el curso)
    available_students = User.objects.filter(
        groups__name='Estudiante'
    ).exclude(
        id__in=course.students.values_list('id', flat=True)
    ).order_by('last_name', 'first_name')
    
    # Búsqueda de estudiantes disponibles
    search_query = request.GET.get('search', '')
    if search_query:
        available_students = available_students.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    context = {
        'course': course,
        'enrolled_students': enrolled_students,
        'available_students': available_students,
        'search_query': search_query,
        'user': request.user,
        'profile': request.user.profile,
    }
    
    return render(request, 'courses/manage_students.html', context)

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
    """
    Vista para desactivar o eliminar permanentemente una asignación.
    - Si está activa y action='deactivate': la desactiva (soft delete)
    - Si está inactiva y action='delete': la elimina permanentemente
    """
    assignment = get_object_or_404(
        Assignment.objects.select_related('course'),
        id=assignment_id,
        course__teacher=request.user
    )
    
    if request.method == 'POST':
        action = request.POST.get('action', 'deactivate')
        assignment_title = assignment.title
        
        if action == 'deactivate' and assignment.is_active:
            # Desactivar la asignación (soft delete)
            assignment.is_active = False
            assignment.save()
            messages.success(
                request, 
                f'La asignación "{assignment_title}" ha sido desactivada exitosamente. '
                f'Los estudiantes ya no podrán subir nuevas presentaciones.'
            )
            
        elif action == 'delete' and not assignment.is_active:
            # Eliminar permanentemente
            from cloudinary import uploader
            from apps.notifications.models import Notification
            import os
            
            try:
                # 1. PRIMERO: Eliminar TODAS las notificaciones relacionadas
                # (tanto de la asignación como de las presentaciones)
                Notification.objects.filter(related_assignment=assignment).delete()
                
                # 2. Obtener presentaciones
                presentations = assignment.presentation_set.all()
                presentation_count = presentations.count()
                
                # 3. Eliminar notificaciones de cada presentación
                for presentation in presentations:
                    Notification.objects.filter(related_presentation=presentation).delete()
                
                # 4. Eliminar presentaciones y sus archivos
                for presentation in presentations:
                    # Eliminar archivo de video local
                    if presentation.video_file:
                        try:
                            if os.path.isfile(presentation.video_file.path):
                                os.remove(presentation.video_file.path)
                        except Exception as e:
                            pass
                    
                    # Eliminar de Cloudinary
                    if presentation.is_stored_in_cloud and presentation.cloudinary_public_id:
                        try:
                            uploader.destroy(
                                presentation.cloudinary_public_id,
                                resource_type='video'
                            )
                        except Exception as e:
                            pass
                    
                    # Eliminar fotos de participantes
                    for participant in presentation.participants.all():
                        if participant.photo:
                            try:
                                if os.path.isfile(participant.photo.path):
                                    os.remove(participant.photo.path)
                            except Exception as e:
                                pass
                        participant.delete()
                    
                    # Eliminar AIAnalysis si existe
                    if hasattr(presentation, 'ai_analysis'):
                        try:
                            presentation.ai_analysis.delete()
                        except Exception:
                            pass
                    
                    # Eliminar la presentación
                    presentation.delete()
                
                # 5. Finalmente eliminar la asignación
                assignment.delete()
                
                messages.success(
                    request,
                    f'La asignación "{assignment_title}" y {presentation_count} presentación(es) '
                    f'han sido eliminadas permanentemente.'
                )
                
            except Exception as e:
                messages.error(
                    request,
                    f'Error al eliminar la asignación: {str(e)}'
                )
        else:
            messages.error(
                request, 
                'Acción no válida. Verifica el estado de la asignación.'
            )
        
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


# =====================================================
# VISTA PARA GRABACIÓN EN VIVO
# =====================================================

@student_required
def live_record_view(request):
    """
    Vista para grabar presentaciones en vivo desde la cámara
    Permite a los estudiantes grabar directamente sin subir archivo
    """
    # Obtener asignaciones disponibles (sin presentación previa del estudiante)
    asignaciones_con_presentacion = Presentation.objects.filter(
        student=request.user
    ).values_list('assignment_id', flat=True)
    
    available_assignments = Assignment.objects.filter(
        is_active=True,
        due_date__gte=timezone.now()
    ).exclude(
        id__in=asignaciones_con_presentacion
    ).select_related('course', 'course__teacher').order_by('due_date')
    
    # Verificar si viene una asignación específica por URL
    assignment_id = request.GET.get('assignment')
    selected_assignment = None
    
    if assignment_id:
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            
            # Verificar que no haya presentación previa para esta asignación
            if assignment.id in asignaciones_con_presentacion:
                messages.warning(
                    request, 
                    f'Ya has subido una presentación para "{assignment.title}". '
                    'Selecciona otra asignación disponible.'
                )
            elif assignment.due_date < timezone.now():
                messages.warning(
                    request,
                    f'La asignación "{assignment.title}" ha vencido. '
                    'Selecciona otra asignación disponible.'
                )
            elif not assignment.is_active:
                messages.warning(
                    request,
                    f'La asignación "{assignment.title}" no está activa. '
                    'Selecciona otra asignación disponible.'
                )
            else:
                # La asignación es válida, preseleccionarla
                selected_assignment = assignment
        except Assignment.DoesNotExist:
            messages.error(request, "Asignación no encontrada.")
    
    if request.method == 'POST':
        # Procesar video grabado
        try:
            video_file = request.FILES.get('video_file')
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            assignment_id = request.POST.get('assignment')
            
            if not video_file:
                return JsonResponse({'success': False, 'error': 'No se recibió el video'}, status=400)
            
            if not title:
                return JsonResponse({'success': False, 'error': 'El título es requerido'}, status=400)
            
            if not assignment_id:
                return JsonResponse({'success': False, 'error': 'Debes seleccionar una asignación'}, status=400)
            
            # Verificar que el estudiante no haya subido ya una presentación para esta asignación
            existing_presentation = Presentation.objects.filter(
                student=request.user,
                assignment_id=assignment_id
            ).exists()
            
            if existing_presentation:
                return JsonResponse({
                    'success': False, 
                    'error': 'Ya has subido una presentación para esta asignación. No puedes subir más de una.'
                }, status=400)
            
            # Crear presentación
            presentation = Presentation(
                title=title,
                description=description or "Grabado en vivo",
                student=request.user,
                video_file=video_file,
                file_size=video_file.size,
                uploaded_at=timezone.now(),
                status='UPLOADED',
                is_live_recording=True  # Marcar como grabación en vivo
            )
            
            if assignment_id:
                try:
                    assignment = Assignment.objects.get(id=assignment_id)
                    presentation.assignment = assignment
                except Assignment.DoesNotExist:
                    pass
            
            presentation.save()
            
            # Subir a Cloudinary automáticamente (igual que con videos pregrabados)
            cloudinary_status = {'uploaded': False, 'message': ''}
            try:
                from apps.ai_processor.services import CloudinaryService
                if CloudinaryService.is_configured():
                    cloudinary_result = presentation.upload_to_cloudinary()
                    if cloudinary_result:
                        cloudinary_status['uploaded'] = True
                        cloudinary_status['message'] = '☁️ Video subido a Cloudinary exitosamente'
                        logger.info(f'☁️ Video subido a Cloudinary exitosamente: {cloudinary_result.get("public_id")}')
                    else:
                        cloudinary_status['message'] = '⚠️ No se pudo subir a Cloudinary, usando almacenamiento local'
                        logger.warning('⚠️ No se pudo subir a Cloudinary, usando almacenamiento local')
                else:
                    cloudinary_status['message'] = '⚠️ Cloudinary no configurado, usando almacenamiento local'
            except Exception as cloud_error:
                cloudinary_status['message'] = f'⚠️ Error al subir a Cloudinary: {str(cloud_error)}'
                logger.error(f"Error subiendo a Cloudinary (no crítico): {str(cloud_error)}")
            
            # Iniciar análisis de IA en segundo plano
            from .tasks import process_presentation_async
            process_presentation_async(presentation.id)
            
            # Crear mensaje de éxito completo
            success_message = f'✅ Grabación en vivo "{title}" guardada exitosamente! El análisis de IA se procesará automáticamente.'
            
            return JsonResponse({
                'success': True, 
                'redirect': '/presentations/my-presentations/',
                'message': success_message,
                'cloudinary_status': cloudinary_status
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    # GET request - redirigir al tab de grabación en upload (esta vista solo maneja POST/AJAX)
    # El formulario de grabación está en presentations_upload.html tab="record"
    if selected_assignment:
        return redirect(f"{reverse('presentations:upload_presentation')}?tab=record&assignment={selected_assignment.id}")
    return redirect(f"{reverse('presentations:upload_presentation')}?tab=record")


@login_required
def get_presentation_progress(request, presentation_id):
    """
    API endpoint para obtener el progreso del análisis de una presentación
    """
    from django.core.cache import cache
    
    # Verificar que el usuario tenga permiso
    try:
        presentation = Presentation.objects.get(id=presentation_id)
        
        # Solo el estudiante dueño o docentes pueden ver el progreso
        if request.user != presentation.student and not request.user.groups.filter(name='Docente').exists():
            return JsonResponse({'error': 'No autorizado'}, status=403)
        
        # Obtener progreso del cache
        progress_data = cache.get(f'presentation_progress_{presentation_id}')
        
        if progress_data:
            return JsonResponse(progress_data)
        else:
            # Si no hay datos en cache, verificar el estado de la presentación
            return JsonResponse({
                'status': presentation.status,
                'progress': 100 if presentation.status == 'ANALYZED' else 0,
                'step': {
                    'UPLOADED': 'En cola para análisis...',
                    'PROCESSING': 'Procesando...',
                    'ANALYZED': 'Análisis completado ✅',
                    'FAILED': 'Error en el análisis ❌',
                    'GRADED': 'Calificada ✅'
                }.get(presentation.status, 'Estado desconocido')
            })
    
    except Presentation.DoesNotExist:
        return JsonResponse({'error': 'Presentación no encontrada'}, status=404)


# =====================================================
# VISTAS PARA CALIFICACIÓN Y EDICIÓN (PROFESORES)
# =====================================================

@teacher_required
def edit_participant_grade(request, participant_id):
    """
    Vista para que el profesor edite la calificación de un participante individual.
    
    La calificación de IA viene pre-llenada en el formulario.
    El profesor puede editarla y agregar comentarios adicionales.
    """
    from .forms_grading import ParticipantGradingForm
    from .models import Participant
    
    participant = get_object_or_404(Participant, id=participant_id)
    presentation = participant.presentation
    
    # Verificar que el profesor tenga acceso a esta presentación
    if presentation.assignment.course.teacher != request.user:
        messages.error(request, 'No tienes permiso para calificar esta presentación.')
        return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        form = ParticipantGradingForm(request.POST, instance=participant)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.grade_modified_by = request.user
            participant.grade_modified_at = timezone.now()
            participant.save()
            
            messages.success(
                request,
                f'✅ Calificación de {participant.label} actualizada correctamente.'
            )
            return redirect('presentation_detail', pk=presentation.id)
    else:
        form = ParticipantGradingForm(instance=participant)
    
    context = {
        'form': form,
        'participant': participant,
        'presentation': presentation,
        'assignment': presentation.assignment,
    }
    
    return render(request, 'presentations/edit_participant_grade.html', context)


@teacher_required
def bulk_grade_presentation(request, presentation_id):
    """
    Vista para calificar todos los participantes de una presentación a la vez.
    
    Muestra un formulario con todos los participantes y sus calificaciones de IA pre-llenadas.
    El profesor puede editar las que desee y guardar todo de una vez.
    """
    from .forms_grading import BulkGradingForm
    from .models import Participant
    
    presentation = get_object_or_404(Presentation, id=presentation_id)
    
    # Verificar permisos
    if presentation.assignment.course.teacher != request.user:
        messages.error(request, 'No tienes permiso para calificar esta presentación.')
        return redirect('teacher_dashboard')
    
    participants = presentation.participants.all().order_by('label')
    
    if request.method == 'POST':
        form = BulkGradingForm(request.POST, participants=participants)
        if form.is_valid():
            updated_count = 0
            
            for participant in participants:
                grade_field = f'grade_{participant.id}'
                feedback_field = f'feedback_{participant.id}'
                
                new_grade = form.cleaned_data.get(grade_field)
                new_feedback = form.cleaned_data.get(feedback_field)
                
                # Solo actualizar si hay cambios
                if new_grade is not None and new_grade != participant.ai_grade:
                    participant.manual_grade = new_grade
                    participant.grade_modified_by = request.user
                    participant.grade_modified_at = timezone.now()
                    updated_count += 1
                
                if new_feedback and new_feedback != participant.teacher_feedback:
                    participant.teacher_feedback = new_feedback
                    if not participant.grade_modified_by:
                        participant.grade_modified_by = request.user
                        participant.grade_modified_at = timezone.now()
                    updated_count += 1
                
                participant.save()
            
            # Actualizar estado de la presentación
            if updated_count > 0:
                presentation.status = 'GRADED'
                presentation.graded_by = request.user
                presentation.graded_at = timezone.now()
                presentation.save()
                
                messages.success(
                    request,
                    f'✅ {updated_count} calificaciones actualizadas correctamente.'
                )
            else:
                messages.info(request, 'No se realizaron cambios.')
            
            return redirect('presentation_detail', pk=presentation.id)
    else:
        form = BulkGradingForm(participants=participants)
    
    context = {
        'form': form,
        'presentation': presentation,
        'participants': participants,
        'assignment': presentation.assignment,
    }
    
    return render(request, 'presentations/bulk_grade.html', context)


@teacher_required
def reset_participant_grade(request, participant_id):
    """
    Restaura la calificación de un participante a la evaluación original de IA.
    """
    from .models import Participant
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    
    participant = get_object_or_404(Participant, id=participant_id)
    presentation = participant.presentation
    
    # Verificar permisos
    if presentation.assignment.course.teacher != request.user:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)
    
    # Restaurar calificación de IA
    participant.manual_grade = None
    participant.teacher_feedback = ''
    participant.grade_modified_by = None
    participant.grade_modified_at = None
    participant.save()
    
    messages.success(request, f'✅ Calificación de {participant.label} restaurada a evaluación de IA.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'ai_grade': participant.ai_grade,
            'final_grade': participant.final_grade
        })
    
    return redirect('presentation_detail', pk=presentation.id)


# =====================================================
# CONFIGURACIÓN DE IA
# =====================================================

@login_required
@group_required('Docente')
def ai_configuration_view(request):
    """Vista informativa sobre niveles de evaluación de IA"""
    
    # Solo mostrar información, sin permitir cambios
    # Obtener configuración actual solo para referencia
    config = AIConfiguration.get_config_for_teacher(request.user)
    
    # Obtener descripciones de cada nivel directamente
    levels_info = {
        'strict': {
            'title': 'Estricto',
            'description': 'Evaluación rigurosa que demanda excelencia en todos los aspectos',
            'items': [
                'Requiere dominio completo del tema',
                'Penaliza imprecisiones y falta de profundidad',
                'Exige estructura clara y ejemplos concretos',
                'Calificaciones típicas: 50-85% (excelentes hasta 90%)'
            ]
        },
        'moderate': {
            'title': 'Moderado (Recomendado)',
            'description': 'Balance ideal entre exigencia académica y reconocimiento del esfuerzo',
            'items': [
                '70-85% para presentaciones bien desarrolladas',
                '85-95% para presentaciones sobresalientes',
                'Balance entre exigencia y comprensión',
                'Valora profundidad y relevancia del contenido'
            ]
        },
        'lenient': {
            'title': 'Suave',
            'description': 'Enfoque motivacional que prioriza el aprendizaje y la participación',
            'items': [
                '70-80% con comprensión básica del tema',
                '85-95% si el contenido es relevante',
                'Valora el esfuerzo y participación',
                'Enfoque en reforzar lo positivo'
            ]
        }
    }
    
    context = {
        'current_level': config.strictness_level,
        'levels_info': levels_info,
        'last_updated': config.updated_at,
        'is_info_only': True,  # Indicar que es solo informativo
    }
    
    return render(request, 'presentations/ai_configuration.html', context)


# IA GROK - MEJORAR INSTRUCCIONES


@login_required
@require_http_methods(["POST"])
def improve_instructions_ai_view(request):
    """Vista para mejorar instrucciones de asignaciones usando Groq AI"""
    
    # Verificar permisos de profesor
    if not request.user.groups.filter(name='Docente').exists():
        return JsonResponse({
            'success': False,
            'error': 'No tienes permisos para usar esta función. Debes ser profesor.'
        }, status=403)
    
    try:
        data = json.loads(request.body)
        instructions = data.get('instructions', '').strip()
        context = data.get('context', {})
        
        if not instructions:
            return JsonResponse({
                'success': False,
                'error': 'No se proporcionaron instrucciones'
            }, status=400)
        
        # Importar Groq client
        from groq import Groq
        from apps.ai_processor.services.groq_key_manager import GroqKeyManager
        
        # Obtener API key usando el sistema de rotación
        key_manager = GroqKeyManager()
        groq_api_key = key_manager.get_current_key()
        
        if not groq_api_key:
            return JsonResponse({
                'success': False,
                'error': 'API Keys de Groq no configuradas. Contacta al administrador.'
            }, status=500)
        
        # Construir el prompt para Groq
        prompt = f"""Eres un experto docente universitario especializado en evaluación de presentaciones virtuales. Tu tarea es mejorar las instrucciones de una asignación de EXPOSICIÓN VIRTUAL que será evaluada automáticamente por IA.

CONTEXTO DE LA ASIGNACIÓN:
- Título: {context.get('title', 'No especificado')}
- Descripción: {context.get('description', 'No especificada')}
- Tipo: {context.get('assignment_type', 'No especificado')}
- Duración máxima: {context.get('max_duration', 'No especificada')} minutos

INSTRUCCIONES ORIGINALES:
{instructions}

IMPORTANTE: Esta es una EXPOSICIÓN VIRTUAL en video que será evaluada por IA en los siguientes aspectos:
1. **Coherencia del contenido**: La IA analizará si el discurso es lógico y bien estructurado
2. **Claridad en la comunicación**: La IA evaluará la expresión oral y fluidez
3. **Cumplimiento de objetivos**: La IA verificará que se cubran todos los puntos solicitados

MEJORA estas instrucciones siguiendo estos criterios:

📹 **Para la grabación del video:**
- Especifica claramente QUÉ debe incluir la presentación
- Indica la ESTRUCTURA requerida (introducción, desarrollo, conclusión)
- Define los PUNTOS CLAVE que debe abordar el estudiante
- Menciona aspectos de CALIDAD (audio claro, iluminación adecuada, postura profesional)

🎯 **Para la evaluación por IA:**
- Sé ESPECÍFICO en los temas que deben cubrirse (la IA buscará estos temas en la transcripción)
- Define criterios MEDIBLES (ej: "mencionar al menos 3 conceptos clave")
- Indica el ORDEN lógico esperado (la IA evaluará la coherencia)
- Especifica EJEMPLOS o CASOS que deben incluirse

📝 **Formato de las instrucciones mejoradas:**
1. Organízalas en secciones claras con títulos
2. Usa viñetas o numeración para mayor claridad
3. Incluye criterios de evaluación específicos
4. Agrega sugerencias técnicas (duración por sección, tips de grabación)
5. Mantén un tono profesional pero motivador
6. NO inventes información que no esté en el contexto original
7. Longitud: 250-400 palabras

**EJEMPLO de lo que se espera:**
"En tu video debes explicar [concepto X], luego analizar [concepto Y], y finalmente proponer [concepto Z]. La IA evaluará que menciones estos tres elementos y que los presentes en este orden lógico."

Responde SOLO con las instrucciones mejoradas, sin explicaciones adicionales ni comentarios."""

        # Intentar con rotación de keys si falla
        max_retries = min(3, len(key_manager.keys))
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Crear cliente Groq con la key actual
                client = Groq(api_key=groq_api_key)
                
                # Hacer petición a Groq API
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un asistente experto en educación que ayuda a docentes a crear instrucciones claras y efectivas para asignaciones académicas."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=800,
                    timeout=30
                )
                
                improved_instructions = response.choices[0].message.content.strip()
                
                return JsonResponse({
                    'success': True,
                    'improved_instructions': improved_instructions
                })
                
            except Exception as e:
                last_error = str(e)
                logger.error(f"Error con API key {attempt + 1}: {last_error}")
                
                # Si falla por rate limit, marcar key como fallida y rotar
                if 'rate_limit' in last_error.lower() or '429' in last_error:
                    key_manager.mark_key_failed(groq_api_key)
                    groq_api_key = key_manager.get_current_key()
                    if not groq_api_key:
                        break
                else:
                    # Si es otro error, no reintentar
                    break
        
        # Si llegamos aquí, todos los intentos fallaron
        return JsonResponse({
            'success': False,
            'error': f'No se pudo procesar la solicitud. Último error: {last_error}'
        }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        }, status=400)
    except Exception as e:
        logger.error(f"Error inesperado en improve_instructions_ai_view: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Error inesperado: {str(e)}'
        }, status=500)