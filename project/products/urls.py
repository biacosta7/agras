from django.urls import path
from .views import (
    create_typeproduct_view,
    create_product_view, 
    product_list_view, 
    product_update_view,
    product_delete_view, 
)

app_name = 'product'

urlpatterns = [
    path('cadastrar/<int:community_id>/', create_typeproduct_view, name='create_typeproduct'),
    path('adicionar/<int:community_id>/<int:seedbed_id>/', create_product_view, name='create_product'),
    path('listar/<int:community_id>/<int:seedbed_id>/', product_list_view, name='product_list'), 

    path('editar/<int:community_id>/<int:seedbed_id>/<int:product_id>/', product_update_view, name='product-update'),
    path('delete/<int:community_id>/<int:seedbed_id>/<int:product_id>/', product_delete_view, name='product-delete'),
]
