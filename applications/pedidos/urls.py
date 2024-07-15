#
from django.urls import path
from . import views

app_name = "pedidos_app"

urlpatterns = [

     # ================= PAY REQUIREMENTSS ================
    path(
        'pedidos/mi-lista-solicitudes/', 
        views.MyRequirementsListView.as_view(),
        name='mi-lista-solicitudes',
    ),
    path(
        'pedidos/nueva-solicitud/',
        views.RequirementsCreateView.as_view(),
        name='nueva-solicitud',
    ),
    path(
        'pedidos/editar-solicitud/<pk>/', 
        views.RequirementsUpdateView.as_view(),
        name='editar-solicitud',
    ),
    path(
        'pedidos/eliminar-solicitud/<pk>/', 
        views.RequirementsDeleteView.as_view(),
        name='eliminar-solicitud',
    ),
    path(
        'pedidos/solicitudes-por-aprobar/', 
        views.RequirementsApproveListView.as_view(),
        name='solicitudes-por-aprobar',
    ),
    path(
        'pedidos/aprobar-solicitud-1/<pk>/', 
        views.ApproveRequestUpdateView1.as_view(),
        name='aprobar-solicitud-1',
    ),
]