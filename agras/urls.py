from django.contrib import admin
from django.urls import include, path, include
from communities.views import home_view
#from products.urls import 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comunidades/', include('communities.urls')),
    path('auth/', include('users.urls')),
    path('', home_view, name='home')
	path('product/', include('products.urls')),
	#path('products/create/', product_create_view, name='product-list'), 
    #path( 'products/<int:id>/', product_detail_view, name='product-detail'), 
	#path ('products/<int:id>/update/', product_update_view, name= 'product-update'),
	#path ('products/<int:id>/delete/', product_delete_view, name= 'product-delete'),
	
	#path('', home_view, name='home'),
	#path('about/', about_view, name='product_detail'),
	#path('contact/', contact_view),
]
