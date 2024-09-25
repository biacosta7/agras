from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),  # Rota pra página inicial
]