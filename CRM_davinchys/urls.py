

from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('applications.home.urls')),
    # users app
    re_path('', include('applications.users.urls')),
    # producto app
    re_path('', include('applications.producto.urls')),
    # venta app
    re_path('', include('applications.clientes.urls')),
    # orders app
    re_path('', include('applications.pedidos.urls')),
    # cuentas app
    re_path('', include('applications.cuentas.urls')),
    # personal app
    re_path('', include('applications.personal.urls')),
    # actividades app
    re_path('', include('applications.actividades.urls')),
    # movimientos app
    re_path('', include('applications.movimientos.urls')),
    # movimientosBancarios app
    re_path('', include('applications.movimientosBancarios.urls')),
    # documentos app
    re_path('', include('applications.documentos.urls')),
    # COMERCIAL - quotes app
    re_path('', include('applications.COMERCIAL.quotes.urls')),
    # COMERCIAL - purchase app
    re_path('', include('applications.COMERCIAL.purchase.urls')),
    # COMERCIAL - sales app
    re_path('', include('applications.COMERCIAL.sales.urls')),
]

