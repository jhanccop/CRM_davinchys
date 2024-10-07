#
from django.urls import path
from . import views

app_name = "cuentas_app"

urlpatterns = [
    path(
        'accounts/lista/', 
        views.AccountListView.as_view(),
        name='cuentas-lista',
    ),
    path(
        'accounts/agregar_cuenta/', 
        views.AccountCreateView.as_view(),
        name='cuentas-add',
    ),
    path(
        'accounts/editar_cuenta/<pk>/', 
        views.AccountUpdateView.as_view(),
        name='cuentas-editar',
    ),
    path(
        'accounts/eliminar_cuenta/<pk>/', 
          views.AccountDeleteView.as_view(),
          name='cuentas-eliminar',
    ),
]