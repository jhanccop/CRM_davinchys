#
from django.urls import path
from . import views

app_name = "movimientosBancarios_app"

urlpatterns = [
    # ============== MOVIMIENTOS =================
    path(
        'movimientosBancarios/', 
        views.MovimientosListView.as_view(),
        name='lista-movimientos',
    ),
    path(
        'movimientosBancarios/agregar/', 
        views.MovimientosCreateView.as_view(),
        name='movimientos-nuevo',
    ),
    path(
        'movimientosBancarios/editar/<pk>/', 
        views.MovimientosEditView.as_view(),
        name='movimientos-editar',
    ),
    path(
        'movimientosBancarios/eliminar-movimientos/<pk>/', 
        views.MovimientosDeleteView.as_view(),
        name='movimientos-eliminar',
    ),
    path(
        'movimientosBancarios/movimientos-detalle/<pk>/', 
        views.MovimientosDetailView.as_view(),
        name='movimientos-detalle',
    ),

    # ============== CONCILIACION =================
    path(
        'movimientosBancarios/conciliar-movimiento-con-movimiento/<pk>/', 
        views.ConciliarMovimientoConMovimientoCreateView.as_view(),
        name='conciliar-movimiento-con-movimiento',
    ),
    path(
        'movimientosBancarios/conciliar-movimiento-con-documento/<pk>/', 
        views.ConciliarMovimientoConDocumentoCreateView.as_view(),
        name='conciliar-movimiento-con-documento',
    ),

    path(
        'movimientosBancarios/editar-movimiento-con-movimiento/<pk>/', 
        views.EditarMovimientoConMovimientoUpdateView.as_view(),
        name='editar-movimiento-con-movimiento',
    ),
    path(
        'movimientosBancarios/editar-movimiento-con-documento/<pk>/', 
        views.EditarMovimientoConDocumentoUpdateView.as_view(),
        name='editar-movimiento-con-documento',
    ),

    path(
        'movimientosBancarios/eliminar-conciliacion/<pk>/', 
        views.MovimientosConciliarDeleteView.as_view(),
        name='eliminar-conciliacion',
    ),

    # ============== REPORTES =================

    path(
        'reporte-de-cuentas/', 
        views.ListAccountReport.as_view(),
        name='reporte-de-cuentas',
    ),
    path(
        'reporte-de-cuentas-detalle/<pk>/', 
        views.AccountReportDetail.as_view(),
        name='reporte-de-cuentas-detalle',
    ),

    # ============== UPLOAD EXCEL FILE MOVIMIENTOS =================
    path(
        'movimientosBancarios/subir-excel/', 
        views.upload_file,
        name='movimientos-subir-excel',
    ),
    
]