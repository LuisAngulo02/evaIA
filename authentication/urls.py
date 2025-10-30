from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('student-dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('check-username/', views.check_username, name='check_username'),
    
    # URLs para recuperación de contraseña
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset-sent/', views.password_reset_sent_view, name='password_reset_sent'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password-reset-complete/', views.password_reset_complete_view, name='password_reset_complete'),
]