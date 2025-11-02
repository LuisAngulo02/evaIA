from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from apps.presentaciones.models import Assignment, Presentation
from apps.notifications.services import NotificationService


class Command(BaseCommand):
    help = 'Envía notificaciones para asignaciones que vencen pronto o ya vencieron'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=3,
            help='Días antes del vencimiento para notificar (por defecto: 3)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Solo mostrar qué notificaciones se enviarían sin enviarlas'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        now = timezone.now()
        
        # Buscar asignaciones que vencen en X días
        due_soon_assignments = Assignment.objects.filter(
            is_active=True,
            due_date__gte=now,
            due_date__lte=now + timedelta(days=days)
        )
        
        # Buscar asignaciones vencidas (hasta 7 días atrás)
        overdue_assignments = Assignment.objects.filter(
            is_active=True,
            due_date__lt=now,
            due_date__gte=now - timedelta(days=7)
        )
        
        total_notifications = 0
        
        # Procesar asignaciones que vencen pronto
        for assignment in due_soon_assignments:
            days_remaining = (assignment.due_date - now).days
            
            # Obtener estudiantes que no han entregado
            students_without_presentation = User.objects.filter(
                groups__name='Estudiante'
            ).exclude(
                presentation__assignment=assignment
            )
            
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        f'[DRY RUN] Notificaría a {students_without_presentation.count()} estudiantes '
                        f'sobre asignación "{assignment.title}" que vence en {days_remaining} día(s)'
                    )
                )
            else:
                notifications = NotificationService.notify_assignment_due_soon(
                    assignment, students_without_presentation, days_remaining
                )
                count = len(notifications)
                total_notifications += count
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Enviadas {count} notificaciones para asignación "{assignment.title}" '
                        f'(vence en {days_remaining} día{"s" if days_remaining != 1 else ""})'
                    )
                )
        
        # Procesar asignaciones vencidas
        for assignment in overdue_assignments:
            days_overdue = (now - assignment.due_date).days
            
            # Obtener estudiantes que no han entregado
            students_without_presentation = User.objects.filter(
                groups__name='Estudiante'
            ).exclude(
                presentation__assignment=assignment
            )
            
            if dry_run:
                self.stdout.write(
                    self.style.ERROR(
                        f'[DRY RUN] Notificaría a {students_without_presentation.count()} estudiantes '
                        f'sobre asignación vencida "{assignment.title}" (vencida hace {days_overdue} día(s))'
                    )
                )
            else:
                notifications = NotificationService.notify_assignment_overdue(
                    assignment, students_without_presentation
                )
                count = len(notifications)
                total_notifications += count
                
                self.stdout.write(
                    self.style.WARNING(
                        f'Enviadas {count} notificaciones para asignación vencida "{assignment.title}" '
                        f'(vencida hace {days_overdue} día{"s" if days_overdue != 1 else ""})'
                    )
                )
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS('Ejecución en modo prueba completada. No se enviaron notificaciones reales.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Proceso completado. Total de notificaciones enviadas: {total_notifications}')
            )