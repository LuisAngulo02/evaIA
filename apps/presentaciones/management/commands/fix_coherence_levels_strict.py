"""
Comando para corregir niveles de coherencia de TODOS los participantes
Usa umbrales FIJOS sin importar la configuración de rigurosidad
"""
from django.core.management.base import BaseCommand
from apps.presentaciones.models import Participant


class Command(BaseCommand):
    help = 'Corrige los niveles de coherencia de todos los participantes basándose en nota_coherencia'

    def handle(self, *args, **options):
        # Umbrales FIJOS (NO ajustables por rigurosidad)
        UMBRALES = {
            'Excelente': 90,      # >= 90/100
            'Muy Buena': 80,      # >= 80/100
            'Buena': 70,          # >= 70/100
            'Regular': 60,        # >= 60/100
            'Baja': 50,           # >= 50/100
            'Insuficiente': 0     # < 50/100
        }
        
        def clasificar_nivel(nota_coherencia):
            """Clasifica el nivel basándose en la nota de coherencia (0-100)"""
            if nota_coherencia >= UMBRALES['Excelente']:
                return 'Excelente'
            elif nota_coherencia >= UMBRALES['Muy Buena']:
                return 'Muy Buena'
            elif nota_coherencia >= UMBRALES['Buena']:
                return 'Buena'
            elif nota_coherencia >= UMBRALES['Regular']:
                return 'Regular'
            elif nota_coherencia >= UMBRALES['Baja']:
                return 'Baja'
            else:
                return 'Insuficiente'
        
        participants = Participant.objects.all()
        total = participants.count()
        updated = 0
        
        self.stdout.write(self.style.WARNING(f'\nRevisando {total} participantes...'))
        self.stdout.write(self.style.WARNING(f'Umbrales FIJOS:'))
        self.stdout.write(f'  - Excelente: >= {UMBRALES["Excelente"]}/100')
        self.stdout.write(f'  - Muy Buena: >= {UMBRALES["Muy Buena"]}/100')
        self.stdout.write(f'  - Buena: >= {UMBRALES["Buena"]}/100')
        self.stdout.write(f'  - Regular: >= {UMBRALES["Regular"]}/100')
        self.stdout.write(f'  - Baja: >= {UMBRALES["Baja"]}/100')
        self.stdout.write(f'  - Insuficiente: < {UMBRALES["Baja"]}/100\n')
        
        for participant in participants:
            old_level = participant.coherence_level
            new_level = clasificar_nivel(participant.coherence_score)
            
            if old_level != new_level:
                participant.coherence_level = new_level
                participant.save(update_fields=['coherence_level'])
                updated += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {participant.presentation.title} - {participant.label}: '
                        f'{participant.coherence_score:.1f}/100 → '
                        f'{old_level} → {new_level}'
                    )
                )
        
        if updated == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Todos los niveles ya son correctos'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Actualizados {updated} de {total} participantes'
                )
            )
