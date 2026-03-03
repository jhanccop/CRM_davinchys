from django.urls import path
from . import views

app_name = "logistica_app"

urlpatterns = [

    # ============== CONTENEDORES =================
    path('logistica/contenedores/',views.ContainerListView.as_view(), name='lista-contenedores'),
    path('logistica/contenedor/nuevo', views.ContainerCreateView.as_view(), name='nuevo-contenedor'),
    path('logistica/contenedor/editar/<int:pk>', views.ContainerUpdateView.as_view(), name='editar-contenedor'),
    #path('logistica/contenedor/eliminar/<int:pk>', views.ContainerDeleteView.as_view(), name='eliminar-contenedor'),
    path('logistica/contenedor/detalle/<int:pk>', views.ContainerDetailView.as_view(), name='detalle-contenedor'),

    # ============== DOCUMENTOS =================
    path('logistica/contenedor/<int:container_pk>/documento/nuevo/', views.DocumentCreateView.as_view(), name='nuevo-documento'),
    path('logistica/contenedor/documento/<int:pk>/eliminar/', views.DocumentDeleteView.as_view(), name='eliminar-documento'),

    # ============== TRACKING CONTENEDORES =================
    path('contenedor/<int:container_pk>/tracking/nuevo/', views.TrackingCreateView.as_view(),   name='nuevo-tracking'),
    path('tracking/<int:pk>/eliminar/', views.TrackingDeleteView.as_view(),   name='eliminar-tracking'),
]