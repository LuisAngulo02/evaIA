from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Configuración para mostrar Profile en línea con User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'
    
    fields = ('institution', 'phone', 'avatar', 'is_verified')

# Extender el UserAdmin para incluir el perfil
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    
    # Añadir la columna de rol basada en grupos
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'groups')
    list_select_related = ('profile',)

    def get_role(self, instance):
        if hasattr(instance, 'profile') and instance.profile:
            return instance.profile.get_role_display()
        return "Sin perfil"
    get_role.short_description = 'Rol'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Desregistrar el User por defecto y registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
