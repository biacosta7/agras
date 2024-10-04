from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_list, name='community_hub'),
    path('criar/', views.create_community, name='create_community'),
    path('editar/<int:pk>/', views.update_community, name='update_community'),
    path('deletar/<int:pk>/', views.delete_community, name='delete_community'),
    path('dashboard/', views.dashoboard_view, name='dashboard')
]