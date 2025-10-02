from django.urls import path
from . import views

app_name = "compras_app"

urlpatterns = [
    
    # ============== REQUERIMIENTOS ==============
    path('comercial/requerimientos/', views.RequirementListView.as_view(), name='list_requirement'),
    path('comercial/requerimientos/nuevo/', views.RequirementCreateView.as_view(), name='create_requirement'),
    path('comercial/requerimientos/detalle/<pk>/', views.RequirementDetailView.as_view(), name='detail_requirement'),
    path('comercial/requerimientos/editar/<pk>/', views.RequirementEditView.as_view(), name='edit_requirement'),
    path('comercial/requirement/delete/<pk>/', views.RequirementDeleteView.as_view(), name='delete_requirement'),

    # ============== REQUERIMIENTOS LOGISTICOS =================
    path('logistica/requerimiento-logisticos/',views.LogisticRequirementListView.as_view(), name='logistic-lista-requerimiento'),
    
    # ==================== ORDENES DE COMPRA ====================
    path('comercial/ordenes-compra/', views.PurchaseOrderListView.as_view(), name='lista_ordenescompra'),

    # ==================== INVOICES COMPRA ====================
    path('comercial/compras/lista/', views.PurchaseListView.as_view(), name='lista_compras'),
    path('comercial/compras/nuevo/<pk>/', views.PurchaseInvoiceCreateView.as_view(), name='crear_compra_id'),

    # ==================== TRACKING REQUIREMENTS ====================
    path('comercial/requerimientos-traking/nuevo/<pk>/', views.RequestTrackingCreateView.as_view(), name='crear_log_requirement'),

    # ==================== CAJA CHICA ====================
    path('comercial/requerimientos/cajachica/lista/', views.PettyCashListView.as_view(), name='lista_cajachica'),
    path('comercial/requerimientos/cajachica/nuevo/', views.PettyCashCreateView.as_view(), name='crear_cajachica'),
    path('comercial/requerimientos/cajachica/detalle/<pk>/', views.PettyCashDetailView.as_view(), name='detalle_cajachica'),
    path('comercial/requerimientos/cajachica/delete/<pk>/', views.PettyCashDeleteView.as_view(), name='eliminar_cajachica'), 

    path('comercial/compras/', views.requirementsInvoiceListView.as_view(), name='compras-lista'),
    path('comercial/compras/nuevo/', views.requirementsInvoiceCreateView.as_view(), name='compras-nuevo'),
    path('comercial/compras/editar/<pk>/', views.requirementsInvoiceEditView.as_view(), name='compras-editar'),
    path('comercial/compras/detalle/<pk>/', views.requirementsInvoiceDetailView.as_view(), name='compras-detalle'),
    path('comercial/compras/eliminar/<pk>/', views.requirementsInvoiceDeleteView.as_view(), name='compras-eliminar'),
]