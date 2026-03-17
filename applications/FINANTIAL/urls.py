"""
FINANTIAL/urls.py

Registro en el urls.py principal del proyecto:
    path('finantial/', include('applications.FINANTIAL.urls', namespace='finantial')),
"""
from django.urls import path
from . import views

app_name = 'finantial'

urlpatterns = [

    # ── Dashboard ─────────────────────────────────────────────────────────────
    path('dashboard-finanzas',                    views.PaymentDashboardView.as_view(),         name='dashboard'),

    # ── Comprobantes de pago ──────────────────────────────────────────────────
    path('comprobantes/',                         views.PaymentDocumentListView.as_view(),      name='document-list'),
    path('comprobantes/nuevo/',                   views.PaymentDocumentCreateView.as_view(),    name='document-create'),
    path('comprobantes/<int:pk>/',                views.PaymentDocumentDetailView.as_view(),    name='document-detail'),
    path('comprobantes/<int:pk>/editar/',         views.PaymentDocumentUpdateView.as_view(),    name='document-update'),
    path('comprobantes/<int:pk>/eliminar/',       views.PaymentDocumentDeleteView.as_view(),    name='document-delete'),

    # ── Transacciones de pago ─────────────────────────────────────────────────
    path('transacciones/',                        views.PaymentTransactionListView.as_view(),   name='transaction-list'),
    path('transacciones/nueva/',                  views.PaymentTransactionCreateView.as_view(), name='transaction-create'),
    path('transacciones/<int:pk>/',               views.PaymentTransactionDetailView.as_view(), name='transaction-detail'),
    path('transacciones/<int:pk>/editar/',        views.PaymentTransactionUpdateView.as_view(), name='transaction-update'),
    path('transacciones/<int:pk>/eliminar/',      views.PaymentTransactionDeleteView.as_view(), name='transaction-delete'),
    path('transacciones/<int:pk>/confirmar/',     views.ConfirmTransactionView.as_view(),       name='transaction-confirm'),

    # ── Movimientos bancarios ─────────────────────────────────────────────────
    path('movimientos/',                          views.BankMovementsListView.as_view(),        name='movement-list'),
    path('movimientos/nuevo/',                    views.BankMovementsCreateView.as_view(),      name='movement-create'),
    path('movimientos/<int:pk>/',                 views.BankMovementsDetailView.as_view(),      name='movement-detail'),
    path('movimientos/<int:pk>/editar/',          views.BankMovementsUpdateView.as_view(),      name='movement-update'),
    path('movimientos/<int:pk>/eliminar/',        views.BankMovementsDeleteView.as_view(),      name='movement-delete'),

    # ── Seguimiento por ítem ──────────────────────────────────────────────────
    path('seguimiento/',                          views.ItemTrackingView.as_view(),             name='item-tracking'),

    # ── API / AJAX ────────────────────────────────────────────────────────────
    path('api/item/<int:pk>/pending/',            views.ItemPendingAmountView.as_view(),        name='api-item-pending'),
]