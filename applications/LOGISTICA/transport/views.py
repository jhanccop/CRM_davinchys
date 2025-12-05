from datetime import date, timedelta
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView
)

from applications.users.mixins import (
  LogisticaMixin,
  AdminClientsPermisoMixin
)

from applications.LOGISTICA.transport.models import Container
from .forms import ContainerForm


# =========================== CONTAINERS ===========================
class ContainerListView(LogisticaMixin, ListView):
  template_name = "LOGISTICA/transport/container-lista.html"
  context_object_name = 'containers'

  def get_queryset(self,**kwargs):
    compania_id = self.request.user.company.id
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
        intervalDate = str(date.today() - timedelta(days = 90)) + " to " + str(date.today())

    container = Container.objects.ListaContenedoresPorRuc(intervalo = intervalDate, idTin = compania_id)
    
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["listContainer"] = container
    return payload

class ContainerCreateView(LogisticaMixin, CreateView):
    template_name = "LOGISTICA/transport/form-container.html"
    model = Container
    form_class = ContainerForm
    success_url = reverse_lazy('logistica_app:lista-contenedores')
  
class ContainerUpdateView(LogisticaMixin, UpdateView):
    template_name = "LOGISTICA/transport/form-container.html"
    model = Container
    form_class = ContainerForm
    success_url = reverse_lazy('logistica_app:lista-contenedores')

    #def get_context_data(self,**kwargs):
    #    pk = self.kwargs['pk']
    #    context = super().get_context_data(**kwargs)
    #    context['pk'] = pk
    #    return context