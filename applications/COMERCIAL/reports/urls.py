from django.urls import path
from . import views

app_name = "comercial_reports_app"

urlpatterns = [
    # ==================== DASHBOARD PRINCIPAL ====================
    path('comercial/reports/dashboard/', views.DashboardView.as_view(), name='dashboard'),
]