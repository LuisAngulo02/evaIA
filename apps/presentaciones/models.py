from django.db import models
from django.contrib.auth.models import User
from authentication.models import Profile

# Modelos específicos para presentaciones
class Presentation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presentations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.student.get_full_name()}"
    
    class Meta:
        verbose_name = 'Presentación'
        verbose_name_plural = 'Presentaciones'

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
