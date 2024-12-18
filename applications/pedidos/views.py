from datetime import date, timedelta
#Django
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, redirect

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
from django.contrib.auth.mixins import LoginRequiredMixin

from applications.users.models import User

from .models import (
  PaymentRequest,
  RequestList
)
from .forms import (
    ListRequestForm,
    PaymentRequestForm,
    ApprovePaymentRequestForm1,
)

# ================ SOLICITUDES ==================
class RequirementsListView(LoginRequiredMixin,ListView):
    template_name = "pedidos/listas-solicitudes.html"
    context_object_name = 'data'
    
    def get_queryset(self):
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 30)) + " to " + str(date.today())
            print(intervalDate)

        userId = self.request.user
        userArea = userId.position
        payload = {}
            
        payload["nRequest"] = RequestList.objects.ListasPendientes(area=userArea)
        
        payload["intervalDate"] = intervalDate
        #payload["ordenes"] = PaymentRequest.objects.MiListarPorIntervalo(user=userId,interval = intervalDate)
        payload["listas"] = RequestList.objects.ListasPorIntervalo(user=userId,interval = intervalDate)
        return payload

class ListDetailView(LoginRequiredMixin,ListView):
    template_name = "pedidos/detalle-lista.html"
    context_object_name = 'data'

    def get_queryset(self,**kwargs):
        pk = self.kwargs['pk']
        payload = {}
        payload["lista"] = RequestList.objects.ListaPorId(pk = pk)
        payload["solicitudes"] = PaymentRequest.objects.RequerimientosPorNombreLista(pk = pk)
        return payload

class RequirementsCreateView(LoginRequiredMixin,CreateView):
    template_name = "pedidos/nueva-solicitud.html"
    model = PaymentRequest
    form_class = PaymentRequestForm

    #success_url = reverse_lazy('pedidos_app:lista-solicitudes')
    def get_success_url(self):
        return reverse_lazy('pedidos_app:detalle-lista',kwargs={'pk': self.object.idList.id})

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']

        context = super().get_context_data(**kwargs)
        # Agregar datos adicionales al contexto
        context['lista'] = pk
        return context
    #def form_valid(self, form):
    #    response = super().form_valid(form)
    #    # You can add additional processing here if needed
    #    return response

class ListCreateView(LoginRequiredMixin,CreateView):
    template_name = "pedidos/nueva-lista.html"
    model = RequestList
    form_class = ListRequestForm

    def get_success_url(self):
        return reverse_lazy('pedidos_app:detalle-lista',kwargs={'pk': self.object.pk})

class RequirementsUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "pedidos/editar-solicitud.html"
    model = PaymentRequest
    form_class = PaymentRequestForm
    #success_url = reverse_lazy('pedidos_app:mi-lista-solicitudes')

    def form_valid(self, form):
        response = super().form_valid(form)
        # You can add additional processing here if needed
        return response

    def get_success_url(self):
        return reverse_lazy('pedidos_app:detalle-lista',kwargs={'pk': self.object.idList.id})

class RequirementsDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "pedidos/eliminar-solicitud.html"
    model = PaymentRequest
    success_url = reverse_lazy('pedidos_app:mi-lista-solicitudes')

class ListRequirementAproved(LoginRequiredMixin,ListView):
    """ lista-de-solicitudes-por-aprobar """
    template_name = "pedidos/lista-de-solicitudes-por-aprobar.html"
    context_object_name = 'data'

    def get_queryset(self):
        user_selected = self.request.GET.get("UserKword", '')
        TimeSelect = self.request.GET.get("timeKword", '')

        if TimeSelect == "" or TimeSelect == None:
            TimeSelect = "0"

        if user_selected =="" or user_selected == None:
            user_selected = "all"
            uselect = "todos"
        else:
            uselect = User.objects.usuarios_sistema_id(id=int(user_selected))
        
        payload = {}
        payload["TimeSelect"] = TimeSelect
        payload["user_selected"] = uselect
        payload["users"] = User.objects.usuarios_sistema_all()
        payload["listas"] = RequestList.objects.ListaPorAreaUsuarioTiempo(area=self.request.user.position,user_selected=user_selected,TimeSelect = TimeSelect)
        return payload

class DetailRequirementAproved(LoginRequiredMixin,ListView):
    """ Lista detalle por aprobar """
    template_name = "pedidos/detalle-lista-aprobar.html"
    context_object_name = 'data'

    def get_queryset(self,**kwargs):
        area=self.request.user.position
        pk = self.kwargs['pk']
        payload = {}
        payload["lista"] = RequestList.objects.ListaPorId(pk = pk)
        payload["solicitudes"] = PaymentRequest.objects.RequerimientosPorNombreLista(pk = pk, area = area)
        return payload

class UpdateStateList(View):
    """ VISTA PARA ACTUALIZAR ESTADO """
    def post(self, request, pk):
        list = get_object_or_404(RequestList, pk=pk)
        # Lógica para actualizar el stock (por ejemplo, incrementar)

        N = PaymentRequest.objects.RequerimientosContabilidadPorId(pk=pk)
        print(N)

        pos = self.request.user.position
        if pos == "5": # ADQUISIONES
            if N['n'] > 0:
                list.tag2 = "0"
            else:
                list.tag3 = "0"
            list.tag1 = "1"
        elif pos == "1": # CONTABILIDAD
            list.tag2 = "1"
            list.tag3 = "0"
        elif pos == "6": # FINANZAS
            list.tag3 = "1"
            list.tag4 = "0"
        elif pos == "0": # ADMINISTRADOR
            list.tag4 = "1"
        list.save()
        return redirect('pedidos_app:lista-de-solicitudes-por-aprobar')

class RequirementsApproveListView(LoginRequiredMixin,ListView):
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
        payload["historico"] = PaymentRequest.objects.ListarHistoricoPorIntervalo(area=self.request.user.position,user_selected=user_selected,interval = intervalDate)
        return payload

class ApproveRequestUpdateView1(LoginRequiredMixin,UpdateView):
    template_name = "pedidos/aprobar-solicitud-1.html"
    model = PaymentRequest
    form_class = ApprovePaymentRequestForm1
    success_url = reverse_lazy('pedidos_app:solicitudes-por-aprobar')

    def get_success_url(self):
        return reverse_lazy('pedidos_app:detalle-lista-aprobar',kwargs={'pk': self.object.idList.id})

