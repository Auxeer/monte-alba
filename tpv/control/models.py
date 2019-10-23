from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from datetime import datetime, date

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Producto(models.Model):
    producto = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    LOAN_CATEGORIA = (
        ('p', 'Platillo'),
        ('b', 'Bebida'),
    )

    categoria = models.CharField(max_length=1, choices=LOAN_CATEGORIA, blank=False, default='p', help_text='Categoria del Producto')
    imagen = models.ImageField(upload_to='photos')

    def get_absolute_url(self):
        return reverse('control:producto-detail', args=[str(self.id)])

    def __str__(self):
        return self.producto

class Pedido(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateField(default=datetime.now, null=True, blank=True)
    estado = models.CharField(max_length=20, default='Pendiente')
    cliente = models.CharField(max_length=50, default='Agregue Cliente')
    observacion = models.CharField(max_length=200, null=False, default='Ninguna')

    def get_absolute_url(self):
        return reverse('control:pedido-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.id) + " | " + str(self.cliente)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, db_column='pedido_id', on_delete=models.SET_NULL, null=True)
    producto = models.ForeignKey(Producto, db_column='producto_id', on_delete=models.SET_NULL, null=True, verbose_name='Productos')

    cantidad = models.DecimalField(max_digits=10, decimal_places=0, default=1)
    precio = models.CharField(max_length=200, default=0)

class Venta(models.Model):
    fecha = models.DateField(default=datetime.now, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, db_column='pedido_id', on_delete=models.SET_NULL, null=True)
    total = models.CharField(max_length=200, default=0)
    cliente = models.CharField(max_length=100, default='Consumidor Final')
    nit = models.CharField(max_length=10, default='C.F')

    def get_absolute_url(self):
        return reverse('control:venta-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.id) + " | " + str(self.cliente)
