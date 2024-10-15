from django.urls import path
from .views import list_seedbeds, create_seedbed, delete_seedbed

app_name = 'seedbeds'

urlpatterns = [
    path('listar/', list_seedbeds, name='list_seedbeds'),
    path('criar/', create_seedbed, name='create_seedbed'),
    path('deletar/<int:seedbed_id>/', delete_seedbed, name='delete_seedbed'),
]
