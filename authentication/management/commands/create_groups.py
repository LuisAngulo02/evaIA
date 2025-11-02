from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Crea los grupos de usuarios necesarios para el sistema (Estudiante y Docente)'
    
    def handle(self, *args, **options):
        # Solo crear grupos Estudiante y Docente (sin Administrador)
        groups = ['Estudiante', 'Docente']
        
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Grupo "{group_name}" creado exitosamente')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  El grupo "{group_name}" ya existe')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 ¡Grupos de usuarios verificados correctamente!')
        )
        self.stdout.write(
            self.style.SUCCESS('   - Estudiante ✓')
        )
        self.stdout.write(
            self.style.SUCCESS('   - Docente ✓')
        )