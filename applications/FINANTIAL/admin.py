
"""
FINANTIAL/admin.py
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    MovementType, BankMovements, Conciliation,

    ExpenseSubCategories, IncomeSubCategories,
    CostCenter, AccountingAccount, ExchangeRate, TaxCode,
    MonthlyClosure, JournalEntry, JournalEntryLine,
    PaymentDocument, PaymentAllocation,
    PaymentTransaction, PaymentTransactionLine,
)


# =============================================================================
# RESOURCES
# =============================================================================
class _Res(resources.ModelResource):
    pass

def _res(model):
    return type(f'{model.__name__}Resource', (_Res,), {'Meta': type('Meta', (), {'model': model, 'import_id_fields': ['id']})})

BankMovementsResource        = _res(BankMovements)
ConciliationResource         = _res(Conciliation)
CostCenterResource           = _res(CostCenter)
AccountingAccountResource    = _res(AccountingAccount)
ExchangeRateResource         = _res(ExchangeRate)
TaxCodeResource              = _res(TaxCode)
MonthlyClosureResource       = _res(MonthlyClosure)
JournalEntryResource         = _res(JournalEntry)
PaymentDocumentResource      = _res(PaymentDocument)
PaymentTransactionResource   = _res(PaymentTransaction)
PaymentTransactionLineResource = _res(PaymentTransactionLine)


# =============================================================================
# HELPERS
# =============================================================================
def _badge(text, color):
    return format_html('<strong style="color:{}">{}</strong>', color, text)

STATUS_COLORS = {
    # Documents
    'PENDING':   '#f5365c', 'PARTIAL': '#fb6340', 'PAID': '#2dce89',
    'CANCELLED': '#8898aa', 'REVERSED': '#8898aa',
    # Transactions
    'DRAFT': '#8898aa', 'CONFIRMED': '#2dce89',
    # Closures
    'OPEN': '#11cdef', 'CLOSED': '#fb6340', 'APPROVED': '#2dce89', 'REOPENED': '#f5365c',
}


# =============================================================================
# INLINES
# =============================================================================
class PaymentAllocationInline(admin.TabularInline):
    model            = PaymentAllocation
    extra            = 0
    fields           = ['item', 'allocated_amount', 'notes']
    show_change_link = True

class PaymentTransactionLineInline(admin.TabularInline):
    model            = PaymentTransactionLine
    extra            = 0
    fields           = ['document', 'amount_applied', 'notes']
    show_change_link = True

class ConciliationInline(admin.TabularInline):
    model       = Conciliation
    fk_name     = 'idMovOrigin'
    extra       = 0
    fields      = ['type', 'payment_document', 'idMovArrival', 'amountReconcilied', 'source', 'status']
    readonly_fields = ['status']

class JournalEntryLineInline(admin.TabularInline):
    model            = JournalEntryLine
    extra            = 2
    fields           = ['account', 'debit', 'credit', 'description', 'cost_center', 'tax_code']
    show_change_link = True


# =============================================================================
# CATÁLOGOS SIMPLES
# =============================================================================
@admin.register(MovementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'flow_badge', 'description', 'active')
    list_filter   = ('flow', 'active')
    search_fields = ('name',)

    @admin.display(description='Flujo', ordering='flow')
    def flow_badge(self, obj):
        c = '#2dce89' if obj.flow == '1' else '#f5365c'
        return _badge(obj.get_flow_display(), c)


@admin.register(ExpenseSubCategories)
class ExpenseSubCategoriesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'description', 'active')
    list_filter   = ('active',)
    search_fields = ('name',)


@admin.register(IncomeSubCategories)
class IncomeSubCategoriesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'description', 'active')
    list_filter   = ('active',)
    search_fields = ('name',)

# =============================================================================
# COST CENTER  (SAP KS01)
# =============================================================================
@admin.register(CostCenter)
class CostCenterAdmin(ImportExportModelAdmin):
    resource_class = CostCenterResource
    list_display   = ('code', 'name', 'tin', 'responsible', 'valid_from', 'valid_to', 'active')
    list_filter    = ('active', 'tin')
    search_fields  = ('code', 'name', 'tin__tinName')
    readonly_fields = ('created', 'modified')


# =============================================================================
# ACCOUNTING ACCOUNT  (SAP FS00)
# =============================================================================
@admin.register(AccountingAccount)
class AccountingAccountAdmin(ImportExportModelAdmin):
    resource_class = AccountingAccountResource
    list_display   = ('code', 'name', 'type_badge', 'currency', 'bank_account', 'active')
    list_filter    = ('account_type', 'currency', 'active')
    search_fields  = ('code', 'name', 'description')
    readonly_fields = ('created', 'modified')

    @admin.display(description='Tipo', ordering='account_type')
    def type_badge(self, obj):
        colors = {
            'ASSET': '#5e72e4', 'LIABILITY': '#f5365c', 'EQUITY': '#fb6340',
            'INCOME': '#2dce89', 'EXPENSE': '#f5365c', 'BANK': '#11cdef', 'TAX': '#fb6340',
        }
        return _badge(obj.get_account_type_display(), colors.get(obj.account_type, '#adb5bd'))


# =============================================================================
# EXCHANGE RATE  (SAP OB08)
# =============================================================================
@admin.register(ExchangeRate)
class ExchangeRateAdmin(ImportExportModelAdmin):
    resource_class = ExchangeRateResource
    list_display   = ('id', 'from_currency', 'to_currency', 'rate_date', 'rate', 'source')
    list_filter    = ('from_currency', 'to_currency', 'source')
    date_hierarchy = 'rate_date'
    search_fields  = ('source',)

    actions = ['duplicate_for_today']

    @admin.action(description='Duplicar para hoy')
    def duplicate_for_today(self, request, queryset):
        count = 0
        for r in queryset:
            ExchangeRate.objects.get_or_create(
                from_currency=r.from_currency,
                to_currency=r.to_currency,
                rate_date=timezone.now().date(),
                defaults={'rate': r.rate, 'source': r.source},
            )
            count += 1
        self.message_user(request, f'{count} tipo(s) de cambio duplicado(s) para hoy.')


# =============================================================================
# TAX CODE  (SAP FTXP)
# =============================================================================
@admin.register(TaxCode)
class TaxCodeAdmin(ImportExportModelAdmin):
    resource_class = TaxCodeResource
    list_display   = ('code', 'name', 'tax_type', 'rate', 'accounting_account', 'active')
    list_filter    = ('tax_type', 'active')
    search_fields  = ('code', 'name')
    readonly_fields = ('created', 'modified')


# =============================================================================
# BANK MOVEMENTS
# =============================================================================
@admin.register(BankMovements)
class BankMovementsAdmin(ImportExportModelAdmin):
    resource_class = BankMovementsResource
    inlines        = [ConciliationInline]

    list_display   = (
        'id', 'date', 'idAccount', 'tin', 'flow_badge',
        'movementType', 'description', 'opNumber',
        'amount', 'amountReconcilied', 'pending_display',
        'conciliated_badge', 'cost_center',
    )
    list_filter    = ('conciliated', 'movementType__flow', 'movementType', 'tin', 'idAccount')
    search_fields  = ('description', 'opNumber', 'tin__tinName', 'idAccount__nickName')
    readonly_fields = ('tin', 'amountReconcilied', 'conciliated', 'is_reconciled_with_payment', 'created', 'modified')
    date_hierarchy = 'date'

    fieldsets = (
        ('Cuenta y tipo',     {'fields': (('idAccount', 'tin'), ('movementType', 'date', 'cost_center'))}),
        ('Datos',             {'fields': (('description', 'opNumber'), 'justification', ('originDestination', 'idDoc'))}),
        ('Subcategorías',     {'classes': ('collapse',), 'fields': (('expenseSubCategory', 'incomeSubCategory'),)}),
        ('Montos',            {'fields': (('amount', 'equivalentAmount', 'balance'), ('amountReconcilied', 'conciliated'))}),
        ('Integración pagos', {'fields': ('payment_transaction', 'is_reconciled_with_payment')}),
        ('Archivo',           {'fields': ('pdf_file',)}),
        ('Auditoría',         {'classes': ('collapse',), 'fields': (('created', 'modified'),)}),
    )

    actions = ['recalculate_reconciled']

    @admin.display(description='Flujo')
    def flow_badge(self, obj):
        if not obj.movementType_id: return '—'
        c, l = ('#2dce89','▼ Ingreso') if obj.movementType.is_ingreso else ('#f5365c','▲ Egreso')
        return _badge(l, c)

    @admin.display(description='Pendiente')
    def pending_display(self, obj):
        p = obj.amount - obj.amountReconcilied
        return _badge(f'{p:.2f}', '#f5365c' if p > 0 else '#2dce89')

    @admin.display(description='Estado', ordering='conciliated')
    def conciliated_badge(self, obj):
        return _badge('✓ Conciliado' if obj.conciliated else '● Pendiente',
                      '#2dce89' if obj.conciliated else '#f5365c')

    @admin.action(description='Recalcular montos conciliados')
    def recalculate_reconciled(self, request, queryset):
        for mov in queryset: mov.recalculate_reconciled()
        self.message_user(request, f'{queryset.count()} movimiento(s) recalculado(s).')


# =============================================================================
# CONCILIATION
# =============================================================================
@admin.register(Conciliation)
class ConciliationAdmin(ImportExportModelAdmin):
    resource_class = ConciliationResource
    list_display   = ('id', 'type_badge', 'idMovOrigin', 'payment_document', 'idMovArrival',
                      'amountReconcilied', 'source_badge', 'status', 'created')
    list_filter    = ('type', 'source', 'status')
    search_fields  = ('idMovOrigin__description', 'payment_document__doc_number')
    readonly_fields = ('status', 'created', 'modified')

    @admin.display(description='Tipo', ordering='type')
    def type_badge(self, obj):
        colors = {'0':'#5e72e4','1':'#11cdef','2':'#fb6340','3':'#f5365c'}
        return _badge(obj.get_type_display(), colors.get(obj.type,'#adb5bd'))

    @admin.display(description='Origen', ordering='source')
    def source_badge(self, obj):
        return _badge(obj.get_source_display(), '#2dce89' if obj.source=='PAYMENT' else '#8898aa')




# =============================================================================
# MONTHLY CLOSURE  (SAP F.16)
# =============================================================================
@admin.register(MonthlyClosure)
class MonthlyClosureAdmin(ImportExportModelAdmin):
    resource_class = MonthlyClosureResource
    list_display   = (
        'id', 'account', 'tin', 'period_label_display',
        'opening_balance', 'total_ingresos', 'total_egresos', 'closing_balance',
        'movements_count', 'unreconciled_alert', 'status_badge', 'is_locked',
        'closed_by', 'approved_by',
    )
    list_filter    = ('status', 'is_locked', 'tin', 'period_year', 'period_month')
    search_fields  = ('account__nickName', 'tin__tinName')
    readonly_fields = (
        'total_ingresos', 'total_egresos', 'closing_balance',
        'movements_count', 'unreconciled_count',
        'closed_by', 'closed_at', 'approved_by', 'approved_at',
        'created', 'modified',
    )

    fieldsets = (
        ('Período',    {'fields': (('account', 'tin'), ('period_year', 'period_month'), 'opening_balance', 'notes')}),
        ('Totales',    {'fields': (('total_ingresos', 'total_egresos', 'closing_balance'), ('movements_count', 'unreconciled_count'))}),
        ('Estado',     {'fields': (('status', 'is_locked'),)}),
        ('Cierre',     {'fields': ('closed_by', 'closed_at')}),
        ('Aprobación', {'fields': ('approved_by', 'approved_at', 'reopen_reason')}),
        ('Auditoría',  {'classes': ('collapse',), 'fields': (('created', 'modified'),)}),
    )

    actions = ['calculate_totals_action', 'close_periods', 'approve_periods']

    @admin.display(description='Período')
    def period_label_display(self, obj):
        return obj.period_label

    @admin.display(description='Sin conciliar')
    def unreconciled_alert(self, obj):
        if obj.unreconciled_count and obj.unreconciled_count > 0:
            return _badge(f'⚠ {obj.unreconciled_count}', '#fb6340')
        return _badge('✓ 0', '#2dce89')

    @admin.display(description='Estado', ordering='status')
    def status_badge(self, obj):
        return _badge(obj.get_status_display(), STATUS_COLORS.get(obj.status, '#adb5bd'))

    @admin.action(description='Recalcular totales del período')
    def calculate_totals_action(self, request, queryset):
        for c in queryset: c.calculate_totals()
        self.message_user(request, f'{queryset.count()} período(s) recalculado(s).')

    @admin.action(description='Cerrar períodos seleccionados')
    def close_periods(self, request, queryset):
        count = 0
        for c in queryset.filter(status__in=('OPEN','REOPENED')):
            try:
                c.close(request.user)
                count += 1
            except Exception as e:
                self.message_user(request, f'Error en {c}: {e}', level='ERROR')
        self.message_user(request, f'{count} período(s) cerrado(s).')

    @admin.action(description='Aprobar períodos seleccionados')
    def approve_periods(self, request, queryset):
        count = 0
        for c in queryset.filter(status='CLOSED'):
            try:
                c.approve(request.user)
                count += 1
            except Exception: pass
        self.message_user(request, f'{count} período(s) aprobado(s).')


# =============================================================================
# JOURNAL ENTRY  (SAP FB50)
# =============================================================================
@admin.register(JournalEntry)
class JournalEntryAdmin(ImportExportModelAdmin):
    resource_class = JournalEntryResource
    inlines        = [JournalEntryLineInline]
    list_display   = (
        'id', 'reference', 'entry_date', 'period_display',
        'tin', 'cost_center', 'currency',
        'total_debit_display', 'total_credit_display',
        'balanced_badge', 'source_badge', 'posted_badge',
    )
    list_filter    = ('is_posted', 'source', 'currency', 'tin', 'period_year', 'period_month')
    search_fields  = ('reference', 'description', 'tin__tinName')
    readonly_fields = ('is_posted', 'posted_by', 'posted_at', 'created', 'modified')
    date_hierarchy = 'entry_date'

    fieldsets = (
        ('Asiento',     {'fields': (('reference', 'entry_date'), ('period_year', 'period_month'), ('currency', 'tin', 'cost_center'), 'description', 'source')}),
        ('Estado',      {'fields': ('is_posted', 'posted_by', 'posted_at')}),
        ('Vinculación', {'classes': ('collapse',), 'fields': ('payment_transaction',)}),
        ('Auditoría',   {'classes': ('collapse',), 'fields': (('created', 'modified'),)}),
    )

    actions = ['post_entries']

    @admin.display(description='Período')
    def period_display(self, obj):
        return f'{obj.period_month:02d}/{obj.period_year}'

    @admin.display(description='Debe')
    def total_debit_display(self, obj):
        return format_html('<span style="color:#5e72e4">{}</span>', f'{obj.total_debit:.2f}')

    @admin.display(description='Haber')
    def total_credit_display(self, obj):
        return format_html('<span style="color:#2dce89">{}</span>', f'{obj.total_credit:.2f}')

    @admin.display(description='Balance')
    def balanced_badge(self, obj):
        if obj.is_balanced:
            return _badge('✓ Balanceado', '#2dce89')
        diff = obj.total_debit - obj.total_credit
        return _badge(f'✗ Dif: {diff:.2f}', '#f5365c')

    @admin.display(description='Origen', ordering='source')
    def source_badge(self, obj):
        colors = {'MANUAL':'#8898aa','PAYMENT':'#5e72e4','CONCILIATION':'#11cdef','CLOSURE':'#fb6340'}
        return _badge(obj.get_source_display(), colors.get(obj.source,'#adb5bd'))

    @admin.display(description='Estado', ordering='is_posted')
    def posted_badge(self, obj):
        return _badge('✓ Contabilizado' if obj.is_posted else '○ Borrador',
                      '#2dce89' if obj.is_posted else '#8898aa')

    @admin.action(description='Contabilizar asientos seleccionados')
    def post_entries(self, request, queryset):
        count = 0
        for entry in queryset.filter(is_posted=False):
            try:
                entry.post(request.user)
                count += 1
            except Exception as e:
                self.message_user(request, f'Error en AST-{entry.id}: {e}', level='ERROR')
        self.message_user(request, f'{count} asiento(s) contabilizado(s).')


@admin.register(JournalEntryLine)
class JournalEntryLineAdmin(admin.ModelAdmin):
    list_display  = ('id', 'entry', 'account', 'debit', 'credit', 'description', 'cost_center', 'tax_code')
    list_filter   = ('account__account_type', 'cost_center', 'tax_code')
    search_fields = ('entry__reference', 'account__code', 'account__name', 'description')
    readonly_fields = ('created', 'modified')


# =============================================================================
# PAYMENT DOCUMENT
# =============================================================================
@admin.register(PaymentDocument)
class PaymentDocumentAdmin(ImportExportModelAdmin):
    resource_class = PaymentDocumentResource
    inlines        = [PaymentAllocationInline]

    list_display = (
        'id', 'doc_type', 'doc_number', 'direction_badge',
        'tin_issuer', 'tin_receiver',
        'currency', 'gross_amount', 'net_amount',
        'paid_amount', 'pending_display', 'status_badge',
        'cost_center', 'tax_code', 'issue_date', 'created_by',
    )
    list_filter   = ('status', 'direction', 'doc_type', 'currency',
                     'tin_issuer', 'has_detraction', 'has_retention', 'cost_center')
    search_fields = ('doc_number', 'short_description', 'tin_issuer__tinName', 'tin_receiver__tinName')
    readonly_fields = ('paid_amount', 'pending_amount', 'status', 'created', 'modified')
    date_hierarchy  = 'issue_date'

    fieldsets = (
        ('Identificación',   {'fields': (('doc_type', 'doc_number', 'direction'),)}),
        ('Partes',           {'fields': (('tin_issuer', 'tin_receiver'), ('client', 'supplier'))}),
        ('Fechas',           {'fields': (('issue_date', 'due_date'), ('declare_month', 'declare_year'))}),
        ('Montos',           {'fields': (('currency', 'exchange_rate'), ('gross_amount', 'tax_amount', 'net_amount'), ('paid_amount', 'pending_amount'))}),
        ('Estado',           {'fields': (('status', 'annotation'),)}),
        ('Detracciones',     {'classes': ('collapse',), 'fields': (('has_detraction', 'detraction_amount'), ('has_retention', 'retention_amount'))}),
        ('Clasificación SAP',{'fields': (('account_category', 'cost_center', 'tax_code'), 'short_description', 'description')}),
        ('Archivos',         {'classes': ('collapse',), 'fields': (('pdf_file', 'xml_file'),)}),
        ('Auditoría',        {'classes': ('collapse',), 'fields': ('created_by', ('created', 'modified'))}),
    )

    actions = ['recalculate_paid_amounts', 'mark_cancelled']

    @admin.display(description='Dirección', ordering='direction')
    def direction_badge(self, obj):
        c = {'IN':'#2dce89','OUT':'#f5365c','INT':'#11cdef'}.get(obj.direction,'#adb5bd')
        l = {'IN':'▼ IN','OUT':'▲ OUT','INT':'⇄ INT'}.get(obj.direction, obj.direction)
        return _badge(l, c)

    @admin.display(description='Estado', ordering='status')
    def status_badge(self, obj):
        return _badge(obj.get_status_display(), STATUS_COLORS.get(obj.status,'#adb5bd'))

    @admin.display(description='Pendiente')
    def pending_display(self, obj):
        return _badge(f'{obj.pending_amount:.2f}',
                      '#f5365c' if obj.pending_amount > 0 else '#2dce89')

    @admin.action(description='Recalcular montos pagados')
    def recalculate_paid_amounts(self, request, queryset):
        for doc in queryset: doc.recalculate_paid()
        self.message_user(request, f'{queryset.count()} comprobante(s) recalculado(s).')

    @admin.action(description='Marcar como Anulado')
    def mark_cancelled(self, request, queryset):
        n = queryset.update(status='CANCELLED')
        self.message_user(request, f'{n} comprobante(s) anulado(s).')


# =============================================================================
# PAYMENT TRANSACTION
# =============================================================================
@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ImportExportModelAdmin):
    resource_class = PaymentTransactionResource
    inlines        = [PaymentTransactionLineInline]

    list_display = (
        'id', 'transaction_date', 'pay_method',
        'tin_payer', 'tin_receiver',
        'bank_account_display', 'bank_movement_link',
        'currency', 'amount', 'reconciled_amount',
        'cost_center', 'status_badge', 'journal_link', 'created_by',
    )
    list_filter   = ('status', 'pay_method', 'currency', 'tin_payer', 'tin_receiver', 'cost_center')
    search_fields = ('reference', 'notes', 'bank_account__nickName', 'tin_payer__tinName')
    readonly_fields = ('reconciled_amount', 'created', 'modified')
    date_hierarchy  = 'transaction_date'

    fieldsets = (
        ('Datos del pago', {'fields': (('reference', 'pay_method', 'transaction_date'), ('currency', 'exchange_rate', 'amount', 'reconciled_amount'), ('bank_account', 'bank_movement', 'cost_center'))}),
        ('Partes',         {'fields': (('tin_payer', 'tin_receiver'), ('client', 'supplier'))}),
        ('Estado',         {'fields': ('status', 'voucher_file', 'notes')}),
        ('Auditoría',      {'classes': ('collapse',), 'fields': ('created_by', ('created', 'modified'))}),
    )

    actions = ['confirm_transactions', 'reverse_transactions']

    @admin.display(description='Cuenta', ordering='bank_account__nickName')
    def bank_account_display(self, obj):
        if obj.bank_account:
            return f'[{obj.bank_account.nickName}] {obj.bank_account.idTin.tinName if obj.bank_account.idTin else ""}'
        return '—'

    @admin.display(description='Mov. Banco')
    def bank_movement_link(self, obj):
        if obj.bank_movement_id:
            return _badge(f'MOV-{obj.bank_movement_id}', '#2dce89')
        return '—'

    @admin.display(description='Estado', ordering='status')
    def status_badge(self, obj):
        return _badge(obj.get_status_display(), STATUS_COLORS.get(obj.status,'#adb5bd'))

    @admin.display(description='Asiento')
    def journal_link(self, obj):
        try:
            je = obj.journal_entry
            return _badge(f'AST-{je.id}', '#5e72e4' if je.is_posted else '#8898aa')
        except Exception:
            return '—'

    @admin.action(description='Confirmar transacciones seleccionadas')
    def confirm_transactions(self, request, queryset):
        count = 0
        for tx in queryset.filter(status='DRAFT'):
            try:
                tx.confirm()
                count += 1
            except Exception as e:
                self.message_user(request, f'Error TX-{tx.id}: {e}', level='ERROR')
        self.message_user(request, f'{count} transacción(es) confirmada(s).')

    @admin.action(description='Revertir transacciones confirmadas')
    def reverse_transactions(self, request, queryset):
        count = 0
        for tx in queryset.filter(status='CONFIRMED'):
            tx.reverse()
            count += 1
        self.message_user(request, f'{count} transacción(es) revertida(s).')


@admin.register(PaymentTransactionLine)
class PaymentTransactionLineAdmin(ImportExportModelAdmin):
    resource_class  = PaymentTransactionLineResource
    list_display    = ('id', 'transaction', 'tx_date', 'document', 'doc_num',
                       'amount_applied', 'overpay_badge', 'notes')
    list_filter     = ('transaction__status', 'document__doc_type', 'document__direction')
    search_fields   = ('transaction__reference', 'document__doc_number', 'notes')
    readonly_fields = ('created', 'modified')

    @admin.display(description='Fecha TX', ordering='transaction__transaction_date')
    def tx_date(self, obj):
        return obj.transaction.transaction_date

    @admin.display(description='Nro. Doc', ordering='document__doc_number')
    def doc_num(self, obj):
        return obj.document.doc_number or f'Doc #{obj.document.id}'

    @admin.display(description='Sobre-pago')
    def overpay_badge(self, obj):
        if obj.amount_applied > obj.document.pending_amount:
            return _badge(f'⚠ +{obj.amount_applied - obj.document.pending_amount:.2f}', '#f5365c')
        return _badge('OK', '#2dce89')