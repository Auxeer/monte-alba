from django.contrib import admin
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import *

# Register your models here.
admin.site.register(Producto)

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido

class PedidoAdmin(admin.ModelAdmin):
    inlines = (DetallePedidoInline,)
    readonly_fields=('estado',)

admin.site.register(Pedido, PedidoAdmin)

