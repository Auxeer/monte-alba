from django.urls import path

from . import views

app_name = 'control'
urlpatterns = [
    path('', views.index, name='index')
]

urlpatterns += [
    path('productos/', views.ProductoListView.as_view(), name='productos'),
    path('producto/<int:pk>', views.ProductoDetailView.as_view(), name='producto-detail'),
    
    path('pedidos/', views.PedidoListView.as_view(), name='pedidos'),
    path('pedido/<int:pk>', views.PedidoDetailView.as_view(), name='pedido-detail'),

    path('ventas/', views.VentaListView.as_view(), name='ventas'),
    path('venta/<int:pk>', views.VentaDetailView.as_view(), name='venta-detail'),
]

# Add URLConf to create, update, and delete authors
urlpatterns += [
    path('producto/create/', views.ProductoCreate.as_view(), name='producto_create'),
    path('producto/<int:pk>/update/', views.ProductoUpdate.as_view(), name='producto_update'),
    path('producto/<int:pk>/delete/', views.ProductoDelete.as_view(), name='producto_delete'),

    path('pedido/create/', views.PedidoCreate.as_view(), name='pedido_create'),
    path('pedido/<int:pk>/update/', views.PedidoUpdate.as_view(), name='pedido_update'),
    path('pedido/<int:pk>/delete/', views.PedidoDelete.as_view(), name='pedido_delete'),
    path('price/<int:pk>', views.fetch_price, name='fetch_price'),

    path('pedido/create/', views.PedidoCreate.as_view(), name='pedido_create'),
    path('pedido/<int:pk>/update/', views.PedidoUpdate.as_view(), name='pedido_update'),
    path('pedido/<int:pk>/delete/', views.PedidoDelete.as_view(), name='pedido_delete'),
    path('price/<int:pk>', views.fetch_price, name='fetch_price'),

    path('venta/create/', views.VentaCreate.as_view(), name='venta_create'),
    path('venta/<int:pk>/delete/', views.VentaDelete.as_view(), name='venta_delete'),
    path('total/<int:pk>', views.fetch_total, name='fetch_total'),
    path('estado/<int:pk>', views.estado_pedido, name='estado_pedido'),
    
]
