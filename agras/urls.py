from django.contrib import admin
from django.urls import path, include
from communities.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comunidades/', include('communities.urls')),
    path('auth/', include('users.urls')),
    path('', home_view, name='home')
]
