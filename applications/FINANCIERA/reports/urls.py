from django.urls import path
from . import views

app_name = "finanzas_reports_app"

urlpatterns = [
    # ==================== DASHBOARD PRINCIPAL ====================
    path(
        'finanzas/reporte-de-cuentas/', 
        views.ListAccountReport.as_view(),
        name='reporte-de-cuentas',
    ),
    path(
        'finanzas/reporte-de-cuentas-detalle/<pk>/', 
        views.AccountReportDetail.as_view(),
        name='reporte-de-cuentas-detalle',
    ),
]