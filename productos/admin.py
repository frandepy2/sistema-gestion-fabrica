from django.contrib import admin
from .models import Producto

# Register your models here.
@admin.register(Producto)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'precio')
