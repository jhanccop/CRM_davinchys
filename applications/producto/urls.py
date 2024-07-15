#
from django.urls import path
from . import views

app_name = "producto_app"

urlpatterns = [
    
    # ================ TRANSFORMADORES =======================
    path(
        'transformador/lista/', 
        views.TransformadorListView.as_view(),
        name='transformador-lista',
    ),
    path(
        'transformador/agregar_transformador/', 
        views.TransformadorCreateView.as_view(),
        name='transformador-add',
    ),
    path(
        'transformador/eliminar_transformador/<pk>/', 
        views.TransformadorDeleteView.as_view(),
        name='transformador-eliminar',
    ),
    path(
        'transformador/editar_transformador/<pk>/', 
        views.TransformadorUpdateView.as_view(),
        name='transformador-editar',
    ),
    path(
        'transformador/detalle_transformador/<pk>/', 
        views.TransformadorDetailView.as_view(),
        name='transformador-detalle',
    ),

    # ================ INVENTARIO =======================
    path(
        'inventario/lista/', 
        views.InventarioListView.as_view(),
        name='inventario-lista',
    ),

]