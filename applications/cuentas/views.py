from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from applications.users.mixins import (
  AdminClientsPermisoMixin,
  AdminPermisoMixin
)
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    FormView
)

from .models import Account

from .forms import AccountForm, SelectTinForm

class AccountListView(AdminClientsPermisoMixin,ListView):
    template_name = "cuentas/lista_cuentas.html"
    context_object_name = 'cuentas'
    model = Account
    ordering = ["accountName"]

class AccountCreateView(AdminPermisoMixin,CreateView):
    template_name = "cuentas/crear_cuentas.html"
    model = Account
    form_class = AccountForm
    success_url = reverse_lazy('cuentas_app:cuenta-lista')

class AccountDeleteView(AdminPermisoMixin,DeleteView):
    model = Account
    success_url = reverse_lazy('cuentas_app:cuenta-lista')

class AccountUpdateView(AdminPermisoMixin,UpdateView):
    template_name = "cuentas/editar_cuentas.html"
    model = Account
    form_class = AccountForm
    success_url = reverse_lazy('cuentas_app:cuenta-lista')

class SelectTinView(FormView):
    template_name = "cuentas/seleccionar_empresa.html"
    form_class = SelectTinForm

    def form_valid(self, form):
        tin = form.cleaned_data['tin']
        self.request.session['compania_id'] = tin.id
        return redirect('movimientosBancarios_app:lista-movimientos')