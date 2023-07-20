# pedidos/forms.py

from django import forms
from .models import CabeceraPedido, DetallePedido

class CabeceraPedidoForm(forms.ModelForm):
    class Meta:
        model = CabeceraPedido
        fields = '__all__'

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'