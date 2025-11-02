"""
Comando para enviar notificaciones a profesores sobre asignaciones próximas a vencer
Ejecutar diariamente con cron o tareas programadas
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.presentaciones.models import Assignment
from apps.notifications.services import NotificationService


class Command(BaseCommand):
    help = 'Envía notificaciones a profesores sobre asignaciones próximas a vencer'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=3,
            help='Notificar cuando falten N días para la fecha límite (default: 3)'
        )

    def handle(self, *args, **options):
        days_threshold = options['days']
        now = timezone.now()
        
        # Buscar asignaciones que vencen en los próximos N días
        target_date = now + timedelta(days=days_threshold)
        
        assignments = Assignment.objects.filter(
            is_active=True,
            due_date__date=target_date.date()
        )
        
        notifications_sent = 0
        
        for assignment in assignments:
            days_remaining = (assignment.due_date - now).days
            
            notification = NotificationService.notify_assignment_deadline_approaching_teacher(
                assignment, 
                days_remaining
            )
            
            if notification:
                notifications_sent += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Notificación enviada a {assignment.course.teacher.username} '
                        f'para la asignación "{assignment.title}" (vence en {days_remaining} días)'
                    )
                )
        
        if notifications_sent == 0:
            self.stdout.write(
                self.style.WARNING(
                    f'No se encontraron asignaciones que venzan en {days_threshold} días'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Total: {notifications_sent} notificación(es) enviada(s)'
                )
            )
