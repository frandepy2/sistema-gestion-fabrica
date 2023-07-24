from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from pedidos.models import CabeceraPedido, EstadoPedido

def is_cliente(user):
    return user.groups.filter(name='CLIENTE').exists()

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_admin(request.user):
                return redirect('/dashboard/')
            elif is_cliente(request.user):
                return redirect('/dashboard/cliente/')
        else:
            error_message = 'Credenciales inválidas. Inténtalo de nuevo.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

@user_passes_test(is_admin, login_url='/dashboard/cliente/')
def dashboard(request):
    # Aquí puedes agregar la lógica para obtener los datos del dashboard desde la base de datos u otras fuentes
    data = {
        'title': 'Dashboard',
        'subtitle': 'Bienvenido al dashboard',
        'data1': 100,
        'data2': 150,
        # Puedes agregar más datos aquí según tus necesidades
    }
    return render(request, 'dashboard.html', data)

@user_passes_test(is_cliente, login_url='/login/')
def dashboard_cliente(request):
    pedidos = CabeceraPedido.objects.filter(cliente=request.user, estado = EstadoPedido.EN_PROCESO.name)
    completados = CabeceraPedido.objects.filter(cliente=request.user, estado = EstadoPedido.COMPLETADO.name)
    data = {
        'title': 'Dashboard Cliente',
        'subtitle': 'Bienvenido al dashboard para clientes',
        'pedidos': pedidos,
        'completados': completados,
    }
    return render(request, 'dashboard_cliente.html', data)