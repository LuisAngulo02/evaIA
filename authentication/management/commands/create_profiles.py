from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import Profile

class Command(BaseCommand):
    help = 'Crea perfiles para usuarios que no tienen uno'
    
    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        
        if not users_without_profile.exists():
            self.stdout.write(
                self.style.SUCCESS('Todos los usuarios ya tienen perfiles asociados.')
            )
            return
        
        created_count = 0
        for user in users_without_profile:
            Profile.objects.create(user=user)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Perfil creado para usuario: {user.username}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'¡{created_count} perfiles creados exitosamente!')
        )