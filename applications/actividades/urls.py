from django.conf import settings
from django.conf.urls.static import static

#
from django.urls import path
from .views import get_task_detail
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


    # ============== ACTIVIDADES SEMANALES ===============
    #path(
    #    'actividades/mi-lista-actividades-semanales/', 
    #    views.MyWeeklyTaskListView.as_view(),
    #    name='mi-lista-actividades-semanales',
    #),

    path('weekly/', views.WeeklyTasksView.as_view(), name='weekly_tasks'),
    path('task/create/', views.CreateDailyTaskView.as_view(), name='create_task'),
    path('task/update/<int:pk>/', views.UpdateDailyTaskView.as_view(), name='update_task'),
    path('task/delete/<int:pk>/', views.DeleteDailyTaskView.as_view(), name='delete_task'),
    # ============== ACTIVIDADES DIARIAS ===============
    path(
        'actividades/mi-lista-actividades-diarias/', 
        views.MyDailyTaskListView.as_view(),
        name='mi-actividad-diaria-lista',
    ),

    path('api/tasks/<int:task_id>/', get_task_detail, name='task-detail'),

    path(
        'actividades/reporte-actividades-diarias/', 
        views.DailyTaskReportView.as_view(),
        name='reporte-actividades-diarias',
    ),

    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/events/', views.DailyTasksListView.as_view(), name='calendar_events'),
    path('calendar/save/', views.DailyTasksSaveView.as_view(), name='calendar_save'),

    # ============== PERMISOS ===============
    path(
        'actividades/mi-lista-permisos/', 
        views.MyListRestDays.as_view(),
        name='mi-lista-permisos',
    ),
    path(
        'actividades/crear-permiso-laboral/', 
        views.RestTimeCreateView.as_view(),
        name='crear-permiso-laboral',
    ),
    path(
        'actividades/editar-permiso-laboral/<pk>/', 
        views.RestTimeUpdateView.as_view(),
        name='permiso-laboral-editar',
    ),
    path(
        'actividades/eliminar-permiso-laboral/<pk>/', 
        views.RestTimeDeleteView.as_view(),
        name='eliminar-permiso-laboral',
    ),

    path('aprobar/rrhh/', views.AprobarPermisoRRHHView.as_view(), name='aprobar_rrhh'),
    path('denegar/rrhh/', views.DenegarPermisoRRHHView.as_view(), name='denegar_rrhh'),
    path('aprobar/gerencia/', views.AprobarPermisoGerenciaView.as_view(), name='aprobar_gerencia'),
    path('denegar/gerencia/', views.DenegarPermisoGerenciaView.as_view(), name='denegar_gerencia'),


    # ============== BUZON DE SUGERENCIAS ===============
    path(
        'actividades/mi-buzon-de-sugerencias/', 
        views.MySuggestionBoxListView.as_view(),
        name='mi-buzon-de-sugerencias',
    ),
    path(
        'actividades/crear-buzon-de-sugerencias/', 
        views.SuggestionBoxCreateView.as_view(),
        name='crear-buzon-de-sugerencias',
    ),
    path(
        'actividades/editar-buzon-de-sugerencias/<pk>/', 
        views.SuggestionBoxUpdateView.as_view(),
        name='editar-buzon-de-sugerencias',
    ),
    path(
        'actividades/eliminar-sugerencia/<pk>/', 
        views.SuggestionBoxDeleteView.as_view(),
        name='eliminar-sugerencia',
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
    path(
        'actividades/crear-transformador/<pk>/', 
        views.TrafoCreateView.as_view(),
        name='crear-transformador',
    ),
    path(
        'actividades/editar-transformador/<pk>/', 
        views.TrafoUpdateView.as_view(),
        name='editar-transformador',
    ),
    path(
        'actividades/eliminar-transformador/<pk>/', 
        views.TrafoDeleteView.as_view(),
        name='eliminar-transformador',
    ),

    path(
        'actividades/cotizaciones-enviar-correo/<pk>/',
        views.InitialEmailCreateView.as_view(),
        name='cotizaciones-enviar-correo',
    ),

    path(
        'actividades/agregar-tareas-orden-transformador/<pk>/', 
        views.TaskQuotesTrafoCreateView.as_view(),
        name='agregar-tareas-orden-transformador',
    ),

    path(
        'actividades/editar-tareas-orden-transformador/<pk>/', 
        views.TaskQuotesTrafoUpdateView.as_view(),
        name='editar-tareas-orden-transformador',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)