import datetime
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout

from pedidos.models import CabeceraPedido, EstadoPedido

def is_cliente(user):
    return user.groups.filter(name='CLIENTE').exists()

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def calcular_rango():
    # Obtener la fecha actual
    fecha_actual = datetime.date.today()

    # Calcular la fecha de inicio de la semana actual (lunes)
    inicio_semana = fecha_actual - datetime.timedelta(days=fecha_actual.weekday())

    # Calcular la fecha de finalización de la semana actual (domingo)
    fin_semana = inicio_semana + datetime.timedelta(days=6)

    datos = {
        "inicio_semana" : inicio_semana,
        "fin_semana": fin_semana,
    }

    return datos

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
    datos = calcular_rango()
    pedidos = CabeceraPedido.objects.filter(cliente=request.user).exclude(estado=EstadoPedido.COMPLETADO.name)
    completados = CabeceraPedido.objects.filter(cliente=request.user, estado = EstadoPedido.COMPLETADO.name, fecha_pedido__range=(datos.get('inicio_semana'),datos.get('fin_semana')))
    # Aquí puedes agregar la lógica para obtener los datos del dashboard desde la base de datos u otras fuentes
    data = {
        'title': 'Dashboard Cliente',
        'subtitle': 'Bienvenido al dashboard para clientes',
        'pedidos': pedidos,
        'completados': completados,
        # Puedes agregar más datos aquí según tus necesidades
    }
    return render(request, 'dashboard.html', data)

@user_passes_test(is_cliente, login_url='/login/')
def dashboard_cliente(request):
    datos = calcular_rango()
    pedidos = CabeceraPedido.objects.filter(cliente=request.user).exclude(estado=EstadoPedido.COMPLETADO.name)
    completados = CabeceraPedido.objects.filter(cliente=request.user, estado = EstadoPedido.COMPLETADO.name, fecha_pedido__range=(datos.get('inicio_semana'),datos.get('fin_semana')))
    data = {
        'title': 'Dashboard Cliente',
        'subtitle': 'Bienvenido al dashboard para clientes',
        'pedidos': pedidos,
        'completados': completados,
    }
    return render(request, 'dashboard_cliente.html', data)

@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualizar la sesión del usuario para evitar el cierre de sesión
            return redirect('/dashboard/')  # Reemplaza 'ruta_de_la_vista_exitosa' con la URL de la vista a la que deseas redirigir después de cambiar la contraseña
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_contrasena.html', {'form': form})  # Reemplaza 'ruta_del_template.html' con la ruta de tu template correspondiente

def logout_view(request):
    logout(request)
    return redirect('/login')