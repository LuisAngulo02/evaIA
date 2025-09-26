# filepath: e:\S5\constr\proyecto\apps\presentations\urls.py
from django.urls import path
from . import views

app_name = 'presentations'

urlpatterns = [
    # URLs específicas de presentaciones
    path('my-presentations/', views.mis_presentaciones_view, name='my_presentations'),
    path('manage-courses/', views.gestionar_cursos_view, name='manage_courses'),
    path('create-assignment/', views.crear_asignacion_view, name='create_assignment'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]