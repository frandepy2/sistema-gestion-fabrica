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

    if request.method == 'POST':
        costo = 0
        cabecera_pedido = CabeceraPedido.objects.create(
            fecha_pedido=datetime.date.today(),
            cliente=usuario_actual
        )

        for key, value in request.POST.items():
            if key.startswith('sugerido_'):
                producto_id = key.replace('sugerido_', '')
                producto = Producto.objects.get(pk=producto_id)
                sugerido = int(value)
                # Supongamos que los otros campos, como stock_operacional y vencido, también se reciben y se procesan aquí
                stock_operacional = int(request.POST.get(f'stock_operacional_{producto_id}', 0))
                vencido = int(request.POST.get(f'vencido_{producto_id}', 0))

                # Verificar si los tres campos son iguales a 0
                if sugerido == 0 and stock_operacional == 0 and vencido == 0:
                    continue  # No crear el detalle si todos los campos son 0

                costo += producto.precio * sugerido

                # Crear el detalle del pedido asociado a la cabecera
                DetallePedido.objects.create(
                    cabecera_pedido=cabecera_pedido,
                    producto=producto,
                    sugerido=sugerido,
                    stock_operacional=stock_operacional,
                    vencido=vencido
                )

        cabecera_pedido.costo_total = costo
        cabecera_pedido.save()

        return redirect('/pedidos')  # Redirigir a la vista después de guardar el pedido

    else:
        detalle_form = DetallePedidoForm()

    return render(request, 'pedidos/crear_pedido.html', {'productos': productos, 'detalle_form': detalle_form})

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(CabeceraPedido, pk=pedido_id)
    detalles =  DetallePedido.objects.filter(cabecera_pedido=pedido)
    productos = Producto.objects.all()
    return render(request, 'pedidos/detalles_pedido.html', {'detalles': detalles , 'cabecera' :pedido, 'productos':productos })