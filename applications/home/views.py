from datetime import date, timedelta

from django.shortcuts import render
from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
)

from django.urls import reverse_lazy

# models
from applications.movimientos.models import DocumentsUploaded
from applications.cuentas.models import Account
from applications.actividades.models import Trafos
from applications.pedidos.models import PaymentRequest

# forms
from applications.actividades.forms import TrafoForm

from django.contrib.auth.mixins import LoginRequiredMixin
#
#from .functions import detalle_resumen_ventas

class HomeView(TemplateView):
    template_name = "home/home.html"
    
class QuoteView(CreateView):
    template_name = "home/quote-with-us.html"
    model = Trafos
    form_class = TrafoForm
    success_url = reverse_lazy('home_app:home')

class PanelHomeView(LoginRequiredMixin,ListView):
    template_name = "home/main.html"
    context_object_name = 'solicitudes'

    def get_queryset(self):
        userId = self.request.user
        userArea = userId.position
        payload = {}
        payload["nRequest"] = PaymentRequest.objects.RequerimientosPendientes(area=userArea)
        return payload

        
