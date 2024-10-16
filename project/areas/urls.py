from django.urls import path
from . import views

app_name = 'areas'

urlpatterns = [
    path('manage/', views.area_manage, name='area_manage'),  # Corrigido para community_id
    path('create/', views.area_create, name='area_create'),
    path('edit/<int:pk>/', views.area_edit, name='area_edit'),
    path('delete/<int:pk>/', views.area_delete, name='area_delete'),
]