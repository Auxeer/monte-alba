from django.shortcuts import render
from control.models import Producto

# Create your views here.

# ------------------------------------

def index1(request):
    return render(request, 'informativa/index.html')

#-------------------------------------
def about(request):
    return render(request, 'informativa/about.html')
#-------------------------------------

#-------------------------------------
def contacto(request):
    return render(request, 'informativa/contacto.html')
#-------------------------------------

from django.views import generic
from control.models import Producto

# ------------------------------------

class ProductosListView(generic.ListView):
    model = Producto
    template_name = "informativa/producto.html"
    
    def get_context_data(self, **kwargs):
        context = super(ProductosListView, self).get_context_data(**kwargs)
        context['platillos_list'] = Producto.objects.filter(categoria='p')
        context['bebidas_list'] = Producto.objects.filter(categoria='b')
        return context  
        
class ProductoDetailView(generic.DetailView):
    model = Producto
