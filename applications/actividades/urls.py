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
        'actividades/cotizaciones-transformadores/', 
        views.QuotesListView.as_view(),
        name='cotizaciones-transformadores',
    ),
    path(
        'actividades/cotizaciones-transformadores-nuevo/',
        views.QuotesCreateView.as_view(),
        name='cotizaciones-transformadores-nuevo',
    ),
    path(
        'actividades/cotizaciones-transformadores-editar/<pk>/', 
        views.QuotesEditView.as_view(),
        name='cotizaciones-transformadores-editar',
    ),
    path(
        'actividades/cotizaciones-transformadores-eliminar/<pk>/', 
        views.QuotesDeleteView.as_view(),
        name='cotizaciones-transformadores-eliminar',
    ),
    path(
        'actividades/cotizaciones-transformadores-detalle/<pk>/', 
        views.QuotesDetailView.as_view(),
        name='cotizaciones-transformadores-detalle',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)