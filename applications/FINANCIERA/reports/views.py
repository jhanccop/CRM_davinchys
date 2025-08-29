from datetime import date, timedelta

from applications.users.mixins import (
  FinanzasMixin,
)

from django.views.generic import (
    DetailView,
    DeleteView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    View
)

from applications.FINANCIERA.movimientosBancarios.models import (
  DocumentsUploaded,
  BankMovements,
  Conciliation
)

from applications.cuentas.models import Account

# ================= REPORTES ========================
class ListAccountReport(FinanzasMixin,ListView):
  template_name = "FINANCIERA/dashboard/reporte-de-cuentas.html"
  context_object_name = 'cuentas'
  
  def get_queryset(self):
    idCompany=self.request.user.company
    payload = {}
    payload['cuenta'] = Account.objects.CuentasByCajaChica(cajaChica = False, idCompany = idCompany)
    return payload
  
class AccountReportDetail(FinanzasMixin,ListView):
  template_name = "FINANCIERA/dashboard/reporte-de-cuentas-detalle.html"
  context_object_name = 'cuenta'

  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())

    payload = {}
    payload["intervalDate"] = intervalDate
    #payload["datos"] = Transactions.objects.ReportePorCuenta(intervalo = intervalDate, cuenta = int(pk)) # 1:dolares
    payload["array"] = BankMovements.objects.ListaMovimientosPorCuenta(intervalo = intervalDate, cuenta = int(pk))
    payload["resumen"] = BankMovements.objects.ResumenMovimientosPorCuenta(intervalo = intervalDate, cuenta = int(pk))
    payload["conciliacion"] = BankMovements.objects.ConciliacionPorMontosPorCuentaPorIntervalo(intervalo = intervalDate, cuenta = int(pk))
    payload["bankMovements"] = BankMovements.objects.ListaMovimientosPorCuenta(intervalo = intervalDate, cuenta = int(pk))
    return payload
  