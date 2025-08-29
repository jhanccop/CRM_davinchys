from django.urls import path
from . import views

app_name = "logistica_app"

urlpatterns = [
    # ============== CONTENEDORES =================
    # path('logistica/nuevo-contenedor',views.CreateContainerView.as_view(), name='crear-cotizacion'),
    path('logistica/lista-contenedores',views.ContainerListView.as_view(), name='lista-contenedores'),
]