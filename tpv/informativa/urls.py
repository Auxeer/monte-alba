from django.urls import path
from django.conf import settings
from . import views

app_name = 'informativa'
urlpatterns = [
    path('', views.index1, name='index'),    
    path('informativa/contacto', views.contacto, name='contacto'),
    path('informativa/about', views.about, name='about'),
]

urlpatterns += [
    path('producto/', views.ProductosListView.as_view(), name='producto-list'),
]

