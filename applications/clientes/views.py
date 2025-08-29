from django.shortcuts import render

from django.urls import reverse_lazy

from applications.users.mixins import AdminClientsPermisoMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.http import JsonResponse

from django.views.generic import (
    View,
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)

from .models import Cliente

from .forms import ClientForm

from .services import consultar_ruc_selenium

# AdminClientsPermisoMixin: Admin, Adquicisiones, Finanza, Tesoreria, Contabilidad

class ClientListView(LoginRequiredMixin,ListView):
    template_name = "clientes/lista_clientes.html"
    context_object_name = 'clientes'
    model = Cliente

class ClientCreateView(AdminClientsPermisoMixin,CreateView):
    template_name = "clientes/crear_clientes.html"
    model = Cliente
    form_class = ClientForm
    #success_url = reverse_lazy('clients_app:cliente-lista')

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '//'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Empresa'
        context['btn_text'] = 'Guardar'
        return context

class ClientDeleteView(AdminClientsPermisoMixin,DeleteView):
    template_name = "clientes/eliminar_clientes.html"
    model = Cliente
    success_url = reverse_lazy('clients_app:cliente-lista')

class ClientUpdateView(AdminClientsPermisoMixin,UpdateView):
    template_name = "clientes/editar_clientes.html"
    model = Cliente
    form_class = ClientForm
    success_url = reverse_lazy('clients_app:cliente-lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Empresa'
        context['btn_text'] = 'Actualizar'
        return context

def buscar_ruc_sunat(request):
    """Vista AJAX para buscar datos de RUC en SUNAT"""
    if request.method == 'GET':
        ruc = request.GET.get('ruc', '').strip()
        
        if not ruc:
            return JsonResponse({
                'success': False, 
                'error': 'RUC es requerido'
            })
        
        if len(ruc) != 11 or not ruc.isdigit():
            return JsonResponse({
                'success': False, 
                'error': 'RUC debe tener 11 dígitos numéricos'
            })
        
        # Consultar en SUNAT
        datos = consultar_ruc_selenium(ruc, headless=True) # no poner FALSE EN PRODUCCION
        
        if datos:
            return JsonResponse({
                'success': True,
                'data': datos
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No se encontraron datos para el RUC ingresado'
            })
    
    return JsonResponse({
        'success': False, 
        'error': 'Método no permitido'
    })



    