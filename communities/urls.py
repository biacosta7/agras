from django.urls import path
from . import views

urlpatterns = [
    path('hub/', views.community_list, name='community_hub'),
    path('criar/', views.create_community, name='create_community'),
    path('editar/<int:id>/', views.update_community, name='update_community'),
    path('deletar/<int:id>/', views.delete_community, name='delete_community')
]