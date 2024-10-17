from django.urls import path
from . import views as community_views  # Importando as views do app de comunidades
from areas import views as area_views    # Importando as views do app de áreas
from seedbeds import views as seedbed_views  # Importando as views do app de canteiros
from products import views as product_views  # Importando as views do app de produtos

urlpatterns = [
    # URL para a lista de comunidades (hub)
    path('', community_views.community_list, name='community_hub'),

    # URLs para criação, edição e deleção de comunidades
    path('criar/', community_views.create_community, name='create_community'),
    path('editar/<int:pk>/', community_views.update_community, name='update_community'),
    path('deletar/<int:pk>/', community_views.delete_community, name='delete_community'),

    # URL para o dashboard de uma comunidade específica
    path('dashboard/<int:community_id>/', community_views.dashboard_view, name='dashboard'),

    # URLs para áreas dentro de uma comunidade
    path('comunidade/<int:community_id>/areas/', area_views.area_manage, name='area_manage'),
    path('comunidade/<int:community_id>/areas/criar/', area_views.area_create, name='create_area'),
    path('comunidade/<int:community_id>/areas/editar/<int:pk>/', area_views.area_edit, name='update_area'),
    path('comunidade/<int:community_id>/areas/deletar/<int:pk>/', area_views.area_delete, name='delete_area'),
    path('comunidade/<int:community_id>/areas/detalhe/<int:area_id>/', area_views.area_detail, name='area_detail'),

    # URLs para canteiros dentro de uma área
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/', seedbed_views.list_seedbeds, name='seedbed_list'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/criar/', seedbed_views.create_seedbed, name='create_seedbed'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/editar/<int:seedbed_id>/', seedbed_views.edit_seedbed, name='update_seedbed'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/deletar/<int:seedbed_id>/', seedbed_views.delete_seedbed, name='delete_seedbed'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/<int:seedbed_id>/produtos/detalhes/', seedbed_views.seedbed_detail_view, name='seedbed_detail'),

    # URLs para produtos dentro de um canteiro
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/<int:seedbed_id>/produtos/', product_views.product_list_view, name='product_list'),
    path('comunidades/comunidade/<int:community_id>/areas/<int:area_id>/canteiros/<int:seedbed_id>/produtos/cadastrar/', product_views.create_typeproduct_view, name='create_typeproduct'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/<int:seedbed_id>/produtos/adicionar/', product_views.create_product_view, name='create_product'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/<int:seedbed_id>/produtos/editar/<int:product_id>/', product_views.product_update_view, name='product_update'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/<int:seedbed_id>/produtos/deletar/<int:product_id>/', product_views.product_delete_view, name='product_delete'),
    path('comunidade/<int:community_id>/areas/<int:area_id>/canteiros/<int:seedbed_id>/produtos/detalhes/<int:product_id>/', product_views.product_detail_view, name='product_detail'),
    path('comunidades/<int:community_id>/areas/<int:area_id>/canteiros/<int:seedbed_id>/produtos/infos/<int:product_id>/', product_views.get_product_info_view, name='get_product_info')
]
