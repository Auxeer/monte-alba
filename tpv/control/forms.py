from django import forms
from django.forms import ModelForm, inlineformset_factory

from .models import *

from django.forms import SelectDateWidget
from django.utils import timezone

# ------------------------------------

class ProductoForm(ModelForm):

    def __init__(self, *args, **kwargs):
            super(ProductoForm, self).__init__(*args, **kwargs)
            self.fields['producto'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['descripcion'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['precio'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['categoria'].widget.attrs\
            .update({
                'class': 'form-control'
            })

    class Meta:
        model = Producto
        fields = '__all__'
        
# ------------------------------------

class PedidoForm(ModelForm):

    def __init__(self, *args, **kwargs):
            super(PedidoForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'                     

    class Meta:
        model = Pedido
        fields = '__all__'
        
# ------------------------------------

class DetallePedidoForm(ModelForm):

    def __init__(self, *args, **kwargs):
            super(DetallePedidoForm, self).__init__(*args, **kwargs)
            self.fields['producto'].widget.attrs\
            .update({
                'class': 'form-control mydropdownclass'
            })
            self.fields['cantidad'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['precio'].widget.attrs\
            .update({
                'class': 'form-control mypricefield'
            })   
            self.fields['cantidad'].widget.attrs['min'] = 1 
            self.fields['cantidad'].widget.attrs['required'] = True  
            self.fields['precio'].widget.attrs['min'] = 1  
            self.fields['precio'].widget.attrs['readonly'] = True
               

    class Meta:
        model = DetallePedido
        exclude = ()

DetallePedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=1, can_delete=True)

# ------------------------------------