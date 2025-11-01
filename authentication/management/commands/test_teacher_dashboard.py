from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

class Command(BaseCommand):
    help = 'Probar login del docente y verificar dashboard'

    def handle(self, *args, **options):
        try:
            client = Client()
            
            # Hacer login como docente1
            login_response = client.post(reverse('auth:login'), {
                'username': 'docente1',
                'password': '123456'
            })
            
            self.stdout.write(f"Login status: {login_response.status_code}")
            
            if login_response.status_code == 302:  # Redirect after successful login
                self.stdout.write("✅ Login exitoso!")
                
                # Acceder al dashboard de docentes
                dashboard_url = reverse('presentations:teacher_dashboard')
                dashboard_response = client.get(dashboard_url)
                
                self.stdout.write(f"Dashboard status: {dashboard_response.status_code}")
                
                if dashboard_response.status_code == 200:
                    self.stdout.write("✅ Dashboard cargado correctamente")
                    
                    # Buscar contenido específico en la respuesta
                    content = dashboard_response.content.decode('utf-8')
                    
                    if 'Presentaciones por Calificar' in content:
                        self.stdout.write("✅ Sección 'Presentaciones por Calificar' encontrada")
                    else:
                        self.stdout.write("❌ Sección 'Presentaciones por Calificar' NO encontrada")
                    
                    # Buscar números de badges o contadores
                    import re
                    badge_numbers = re.findall(r'<span[^>]*badge[^>]*>(\d+)</span>', content)
                    if badge_numbers:
                        self.stdout.write(f"✅ Badges encontrados con números: {badge_numbers}")
                    
                    # Verificar si aparece el número 3 (que esperamos)
                    if '3' in content:
                        self.stdout.write("✅ El número 3 aparece en el dashboard (esperado)")
                    
                    self.stdout.write(f"Content length: {len(content)} bytes")
                    
                else:
                    self.stdout.write(f"❌ Error en dashboard: {dashboard_response.status_code}")
            else:
                self.stdout.write(f"❌ Error en login: {login_response.status_code}")
                
        except Exception as e:
            self.stdout.write(f"ERROR: {str(e)}")
            import traceback
            self.stdout.write(traceback.format_exc())