from django.urls import path
from .views import list_seedbeds, create_seedbed, delete_seedbed

app_name = 'seedbeds'

urlpatterns = [
    path('listar/', list_seedbeds, name='list-seedbeds'),
    path('criar/', create_seedbed, name='create-seedbeds'),
    path('deletar/<int:seedbed_id>/', delete_seedbed, name='delete-seedbed'),
]
