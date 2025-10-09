from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_guide_view(request):
    """Vista para mostrar la guía de usuario"""
    context = {
        'user': request.user,
    }
    return render(request, 'help/user_guide.html', context)