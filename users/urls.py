from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.create_user, name='create_user'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('users/', views.get_all_users, name='get_users'),
    path('users/<int:id>/', views.update_user, name='update_user'), 
    path('users/delete/<int:id>/', views.delete_user, name='update_user'), 
]
