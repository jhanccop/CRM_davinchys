from django.urls import path
from . import views

app_name = "logistica_app"

urlpatterns = [

    # ============== CONTENEDORES =================
    path('logistica/contenedores/',views.ContainerListView.as_view(), name='lista-contenedores'),
    path('logistica/contenedor/nuevo', views.ContainerCreateView.as_view(), name='nuevo-contenedor'),
    path('logistica/contenedor/editar/<int:pk>', views.ContainerUpdateView.as_view(), name='editar-contenedor'),
    #path('logistica/contenedor/eliminar/<int:pk>', views.ContainerDeleteView.as_view(), name='eliminar-contenedor'),
    #path('logistica/contenedor/detalle/<int:pk>', views.ContainerDetailView.as_view(), name='detalle-contenedor'),
]