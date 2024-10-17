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

from applications.users.mixins import AdminPermisoMixin,ProduccionPermisoMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
  TrafoQuote,
  Trafos,
  Projects,
  Commissions,
  DailyTasks,
  EmailSent,
  TrafoTask,
  SuggestionBox
)
from applications.users.models import User

from .forms import (
  TrafoForm,
  QuoteTrafoForm,
  ProjectsForm,
  CommissionsForm,
  DailyTaskForm,
  EmailSentForm,
  TrafoTaskForm,
  SuggestionBoxForm
)
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
            selected = "2" # todo

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
            selected = "2" # todo
        
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
    
# ======================= BUZON DE SUGERENCIAS ===========================
class MySuggestionBoxListView(LoginRequiredMixin,ListView):
    template_name = "actividades/mi-buzon-de-sugerencias.html"
    context_object_name = 'buzon'
    #model = SuggestionBox

    def get_queryset(self):
        payload = {}
        payload["suggestion"] = SuggestionBox.objects.MiListaDeSugerencias(user=self.request.user)
        return payload

class SuggestionBoxCreateView(LoginRequiredMixin,CreateView):
    template_name = "actividades/crear-buzon-de-sugerencias.html"
    model = SuggestionBox
    form_class = SuggestionBoxForm
    success_url = reverse_lazy('activities_app:mi-buzon-de-sugerencias')

class SuggestionBoxUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "actividades/editar-buzon-de-sugerencias.html"
    model = SuggestionBox
    form_class = SuggestionBoxForm
    success_url = reverse_lazy('activities_app:mi-buzon-de-sugerencias')

class SuggestionBoxDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "actividades/eliminar-sugerencia.html"
    model = SuggestionBox
    success_url = reverse_lazy('activities_app:mi-buzon-de-sugerencias')
    

# ======================= COTIZACIONES TRANSFORMADORES ===========================
class QuotesListView(LoginRequiredMixin,ListView):
    template_name = "actividades/lista-cotizaciones-transformadores.html"
    context_object_name = 'cotizaciones'
    
    def get_queryset(self):
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 30)) + " to " + str(date.today())
        
        quotes = TrafoQuote.objects.ListarPorIntervalo(interval=intervalDate)
        #trafos = Trafos.objects.ListaPorCotizaciones(quotes=quotes)

        dictResult = {}
        for i in quotes:
            dictResult[i] =  Trafos.objects.ListaPorCotizaciones(quote=i.id)
        
        payload = {}
        payload["intervalDate"] = intervalDate
        payload["data"] = dictResult
            
        return payload

class QuotesCreateView(ProduccionPermisoMixin,CreateView):
    template_name = "actividades/cotizaciones-transformadores-nuevo.html"
    form_class = QuoteTrafoForm
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

class QuotesEditView(ProduccionPermisoMixin,UpdateView):
    template_name = "actividades/cotizaciones-transformadores-editar.html"
    model = TrafoQuote
    form_class = QuoteTrafoForm
     
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

class QuotesDeleteView(ProduccionPermisoMixin,DeleteView):
    template_name = "actividades/cotizaciones-transformadores-eliminar.html"
    model = TrafoQuote
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

class QuotesDetailView(LoginRequiredMixin,ListView):
    template_name = "actividades/cotizaciones-transformadores-detalle.html"
    context_object_name = 'data'

    #model = TrafoQuote

    def get_queryset(self,**kwargs):
        pk = self.kwargs['pk']
        payload = {}
        quotation = TrafoQuote.objects.CotizacionPorId(id = int(pk))
        trafos = Trafos.objects.ListaPorCotizaciones(quotation.id)
        tasks = TrafoTask.objects.ListaTareasPorCotizacion(quotation.id)
        payload["quotation"] = quotation
        payload["trafos"] = trafos
        payload["tasks"] = tasks
        return payload

class TrafoCreateView(ProduccionPermisoMixin,CreateView):
    template_name = "actividades/crear-transformador.html"
    model = Trafos
    form_class = TrafoForm
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

    def get_context_data(self, **kwargs):
        context = super(TrafoCreateView, self).get_context_data(**kwargs)
        trafoQuote = TrafoQuote.objects.get(id = self.kwargs['pk'])
        context['quotation'] = trafoQuote
        return context

class TrafoUpdateView(ProduccionPermisoMixin,UpdateView):
    template_name = "actividades/editar-transformador.html"
    model = Trafos
    form_class = TrafoForm

    def get_success_url(self, *args, **kwargs):
        #print(self.object.TrafoQuote)
        pk = self.object.idQuote.id
        return reverse_lazy('activities_app:cotizaciones-transformadores-detalle', kwargs={'pk':pk})

class TrafoDeleteView(ProduccionPermisoMixin,DeleteView):
    template_name = "actividades/eliminar-transformador.html"
    model = Trafos
    def get_success_url(self, *args, **kwargs):
        pk = self.object.idQuote.id
        return reverse_lazy('activities_app:cotizaciones-transformadores-detalle', kwargs={'pk':pk})

class TaskQuotesTrafoCreateView(ProduccionPermisoMixin,CreateView):
    template_name = "actividades/agregar-tareas-orden-transformador.html"
    model = TrafoTask
    form_class = TrafoTaskForm
    #success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

    def get_success_url(self, *args, **kwargs):
        print(self.object.idTrafoQuote)
        pk = self.object.idTrafoQuote.id
        return reverse_lazy('activities_app:cotizaciones-transformadores-detalle', kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        context = super(TaskQuotesTrafoCreateView, self).get_context_data(**kwargs)
        trafoQuote = TrafoQuote.objects.get(id = self.kwargs['pk'])
        context['quotation'] = trafoQuote
        return context
    
class TaskQuotesTrafoUpdateView(ProduccionPermisoMixin,UpdateView):
    template_name = "actividades/editar-tareas-orden-transformador.html"
    model = TrafoTask
    form_class = TrafoTaskForm
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

    def get_success_url(self, *args, **kwargs):
        pk = self.object.idTrafoQuote.id
        return reverse_lazy('activities_app:cotizaciones-transformadores-detalle', kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        context = super(TaskQuotesTrafoUpdateView, self).get_context_data(**kwargs)
        trafoQuote = TrafoQuote.objects.get(id = self.object.idTrafoQuote.id)
        context['quotation'] = trafoQuote
        return context

# ========================== EMAILS ==========================
class InitialEmailCreateView(LoginRequiredMixin,CreateView):
    template_name = "actividades/initial-email.html"
    model = EmailSent
    form_class = EmailSentForm
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

    def get_context_data(self, **kwargs):
        context = super(InitialEmailCreateView, self).get_context_data(**kwargs)
        trafoQuote = TrafoQuote.objects.get(id = self.kwargs['pk'])
        context['quotation'] = trafoQuote
        return context

