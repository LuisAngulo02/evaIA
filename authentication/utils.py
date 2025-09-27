from django.contrib.auth.models import User
from authentication.models import Profile

def get_or_create_profile(user):
    """
    Obtiene o crea un perfil para el usuario dado
    """
    if hasattr(user, 'profile'):
        return user.profile
    else:
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

# Agregar método al modelo User
User.get_or_create_profile = lambda self: get_or_create_profile(self)