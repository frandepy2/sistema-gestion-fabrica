import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import CabeceraPedido, DetallePedido
from .forms import CabeceraPedidoForm, DetallePedidoForm
from productos.models import Producto

# Create your views here.
def listar_pedidos(request):
    pedidos = CabeceraPedido.objects.filter(cliente=request.user)
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})

def crear_pedido(request):
    productos = Producto.objects.all()
    usuario_actual = request.user
    print(usuario_actual)

    if request.method == 'POST':
        cabecera_pedido = CabeceraPedido.objects.create(
            fecha_pedido= datetime.date.today(),
            cliente=usuario_actual
        )
        
        print("##DEBUG##")
        print(cabecera_pedido.cliente)
        print(cabecera_pedido.fecha_pedido)

        return redirect('/pedidos')  # Redirigir a la vista después de guardar el pedido

    else:
        detalle_form = DetallePedidoForm()

    return render(request, 'pedidos/crear_pedido.html', {'productos': productos, 'detalle_form': detalle_form})