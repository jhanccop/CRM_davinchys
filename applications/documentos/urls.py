#
from django.urls import path
from . import views

app_name = "documentos_app"

urlpatterns = [
    # ============== DOCUMENTACION FINANCIERA =================
    path(
        'documento-financiero/', 
        views.FinancialDocumentsListView.as_view(),
        name='documento-financiero-lista',
    ),
    path(
        'documento-financiero/nuevo/', 
        views.FinancialDocumentsCreateView.as_view(),
        name='documento-financiero-nuevo',
    ),
    path(
        'documento-financiero/editar/<pk>/', 
        views.FinancialDocumentsEditView.as_view(),
        name='documento-financiero-editar',
    ),

    path(
        'documento-financiero/detalle/<pk>/', 
        views.DocumentacionDetailView.as_view(),
        name='documento-financiero-detalle',
    ),

    path(
        'documento-financiero/eliminar/<pk>/', 
        views.FinancialDocumentsDeleteView.as_view(),
        name='documento-financiero-eliminar',
    ),

    # ============== DOCUMENTACION GENERICA =================
    path(
        'documento-generico/', 
        views.OthersDocumentsListView.as_view(),
        name='documento-generico-lista',
    ),
    path(
        'documento-generico/nuevo/', 
        views.OthersDocumentsCreateView.as_view(),
        name='documento-generico-nuevo',
    ),
    path(
        'documento-generico/editar/<pk>/', 
        views.OthersDocumentsEditView.as_view(),
        name='documento-generico-editar',
    ),

    path(
        'documento-generico/detalle/<pk>/', 
        views.OthersDocumentsDetailView.as_view(),
        name='documento-generico-detalle',
    ),

    path(
        'documento-generico/eliminar/<pk>/', 
        views.OthersDocumentsDeleteView.as_view(),
        name='documento-generico-eliminar',
    ),
]