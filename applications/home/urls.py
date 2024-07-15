#
from django.urls import path
from . import views

app_name = "home_app"

urlpatterns = [
    path(
        'panel/', 
        views.PanelHomeView.as_view(),
        name='index',
    ),
    path(
        'panel/reporte-cuentas/', 
        views.PanelReport.as_view(),
        name='reporte-cuentas',
    ),
    
]