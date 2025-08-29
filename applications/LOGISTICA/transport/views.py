from datetime import date, timedelta
from django.shortcuts import render

from django.views.generic import (
    ListView,
)

from .models import (
  Container,
)

from applications.users.mixins import (
  AdminPermisoMixin,
  AdminClientsPermisoMixin
)

# ==================== CONTENEDORES ====================
class ContainerListView(AdminClientsPermisoMixin,ListView):
  template_name = "LOGISTICA/transport/lista-contenedores.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    idTin = self.request.user.company

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())


    container = Container.objects.ListaContainer(
      idTin = idTin,
      intervalo = intervalDate,
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["idTin"] = idTin
    payload["contenedor"] = container
    
    return payload