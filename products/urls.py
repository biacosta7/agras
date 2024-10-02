from django.urls import path
from products.views import(
	create_type_product, 
    add_product, 
	product_detail_view, 
	#product_delete_view, 
	product_list_view, 
	#product_update_view
    
	)

app_name = 'product'

urlpatterns = [
	path('', product_list_view, name='product-list'), 
	path('cadastrar/', create_type_product, name='create-typeproduct'), 
    path('adicionar/', add_product, name='add-product'), 
	#path ('<int:id>/update/', product_update_view, name= 'product-update'),
	#path ('<int:id>/delete/', product_delete_view, name= 'product-delete'),
    path('details/<int:id>/', product_detail_view, name='product-detail')
] 
