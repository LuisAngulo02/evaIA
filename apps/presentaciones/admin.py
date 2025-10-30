from django.contrib import admin
from .models import Presentation, Course, Assignment, AIAnalysis, Participant


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    readonly_fields = ('label', 'participation_time', 'time_percentage', 'coherence_score', 'final_grade')
    fields = ('label', 'participation_time', 'time_percentage', 'coherence_score', 'final_grade', 'coherence_level')


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'assignment', 'status', 'created_at', 'final_score')
    list_filter = ('status', 'created_at', 'assignment')
    search_fields = ('title', 'student__username', 'student__first_name', 'student__last_name')
    raw_id_fields = ('student', 'assignment', 'graded_by')
    inlines = [ParticipantInline]
    readonly_fields = ('created_at', 'updated_at', 'processed_at', 'analyzed_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'teacher__username')
    raw_id_fields = ('teacher',)
    filter_horizontal = ('students',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'assignment_type', 'due_date', 'is_active')
    list_filter = ('assignment_type', 'is_active', 'due_date')
    search_fields = ('title', 'course__name', 'course__code')
    raw_id_fields = ('course',)


@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ('presentation', 'analyzed_at', 'content_relevance', 'topic_coverage')
    list_filter = ('analyzed_at',)
    search_fields = ('presentation__title',)
    raw_id_fields = ('presentation',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('label', 'presentation', 'final_grade', 'coherence_level', 'time_percentage', 'contribution_percentage')
    list_filter = ('coherence_level', 'created_at')
    search_fields = ('label', 'presentation__title')
    raw_id_fields = ('presentation',)
    readonly_fields = ('created_at', 'updated_at')


