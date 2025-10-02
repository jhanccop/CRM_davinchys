from django.urls import path
from . import views

app_name = "finanzas_reports_app"

urlpatterns = [
    # ==================== DASHBOARD PRINCIPAL ====================
    path(
        'finanzas/dashboard/', 
        views.ListAccountReport.as_view(),
        name='reporte-de-cuentas',
    ),
    path(
        'finanzas/dashboard/detalle/<pk>/', 
        views.AccountReportDetail.as_view(),
        name='reporte-de-cuentas-detalle',
    ),
]