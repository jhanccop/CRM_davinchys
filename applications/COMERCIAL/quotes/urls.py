from django.urls import path
from . import views

app_name = "comercial_app"

urlpatterns = [
    # ============== COTIZACIONES =================
    path(
        'comercial/get-quote-with-us', 
        views.FinancialDocumentsListView.as_view(),
        name='documento-financiero-lista',
    ),
]