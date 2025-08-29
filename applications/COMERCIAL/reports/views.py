from datetime import date, timedelta

from applications.users.mixins import (
  ComercialMixin,
  AdminClientsPermisoMixin
)

from django.views.generic import (
    DetailView,
    DeleteView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView,
)

from applications.COMERCIAL.purchase.models import (
  requirements,
  requirementItems,
  RequestTracking,
  PettyCash,
  PettyCashItems,
  requirementsInvoice,
  requirementsQuotes
)

from applications.COMERCIAL.sales.models import (
  quotes,
)

# ==================== DASHBOARD COMERCIAL ====================
class DashboardView(ComercialMixin,ListView):
  template_name = "COMERCIAL/dashboard/dashboard-comercial.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    #compania_id = self.request.session.get('compania_id')
    user = self.request.user

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    requerimiento = requirements.objects.ListaOrdenesdeCompra(
      intervalo = intervalDate,
      )

    pedido = quotes.objects.ListaPOs(
      intervalo = intervalDate,
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["requerimientos"] = requerimiento
    payload["pedidos"] = pedido
    return payload

