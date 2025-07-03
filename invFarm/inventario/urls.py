from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView,
    registrar_entrada, registrar_salida,
    lista_proveedores, crear_proveedor,
    lista_ordenes_compra, crear_orden_compra,
    lista_proyectos, crear_proyecto,
    reporte_inventario, panel_gestion_inventario,
    ProductoListAPIView, ProductoDetailAPIView,
    registro_usuario, login_usuario, usuario_con_grupo_required,
    recuperar_password
)

urlpatterns = [
    # Panel principal de gestión
    path('panel/', usuario_con_grupo_required(panel_gestion_inventario), name='panel_gestion_inventario'),

    # Productos
    path('', usuario_con_grupo_required(ProductoListView.as_view()), name='producto_list'),
    path('nuevo/', usuario_con_grupo_required(ProductoCreateView.as_view()), name='producto_create'),
    path('<int:pk>/editar/', usuario_con_grupo_required(ProductoUpdateView.as_view()), name='producto_update'),
    path('<int:pk>/eliminar/', usuario_con_grupo_required(ProductoDeleteView.as_view()), name='producto_delete'),
    path('producto/<int:producto_id>/entrada/', usuario_con_grupo_required(registrar_entrada), name='registrar_entrada'),
    path('producto/<int:producto_id>/salida/', usuario_con_grupo_required(registrar_salida), name='registrar_salida'),

    # Proveedores
    path('proveedores/', usuario_con_grupo_required(lista_proveedores), name='lista_proveedores'),
    path('proveedores/nuevo/', usuario_con_grupo_required(crear_proveedor), name='crear_proveedor'),

    # Órdenes de compra
    path('ordenes_compra/', usuario_con_grupo_required(lista_ordenes_compra), name='lista_ordenes_compra'),
    path('ordenes_compra/nueva/', usuario_con_grupo_required(crear_orden_compra), name='crear_orden_compra'),

    # Proyectos
    path('proyectos/', usuario_con_grupo_required(lista_proyectos), name='lista_proyectos'),
    path('proyectos/nuevo/', usuario_con_grupo_required(crear_proyecto), name='crear_proyecto'),

    # Reportes
    path('reporte_inventario/', usuario_con_grupo_required(reporte_inventario), name='reporte_inventario'),

    # API
    path('api/productos/', usuario_con_grupo_required(ProductoListAPIView.as_view()), name='api_productos_list'),
    path('api/productos/<int:pk>/', usuario_con_grupo_required(ProductoDetailAPIView.as_view()), name='api_productos_detail'),

    # Autenticación (sin restricción)
    path('registro/', registro_usuario, name='registro_usuario'),
    path('login/', login_usuario, name='login_usuario'),
    path('recuperar-password/', recuperar_password, name='recuperar_password'),
]