from django.shortcuts import render, redirect, get_object_or_404
from .models import CabeceraPedido, DetallePedido
from .forms import CabeceraPedidoForm, DetallePedidoForm

# Create your views here.
def listar_pedidos(request):
    pedidos = CabeceraPedido.objects.filter(cliente=request.user)
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})
