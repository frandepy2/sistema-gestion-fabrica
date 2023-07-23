from django.contrib import admin
from .models import CabeceraPedido, DetallePedido

# Register your models here.

@admin.register(CabeceraPedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_pedido', 'cliente', 'costo_total', 'estado')

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cabecera_pedido', 'stock_operacional', 'sugerido','vencido')