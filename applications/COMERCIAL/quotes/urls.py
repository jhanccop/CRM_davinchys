from django.urls import path
from . import views

app_name = "comercial_app"

urlpatterns = [
    # ============== COTIZACIONES =================
    path(
        'comercial/crear-cotizacion', 
        views.CreateTrafoQuoteView.as_view(),
        name='crear-cotizacion',
    ),
    path(
        'comercial/lista-cotizaciones', 
        views.TrafoQuoteListView.as_view(),
        name='lista-cotizaciones',
    ),
    #path(
    #    'comercial/get-quote-with-us', 
    #    views.FinancialDocumentsListView.as_view(),
    #    name='documento-financiero-lista',
    #),
]