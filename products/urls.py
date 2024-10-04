from django.urls import path
from .views import(
	product_detail_view, 
	product_delete_view, 
	product_list_view, 
	product_update_view,
    create_product_view, 
    create_typeproduct_view
)

app_name = 'product'

urlpatterns = [
    path('adicionar/<int:seedbed_id>/', create_product_view, name='create_product'),
    path('cadastrar/<int:seedbed_id>/', create_typeproduct_view, name='create_typeproduct'),
	path('listar/<int:seedbed_id>/', product_list_view, name='product-list'), 
	path ('<int:product_id>/edit/', product_update_view, name= 'product-update'),
	path ('<int:id>/delete/', product_delete_view, name= 'product-delete'),
    path('details/<int:id>/', product_detail_view, name='product-detail'),
]
