from django.shortcuts import render

from django.urls import reverse_lazy

from applications.users.mixins import (
  AdminPermisoMixin
)

from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)

from .models import Workers

from .forms import WorkersForm

class WorkerListView(AdminPermisoMixin,ListView):
    template_name = "personal/lista-personal.html"
    context_object_name = 'personal'
    model = Workers

class WorkerCreateView(AdminPermisoMixin,CreateView):
    template_name = "personal/crear-personal.html"
    model = Workers
    form_class = WorkersForm
    success_url = reverse_lazy('workers_app:personal-lista')

class WorkerDeleteView(AdminPermisoMixin,DeleteView):
    template_name = "personal/eliminar-personal.html"
    model = Workers
    success_url = reverse_lazy('workers_app:personal-lista')

class WorkerUpdateView(AdminPermisoMixin,UpdateView):
    template_name = "personal/editar-personal.html"
    model = Workers
    form_class = WorkersForm
    success_url = reverse_lazy('workers_app:personal-lista')
