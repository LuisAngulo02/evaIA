from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
import json

class Command(BaseCommand):
    help = 'Probar el login y acceso al dashboard del estudiante'

    def handle(self, *args, **options):
        try:
            # Crear cliente de prueba
            client = Client()
            
            # Hacer login
            login_data = {
                'username': 'estudiante_test',
                'password': '123456'
            }
            
            response = client.post('/auth/login/', login_data, follow=True)
            self.stdout.write(f"Login response status: {response.status_code}")
            
            if response.status_code == 200:
                self.stdout.write("Login exitoso")
                
                # Acceder al dashboard
                dashboard_response = client.get('/auth/student-dashboard/')
                self.stdout.write(f"Dashboard response status: {dashboard_response.status_code}")
                
                if dashboard_response.status_code == 200:
                    # Verificar si el contenido contiene las asignaciones
                    content = dashboard_response.content.decode('utf-8')
                    
                    # Buscar referencias a las asignaciones específicas
                    if 'Historia de la Computación' in content or 'Algoritmos Básicos' in content:
                        self.stdout.write("✓ Las asignaciones específicas SÍ están presentes")
                    else:
                        self.stdout.write("✗ Las asignaciones específicas NO están presentes")
                    
                    # Buscar el condicional del template
                    if '{% if pending_assignments %}' in content:
                        self.stdout.write("✓ El condicional del template está presente")
                    elif 'No tienes tareas pendientes' in content:
                        self.stdout.write("✗ Se está mostrando el mensaje de 'No hay tareas'")
                    
                    # Buscar el badge con el número
                    if 'badge bg-primary rounded-pill' in content:
                        self.stdout.write("✓ El badge está presente en el HTML")
                        # Buscar el número específico
                        import re
                        badge_match = re.search(r'<span class="badge bg-primary rounded-pill">(\d+)</span>', content)
                        if badge_match:
                            badge_number = badge_match.group(1)
                            self.stdout.write(f"Número en el badge: {badge_number}")
                        else:
                            self.stdout.write("No se pudo extraer el número del badge")
                    else:
                        self.stdout.write("✗ El badge NO está presente")
                        
                else:
                    self.stdout.write(f"Error accediendo al dashboard: {dashboard_response.status_code}")
            else:
                self.stdout.write("Error en login")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))