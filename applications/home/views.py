from datetime import date, timedelta

from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView
)

from applications.movimientos.models import DocumentsUploaded
from applications.cuentas.models import Account

from django.contrib.auth.mixins import LoginRequiredMixin

from applications.pedidos.models import PaymentRequest
#
#from .functions import detalle_resumen_ventas

class PanelHomeView(LoginRequiredMixin,ListView):
    template_name = "home/main.html"
    context_object_name = 'solicitudes'

    def get_queryset(self):
        userId = self.request.user
        userArea = userId.position
        payload = {}
        payload["nRequest"] = PaymentRequest.objects.RequerimientosPendientes(area=userArea)
        return payload

class PanelReport(ListView):
    template_name = "home/reporte-cuentas.html"
    context_object_name = 'cuenta'

    def get_queryset(self,**kwargs):
        selectedAccount = self.request.GET.get("AccountKword", '')
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 15)) + " to " + str(date.today())

        payload = {}
        payload["intervalDate"] = intervalDate
        
        payload["listAccount"] = Account.objects.listarcuentas()

        if selectedAccount == "None" or selectedAccount == None or selectedAccount =="" :
            payload["AmountDocs"] = None
        else:
            payload["selectedAccount"] = Account.objects.CuentasById(int(selectedAccount))
            payload["AmountDocs"] = DocumentsUploaded.objects.MontosHistorico(intervalo = intervalDate, cuenta = int(selectedAccount)) # 1:dolares
        return payload

        
