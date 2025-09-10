from django.urls import path
from . import views

app_name = "stakeholders_app"

urlpatterns = [
    # ============================ clientes ============================
    path(
        'comercial/clientes/lista/', 
        views.ClientListView.as_view(),
        name='cliente-lista',
    ),
    path(
        'comercial/clientes/agregar/', 
        views.ClientCreateView.as_view(),
        name='cliente-nuevo',
    ),
    path(
        'comercial/clientes/detalle/<pk>/', 
        views.ClientDetailView.as_view(),
        name='cliente-detalle',
    ),
    path(
        'comercial/clientes/editar_cliente/<pk>/', 
        views.ClientUpdateView.as_view(),
        name='cliente-editar',
    ),
    path(
        'comercial/clientes/eliminar_cliente/<pk>/', 
        views.ClientDeleteView.as_view(),
        name='cliente-eliminar',
    ),
    
    path(
        'comercial/buscar-ruc/', 
        views.buscar_ruc_sunat,
        name='buscar_ruc',
    ),

    # ============================ proveedores ============================
    path(
        'comercial/proveedores/lista/', 
        views.SupplierListView.as_view(),
        name='proveedor-lista',
    ),
    path(
        'comercial/proveedores/agregar/', 
        views.SupplierCreateView.as_view(),
        name='proveedor-nuevo',
    ),
    path(
        'comercial/proveedores/editar/<pk>/', 
        views.SupplierUpdateView.as_view(),
        name='proveedor-editar',
    ),
    path(
        'comercial/proveedores/eliminar/<pk>/', 
        views.SupplierDeleteView.as_view(),
        name='proveedor-eliminar',
    ),

    
]