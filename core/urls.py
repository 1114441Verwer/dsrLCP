from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('community/', views.community_view, name='community'),
    path('zoeken/', views.zoeken_view, name='zoeken'),
    path('profiel/', views.profiel_view, name='profiel'),
]