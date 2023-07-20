from django.db import models
from enum import Enum

class EstadoPedido(Enum):
    EN_PROCESO = 'EN_PROCESO'
    ENVIADO = 'ENVIADO'
    CONFIRMADO = 'CONFIRMADO'
    COMPLETADO = 'COMPLETADO'


# Create your models here.
class CabeceraPedido(models.Model):
    fecha_pedido = models.DateField()
    cliente = models.CharField(max_length=100)

    ESTADO_CHOICES = [
        (EstadoPedido.EN_PROCESO, 'EN_PROCESO'),
        (EstadoPedido.ENVIADO, 'ENVIADO'),
        (EstadoPedido.CONFIRMADO, 'CONFIRMADO'),
        (EstadoPedido.CONFIRMADO, 'COMPLETADO'),
    ]

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=EstadoPedido.EN_PROCESO,
    )

class DetallePedido(models.Model):
    cabecera_pedido = models.ForeignKey(CabeceraPedido, on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Pedido {self.pk}"
