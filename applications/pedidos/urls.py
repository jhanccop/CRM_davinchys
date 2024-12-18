#
from django.urls import path
from . import views

app_name = "pedidos_app"

urlpatterns = [

     # ================= PAY REQUIREMENTSS ================
    path(
        'pedidos/listas-solicitudes/', 
        views.RequirementsListView.as_view(),
        name='listas-solicitudes',
    ),
    path(
        'pedidos/nueva-lista/',
        views.ListCreateView.as_view(),
        name='nueva-lista',
    ),
    path(
        'pedidos/detalle-lista/<pk>/',
        views.ListDetailView.as_view(),
        name='detalle-lista',
    ),
    path(
        'pedidos/nueva-solicitud/<pk>/',
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
        'pedidos/lista-de-solicitudes-por-aprobar/', 
        views.ListRequirementAproved.as_view(),
        name='lista-de-solicitudes-por-aprobar',
    ),
    path(
        'pedidos/detalle-lista-aprobar/<pk>/', 
        views.DetailRequirementAproved.as_view(),
        name='detalle-lista-aprobar',
    ),
    path(
        'pedidos/actualizar-estado-lista/<pk>/', 
        views.UpdateStateList.as_view(),
        name='actualizar-estado-lista',
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