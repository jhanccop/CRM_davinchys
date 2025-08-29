#
from django.urls import path
from . import views

app_name = "movimientosBancarios_app"

urlpatterns = [
    # ============== MOVIMIENTOS =================
    path(
        'finanzas/movimientosBancarios/', 
        views.MovimientosListView.as_view(),
        name='lista-movimientos',
    ),
    path(
        'finanzas/movimientosBancarios/agregar/', 
        views.MovimientosCreateView.as_view(),
        name='movimientos-nuevo',
    ),
    path(
        'finanzas/movimientosBancarios/editar/<pk>/', 
        views.MovimientosEditView.as_view(),
        name='movimientos-editar',
    ),
    path(
        'finanzas/movimientosBancarios/eliminar-movimientos/<pk>/', 
        views.MovimientosDeleteView.as_view(),
        name='movimientos-eliminar',
    ),
    path(
        'finanzas/movimientosBancarios/movimientos-detalle/<pk>/', 
        views.MovimientosDetailView.as_view(),
        name='movimientos-detalle',
    ),

    # ============== CONCILIACION =================
    path(
        'finanzas/movimientosBancarios/conciliar-interno/<pk>/', 
        views.ConciliarInternoCreateView.as_view(),
        name='conciliar-interno',
    ),
    path(
        'finanzas/movimientosBancarios/conciliar-movimiento-con-movimiento/<pk>/', 
        views.ConciliarMovimientoConMovimientoCreateView.as_view(),
        name='conciliar-movimiento-con-movimiento',
    ),
    path(
        'finanzas/movimientosBancarios/conciliar-movimiento-con-documento/<pk>/', 
        views.ConciliarMovimientoConDocumentoCreateView.as_view(),
        name='conciliar-movimiento-con-documento',
    ),

    path(
        'finanzas/movimientosBancarios/editar-movimiento-con-movimiento/<pk>/', 
        views.EditarMovimientoConMovimientoUpdateView.as_view(),
        name='editar-movimiento-con-movimiento',
    ),
    path(
        'finanzas/movimientosBancarios/editar-movimiento-con-documento/<pk>/', 
        views.EditarMovimientoConDocumentoUpdateView.as_view(),
        name='editar-movimiento-con-documento',
    ),

    path(
        'finanzas/movimientosBancarios/eliminar-conciliacion/<pk>/', 
        views.MovimientosConciliarDeleteView.as_view(),
        name='eliminar-conciliacion',
    ),

    # ============== UPLOAD EXCEL FILE MOVIMIENTOS =================
    path(
        'finanzas/movimientosBancarios/subir-excel/', 
        views.upload_file,
        name='movimientos-subir-excel',
    ),
]