from datetime import date, timedelta
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView
)

from applications.users.mixins import (
  LogisticaMixin,
  AdminClientsPermisoMixin
)

from applications.LOGISTICA.transport.models import Container, ContainerTracking, File
from .forms import ContainerForm, FileForm, ContainerTrackingForm


# =========================== CONTAINERS ===========================
class ContainerListView(LogisticaMixin, ListView):
  template_name = "LOGISTICA/transport/container-lista.html"
  context_object_name = 'containers'

  def get_queryset(self,**kwargs):
    compania_id = self.request.user.company.id
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
        intervalDate = str(date.today() - timedelta(days = 90)) + " to " + str(date.today())

    container = Container.objects.ListaContenedoresPorRuc(intervalo = intervalDate, idTin = compania_id)
    
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["listContainer"] = container
    return payload
  
class ContainerDetailView(LogisticaMixin, DetailView):
    model = Container
    template_name = 'LOGISTICA/transport/detalle_contenedor.html'
    context_object_name = 'container'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracking'] = ContainerTracking.objects.filter(
            idContainer=self.object
        ).order_by('created')
        context['documentos'] = File.objects.filter(
            idContainer=self.object
        ).order_by('-date')
        return context

class ContainerCreateView(LogisticaMixin, CreateView):
    model = Container
    form_class = ContainerForm
    template_name = 'LOGISTICA/transport/form-container.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Contenedor'
        context['btn_label'] = 'Crear Contenedor'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Contenedor creado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores del formulario.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('logistica_app:lista-contenedores')

class ContainerUpdateView(LogisticaMixin, UpdateView):
    model = Container
    form_class = ContainerForm
    template_name = 'LOGISTICA/transport/form-container.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Contenedor'
        context['btn_label'] = 'Actualizar Contenedor'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Contenedor actualizado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores del formulario.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('logistica_app:detalle-contenedor', kwargs={'pk': self.object.pk})
  
# =========================== DOCUMENTS ===========================
class DocumentCreateView(LogisticaMixin, CreateView):
    model = File
    form_class = FileForm
    template_name = 'LOGISTICA/transport/documento_form.html'

    def get_container(self):
        return get_object_or_404(Container, pk=self.kwargs['container_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['container'] = self.get_container()
        context['titulo'] = 'Agregar Documento'
        return context

    def form_valid(self, form):
        form.instance.idContainer = self.get_container()
        messages.success(self.request, 'Documento agregado correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('logistica_app:detalle-contenedor', kwargs={'pk': self.kwargs['container_pk']})

class DocumentDeleteView(LogisticaMixin, DeleteView):
    model = File

    def get_success_url(self):
        return reverse('logistica_app:detalle-contenedor', kwargs={'pk': self.object.idContainer.pk})

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Documento eliminado correctamente.')
        return super().post(request, *args, **kwargs)
    
# =========================== TRACKING ===========================

class TrackingCreateView(LogisticaMixin, CreateView):
    model = ContainerTracking
    form_class = ContainerTrackingForm
    template_name = 'LOGISTICA/transport/tracking_form.html'

    def get_container(self):
        return get_object_or_404(Container, pk=self.kwargs['container_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['container'] = self.get_container()
        context['titulo'] = 'Nuevo Estado de Tracking'
        context['btn_label'] = 'Guardar Estado'
        return context

    def form_valid(self, form):
        form.instance.idContainer = self.get_container()
        messages.success(self.request, 'Estado de tracking agregado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores del formulario.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('logistica_app:detalle-contenedor', kwargs={'pk': self.kwargs['container_pk']})

class TrackingDeleteView(LogisticaMixin, DeleteView):
    model = ContainerTracking

    def get_success_url(self):
        return reverse('logistica_app:detalle-contenedor', kwargs={'pk': self.object.idContainer.pk})

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Estado de tracking eliminado correctamente.')
        return super().post(request, *args, **kwargs)

