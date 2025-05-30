#
from django.urls import path
from . import views

app_name = "clients_app"

urlpatterns = [
    path(
        'clients/lista/', 
        views.ClientListView.as_view(),
        name='cliente-lista',
    ),
    path(
        'clients/agregar_cliente/', 
        views.ClientCreateView.as_view(),
        name='cliente-add',
    ),
    path(
        'clients/editar_cliente/<pk>/', 
        views.ClientUpdateView.as_view(),
        name='cliente-editar',
    ),
    path(
        'clients/eliminar_cliente/<pk>/', 
        views.ClientDeleteView.as_view(),
        name='cliente-eliminar',
    ),
    path(
        'clients/buscar-ruc/', 
        views.buscar_ruc_sunat,
        name='buscar_ruc',
    ),

    
]