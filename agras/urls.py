"""
URL configuration for agras project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
#from products.urls import 

urlpatterns = [
    path('admin/', admin.site.urls),
	path('product/', include('products.urls')),
	#path('products/create/', product_create_view, name='product-list'), 
    #path( 'products/<int:id>/', product_detail_view, name='product-detail'), 
	#path ('products/<int:id>/update/', product_update_view, name= 'product-update'),
	#path ('products/<int:id>/delete/', product_delete_view, name= 'product-delete'),
	
	#path('', home_view, name='home'),
	#path('about/', about_view, name='product_detail'),
	#path('contact/', contact_view),
]
