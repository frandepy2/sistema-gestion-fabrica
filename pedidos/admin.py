from django.contrib import admin
from .models import CabeceraPedido, DetallePedido

# Register your models here.

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

@admin.register(CabeceraPedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_pedido', 'cliente', 'costo_total', 'estado')
    inlines = [DetallePedidoInline]

