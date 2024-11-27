from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.create_user, name='create_user'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('esqueci-senha/', views.forgot_password, name='forgot_password'),
    path('perfil/', views.profile, name='profile'),
]
