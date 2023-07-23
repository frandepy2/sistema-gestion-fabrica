from django.db import models
from enum import Enum
from django.contrib.auth.models import User

class EstadoPedido(Enum):
    EN_PROCESO = 'EN_PROCESO'
    ENVIADO = 'ENVIADO'
    CONFIRMADO = 'CONFIRMADO'
    COMPLETADO = 'COMPLETADO'


# Create your models here.
from django.db import models

class CabeceraPedido(models.Model):
    fecha_pedido = models.DateField()
    cliente = models.ForeignKey(User, on_delete=models.PROTECT)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    ESTADO_CHOICES = [
        (EstadoPedido.EN_PROCESO, 'EN_PROCESO'),
        (EstadoPedido.ENVIADO, 'ENVIADO'),
        (EstadoPedido.CONFIRMADO, 'CONFIRMADO'),
        (EstadoPedido.COMPLETADO, 'COMPLETADO'),
    ]

    estado = models.CharField(
        max_length=100,
        choices=ESTADO_CHOICES,
        default=EstadoPedido.EN_PROCESO,
    )

    def __str__(self):
        return f"Cabecera Pedido {self.pk}"


class DetallePedido(models.Model):
    cabecera_pedido = models.ForeignKey(CabeceraPedido, on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    stock_operacional = models.PositiveIntegerField(default=0)
    sugerido = models.PositiveIntegerField(default=0)
    vencido = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Detalle Pedido {self.pk}"
