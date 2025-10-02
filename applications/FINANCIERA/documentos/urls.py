#
from django.urls import path
from . import views

app_name = "documentos_app"

urlpatterns = [
    # ============== CARGA Y PROCESAMIENTO =================
    path('finanzas/documento-financiero/carga-rhe/', views.UploadRHEFileView.as_view(), name='carga-doc-rhe'),
    path('finanzas/documento-financiero/procesamiento-doc-rhe/', views.ProcessRHEFileView.as_view(), name='procesamiento-doc-rhe'),
    #path('rhe-verification/', views.RHEFileVerificationView.as_view(), name='rhe-verification'),
    # ============== DOCUMENTACION FINANCIERA =================
    path(
        'finanzas/documento-financiero/', 
        views.FinancialDocumentsListView.as_view(),
        name='documento-financiero-lista',
    ),
    path(
        'finanzas/documento-financiero/nuevo/', 
        views.FinancialDocumentsCreateView.as_view(),
        name='documento-financiero-nuevo',
    ),
    path(
        'finanzas/documento-financiero/editar/<pk>/', 
        views.FinancialDocumentsEditView.as_view(),
        name='documento-financiero-editar',
    ),

    path(
        'finanzas/documento-financiero/detalle/<pk>/', 
        views.DocumentacionDetailView.as_view(),
        name='documento-financiero-detalle',
    ),

    path(
        'finanzas/documento-financiero/eliminar/<pk>/', 
        views.FinancialDocumentsDeleteView.as_view(),
        name='documento-financiero-eliminar',
    ),

    # ============== DOCUMENTACION GENERICA =================
    path(
        'finanzas/documento-generico/', 
        views.OthersDocumentsListView.as_view(),
        name='documento-generico-lista',
    ),
    path(
        'finanzas/documento-generico/nuevo/', 
        views.OthersDocumentsCreateView.as_view(),
        name='documento-generico-nuevo',
    ),
    path(
        'finanzas/documento-generico/editar/<pk>/', 
        views.OthersDocumentsEditView.as_view(),
        name='documento-generico-editar',
    ),

    path(
        'finanzas/documento-generico/detalle/<pk>/', 
        views.OthersDocumentsDetailView.as_view(),
        name='documento-generico-detalle',
    ),

    path(
        'finanzas/documento-generico/eliminar/<pk>/', 
        views.OthersDocumentsDeleteView.as_view(),
        name='documento-generico-eliminar',
    ),
]