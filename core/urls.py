from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('community/', views.community_view, name='community'),
    path('community/nieuwe-post/', views.create_post_view, name='create_post'),
    path('community/post/<int:post_id>/bewerken/', views.edit_post_view, name='edit_post'),
    path('community/post/<int:post_id>/verwijderen/', views.delete_post_view, name='delete_post'),
    path('zoeken/', views.zoeken_view, name='zoeken'),
    path('profiel/', views.profiel_view, name='profiel'),
    path('profiel/bewerken/', views.edit_profile_view, name='edit_profile'),
    path('profiel/<str:username>/', views.user_profile_view, name='user_profile'),
    path('register/', views.register_view, name='register'),
]