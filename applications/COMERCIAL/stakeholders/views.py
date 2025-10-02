from django.urls import reverse_lazy

from applications.users.mixins import ComercialMixin, ComercialFinanzasMixin

from django.http import HttpResponseRedirect
from django.http import JsonResponse

from django.views.generic import (
    View,
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)

from .models import client, supplier

from .forms import clientForm, supplierForm

from .services import consultar_ruc_selenium

# ============================= CLIENTES =============================
class ClientListView(ComercialFinanzasMixin,ListView):
    template_name = "COMERCIAL/stakeholders/lista_clientes.html"
    context_object_name = 'clientes'
    model = client

class ClientDetailView(ComercialFinanzasMixin,DeleteView):
    template_name = "COMERCIAL/stakeholders/cliente-detalle.html"
    context_object_name = 'clientes'
    model = client

class ClientCreateView(ComercialFinanzasMixin,CreateView):
    template_name = "COMERCIAL/stakeholders/cliente_form.html"
    model = client
    form_class = clientForm
    success_url = reverse_lazy('stakeholders_app:cliente-lista')

    def form_valid(self, form):
        self.object = form.save()
        #return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '//'))
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Empresa'
        context['btn_text'] = 'Guardar'
        return context

class ClientDeleteView(ComercialFinanzasMixin,DeleteView):
    template_name = "COMERCIAL/stakeholders/eliminar_clientes.html"
    model = client
    success_url = reverse_lazy('stakeholders_app:cliente-lista')

class ClientUpdateView(ComercialFinanzasMixin,UpdateView):
    template_name = "COMERCIAL/stakeholders/cliente_form.html"
    model = client
    form_class = clientForm
    success_url = reverse_lazy('stakeholders_app:cliente-lista')

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

# ============================= PROVEEDORES =============================

class SupplierListView(ComercialFinanzasMixin,ListView):
    template_name = "COMERCIAL/stakeholders/lista_proveedores.html"
    context_object_name = 'proveedores'
    model = supplier

class SupplierCreateView(ComercialFinanzasMixin,CreateView):
    template_name = "COMERCIAL/stakeholders/proveedor_form.html"
    model = supplier
    form_class = supplierForm
    success_url = reverse_lazy('stakeholders_app:proveedor-lista')

    def form_valid(self, form):
        self.object = form.save()
        #return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '//'))
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Crear Empresa'
        context['btn_text'] = 'Guardar'
        return context
    
class SupplierCreateViewRHE(ComercialFinanzasMixin,CreateView):
    template_name = "COMERCIAL/stakeholders/crear_proveedores.html"
    model = supplier
    form_class = supplierForm
    success_url = reverse_lazy('documentos_app:procesamiento-doc-rhe')

    def form_valid(self, form):
        self.object = form.save()
        #return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '//'))
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ruc'] = self.request.GET.get('ruc', '')
        context['razon_social'] = self.request.GET.get('razon_social', '')
        
        context['title'] = 'Crear Empresa'
        context['btn_text'] = 'Guardar'
        return context

class SupplierDeleteView(ComercialFinanzasMixin,DeleteView):
    template_name = "COMERCIAL/stakeholders/eliminar_proveedores.html"
    model = supplier
    success_url = reverse_lazy('stakeholders_app:proveedor-lista')

class SupplierUpdateView(ComercialFinanzasMixin,UpdateView):
    template_name = "COMERCIAL/stakeholders/proveedor_form.html"
    model = supplier
    form_class = supplierForm
    success_url = reverse_lazy('stakeholders_app:proveedor-lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Empresa'
        context['btn_text'] = 'Actualizar'
        return context
