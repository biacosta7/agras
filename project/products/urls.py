from django.urls import path
from .views import (
    create_product_view, 
    create_typeproduct_view
)

app_name = 'product'

urlpatterns = [
    path('adicionar/<int:community_id>/', create_product_view, name='create_product'),
    path('cadastrar/<int:community_id>/', create_typeproduct_view, name='create_typeproduct'),
]
