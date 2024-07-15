from django.conf import settings
from django.conf.urls.static import static

#
from django.urls import path
from . import views

app_name = "activities_app"

urlpatterns = [
    # ============== PROYECTOS ===============
    path(
        'actividades/lista-proyectos/', 
        views.ProjectsListView.as_view(),
        name='proyecto-lista',
    ),
    path(
        'actividades/agregar-proyecto/', 
        views.ProjectsCreateView.as_view(),
        name='proyecto-nuevo',
    ),
    path(
        'actividades/editar-proyecto/<pk>/', 
        views.ProjectsUpdateView.as_view(),
        name='proyecto-editar',
    ),
    path(
        'actividades/eliminar-proyecto/<pk>/', 
        views.ProjectsDeleteView.as_view(),
        name='proyecto-eliminar',
    ),

    # ============== COMISIONES ===============
    path(
        'actividades/lista-comisiones/', 
        views.CommissionsListView.as_view(),
        name='comision-lista',
    ),
    path(
        'actividades/agregar-comision/', 
        views.CommissionsCreateView.as_view(),
        name='comision-nuevo',
    ),
    path(
        'actividades/editar-comision/<pk>/', 
        views.CommissionsUpdateView.as_view(),
        name='comision-editar',
    ),
    path(
        'actividades/eliminar-comision/<pk>/', 
        views.CommissionsDeleteView.as_view(),
        name='comision-eliminar',
    ),

    # ============== ACTIVIDADES DIARIAS ===============
    path(
        'actividades/mi-lista-actividades-diarias/', 
        views.MyDailyTaskListView.as_view(),
        name='mi-actividad-diaria-lista',
    ),
    path(
        'actividades/crear-actividad-diaria/', 
        views.DailyTaskCreateView.as_view(),
        name='actividad-diaria-nuevo',
    ),
    path(
        'actividades/editar-actividad-diaria/<pk>/', 
        views.DailyTaskUpdateView.as_view(),
        name='actividad-diaria-editar',
    ),
    path(
        'actividades/eliminar-actividad-diaria/<pk>/', 
        views.DailyTaskDeleteView.as_view(),
        name='actividad-diaria-eliminar',
    ),
    path(
        'actividades/reporte-actividades-diarias/', 
        views.DailyTaskReportView.as_view(),
        name='reporte-actividades-diarias',
    ),

    # ============== FABRICACION DE TRANSFORMADORES ===============
    path(
        'actividades/pedidos-transformadores/', 
        views.OrdersListView.as_view(),
        name='pedidos-transformadores',
    ),
    path(
        'actividades/pedidos-transformadores-nuevo/',
        views.OrdersCreateView.as_view(),
        name='pedidos-transformadores-nuevo',
    ),
    path(
        'actividades/pedidos-transformadores-editar/<pk>/', 
        views.OrderEditView.as_view(),
        name='pedidos-transformadores-editar',
    ),
    path(
        'actividades/pedidos-transformadores-eliminar/<pk>/', 
        views.OrderDeleteView.as_view(),
        name='pedidos-transformadores-eliminar',
    ),
    path(
        'actividades/pedidos-transformadores-detalle/<pk>/', 
        views.OrderDetailView.as_view(),
        name='pedidos-transformadores-detalle',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)