from datetime import date, timedelta
from django.shortcuts import render

from django.views.generic import (
    ListView,
)

from .models import (
  Container,
)

from applications.COMERCIAL.purchase.models import requirements

from applications.users.mixins import (
  LogisticaMixin,
  AdminClientsPermisoMixin
)

# ==================== REQUERIMIENTOS LOGISTICOS ====================
class LogisticRequirementListView(LogisticaMixin,ListView):
  template_name = "LOGISTICA/transport/logistica-requirement-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    #compania_id = self.request.session.get('compania_id')
    user = self.request.user

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    areaDocumentation = requirements.objects.ListaRequerimientosPorArea(
      intervalo = intervalDate,
      idArea = user.company.id
      )
    
    bossDocumentation = []

    isBoss = self.request.user.is_boss
    if isBoss:
        bossDocumentation = requirements.objects.ListaRequerimientosForBoss(
        intervalo = intervalDate,
        )

    payload = {}
    payload["intervalDate"] = intervalDate
    payload["documentation"] = areaDocumentation
    payload["allDocumentation"] = bossDocumentation
    
    return payload



# ==================== CONTENEDORES ====================
class ContainerListView(LogisticaMixin,ListView):
  template_name = "LOGISTICA/transport/lista-contenedores.html"
  context_object_name = 'data'

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