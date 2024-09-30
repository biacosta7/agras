from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comunidades/', include('communities.urls')),
    path('auth/', include('users.urls')),
]
