"""
FINANTIAL/urls.py  — v3

Registro en urls.py principal:
    path('finantial/', include('applications.FINANTIAL.urls', namespace='finantial')),
"""
from django.urls import path
from . import views

app_name = 'finantial'

urlpatterns = [

    # ── Dashboard ─────────────────────────────────────────────────────────────
    path('finaciera_v1/comprobantes/dashboard', views.PaymentDashboardView.as_view(), name='dashboard'),

    # ── Comprobantes ──────────────────────────────────────────────────────────
    path('finaciera_v1/comprobantes/',                   views.PaymentDocumentListView.as_view(),   name='document-list'),
    path('finaciera_v1/comprobantes/nuevo/',             views.PaymentDocumentCreateView.as_view(), name='document-create'),
    path('finaciera_v1/comprobantes/<int:pk>/',          views.PaymentDocumentDetailView.as_view(), name='document-detail'),
    path('finaciera_v1/comprobantes/<int:pk>/editar/',   views.PaymentDocumentUpdateView.as_view(), name='document-update'),
    path('finaciera_v1/comprobantes/<int:pk>/eliminar/', views.PaymentDocumentDeleteView.as_view(), name='document-delete'),

    # ── Transacciones ─────────────────────────────────────────────────────────
    path('finaciera_v1/transacciones/',                      views.PaymentTransactionListView.as_view(),   name='transaction-list'),
    path('finaciera_v1/transacciones/nueva/',                views.PaymentTransactionCreateView.as_view(), name='transaction-create'),
    path('finaciera_v1/transacciones/<int:pk>/',             views.PaymentTransactionDetailView.as_view(), name='transaction-detail'),
    path('finaciera_v1/transacciones/<int:pk>/editar/',      views.PaymentTransactionUpdateView.as_view(), name='transaction-update'),
    path('finaciera_v1/transacciones/<int:pk>/eliminar/',    views.PaymentTransactionDeleteView.as_view(), name='transaction-delete'),
    path('finaciera_v1/transacciones/<int:pk>/confirmar/',   views.ConfirmTransactionView.as_view(),       name='transaction-confirm'),

    # ── Movimientos bancarios ─────────────────────────────────────────────────
    path('finaciera_v1/movimientos/',                    views.BankMovementsListView.as_view(),   name='movement-list'),
    path('finaciera_v1/movimientos/nuevo/',              views.BankMovementsCreateView.as_view(), name='movement-create'),
    path('finaciera_v1/movimientos/<int:pk>/',           views.BankMovementsDetailView.as_view(), name='movement-detail'),
    path('finaciera_v1/movimientos/<int:pk>/editar/',    views.BankMovementsUpdateView.as_view(), name='movement-update'),
    path('finaciera_v1/movimientos/<int:pk>/eliminar/',  views.BankMovementsDeleteView.as_view(), name='movement-delete'),

    # ── Cierre mensual  (SAP F.16) ────────────────────────────────────────────
    path('finaciera_v1/cierres/',                        views.MonthlyClosureListView.as_view(),  name='closure-list'),
    path('finaciera_v1/cierres/nuevo/',                  views.MonthlyClosureCreateView.as_view(),name='closure-create'),
    path('finaciera_v1/cierres/<int:pk>/',               views.MonthlyClosureDetailView.as_view(),name='closure-detail'),
    path('finaciera_v1/cierres/<int:pk>/cerrar/',        views.CloseMonthView.as_view(),          name='closure-close'),
    path('finaciera_v1/cierres/<int:pk>/aprobar/',       views.ApproveClosureView.as_view(),      name='closure-approve'),
    path('finaciera_v1/cierres/<int:pk>/reabrir/',       views.ReopenClosureView.as_view(),       name='closure-reopen'),

    # ── Asientos contables  (SAP FB50) ────────────────────────────────────────
    path('finaciera_v1/asientos/',                       views.JournalEntryListView.as_view(),    name='journal-list'),
    path('finaciera_v1/asientos/nuevo/',                 views.JournalEntryCreateView.as_view(),  name='journal-create'),
    path('finaciera_v1/asientos/<int:pk>/',              views.JournalEntryDetailView.as_view(),  name='journal-detail'),
    path('finaciera_v1/asientos/<int:pk>/contabilizar/', views.PostJournalEntryView.as_view(),    name='journal-post'),

    # ── Plan de cuentas  (SAP FS00) ───────────────────────────────────────────
    path('finaciera_v1/plan-cuentas/',                   views.AccountingAccountListView.as_view(),  name='chart-of-accounts'),
    path('finaciera_v1/plan-cuentas/nueva/',             views.AccountingAccountCreateView.as_view(),name='account-create'),

    # ── Centros de costos  (SAP KS01) ────────────────────────────────────────
    path('finaciera_v1/centros-costo/',                  views.CostCenterListView.as_view(),   name='costcenter-list'),
    path('finaciera_v1/centros-costo/nuevo/',            views.CostCenterCreateView.as_view(), name='costcenter-create'),

    # ── Tipos de cambio  (SAP OB08) ───────────────────────────────────────────
    path('finaciera_v1/tipos-cambio/',                   views.ExchangeRateListView.as_view(),   name='exchangerate-list'),
    path('finaciera_v1/tipos-cambio/nuevo/',             views.ExchangeRateCreateView.as_view(), name='exchangerate-create'),

    # ── Códigos de impuesto  (SAP FTXP) ──────────────────────────────────────
    path('finaciera_v1/codigos-impuesto/',               views.TaxCodeListView.as_view(),   name='taxcode-list'),
    path('finaciera_v1/codigos-impuesto/nuevo/',         views.TaxCodeCreateView.as_view(), name='taxcode-create'),

    # ── Seguimiento por ítem ──────────────────────────────────────────────────
    path('finaciera_v1/seguimiento/',                    views.ItemTrackingView.as_view(), name='item-tracking'),

    # ── Antigüedad de cartera ─────────────────────────────────────────────────
    path('finaciera_v1/cartera/',                        views.ARAgingView.as_view(),            name='ar-aging'),

    # ── Flujo de caja proyectado ──────────────────────────────────────────────
    path('finaciera_v1/flujo-caja/',                     views.CashFlowView.as_view(),           name='cashflow'),

    # ── Importación de extracto bancario ─────────────────────────────────────
    path('finaciera_v1/importar-extracto/',              views.BankStatementImportView.as_view(),name='import-statement'),

    # ── PLE SUNAT ─────────────────────────────────────────────────────────────
    path('finaciera_v1/ple/',                            views.PLEExportView.as_view(),          name='ple-export'),

    # ── Estado de Resultados P&L ──────────────────────────────────────────────
    path('finaciera_v1/estado-resultados/',              views.ProfitLossView.as_view(),         name='profit-loss'),

    # ── API / AJAX ────────────────────────────────────────────────────────────
    path('api/item/<int:pk>/pending/',      views.ItemPendingAmountView.as_view(),      name='api-item-pending'),
    path('api/documento/<int:pk>/pending/', views.DocumentPendingAmountView.as_view(),  name='api-doc-pending'),
    path('api/tipo-cambio/',                views.ExchangeRateAPIView.as_view(),        name='api-exchange-rate'),
]