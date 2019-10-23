from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'control/dashboard.html')

# ------------------------------------

from django.views import generic
from .models import *
from .forms import *

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

# ------------------------------------

class ProductoListView(generic.ListView):
    model = Producto

class ProductoDetailView(generic.DetailView):
    model = Producto

# ------------------------------------

class PedidoListView(generic.ListView):
    model = Pedido

    def get_queryset(self):

        qs1 = Pedido.objects.all() #your first qs
        t2 = Pedido.objects.filter(estado='Pendiente')
        
        return qs1

class PedidoDetailView(generic.DetailView):
    model = Pedido

def fetch_price(request, pk):
    product = get_object_or_404(Producto, pk=pk)

    if request.method=='GET':
        price = product.precio

        return HttpResponse(str(price), content_type="text/plain")

# ------------------------------------

class VentaListView(generic.ListView):
    model = Venta

class VentaDetailView(generic.DetailView):
    model = Venta

def fetch_total(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method=='GET':
        total = pedido.total

        return HttpResponse(str(total), content_type="text/plain")

# ------------------------------------

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

@csrf_exempt   
def estado_pedido(request, pk):
    obj = Pedido.objects.get(pk=pk)
    obj.estado = "Cocinado"
    obj.save()

    return redirect('/control/pedidos')
    # return render(request, 'control/venta_list.html')

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

from django.db import transaction

class PedidoCreate(CreateView):
    model = Pedido
    # fields = '__all__'
    form_class = PedidoForm
    success_url = reverse_lazy('control:pedidos')
    template_name_suffix = '_crear'

    def get_context_data(self, **kwargs):
        data = super(PedidoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['detalle'] = DetallePedidoFormSet(self.request.POST)
        else:
            data['detalle'] = DetallePedidoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalle = context['detalle']
        with transaction.atomic():
            self.object = form.save()

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

    def get_context_data(self, **kwargs):
        context = super(PedidoUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['detalle'] = DetallePedidoFormSet(self.request.POST, instance=self.object)
            context['detalle'].full_clean()
        else:
            context['detalle'] = DetallePedidoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        detalle = context['detalle']
        with transaction.atomic():
            self.object = form.save()
            
        if detalle.is_valid():
            response = super().form_valid(form)
            detalle.instance = self.object
            detalle.save()
            return response
        else:
            return super(PedidoUpdate, self).form_valid(form)

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

class VentaCreate(CreateView):
    model = Venta
    # fields = '__all__'
    form_class = VentaForm
    # success_url = reverse_lazy('control:ventas')
    template_name_suffix = '_crear'

    @method_decorator(permission_required('control.add_venta',reverse_lazy('control:ventas')))
    def dispatch(self, *args, **kwargs):
            return super(VentaCreate, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('control:venta-detail',  kwargs={'pk':self.object.pk})

class VentaDelete(DeleteView):
    model = Venta
    success_url = reverse_lazy('control:ventas')
    template_name_suffix = '_eliminar'

    @method_decorator(permission_required('control.delete_venta',reverse_lazy('control:ventas')))
    def dispatch(self, *args, **kwargs):
            return super(VentaDelete, self).dispatch(*args, **kwargs)

# ------------------------------------