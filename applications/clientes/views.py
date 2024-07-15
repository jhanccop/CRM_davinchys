from django.shortcuts import render

from django.urls import reverse_lazy

from applications.users.mixins import ComprasProducciónPermisoMixin

from django.views.generic import (
    View,
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)

from .models import Cliente

from .forms import ClientForm

class ClientListView(ComprasProducciónPermisoMixin,ListView):
    template_name = "clientes/lista_clientes.html"
    context_object_name = 'clientes'
    model = Cliente

class ClientCreateView(ComprasProducciónPermisoMixin,CreateView):
    template_name = "clientes/crear_clientes.html"
    model = Cliente
    form_class = ClientForm
    success_url = reverse_lazy('clients_app:cliente-lista')

class ClientDeleteView(ComprasProducciónPermisoMixin,DeleteView):
    template_name = "clientes/eliminar_clientes.html"
    model = Cliente
    success_url = reverse_lazy('clients_app:cliente-lista')

class ClientUpdateView(ComprasProducciónPermisoMixin,UpdateView):
    template_name = "clientes/editar_clientes.html"
    model = Cliente
    form_class = ClientForm
    success_url = reverse_lazy('clients_app:cliente-lista')
