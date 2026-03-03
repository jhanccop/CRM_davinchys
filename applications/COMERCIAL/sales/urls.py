from django.urls import path
from . import views

app_name = "ventas_app"

urlpatterns = [
    # ==================== COTIZACIONES DE FABRICACION ====================
    path('comercial/cotizaciones/', views.TrafoQuoteListView.as_view(), name='cotizaciones-lista'),
    path('comercial/cotizaciones/nuevo/', views.QuoteCreateView.as_view(), name='cotizacion-nuevo'),
    path('comercial/cotizaciones/agregar/', views.AddTrafoToQuoteView.as_view(), name='agregar-a-cotizacion'),
    path('comercial/cotizaciones/detalle/<pk>/', views.QuoteDetailView.as_view(), name='cotizacion-detalle'),
    path('comercial/cotizaciones/editar/<pk>/', views.QuoteUpdateView.as_view(), name='cotizacion-editar'),
    path('comercial/cotizaciones/eliminar/<pk>/', views.QuoteDeleteView.as_view(), name='cotizacion-eliminar'),

    path('comercial/po/lista/', views.TrafoPoListView.as_view(), name='po-lista'),

    # ==================== COTIZACIONES DE INTERMEDIO QUOTES ====================
    # Vista Kanban principal
    path('comercial/cotizaciones/<int:pk>/asignar/', views.QuoteKanbanView.as_view(),name='quote-assignment'),
    # API: Crear nueva IntQuote
    path('comercial/cotizaciones/<int:quote_pk>/intquote/create/', views.CreateIntQuoteAPI.as_view(),name='create-intquote-api'),
    # API: Asignar items (drag & drop)
    path('comercial/cotizaciones/<int:quote_pk>/assign-items/', views.AssignItemsAPI.as_view(),name='assign-items-api'),
    # API: Eliminar IntQuote
    path('comercial/cotizaciones/intquote/<int:int_quote_pk>/delete/', views.DeleteIntQuoteAPI.as_view(),name='delete-intquote-api'),
    # API: Actualizar costo unitario de item
    path('comercial/cotizaciones/item/<int:item_pk>/update-cost/', views.UpdateItemCostAPI.as_view(),name='update-item-cost-api'),
    path('intquote/<int:pk>/', views.IntQuoteDetailView.as_view(), name='intquote-detail' ),
    path('intquote/<int:pk>/editar/', views.IntQuoteEditView.as_view(), name='intquote-edit' ),

    # ==================== WORK ORDERS asignned ====================
    
    # Vista Kanban: IntQuote -> WorkOrders
    path('comercial/ordenes-trabajo/<int:pk>/asignar/', views.IntQuoteWOView.as_view(),name='intquote-wo-assignment'),
    # API: Crear nueva WorkOrder
    path('comercial/ordenes-trabajo/<int:int_quote_pk>/workorder/create/', views.CreateWorkOrderAPI.as_view(), name='create-workorder-api'),
    # API: Asignar items a WorkOrders (drag & drop)
    path('comercial/ordenes-trabajo/<int:int_quote_pk>/assign-items-wo/', views.AssignItemsToWOAPI.as_view(), name='assign-items-wo-api' ),
    # API: Eliminar WorkOrder
    path('comercial/ordenes-trabajo/<int:wo_pk>/delete/',  views.DeleteWorkOrderAPI.as_view(), name='delete-workorder-api'),
    # API: Actualizar costo unitario WO de un item
    path('comercial/ordenes-trabajo/<int:item_pk>/update-cost-wo/', views.UpdateItemCostWOAPI.as_view(), name='update-item-cost-wo-api'),

    # ==================== CRUD PLANTILLAS ====================
    path('comercial/cotizaciones/plantillas/', views.TrafoTemplatesListView.as_view(), name='plantilla-lista'),
    #path('comercial/cotizaciones/plantillas/nuevo/', views.TrafoTemplatesCreateView.as_view(), name='plantilla-nuevo'),
    #path('comercial/cotizaciones/plantillas/editar/<pk>/', views.TrafoTemplatesUpdateView.as_view(), name='plantilla-editar'),
    #path('comercial/cotizaciones/plantillas/detalle/<pk>/', views.TrafoTemplatesDetailView.as_view(), name='plantilla-editar'),
    #path('comercial/cotizaciones/plantillas/eliminar/<pk>/', views.TrafoTemplatesDeleteListView.as_view(), name='plantilla-eliminar'),

    # ==================== ITEMS DE COTIZACION ====================
    path('comercial/cotizaciones/crear/item/<pk>/', views.CreateTrafoItemView.as_view(), name='crear-item'),
    path('comercial/cotizaciones/editar/item/<pk>/', views.UpdateTrafoItemView.as_view(), name='editar-item'),
    path('comercial/cotizaciones/detalle/item/<pk>/', views.DetailTrafoItemView.as_view(), name='detalle-item'),
    path('comercial/cotizaciones/elimnar/item/<pk>/', views.DeleteTrafoItemView.as_view(), name='eliminar-item'),

    # ==================== IMAGENES ITEMS ====================
    # ==================== CRUD IMÁGENES ====================
    path('comercial/cotizaciones/items/<int:item_pk>/imagenes/', views.ItemDetailAllListView.as_view(), name='detail-item-all'),
    path('comercial/cotizaciones/items/<int:item_pk>/imagenes/agregar/', views.ItemImageCreateView.as_view(), name='image_create'),
    path('comercial/cotizaciones/items/<int:pk>/imagenes/agregar-multiples/', views.ItemMultipleImageUploadView.as_view(), name='item_add_images'),
    path('comercial/cotizaciones/items/<int:item_pk>/imagenes/<int:pk>/editar/', views.ItemImageUpdateView.as_view(), name='image_update'),
    path('comercial/cotizaciones/items/<int:item_pk>/imagenes/<int:pk>/eliminar/', views.ItemImageDeleteView.as_view(), name='image_delete'),

    # ==================== ITEMS UPDATE TRACKING ====================
    path('comercial/cotizaciones/seguimiento/actualizar/<pk>/',views.UpdateTrackingItemView.as_view(),name='actualizar-estado-item'),

    # ==================== FAQ SEARCH ====================
    path('comercial/fats-search/',views.DetailSerialNumberView.as_view(),name='detail-serial-number'),
    path('comercial/tracking/',views.TransformerSearchView.as_view(), name='transformer-search'),
    path('comercial/tracking/<int:pk>/',views.TransformerItemDetailView.as_view(), name='transformer-detail'),

    #path('comercial/cotizaciones/editar/<pk>/', views.IncomesEditView.as_view(), name='ventas-editar'),
    #path('comercial/cotizaciones/detalle/<pk>/', views.IncomesDetailView.as_view(), name='ventas-detalle'),
    #path('comercial/cotizaciones/eliminar/<pk>/', views.IncomesDeleteView.as_view(), name='ventas-eliminar'),

    # ==================== PO ====================
    #path('comercial/po/lista', views.QuotesListView.as_view(), name='po-lista'),
    #path('comercial/ventas/nuevo/', views.IncomesCreateView.as_view(), name='ventas-nuevo'),
    #path('comercial/ventas/editar/<pk>/', views.IncomesEditView.as_view(), name='ventas-editar'),
    #path('comercial/ventas/detalle/<pk>/', views.IncomesDetailView.as_view(), name='ventas-detalle'),
    #path('comercial/ventas/eliminar/<pk>/', views.IncomesDeleteView.as_view(), name='ventas-eliminar'),
]