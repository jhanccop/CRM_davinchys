from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from applications.users.mixins import (
  ContabilidadPermisoMixin,
  AdminPermisoMixin
)
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)

from .models import Account,ManualAccount

from .forms import AccountForm, ManualAccountForm

class AccountListView(ContabilidadPermisoMixin,ListView):
    template_name = "cuentas/lista_cuentas.html"
    context_object_name = 'cuentas'
    model = Account
    ordering = ["accountName"]

class ManualAccountCreateView(AdminPermisoMixin,CreateView):
    template_name = "cuentas/crear-cuenta-manual.html"
    model = ManualAccount
    form_class = ManualAccountForm
    success_url = reverse_lazy('cuentas_app:cuentas-lista')

    def get_context_data(self, **kwargs):
        context = super(ManualAccountCreateView, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(id = self.kwargs['pk'])
        return context

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