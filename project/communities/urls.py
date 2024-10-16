from django.urls import path
from . import views as community_views  # Importando as views do app de comunidades
from areas import views as area_views    # Importando as views do app de áreas
from seedbeds import views as seedbed_views  # Importando as views do app de canteiros

urlpatterns = [
    # URL para a lista de comunidades (hub)
    path('', community_views.community_list, name='community_hub'),

    # URLs para criação, edição e deleção de comunidades
    path('criar/', community_views.create_community, name='create_community'),
    path('editar/<int:pk>/', community_views.update_community, name='update_community'),
    path('deletar/<int:pk>/', community_views.delete_community, name='delete_community'),

    # URL para o dashboard de uma comunidade específica
    path('dashboard/<int:community_id>/', community_views.dashboard_view, name='dashboard'),

    # URLs para áreas dentro de uma comunidade (novas URLs)
    path('comunidade/<int:community_id>/areas/', area_views.area_manage, name='area_manage'),
    path('comunidade/<int:community_id>/areas/criar/', area_views.area_create, name='create_area'),
    path('comunidade/<int:community_id>/areas/editar/<int:pk>/', area_views.area_edit, name='update_area'),
    path('comunidade/<int:community_id>/areas/deletar/<int:pk>/', area_views.area_delete, name='delete_area'),

    # URLs para canteiros dentro de uma área (novas URLs)
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/', seedbed_views.list_seedbeds, name='seedbed_list'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/criar/', seedbed_views.create_seedbed, name='create_seedbed'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/editar/<int:pk>/', seedbed_views.edit_seedbed, name='update_seedbed'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/deletar/<int:pk>/', seedbed_views.delete_seedbed, name='delete_seedbed'),
]
