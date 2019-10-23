from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Venta)
def update_estado(sender, **kwargs):
    instance = kwargs['instance']

    obj = Pedido.objects.get(pk=instance.pedido.pk)
    # obj = instance.pedido Con este tambien si puede sin necesidad de lo de arriba
    obj.estado = "Finalizado"
    obj.save() 
