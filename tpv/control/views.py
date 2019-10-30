from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@login_required(login_url='/accounts/login/')
# @staff_member_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'control/dashboard.html')

# ------------------------------------

from django.views import generic
from .models import *
from .forms import *

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

# ------------------------------------

class ProductoListView(LoginRequiredMixin, generic.ListView):
    model = Producto

    @method_decorator(permission_required('control.view_producto'))
    def dispatch(self, *args, **kwargs):
            return super(ProductoListView, self).dispatch(*args, **kwargs)

class ProductoDetailView(LoginRequiredMixin, generic.DetailView):
    model = Producto

    @method_decorator(permission_required('control.view_producto',reverse_lazy('control:productos')))
    def dispatch(self, *args, **kwargs):
            return super(ProductoDetailView, self).dispatch(*args, **kwargs)

# ------------------------------------

class PedidoListView(LoginRequiredMixin, generic.ListView):
    model = Pedido

    # def get_queryset(self):
        # qs1 = Pedido.objects.all()
        # t2 = Pedido.objects.filter(estado='Pendiente')
        
        # return qs1

    def get_context_data(self, **kwargs):
        context = super(PedidoListView, self).get_context_data(**kwargs)
        context['pendiente_list'] = Pedido.objects.filter(estado='Pendiente')
        context['pendientelistos_list'] = Pedido.objects.filter(estado='Pendiente') | Pedido.objects.filter(estado='Listo')
        return context  
    
    @method_decorator(permission_required('control.view_pedido'))
    def dispatch(self, *args, **kwargs):
            return super(PedidoListView, self).dispatch(*args, **kwargs)

class PedidoDetailView(LoginRequiredMixin, generic.DetailView):
    model = Pedido

    @method_decorator(permission_required('control.view_pedido',reverse_lazy('control:pedidos')))
    def dispatch(self, *args, **kwargs):
            return super(PedidoDetailView, self).dispatch(*args, **kwargs)

def fetch_price(request, pk):
    product = get_object_or_404(Producto, pk=pk)

    if request.method=='GET':
        price = product.precio

        return HttpResponse(str(price), content_type="text/plain")

# ------------------------------------

class VentaListView(LoginRequiredMixin, generic.ListView):
    model = Venta

    @method_decorator(permission_required('control.view_venta'))
    def dispatch(self, *args, **kwargs):
            return super(VentaListView, self).dispatch(*args, **kwargs)

class VentaDetailView(LoginRequiredMixin, generic.DetailView):
    model = Venta

    @method_decorator(permission_required('control.view_venta',reverse_lazy('control:ventas')))
    def dispatch(self, *args, **kwargs):
            return super(VentaDetailView, self).dispatch(*args, **kwargs)

def fetch_total(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method=='GET':
        total = pedido.total

        return HttpResponse(str(total), content_type="text/plain")

# ------------------------------------

@csrf_exempt   
def estado_pedido(request, pk):
    obj = Pedido.objects.get(pk=pk)
    obj.estado = "Listo"
    obj.save()

    return redirect('/control/pedidos')
    # return render(request, 'control/venta_list.html')

# ------------------------------------


# ------------------------------------

class ProductoCreate(LoginRequiredMixin, CreateView):
    model = Producto
    # fields = '__all__'
    form_class = ProductoForm
    success_url = reverse_lazy('control:productos')
    template_name_suffix = '_crear'

    @method_decorator(permission_required('control.add_producto',reverse_lazy('control:productos')))
    def dispatch(self, *args, **kwargs):
            return super(ProductoCreate, self).dispatch(*args, **kwargs)

class ProductoUpdate(LoginRequiredMixin, UpdateView):
    model = Producto
    # fields = '__all__'
    form_class = ProductoForm
    template_name_suffix = '_crear'

    @method_decorator(permission_required('control.change_producto',reverse_lazy('control:productos')))
    def dispatch(self, *args, **kwargs):
            return super(ProductoUpdate, self).dispatch(*args, **kwargs)

class ProductoDelete(LoginRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy('control:productos')
    template_name_suffix = '_eliminar'

    @method_decorator(permission_required('control.delete_producto',reverse_lazy('control:productos')))
    def dispatch(self, *args, **kwargs):
            return super(ProductoDelete, self).dispatch(*args, **kwargs)

# ------------------------------------

from django.db import transaction

class PedidoCreate(LoginRequiredMixin, CreateView):
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

class PedidoUpdate(LoginRequiredMixin, UpdateView):
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

class PedidoDelete(LoginRequiredMixin, DeleteView):
    model = Pedido
    success_url = reverse_lazy('control:pedidos')
    template_name_suffix = '_eliminar'

    @method_decorator(permission_required('control.delete_pedido',reverse_lazy('control:pedidos')))
    def dispatch(self, *args, **kwargs):
            return super(PedidoDelete, self).dispatch(*args, **kwargs)

# ------------------------------------

class VentaCreate(LoginRequiredMixin, CreateView):
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

class VentaDelete(LoginRequiredMixin, DeleteView):
    model = Venta
    success_url = reverse_lazy('control:ventas')
    template_name_suffix = '_eliminar'

    @method_decorator(permission_required('control.delete_venta',reverse_lazy('control:ventas')))
    def dispatch(self, *args, **kwargs):
            return super(VentaDelete, self).dispatch(*args, **kwargs)

# ------------------------------------