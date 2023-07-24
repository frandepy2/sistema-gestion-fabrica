from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def is_cliente(user):
    return user.groups.filter(name='CLIENTE').exists()

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

# Create your views here.
@login_required
@user_passes_test(is_admin, login_url='/dashboard/cliente/')
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})

@login_required
@user_passes_test(is_admin, login_url='/dashboard/cliente/')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='/dashboard/cliente/')
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

@login_required
@user_passes_test(is_admin, login_url='/dashboard/cliente/')
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})