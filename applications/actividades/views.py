from datetime import date, timedelta
from django.shortcuts import render

from django.urls import reverse_lazy

from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView
)

from applications.users.mixins import AdminPermisoMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TrafoQuote, Projects, Commissions, DailyTasks
from applications.users.models import User

from .forms import QuoteTrafoForm, ProjectsForm, CommissionsForm, DailyTaskForm

# ======================= PROYECTOS ===========================
class ProjectsListView(LoginRequiredMixin,ListView):
    template_name = "actividades/lista-proyectos.html"
    context_object_name = 'proyecto'
    model = Projects

class ProjectsCreateView(AdminPermisoMixin, CreateView):
    template_name = "actividades/crear-proyecto.html"
    model = Projects
    form_class = ProjectsForm
    success_url = reverse_lazy('activities_app:proyecto-lista')

class ProjectsDeleteView(AdminPermisoMixin,DeleteView):
    template_name = "actividades/eliminar-proyecto.html"
    model = Projects
    success_url = reverse_lazy('activities_app:proyecto-lista')

class ProjectsUpdateView(AdminPermisoMixin,UpdateView):
    template_name = "actividades/editar-proyecto.html"
    model = Projects
    form_class = ProjectsForm
    success_url = reverse_lazy('activities_app:proyecto-lista')

# ======================= COMISIONES ===========================
class CommissionsListView(LoginRequiredMixin,ListView):
    template_name = "actividades/lista-comision.html"
    context_object_name = 'comision'
    model = Commissions

class CommissionsCreateView(AdminPermisoMixin,CreateView):
    template_name = "actividades/crear-comision.html"
    model = Commissions
    form_class = CommissionsForm
    success_url = reverse_lazy('activities_app:comision-lista')

class CommissionsDeleteView(AdminPermisoMixin,DeleteView):
    template_name = "actividades/eliminar-comision.html"
    model = Commissions
    success_url = reverse_lazy('activities_app:comision-lista')

class CommissionsUpdateView(AdminPermisoMixin,UpdateView):
    template_name = "actividades/editar-comision.html"
    model = Commissions
    form_class = CommissionsForm
    success_url = reverse_lazy('activities_app:comision-lista')

# ======================= ACTIVIDAD DIARIA ===========================
class MyDailyTaskListView(LoginRequiredMixin,ListView):
    template_name = "actividades/mi-lista-actividades-diarias.html"
    context_object_name = 'actividadesDiarias'

    def get_queryset(self):
        selected = self.request.GET.get("TypeKword", '')
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())
        
        if selected =="" or selected == None:
            selected = "3" # todo

        payload = {}
        payload["selected"] = selected
        payload["intervalDate"] = intervalDate

        if selected == "1": # horas extra
            payload["actividades"] = DailyTasks.objects.MiListarPorIntervaloHorasExtra(user=self.request.user,interval=intervalDate)
            payload["acc"] = DailyTasks.objects.MiListarPorIntervaloHorasExtraAcc(user=self.request.user,interval=intervalDate)
        else:
            payload["actividades"] = DailyTasks.objects.MiListarPorIntervalo(user=self.request.user,interval=intervalDate,type=selected)
        return payload

class DailyTaskCreateView(LoginRequiredMixin,CreateView):
    template_name = "actividades/crear-actividad-diaria.html"
    model = DailyTasks
    form_class = DailyTaskForm
    success_url = reverse_lazy('activities_app:mi-actividad-diaria-lista')

class DailyTaskDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "actividades/eliminar-actividad-diaria.html"
    model = DailyTasks
    success_url = reverse_lazy('activities_app:mi-actividad-diaria-lista')

class DailyTaskUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "actividades/editar-actividad-diaria.html"
    model = DailyTasks
    form_class = DailyTaskForm
    success_url = reverse_lazy('activities_app:mi-actividad-diaria-lista')

class DailyTaskReportView(AdminPermisoMixin,ListView):
    template_name = "actividades/reporte-actividades-diarias.html"
    context_object_name = 'actividadesDiarias'
    model = DailyTasks

    def get_queryset(self):
        userid = self.request.GET.get("UserKword", '')
        selected = self.request.GET.get("TypeKword", '')
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())
        
        if selected =="" or selected == None:
            selected = "3" # todo
        
        if userid =="" or userid == None:
            userid=self.request.user.id

        payload = {}
        payload["selected"] = selected
        payload["user_selected"] = User.objects.usuarios_sistema_id(id=int(userid))
        payload["users"] = User.objects.usuarios_sistema_all()
        payload["intervalDate"] = intervalDate

        # View admin or no
       
        if selected == "1":
            payload["actividades"]= DailyTasks.objects.MiListarPorIntervaloHorasExtra(user=int(userid),interval=intervalDate)
        else:
            payload["actividades"] = DailyTasks.objects.MiListarPorIntervalo(user=int(userid),interval=intervalDate,type=selected)
        payload["dias"] = DailyTasks.objects.MiListarPorIntervaloDias(user=int(userid),interval=intervalDate)
        payload["acc"] = DailyTasks.objects.MiListarPorIntervaloHorasExtraAcc(user=int(userid),interval=intervalDate)
        return payload
    
# ======================= PEDIDOS TRANSFORMADORES ===========================
class QuotesListView(LoginRequiredMixin,ListView):
    template_name = "actividades/lista-cotizaciones-transformadores.html"
    context_object_name = 'cotizaciones'
    
    def get_queryset(self):
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 30)) + " to " + str(date.today())
            print(intervalDate)
        
        payload = {}
        payload["intervalDate"] = intervalDate
        payload["ordenes"] = TrafoQuote.objects.ListarPorIntervalo(intervalDate)
            
        return payload

class QuotesCreateView(AdminPermisoMixin,CreateView):
    template_name = "actividades/cotizaciones-transformadores-nuevo.html"
    form_class = QuoteTrafoForm
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

class QuotesEditView(AdminPermisoMixin,UpdateView):
    template_name = "actividades/cotizaciones-transformadores-editar.html"
    model = TrafoQuote
    form_class = QuoteTrafoForm
     
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

class QuotesDeleteView(AdminPermisoMixin,DeleteView):
    model = TrafoQuote
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

class QuotesDetailView(LoginRequiredMixin,DetailView):
    template_name = "actividades/cotizaciones-transformadores-detalle.html"
    context_object_name = 'cotizacion'

    model = TrafoQuote
    
    def get_context_data(self, **kwargs):
        context = super(QuotesDetailView, self).get_context_data(**kwargs)
        pk = context["pedido"]

        #orderTrack =OrderTracking.objects.obtenerTrack(pk)
        #context["orderTrack"] = orderTrack

        #ordersRecived =OrdersRecived.objects.obtenerPagosRecibidosPorId(pk)
        #context["ordersRecived"] = ordersRecived

        #context["Supplier"] = Supplier.objects.obtenerPagosPorId(pk)
        
        
        #context["Services"] = Services.objects.obtenerPagosPorId(pk)
        #context["WorkCommission"] = WorkCommission.objects.obtenerPagosPorId(pk)
        #context["Purchases"] = Purchases.objects.obtenerPagosPorId(pk)
        #context["Taxes"] = Taxes.objects.obtenerPagosPorId(pk)

        return context

