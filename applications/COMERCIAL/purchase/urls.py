from django.urls import path
from . import views

app_name = "compras_app"

urlpatterns = [
    # ==================== DASHBOARD PRINCIPAL ====================
    path('comercial/dashboard/', views.DashboardView.as_view(), name='dashboard'),
    #path('comercial/ordenes-compra/cotizar-con-proveedores/<pk>/', views.QuoteWithSuppliers.as_view(), name='cotizar-con-proveedores'),
    path('comercial/ordenes-compra/nueva-cotizacion/<pk>/', views.NewQuoteRequirementCreateView.as_view(), name='nueva_cotizacion_id'),
    #path('comercial/ordenes-compra/nuevo-voucher/<pk>/', views.NewVoucherRequirementCreateView.as_view(), name='nueva_cotizacion_id'),

    # ==================== REQUERIMIENTOS ====================
    # REQUERIMIENTOS
    path('comercial/requerimientos/lista/', views.RequirementListView.as_view(), name='list_requirement'),
    path('comercial/requerimientos/nuevo/', views.RequirementCreateView.as_view(), name='create_requirement'),
    path('comercial/requerimientos/detalle/<pk>/', views.RequirementDetailView.as_view(), name='detail_requirement'),
    path('comercial/requirement/editar/<pk>/', views.RequirementEditView.as_view(), name='edit_requirement'),
    path('comercial/requirement/delete/<pk>/', views.RequirementDeleteView.as_view(), name='delete_requirement'),

    # ==================== ORDENES DE COMPRA ====================
    path('comercial/ordenes-compra/lista/', views.PurchaseOrderListView.as_view(), name='lista_ordenescompra'),


    # ==================== INVOICES COMPRA ====================
    path('comercial/compras/lista/', views.PurchaseListView.as_view(), name='lista_compras'),
    path('comercial/compras/nuevo/<pk>/', views.PurchaseInvoiceCreateView.as_view(), name='crear_compra_id'),

    # ==================== TRACKING REQUIREMENTS ====================
    path('comercial/requerimientos-traking/nuevo/<pk>/', views.RequestTrackingCreateView.as_view(), name='crear_log_requirement'),

    # ==================== CAJA CHICA ====================
    path('comercial/cajachica/lista/', views.PettyCashListView.as_view(), name='lista_cajachica'),
    path('comercial/cajachica/nuevo/', views.PettyCashCreateView.as_view(), name='crear_cajachica'),
    path('comercial/cajachica/detalle/<pk>/', views.PettyCashDetailView.as_view(), name='detalle_cajachica'),
    path('comercial/cajachica/delete/<pk>/', views.PettyCashDeleteView.as_view(), name='eliminar_cajachica'), 

    path('comercial/compras/', views.requirementsInvoiceListView.as_view(), name='compras-lista'),
    path('comercial/compras/nuevo/', views.requirementsInvoiceCreateView.as_view(), name='compras-nuevo'),
    path('comercial/compras/editar/<pk>/', views.requirementsInvoiceEditView.as_view(), name='compras-editar'),
    path('comercial/compras/detalle/<pk>/', views.requirementsInvoiceDetailView.as_view(), name='compras-detalle'),
    path('comercial/compras/eliminar/<pk>/', views.requirementsInvoiceDeleteView.as_view(), name='compras-eliminar'),
]