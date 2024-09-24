from django.urls import path
from products.views import(
	product_register_view, 
	product_detail_view, 
	#product_delete_view, 
	product_list_view, 
	#product_update_view
    
	)

app_name = 'product'

urlpatterns = [
	path('', product_list_view, name='product-list'), 
	path('registrar/', product_register_view, name='product-list'), 
	#path ('<int:id>/update/', product_update_view, name= 'product-update'),
	#path ('<int:id>/delete/', product_delete_view, name= 'product-delete'),
    path('details/<int:id>/', product_detail_view, name='product-detail')
] 
