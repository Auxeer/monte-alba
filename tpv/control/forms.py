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
import datetime

class PedidoForm(ModelForm):
    fecha = forms.DateTimeField(initial=datetime.datetime.now, 
        widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
            super(PedidoForm, self).__init__(*args, **kwargs)
            self.fields['total'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['fecha'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['estado'].widget.attrs\
            .update({
                'class': 'form-control'
            })  
            self.fields['cliente'].widget.attrs\
            .update({
                'class': 'form-control'
            }) 
            self.fields['observacion'].widget.attrs\
            .update({
                'class': 'form-control'
            }) 
            self.fields['fecha'].widget.attrs['readonly'] = True 
                           

    class Meta:
        model = Pedido
        fields = '__all__'

class DetallePedidoForm(ModelForm):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(),empty_label="Seleccione el Producto a Agregar")

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
            # self.fields['producto'].widget.attrs['required'] = True 
            self.fields['cantidad'].widget.attrs['min'] = 1 
            self.fields['cantidad'].widget.attrs['required'] = True  
            self.fields['precio'].widget.attrs['min'] = 1  
            self.fields['precio'].widget.attrs['readonly'] = True           

    class Meta:
        model = DetallePedido
        exclude = ()

DetallePedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=1, can_delete=True)

# ------------------------------------

class VentaForm(ModelForm):
    pedido = forms.ModelChoiceField(queryset=Pedido.objects.all(),empty_label="Seleccione el Numero del Pedido a Cancelar")
    fecha = forms.DateTimeField(initial=datetime.datetime.now, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
            super(VentaForm, self).__init__(*args, **kwargs)
            self.fields['fecha'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['pedido'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['total'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['cliente'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['nit'].widget.attrs\
            .update({
                'class': 'form-control'
            })
            self.fields['pedido'].widget.attrs['required'] = True 
            self.fields['fecha'].widget.attrs['readonly'] = True
            self.fields['total'].widget.attrs['readonly'] = True
            self.fields['pedido'].queryset = Pedido.objects.filter(estado='Listo')

    class Meta:
        model = Venta
        fields = '__all__'

# ------------------------------------