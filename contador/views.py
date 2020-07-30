from django.shortcuts import render
from django.contrib.auth.views import LoginView

def custom_login(request):
    if request.user.is_authenticated:
        return render(request, 'registro/inicio.html')
    else:
        return render(request, 'registration/login.html')