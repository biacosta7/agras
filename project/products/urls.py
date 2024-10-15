from django.urls import path
from .views import (
    create_product_view, 
    create_typeproduct_view,
    product_detail_view, 
	product_delete_view, 
	product_list_view, 
	product_update_view,
)

app_name = 'product'

urlpatterns = [
    #path('adicionar/<int:community_id>/', create_product_view, name='create_product'),
    path('cadastrar/<int:community_id>/', create_typeproduct_view, name='create_typeproduct'),
    path('adicionar/<int:community_id>/<int:seedbed_id>/', create_product_view, name='create_product'),

    path('editar/<int:seedbed_id>/<int:product_id>/', product_update_view, name='product-update'),
	path('listar/<int:seedbed_id>/', product_list_view, name='product-list'), 
	path('<int:seedbed_id>/<int:product_id>/delete/', product_delete_view, name='product-delete'),
    path('details/<int:id>/', product_detail_view, name='product-detail'),
    
]
