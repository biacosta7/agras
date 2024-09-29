from django.urls import path
from . import views

urlpatterns = [
    path('/comunidades/', views.community_list, name='community_hub'),
    path('/comunidades/criar/', views.create_community, name='create_community'),
    path('/comunidades/editar/<int:id>/', views.update_community, name='update_community'),
    path('/comunidades/deletar/<int:id>/', views.delete_community, name='delete_community')
]