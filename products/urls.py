from django.urls import path
from .views import(
	product_detail_view, 
    add_product,
	product_delete_view, 
	product_list_view, 
	product_update_view,
    mostrar_formulario, 
    cadastrar_produto, 
)

app_name = 'product'

urlpatterns = [
    path('cadastrar_produto/<int:seedbed_id>/', mostrar_formulario, name='mostrar_formulario'),
    path('cadastrar_produto/<int:seedbed_id>/salvar/', cadastrar_produto, name='cadastrar_produto'),

	path('listar/<int:seedbed_id>/', product_list_view, name='product-list'), 
	path ('<int:id>/update/', product_update_view, name= 'product-update'),
	path ('<int:id>/delete/', product_delete_view, name= 'product-delete'),
    path('details/<int:id>/', product_detail_view, name='product-detail'),
    path('adicionar/<int:seedbed_id>/', add_product, name='add-product'),
]
