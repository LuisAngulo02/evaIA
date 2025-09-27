from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role()}"
    
    def get_role(self):
        """Obtener el primer grupo del usuario (rol principal)"""
        user_group = self.user.groups.filter(name__in=['Administrador', 'Docente', 'Estudiante']).first()
        return user_group.name if user_group else None
    
    def get_role_display(self):
        """Obtener el nombre del rol para mostrar"""
        role = self.get_role()
        return role if role else 'Sin rol asignado'
    
    @property
    def role(self):
        """Propiedad para obtener el rol del usuario"""
        return self.get_role()
    
    def has_role(self, role_name):
        """Verificar si el usuario tiene un rol específico"""
        return self.user.groups.filter(name=role_name).exists()
    
    def is_student(self):
        """Verificar si el usuario es estudiante"""
        return self.has_role('Estudiante')
    
    def is_teacher(self):
        """Verificar si el usuario es docente"""
        return self.has_role('Docente')
    
    def is_admin(self):
        """Verificar si el usuario es administrador"""
        return self.has_role('Administrador')
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

# Señal para crear automáticamente un perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Crear perfil si no existe
    if not hasattr(instance, 'profile'):
        Profile.objects.get_or_create(user=instance)
    else:
        instance.profile.save()
