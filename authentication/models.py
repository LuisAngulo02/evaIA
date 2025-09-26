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
        """Obtener el rol desde los grupos de Django"""
        if self.user.groups.filter(name='Administrador').exists():
            return 'ADMIN'
        elif self.user.groups.filter(name='Docente').exists():
            return 'DOCENTE'
        elif self.user.groups.filter(name='Estudiante').exists():
            return 'ESTUDIANTE'
        return 'SIN_ROL'
    
    def get_role_display(self):
        """Obtener el nombre del rol para mostrar"""
        role = self.get_role()
        role_names = {
            'ADMIN': 'Administrador',
            'DOCENTE': 'Docente', 
            'ESTUDIANTE': 'Estudiante',
            'SIN_ROL': 'Sin rol asignado'
        }
        return role_names.get(role, 'Sin rol')
    
    @property
    def role(self):
        """Propiedad para compatibilidad con código existente"""
        return self.get_role()
    
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
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
