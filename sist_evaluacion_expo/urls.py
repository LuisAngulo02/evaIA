"""
URL configuration for sist_evaluacion_expo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from django.shortcuts import render

def test_export_view(request):
    return render(request, 'test_export.html')

def test_notifications_view(request):
    return render(request, 'test_notifications.html')

def test_simple_notifications_view(request):
    return render(request, 'test_simple_notifications.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('auth:dashboard' if request.user.is_authenticated else 'auth:login')),
    path('auth/', include('authentication.urls')),
    path('presentations/', include('apps.presentaciones.urls')),
    path('reports/', include('apps.reportes.urls')),
    path('help/', include('apps.help.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('notificaciones/', include('apps.notifications.urls')),  # Alias en español
    path('test-export/', test_export_view, name='test_export'),
    path('test-notifications/', test_notifications_view, name='test_notifications'),
    path('test-simple/', test_simple_notifications_view, name='test_simple_notifications'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
