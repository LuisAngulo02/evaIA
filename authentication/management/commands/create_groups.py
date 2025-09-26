from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Crea los grupos de usuarios necesarios para el sistema'
    
    def handle(self, *args, **options):
        groups = ['Estudiante', 'Docente', 'Administrador']
        
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Grupo "{group_name}" creado exitosamente')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'El grupo "{group_name}" ya existe')
                )
        
        self.stdout.write(
            self.style.SUCCESS('¡Todos los grupos han sido verificados!')
        )