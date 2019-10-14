from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'control/dashboard.html')

# ------------------------------------

from django.views import generic
from .models import *
from .forms import *

# ------------------------------------

class ProductoListView(generic.ListView):
    model = Producto
    # paginate_by = 10

class ProductoDetailView(generic.DetailView):
    model = Producto

# ------------------------------------

class PedidoListView(generic.ListView):
    model = Pedido
    # paginate_by = 10

class PedidoDetailView(generic.DetailView):
    model = Pedido

def load_precios(request):
    producto_id = request.GET.get('producto')
    precios = Producto.objects.get(producto_id=producto_id)
    return render(request, 'control/precios_list_options.html', {'precios': precios})

# ------------------------------------

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

# ------------------------------------

class ProductoCreate(CreateView):
    model = Producto
    # fields = '__all__'
    form_class = ProductoForm
    success_url = reverse_lazy('control:productos')
    template_name_suffix = '_crear'

    @method_decorator(permission_required('control.add_producto',reverse_lazy('control:productos')))
    def dispatch(self, *args, **kwargs):
            return super(ProductoCreate, self).dispatch(*args, **kwargs)

class ProductoUpdate(UpdateView):
    model = Producto
    # fields = '__all__'
    form_class = ProductoForm
    template_name_suffix = '_crear'

    @method_decorator(permission_required('control.change_producto',reverse_lazy('control:productos')))
    def dispatch(self, *args, **kwargs):
            return super(ProductoUpdate, self).dispatch(*args, **kwargs)

class ProductoDelete(DeleteView):
    model = Producto
    success_url = reverse_lazy('control:productos')
    template_name_suffix = '_eliminar'

    @method_decorator(permission_required('control.delete_producto',reverse_lazy('control:productos')))
    def dispatch(self, *args, **kwargs):
            return super(ProductoDelete, self).dispatch(*args, **kwargs)

# ------------------------------------

class PedidoCreate(CreateView):
    model = Pedido
    # fields = '__all__'
    form_class = PedidoForm
    success_url = reverse_lazy('control:pedidos')
    template_name_suffix = '_crear'

    def get_context_data(self, **kwargs):
        context = super(PedidoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['detalle'] = DetallePedidoFormSet(self.request.POST)
        else:
            context['detalle'] = DetallePedidoFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalle = context['detalle']
        if detalle.is_valid():
            response = super().form_valid(form)
            detalle.instance = self.object
            detalle.save()
            return response
        else:           
            return super(PedidoCreate, self).form_valid(form)

    @method_decorator(permission_required('control.add_pedido',reverse_lazy('control:pedidos')))
    def dispatch(self, *args, **kwargs):
            return super(PedidoCreate, self).dispatch(*args, **kwargs)

class PedidoUpdate(UpdateView):
    model = Pedido
    # fields = '__all__'
    form_class = PedidoForm
    template_name_suffix = '_crear'

    @method_decorator(permission_required('control.change_pedido',reverse_lazy('control:pedidos')))
    def dispatch(self, *args, **kwargs):
            return super(PedidoUpdate, self).dispatch(*args, **kwargs)

class PedidoDelete(DeleteView):
    model = Pedido
    success_url = reverse_lazy('control:pedidos')
    template_name_suffix = '_eliminar'

    @method_decorator(permission_required('control.delete_pedido',reverse_lazy('control:pedidos')))
    def dispatch(self, *args, **kwargs):
            return super(PedidoDelete, self).dispatch(*args, **kwargs)

# ------------------------------------