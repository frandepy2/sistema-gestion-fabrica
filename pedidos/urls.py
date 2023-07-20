# pedidos/urls.py

from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('listar/', views.listar_pedidos, name='listar_pedidos'),
]