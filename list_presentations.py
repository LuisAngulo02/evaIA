import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sist_evaluacion_expo.settings')
django.setup()

from apps.presentaciones.models import Presentation

print("\n📋 Últimas 10 presentaciones:")
print("=" * 80)

ps = Presentation.objects.all().order_by('-id')[:10]
for p in ps:
    title = p.assignment.title if p.assignment else "Sin título"
    print(f"  ID {p.id}: {p.user.username} - {title} - Estado: {p.status}")
    if p.participants.exists():
        print(f"         Participantes: {p.participants.count()}")
        for part in p.participants.all():
            chars = len(part.transcription_text)
            print(f"           - {part.name}: {chars} caracteres")

print()
