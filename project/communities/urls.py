from django.urls import path
from . import views as community_views
from areas import views as area_views
from seedbeds import views as seedbed_views
from products import views as product_views  
from chat import views as chat_views
from tasks import views as tasks_views

urlpatterns = [
    path('', community_views.community_list, name='community_hub'),
    path('criar/', community_views.create_community, name='create_community'),
    path('editar/<int:pk>/', community_views.update_community, name='update_community'),
    path('deletar/<int:pk>/', community_views.delete_community, name='delete_community'),
    path('comunidade/<int:community_id>/gerenciamento/', community_views.manage_community, name='manage_community'),
    path('dashboard/<int:community_id>/', community_views.dashboard_view, name='dashboard'),
    
    # URLs para aceitar e rejeitar solicitações
    path('solicitacao/aceitar/<int:request_id>/', community_views.aceitar_solicitacao, name='aceitar_solicitacao'),
    path('solicitacao/rejeitar/<int:request_id>/', community_views.rejeitar_solicitacao, name='rejeitar_solicitacao'),

    # URLs para áreas dentro de uma comunidade
    path('comunidade/<int:community_id>/areas/', area_views.area_manage, name='area_manage'),
    path('comunidade/<int:community_id>/areas/criar/', area_views.area_create, name='create_area'),
    path('comunidade/<int:community_id>/areas/editar/<int:pk>/', area_views.area_edit, name='update_area'),
    path('comunidade/<int:community_id>/areas/deletar/<int:pk>/', area_views.area_delete, name='delete_area'),
    path('comunidade/<int:community_id>/areas/detalhe/<int:area_id>/', area_views.area_detail, name='area_detail'),

    # URLs para canteiros dentro de uma área
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
    path('comunidades/<int:community_id>/areas/<int:area_id>/canteiros/<int:seedbed_id>/produtos/infos/<int:product_id>/', product_views.get_product_info_view, name='get_product_info'),

    # chatbot (IA)
    path("comunidade/<int:community_id>/<int:user_id>/chat/", chat_views.chat, name="chat"),
    path("comunidade/<int:community_id>/<int:user_id>/perguntar/", chat_views.ask_question, name="ask_question"),

    # tasks
    path('comunidade/<int:community_id>/tarefas', tasks_views.task_page, name='task_page'),
    path('comunidade/<int:community_id>/tarefas/editar/<int:task_id>', tasks_views.edit_task, name='edit_task'),
    path('comunidade/<int:community_id>/tarefas/excluir/<int:task_id>', tasks_views.delete_task, name='delete_task'),

]
