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