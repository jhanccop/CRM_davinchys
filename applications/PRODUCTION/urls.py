from django.urls import path
from . import views

app_name = 'produccion_app'

urlpatterns = [
    # Transformadores
    path('produccion/catalogo/lista/', views.TrafosListView.as_view(), name='trafos-lista'),
    path('produccion/catalogo/crear/', views.TrafosCreateView.as_view(), name='trafos-crear'),
    path('produccion/catalogo/<int:pk>/', views.TrafosDetailView.as_view(), name='trafos-detalle'),
    path('produccion/catalogo/<int:pk>/editar/', views.TrafosUpdateView.as_view(), name='trafos-editar'),
    path('produccion/catalogo/<int:pk>/eliminar/', views.TrafosDeleteView.as_view(), name='trafos-eliminar'),
]