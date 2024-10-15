from django.urls import path
from .views import list_seedbeds, create_seedbed, delete_seedbed

app_name = 'seedbeds'

urlpatterns = [
    path('listar/<int:community_id>/', list_seedbeds, name='list_seedbeds'),
    path('criar/<int:community_id>/', create_seedbed, name='create_seedbed'),
    path('deletar/<int:community_id>/<int:seedbed_id>/', delete_seedbed, name='delete_seedbed'),
]