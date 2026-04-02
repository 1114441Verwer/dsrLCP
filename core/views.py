from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def dashboard_view(request):
    return render(request, 'core/dashboard.html')


def community_view(request):
    return render(request, 'core/community.html')


def zoeken_view(request):
    return render(request, 'core/zoeken.html')


def profiel_view(request):
    return render(request, 'core/profiel.html')