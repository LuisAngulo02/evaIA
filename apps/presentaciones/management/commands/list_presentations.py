# apps/presentaciones/management/commands/list_presentations.py
from django.core.management.base import BaseCommand
from apps.presentaciones.models import Presentation

class Command(BaseCommand):
    help = 'Lista todas las presentaciones disponibles'

    def handle(self, *args, **options):
        presentations = Presentation.objects.all().order_by('-uploaded_at')
        
        if not presentations.exists():
            self.stdout.write(self.style.WARNING('⚠️ No hay presentaciones en el sistema'))
            return
        
        self.stdout.write("📋 Presentaciones disponibles:")
        self.stdout.write("-" * 80)
        
        for p in presentations:
            status_color = {
                'UPLOADED': self.style.HTTP_INFO,
                'PROCESSING': self.style.WARNING,
                'ANALYZED': self.style.HTTP_SUCCESS,
                'GRADED': self.style.SUCCESS,
                'FAILED': self.style.ERROR,
            }.get(p.status, self.style.NOTICE)
            
            self.stdout.write(
                f"ID: {p.id:3d} | "
                f"{p.title[:30]:30s} | "
                f"{p.student.username:15s} | "
                f"{status_color(p.status):12s} | "
                f"{'✅' if p.video_file else '❌'} Video"
            )
        
        self.stdout.write("-" * 80)
        self.stdout.write(f"Total: {presentations.count()} presentaciones")