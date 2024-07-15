#
from django.urls import path
from . import views

app_name = "workers_app"

urlpatterns = [
    path(
        'workers/lista/', 
        views.WorkerListView.as_view(),
        name='personal-lista',
    ),
    path(
        'workers/agregar-personal/', 
        views.WorkerCreateView.as_view(),
        name='personal-nuevo',
    ),
    path(
        'workers/editar-personal/<pk>/', 
        views.WorkerUpdateView.as_view(),
        name='personal-editar',
    ),
    path(
        'workers/eliminar-personal/<pk>/', 
        views.WorkerDeleteView.as_view(),
        name='personal-eliminar',
    ),

    
]