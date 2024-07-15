from datetime import date, timedelta
#Django
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import (
    View,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView
)

from applications.users.mixins import (
  TrabajadorComprasProducciónPermisoMixin
)

from applications.users.models import User

from .models import (
  PaymentRequest
)
from .forms import (
  PaymentRequestForm,
  ApprovePaymentRequestForm1
)

# ================ SOLICITUDES ==================
class MyRequirementsListView(ListView):
    template_name = "pedidos/mi-lista-solicitudes.html"
    context_object_name = 'solicitudes'
    
    def get_queryset(self):
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 30)) + " to " + str(date.today())
            print(intervalDate)

        userId = self.request.user
        userArea = userId.position
        payload = {}
            
        payload["nRequest"] = PaymentRequest.objects.RequerimientosPendientes(area=userArea)
        
        payload["intervalDate"] = intervalDate
        payload["ordenes"] = PaymentRequest.objects.MiListarPorIntervalo(user=userId,interval = intervalDate)
        return payload
    
class RequirementsCreateView(CreateView):
    template_name = "pedidos/nueva-solicitud.html"
    model = PaymentRequest
    form_class = PaymentRequestForm
    success_url = reverse_lazy('pedidos_app:mi-lista-solicitudes')

    def form_valid(self, form):
        response = super().form_valid(form)
        # You can add additional processing here if needed
        return response

class RequirementsUpdateView(UpdateView):
    template_name = "pedidos/editar-solicitud.html"
    model = PaymentRequest
    form_class = PaymentRequestForm
    success_url = reverse_lazy('pedidos_app:mi-lista-solicitudes')

    def form_valid(self, form):
        response = super().form_valid(form)
        # You can add additional processing here if needed
        return response

class RequirementsDeleteView(DeleteView):
    template_name = "pedidos/eliminar-solicitud.html"
    model = PaymentRequest
    success_url = reverse_lazy('pedidos_app:mi-lista-solicitudes')

class RequirementsApproveListView(ListView):
    template_name = "pedidos/solicitudes-por-aprobar.html"
    context_object_name = 'solicitudes'
    
    def get_queryset(self):
        user_selected = self.request.GET.get("UserKword", '')
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 30)) + " to " + str(date.today())
            print(intervalDate)

        if user_selected =="" or user_selected == None:
            user_selected = "all"
            uselect = "todos"
        else:
            uselect = User.objects.usuarios_sistema_id(id=int(user_selected))
        payload = {}
        payload["intervalDate"] = intervalDate
        payload["user_selected"] = uselect
        payload["users"] = User.objects.usuarios_sistema_all()
        payload["ordenes"] = PaymentRequest.objects.ListarAprobarPorIntervalo(area=self.request.user.position,user_selected=user_selected,interval = intervalDate)
        return payload

class ApproveRequestUpdateView1(UpdateView):
    template_name = "pedidos/aprobar-solicitud-1.html"
    model = PaymentRequest
    form_class = ApprovePaymentRequestForm1
    success_url = reverse_lazy('pedidos_app:solicitudes-por-aprobar')

