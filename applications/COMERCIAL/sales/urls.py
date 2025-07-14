from django.urls import path
from . import views

app_name = "ventas_app"

urlpatterns = [
    path('comercial/ventas/', views.IncomesListView.as_view(), name='ventas-lista'),
    path('comercial/ventas/nuevo/', views.IncomesCreateView.as_view(), name='ventas-nuevo'),
    path('comercial/ventas/editar/<pk>/', views.IncomesEditView.as_view(), name='ventas-editar'),
    path('comercial/ventas/detalle/<pk>/', views.IncomesDetailView.as_view(), name='ventas-detalle'),
    path('comercial/ventas/eliminar/<pk>/', views.IncomesDeleteView.as_view(), name='ventas-eliminar'),
]