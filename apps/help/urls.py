from django.urls import path
from . import views

app_name = 'help'

urlpatterns = [
    path('guide/', views.user_guide_view, name='user_guide'),
]