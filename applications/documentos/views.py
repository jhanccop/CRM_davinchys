from datetime import date, timedelta

from django.shortcuts import render

from applications.users.mixins import (
  AdminPermisoMixin,
  AdminClientsPermisoMixin, # Adquisiciones, Finanzas, Tesoreria, contabilidad y administrador
  ContabilidadPermisoMixin,
  ComprasContabilidadPermisoMixin
)

from django.urls import reverse_lazy, reverse

from django.views.generic import (
    DetailView,
    DeleteView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    View
)

from .models import (
  FinancialDocuments,
  OthersDocuments
)

from .forms import (
  FinancialDocumentsForm,
  OthersDocumentsForm
)

# ================= DOCUMENTACION FINANCIEROS ========================
class FinancialDocumentsListView(AdminClientsPermisoMixin,ListView):
  template_name = "documentos/documento-financiero-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    compania_id = self.request.session.get('compania_id')
    selectedType = self.request.GET.get("DocKword", '')

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    if selectedType == "Todo" or selectedType == None or selectedType =="" :
      selectedType = 5

    documentation = FinancialDocuments.objects.ListaDocumentosPorTipo(
      intervalo = intervalDate,
      tipo = int(selectedType),
      compania_id = compania_id
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["selected"] = selectedType
    payload["documentation"] = documentation
    
    return payload

class FinancialDocumentsCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "documentos/documento-financiero-nuevo.html"
  model = FinancialDocuments
  form_class = FinancialDocumentsForm
  success_url = reverse_lazy('documentos_app:documento-financiero-lista')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['request'] = self.request
    return kwargs
  
class FinancialDocumentsEditView(AdminClientsPermisoMixin,UpdateView):
  template_name = "documentos/documento-financiero-editar.html"
  model = FinancialDocuments
  form_class = FinancialDocumentsForm
  success_url = reverse_lazy('documentos_app:documento-financiero-lista')

class DocumentacionDetailView(AdminClientsPermisoMixin,ListView):
  template_name = "documentos/documento-financiero-detalle.html"
  context_object_name = 'doc'
  
  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    payload = {}
    document = FinancialDocuments.objects.DocumentosPorId(id = int(pk))
    payload["document"] = document
    return payload
  
class FinancialDocumentsDeleteView(AdminClientsPermisoMixin,DeleteView):
  template_name = "documentos/documento-financiero-eliminar.html"
  model = FinancialDocuments
  success_url = reverse_lazy('documentos_app:documento-financiero-lista')


# ================= DOCUMENTACION GENERICOS ========================
class OthersDocumentsListView(AdminClientsPermisoMixin,ListView):
  template_name = "documentos/documento-generico-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    compania_id = self.request.session.get('compania_id')
    selectedType = self.request.GET.get("DocKword", '')

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    if selectedType == "Todo" or selectedType == None or selectedType =="" :
      selectedType = 5

    documentation = OthersDocuments.objects.ListaDocumentosPorTipo(
      intervalo = intervalDate,
      tipo = int(selectedType),
      compania_id = compania_id
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["selected"] = selectedType
    payload["documentation"] = documentation
    
    return payload

class OthersDocumentsCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "documentos/documento-generico-nuevo.html"
  model = OthersDocuments
  form_class = OthersDocumentsForm
  success_url = reverse_lazy('documentos_app:documento-generico-lista')
  
class OthersDocumentsEditView(AdminClientsPermisoMixin,UpdateView):
  template_name = "documentos/documento-generico-editar.html"
  model = OthersDocuments
  form_class = OthersDocumentsForm
  success_url = reverse_lazy('documentos_app:documento-generico-lista')

class OthersDocumentsDetailView(AdminClientsPermisoMixin,ListView):
  template_name = "documentos/documento-generico-detalle.html"
  context_object_name = 'doc'
  
  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    payload = {}
    document = OthersDocumentsForm.objects.DocumentosPorId(id = int(pk))
    payload["document"] = document
    return payload
  
class OthersDocumentsDeleteView(AdminClientsPermisoMixin,DeleteView):
  template_name = "documentos/documento-generico-eliminar.html"
  model = OthersDocuments
  success_url = reverse_lazy('documentos_app:documento-generico-lista')
