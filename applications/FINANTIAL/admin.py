
"""
FINANTIAL/admin.py
"""
from django.contrib import admin
from django.utils.html import format_html

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    MovementType, BankMovements, Conciliation,
    FinancialDocuments, DocumentsUploaded,
    ExpenseSubCategories, IncomeSubCategories, bankAccountsClient,
    PaymentDocument, PaymentAllocation,
    PaymentTransaction, PaymentTransactionLine,
)

# =============================================================================
# RESOURCES
# =============================================================================

class BankMovementsResource(resources.ModelResource):
    class Meta:
        model = BankMovements
        import_id_fields = ['id']

class ConciliationResource(resources.ModelResource):
    class Meta:
        model = Conciliation
        import_id_fields = ['id']

class FinancialDocumentsResource(resources.ModelResource):
    class Meta:
        model = FinancialDocuments
        import_id_fields = ['id']

class PaymentDocumentResource(resources.ModelResource):
    class Meta:
        model = PaymentDocument
        import_id_fields = ['id']

class PaymentTransactionResource(resources.ModelResource):
    class Meta:
        model = PaymentTransaction
        import_id_fields = ['id']

class PaymentTransactionLineResource(resources.ModelResource):
    class Meta:
        model = PaymentTransactionLine
        import_id_fields = ['id']


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
    model      = Conciliation
    fk_name    = 'idMovOrigin'
    extra      = 0
    fields     = ['type', 'idDoc', 'idMovArrival', 'amountReconcilied', 'source', 'status']
    readonly_fields = ['status']


# =============================================================================
# CATÁLOGOS
# =============================================================================
@admin.register(MovementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'flow_badge', 'description', 'active')
    list_filter  = ('flow', 'active')
    search_fields = ('name',)

    @admin.display(description='Flujo', ordering='flow')
    def flow_badge(self, obj):
        c = '#2dce89' if obj.flow == '1' else '#f5365c'
        return format_html('<strong style="color:{}">{}</strong>', c, obj.get_flow_display())


@admin.register(ExpenseSubCategories)
class ExpenseSubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'active')
    list_filter  = ('active',)
    search_fields = ('name',)


@admin.register(IncomeSubCategories)
class IncomeSubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'active')
    list_filter  = ('active',)
    search_fields = ('name',)


@admin.register(bankAccountsClient)
class bankAccountsClientAdmin(admin.ModelAdmin):
    list_display  = ('id', 'idClient', 'account', 'bankName')
    search_fields = ('account', 'idClient__name', 'bankName')

# =============================================================================
# BANK MOVEMENTS
# =============================================================================
@admin.register(BankMovements)
class BankMovementsAdmin(ImportExportModelAdmin):
    resource_class = BankMovementsResource
    inlines        = [ConciliationInline]

    list_display = (
        'id', 'date', 'idAccount', 'tin', 'flow_badge',
        'movementType', 'description', 'opNumber',
        'amount', 'amountReconcilied', 'pending_display',
        'conciliated_badge', 'payment_tx_link',
    )
    list_filter  = (
        'conciliated', 'movementType__flow', 'movementType',
        'tin', 'idAccount', 'is_reconciled_with_payment',
    )
    search_fields  = ('description', 'opNumber', 'tin__tinName', 'idAccount__nickName')
    readonly_fields = (
        'tin', 'amountReconcilied', 'conciliated',
        'is_reconciled_with_payment', 'created', 'modified',
    )
    date_hierarchy = 'date'

    fieldsets = (
        ('Cuenta y tipo', {
            'fields': (('idAccount', 'tin'), ('movementType', 'date'))
        }),
        ('Datos', {
            'fields': (('description', 'opNumber'), 'justification', ('originDestination', 'idDoc'))
        }),
        ('Subcategorías', {
            'classes': ('collapse',),
            'fields': (('expenseSubCategory', 'incomeSubCategory'),)
        }),
        ('Montos', {
            'fields': (
                ('amount', 'equivalentAmount', 'balance'),
                ('amountReconcilied', 'conciliated'),
            )
        }),
        ('Integración con pagos', {
            'fields': ('payment_transaction', 'is_reconciled_with_payment')
        }),
        ('Archivo', {'fields': ('pdf_file',)}),
        ('Auditoría', {'classes': ('collapse',), 'fields': (('created', 'modified'),)}),
    )

    actions = ['recalculate_reconciled']

    @admin.display(description='Flujo')
    def flow_badge(self, obj):
        if not obj.movementType_id:
            return '—'
        c, l = ('#2dce89', '▼ Ingreso') if obj.movementType.is_ingreso else ('#f5365c', '▲ Egreso')
        return format_html('<strong style="color:{}">{}</strong>', c, l)

    @admin.display(description='Pendiente')
    def pending_display(self, obj):
        p = obj.amount - obj.amountReconcilied
        c = '#f5365c' if p > 0 else '#2dce89'
        return format_html('<span style="color:{}">{}</span>', c, f'{p:.2f}')

    @admin.display(description='Estado', ordering='conciliated')
    def conciliated_badge(self, obj):
        c, l = ('#2dce89', '✓ Conciliado') if obj.conciliated else ('#f5365c', '● Pendiente')
        return format_html('<strong style="color:{}">{}</strong>', c, l)

    @admin.display(description='TX Pago')
    def payment_tx_link(self, obj):
        if obj.payment_transaction_id:
            return format_html('<span style="color:#5e72e4">TX-{}</span>', obj.payment_transaction_id)
        return '—'

    @admin.action(description='Recalcular montos conciliados')
    def recalculate_reconciled(self, request, queryset):
        count = 0
        for mov in queryset:
            mov.recalculate_reconciled()
            count += 1
        self.message_user(request, f'{count} movimiento(s) recalculado(s).')


# =============================================================================
# CONCILIATION
# =============================================================================
@admin.register(Conciliation)
class ConciliationAdmin(ImportExportModelAdmin):
    resource_class = ConciliationResource
    list_display   = ('id', 'type_badge', 'idMovOrigin', 'idDoc', 'idMovArrival',
                      'amountReconcilied', 'source_badge', 'status', 'created')
    list_filter    = ('type', 'source', 'status')
    search_fields  = ('idMovOrigin__description', 'idDoc__docNumber')
    readonly_fields = ('status', 'created', 'modified')

    @admin.display(description='Tipo', ordering='type')
    def type_badge(self, obj):
        colors = {'0': '#5e72e4', '1': '#11cdef', '2': '#fb6340', '3': '#f5365c'}
        return format_html('<strong style="color:{}">{}</strong>',
                           colors.get(obj.type, '#adb5bd'), obj.get_type_display())

    @admin.display(description='Origen', ordering='source')
    def source_badge(self, obj):
        c = '#2dce89' if obj.source == 'PAYMENT' else '#8898aa'
        return format_html('<span style="color:{}">{}</span>', c, obj.get_source_display())


# =============================================================================
# FINANCIAL DOCUMENTS
# =============================================================================
@admin.register(FinancialDocuments)
class FinancialDocumentsAdmin(ImportExportModelAdmin):
    resource_class = FinancialDocumentsResource
    list_display   = ('id', 'docType', 'docNumber', 'idTin', 'amount',
                      'amountReconcilied', 'pending_display', 'date')
    list_filter    = ('docType', 'idTin')
    search_fields  = ('docNumber', 'description', 'idTin__tinName')
    date_hierarchy = 'date'

    @admin.display(description='Pendiente')
    def pending_display(self, obj):
        p = obj.pending_amount
        c = '#f5365c' if p > 0 else '#2dce89'
        return format_html('<span style="color:{}">{:.2f}</span>', c, p)


@admin.register(DocumentsUploaded)
class DocumentsUploadedAdmin(admin.ModelAdmin):
    list_display  = ('id', 'description', 'uploaded_by', 'created')
    search_fields = ('description',)


# =============================================================================
# PAYMENT DOCUMENT
# =============================================================================
@admin.register(PaymentDocument)
class PaymentDocumentAdmin(ImportExportModelAdmin):
    resource_class = PaymentDocumentResource
    inlines        = [PaymentAllocationInline]

    list_display = (
        'id', 'doc_type', 'doc_number', 'direction_badge',
        'tin_issuer', 'tin_receiver', 'client', 'supplier',
        'currency', 'gross_amount', 'net_amount',
        'paid_amount', 'pending_amount', 'status_badge',
        'issue_date', 'created_by',
    )
    list_filter   = ('status', 'direction', 'doc_type', 'currency', 'tin_issuer', 'has_detraction', 'has_retention')
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
        ('Contabilidad',     {'classes': ('collapse',), 'fields': (('account_category', 'cost_center'), 'short_description', 'description')}),
        ('Archivos',         {'classes': ('collapse',), 'fields': (('pdf_file', 'xml_file'),)}),
        ('Auditoría',        {'classes': ('collapse',), 'fields': ('created_by', ('created', 'modified'))}),
    )

    actions = ['recalculate_paid_amounts', 'mark_cancelled']

    @admin.display(description='Dirección', ordering='direction')
    def direction_badge(self, obj):
        c = {'IN': '#2dce89', 'OUT': '#f5365c', 'INT': '#11cdef'}.get(obj.direction, '#adb5bd')
        l = {'IN': '▼ IN',    'OUT': '▲ OUT',   'INT': '⇄ INT'}.get(obj.direction, obj.direction)
        return format_html('<strong style="color:{}">{}</strong>', c, l)

    @admin.display(description='Estado', ordering='status')
    def status_badge(self, obj):
        colors = {'PENDING': '#f5365c', 'PARTIAL': '#fb6340', 'PAID': '#2dce89',
                  'CANCELLED': '#8898aa', 'REVERSED': '#8898aa'}
        return format_html('<strong style="color:{}">{}</strong>',
                           colors.get(obj.status, '#adb5bd'), obj.get_status_display())

    @admin.action(description='Recalcular montos pagados')
    def recalculate_paid_amounts(self, request, queryset):
        for doc in queryset:
            doc.recalculate_paid()
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
        'status_badge', 'created_by',
    )
    list_filter   = ('status', 'pay_method', 'currency', 'tin_payer', 'tin_receiver')
    search_fields = ('reference', 'notes', 'bank_account__nickName', 'tin_payer__tinName')
    readonly_fields = ('reconciled_amount', 'created', 'modified')
    date_hierarchy  = 'transaction_date'

    fieldsets = (
        ('Datos del pago', {'fields': (('reference', 'pay_method', 'transaction_date'), ('currency', 'exchange_rate', 'amount', 'reconciled_amount'), ('bank_account', 'bank_movement'))}),
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
            return format_html('<span style="color:#2dce89">MOV-{}</span>', obj.bank_movement_id)
        return '—'

    @admin.display(description='Estado', ordering='status')
    def status_badge(self, obj):
        colors = {'DRAFT': '#8898aa', 'CONFIRMED': '#2dce89', 'REVERSED': '#f5365c'}
        return format_html('<strong style="color:{}">{}</strong>',
                           colors.get(obj.status, '#adb5bd'), obj.get_status_display())

    @admin.action(description='Confirmar transacciones seleccionadas')
    def confirm_transactions(self, request, queryset):
        count = 0
        for tx in queryset.filter(status='DRAFT'):
            tx.confirm()
            count += 1
        self.message_user(request, f'{count} transacción(es) confirmada(s).')

    @admin.action(description='Revertir transacciones seleccionadas')
    def reverse_transactions(self, request, queryset):
        count = 0
        for tx in queryset.filter(status='CONFIRMED'):
            tx.reverse()
            count += 1
        self.message_user(request, f'{count} transacción(es) revertida(s).')


@admin.register(PaymentTransactionLine)
class PaymentTransactionLineAdmin(ImportExportModelAdmin):
    resource_class = PaymentTransactionLineResource
    list_display   = ('id', 'transaction', 'tx_date', 'document', 'doc_num', 'amount_applied', 'notes')
    list_filter    = ('transaction__status', 'document__doc_type', 'document__direction')
    search_fields  = ('transaction__reference', 'document__doc_number', 'notes')
    readonly_fields = ('created', 'modified')

    @admin.display(description='Fecha TX', ordering='transaction__transaction_date')
    def tx_date(self, obj):
        return obj.transaction.transaction_date

    @admin.display(description='Nro. Doc', ordering='document__doc_number')
    def doc_num(self, obj):
        return obj.document.doc_number or f'Doc #{obj.document.id}'