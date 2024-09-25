from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Inclui as URLs da app 'core' para a home page ('' = http://127.0.0.1:8000/)
    path('auth/', include('users.urls')),
]
