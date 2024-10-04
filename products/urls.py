from django.urls import path
from .views import(
	product_detail_view, 
    #add_product,
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
	path ('<int:id>/update/', product_update_view, name= 'product-update'),
	path ('<int:id>/delete/', product_delete_view, name= 'product-delete'),
    path('details/<int:id>/', product_detail_view, name='product-detail'),
    #path('adicionar/<int:seedbed_id>/', add_product, name='add-product'),
]
