from django.contrib import admin
from .models import Presentation, Course

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'student__username', 'student__first_name', 'student__last_name')
    raw_id_fields = ('student',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'code', 'teacher__username')
    raw_id_fields = ('teacher',)
    filter_horizontal = ('students',)


