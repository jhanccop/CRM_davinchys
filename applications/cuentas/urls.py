#
from django.urls import path
from . import views

app_name = "cuentas_app"

urlpatterns = [
    path(
        'finanzas/seleccionar-empresa/', 
        views.SelectTinView.as_view(),
        name='seleccionar-empresa',
    ),
    path(
        'finanzas/cuentas-bancarias/', 
        views.AccountListView.as_view(),
        name='cuentas-lista',
    ),
    path(
        'finanzas/cuentas-bancarias/nuevo/', 
        views.AccountCreateView.as_view(),
        name='cuentas-add',
    ),
    path(
        'finanzas/cuentas-bancarias/nuevo/<pk>/', 
        views.AccountUpdateView.as_view(),
        name='cuentas-editar',
    ),
    path(
        'accounts/eliminar_cuenta/<pk>/', 
          views.AccountDeleteView.as_view(),
          name='cuentas-eliminar',
    ),
]