from django.urls import path
from . import views
app_name = 'tasks'
urlpatterns = [
    path('add_task/', views.add_task, name='add_task'),  # Nenhum ID
    path('add_task/<int:community_id>/', views.add_task, name='add_task'),  # Somente community_id
    path('add_task/<int:community_id>/<int:area_id>/', views.add_task, name='add_task'),  # community_id e area_id
    path('add_task/<int:community_id>/<int:area_id>/<int:seedbed_id>/', views.add_task, name='add_task'),  # community_id, area_id e seedbed_id
    path('add_task/<int:community_id>/<int:area_id>/<int:seedbed_id>/<int:product_id>/', views.add_task, name='add_task'),  # community_id, area_id, seedbed_id e product_id
    path('add_task/<int:community_id>/<int:area_id>/<int:seedbed_id>/<int:product_id>/<int:type_product_id>/', views.add_task, name='add_task'),  # Todos os IDs
]
