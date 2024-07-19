#
from django.urls import path
from . import views

app_name = "movimientos_app"

urlpatterns = [
    # ============== TRANSFERENCIAS =================
    path(
        'reporte-principal/', 
        views.MainReport.as_view(),
        name='reporte-principal',
    ),
    path(
        'reporte-cuentas/', 
        views.ListAccount.as_view(),
        name='reporte-cuentas',
    ),
    path(
        'reporte-cuentas-detalle/<pk>/', 
        views.AccountDetail.as_view(),
        name='reporte-cuentas-detalle',
    ),
    path(
        'reporte-cajaChica/', 
        views.ListCajaChica.as_view(),
        name='reporte-cajaChica',
    ),
    path(
        'reporte-cajaChica-detalle/<pk>/', 
        views.CajaChicaDetail.as_view(),
        name='reporte-cajaChica-detalle',
    ),
    path(
        'reporte-transferencias/', 
        views.TransfersReport.as_view(),
        name='reporte-transferencias',
    ),

    # ============== DOCUMENTACION =================
    path(
        'documentacion/', 
        views.DocumentacionListView.as_view(),
        name='lista-documentacion',
    ),
    path(
        'documentacion/nuevo/', 
        views.DocumentacionCreateView.as_view(),
        name='documentacion-nuevo',
    ),
    path(
        'documentacion/editar/<pk>/', 
        views.DocumentacionEditView.as_view(),
        name='documentacion-editar',
    ),

    # ============== MOVIMIENTOS =================
    path(
        'movimientos/', 
        views.MovimientosListView.as_view(),
        name='lista-movimientos',
    ),
    path(
        'movimientos/agregar/', 
        views.MovimientosCreateView.as_view(),
        name='movimientos-nuevo',
    ),
    path(
        'movimientos/editar/<pk>/', 
        views.MovimientosEditView.as_view(),
        name='movimientos-editar',
    ),
    path(
        'movimientos/detalle/<pk>/', 
        views.MovimientosDetailView.as_view(),
        name='movimientos-detalle',
    ),
    # ============== UPLOAD EXCEL FILE MOVIMIENTOS =================
    path(
        'movimientos/subir-excel/', 
        views.upload_file,
        name='movimientos-subir-excel',
    ),

    # ============== CONCILIAR =================

    path(
        'movimientos/conciliar/<pk>/', 
        views.MovimientosConciliarCreateView.as_view(),
        name='movimientos-conciliar',
    ),
    path(
        'movimientos/editar-conciliar/<pk>/', 
        views.MovimientosConciliarUpdateView.as_view(),
        name='movimientos-conciliar-editar',
    ),
    path(
        'movimientos/eliminar-conciliacion/<pk>/', 
        views.MovimientosConciliarDeleteView.as_view(),
        name='movimientos-conciliacion-eliminar',
    ),

    # ============== TRANSFERENCIAS =================
    path(
        'movimientos/transferencias/', 
        views.TransferenciasListView.as_view(),
        name='lista-transferencias',
    ),
    path(
        'movimientos/agregar-transferencia/', 
        views.TransferenciasCreateView.as_view(),
        name='transferencia-nuevo',
    ),
    path(
        'movimientos/editar-transferencia/<pk>/', 
        views.TransferenciasUpdateView.as_view(),
        name='transferencia-editar',
    ),
    path(
        'movimientos/eliminar-transferencia/<pk>/', 
        views.TransferenciasDeleteView.as_view(),
        name='transferencia-eliminar',
    ),
]