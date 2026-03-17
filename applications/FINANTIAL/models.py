"""
FINANTIAL/models.py
===================
App financiera completa de Davinchy Corporation.

Arquitectura corporativa:
  CLIENTS → DAV LLC (Holding USA) → DAV1/DAV2/DAV3/RUC10 (Subsidiarias Perú) → SUPPLIERS

Módulos en este archivo:
  1. Cuentas bancarias          — Account
  2. Tipos de movimiento        — MovementType
  3. Movimientos bancarios      — BankMovements
  4. Conciliaciones             — Conciliation
  5. Documentos financieros     — FinancialDocuments, DocumentsUploaded
  6. Categorías de gasto/ingreso — ExpenseSubCategories, IncomeSubCategories
  7. Cuentas de clientes        — bankAccountsClient
  8. Comprobantes de pago       — PaymentDocument, PaymentAllocation
  9. Transacciones de pago      — PaymentTransaction, PaymentTransactionLine
"""

import re
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum, Q, F

from model_utils.models import TimeStampedModel

# ── Imports externos (otras apps del proyecto) ────────────────────────────────
from applications.cuentas.models import Tin, Account      # noqa
from applications.COMERCIAL.stakeholders.models import client, supplier       # noqa
from applications.COMERCIAL.sales.models import Items     # noqa  (para PaymentAllocation)

from .managers import BankMovementsManager, ConciliationManager, PaymentDocumentManager,PaymentTransactionManager

# =============================================================================
# CONSTANTES COMPARTIDAS
# =============================================================================
CURRENCY_CHOICES = [
    ('0', 'PEN'),
    ('1', 'USD'),
]

PAYMENT_CURRENCY_CHOICES = [
    ('PEN', 'Soles (PEN)'),
    ('USD', 'Dólares (USD)'),
    ('EUR', 'Euros (EUR)'),
]

DOC_TYPE_CHOICES = [
    ('FAC', 'Factura'),
    ('BOL', 'Boleta de Venta'),
    ('RHE', 'Recibo por Honorarios'),
    ('NCR', 'Nota de Crédito'),
    ('NDB', 'Nota de Débito'),
    ('DUA', 'DUA (Importación)'),
    ('GRE', 'Guía de Remisión'),
    ('LIQ', 'Liquidación'),
    ('PLA', 'Planilla'),
    ('IMP', 'Impuesto / Tributo'),
    ('PER', 'Percepción'),
    ('OTR', 'Otro'),
]

PAYMENT_DIRECTION = [
    ('IN',  'Ingreso  (cobro al cliente)'),
    ('OUT', 'Egreso   (pago al proveedor)'),
    ('INT', 'Interno  (holding ↔ subsidiaria)'),
]

DOC_STATUS_CHOICES = [
    ('PENDING',   'Pendiente'),
    ('PARTIAL',   'Pago parcial'),
    ('PAID',      'Pagado'),
    ('CANCELLED', 'Anulado'),
    ('REVERSED',  'Revertido'),
]

ANNOTATION_CHOICES = [
    ('ADVANCE', 'Anticipo'),
    ('BALANCE', 'Saldo / Pago final'),
    ('FULL',    'Total'),
]

PAY_METHOD_CHOICES = [
    ('TRANSFER', 'Transferencia bancaria'),
    ('CHECK',    'Cheque'),
    ('CASH',     'Efectivo'),
    ('CARD',     'Tarjeta'),
    ('OTHER',    'Otro'),
]



# =============================================================================
# 1. CATEGORÍAS DE GASTO / INGRESO
# =============================================================================
class ExpenseSubCategories(TimeStampedModel):
    name        = models.CharField('Nombre', max_length=60)
    description = models.CharField('Descripción', max_length=150, null=True, blank=True)
    active      = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name        = 'Subcategoría de gasto'
        verbose_name_plural = 'Subcategorías de gasto'
        ordering            = ['name']

    def __str__(self):
        return self.name

class IncomeSubCategories(TimeStampedModel):
    name        = models.CharField('Nombre', max_length=60)
    description = models.CharField('Descripción', max_length=150, null=True, blank=True)
    active      = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name        = 'Subcategoría de ingreso'
        verbose_name_plural = 'Subcategorías de ingreso'
        ordering            = ['name']

    def __str__(self):
        return self.name

# =============================================================================
# 3. CUENTAS DE CLIENTES (bankAccountsClient)
# =============================================================================
class bankAccountsClient(TimeStampedModel):
    idClient = models.ForeignKey(client, on_delete=models.CASCADE, related_name='bank_accounts')
    account  = models.CharField('Número de cuenta', max_length=30)
    bankName = models.CharField('Banco', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name        = 'Cuenta bancaria de cliente'
        verbose_name_plural = 'Cuentas bancarias de clientes'

    def __str__(self):
        return f"{self.idClient} | {self.account}"

# =============================================================================
# 4. DOCUMENTOS FINANCIEROS
# =============================================================================
class DocumentsUploaded(TimeStampedModel):
    """Archivo adjunto genérico para movimientos bancarios."""
    file        = models.FileField('Archivo', upload_to='financial_docs/')
    description = models.CharField('Descripción', max_length=150, null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='uploaded_docs'
    )

    class Meta:
        verbose_name        = 'Documento adjunto'
        verbose_name_plural = 'Documentos adjuntos'

    def __str__(self):
        return self.description or f'Doc #{self.id}'

class FinancialDocuments(TimeStampedModel):
    """
    Documento financiero existente (facturas, boletas, etc.)
    Compatible con el sistema de conciliación.
    """
    docNumber        = models.CharField('Número', max_length=50, null=True, blank=True)
    docType          = models.CharField('Tipo', max_length=10, null=True, blank=True)
    amount           = models.DecimalField('Monto', max_digits=14, decimal_places=2, default=0)
    amountReconcilied= models.DecimalField('Monto conciliado', max_digits=14, decimal_places=2, default=0)
    idTin            = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='financial_docs')
    description      = models.CharField('Descripción', max_length=200, null=True, blank=True)
    date             = models.DateField('Fecha', null=True, blank=True)

    class Meta:
        verbose_name        = 'Documento financiero'
        verbose_name_plural = 'Documentos financieros'
        ordering            = ['-date']

    def __str__(self):
        return f"{self.docType or ''} {self.docNumber or '—'} | {self.amount}"

    @property
    def pending_amount(self):
        return self.amount - self.amountReconcilied


# =============================================================================
# 5. TIPO DE MOVIMIENTO (catálogo)
# =============================================================================
class MovementType(TimeStampedModel):
    """
    Catálogo de tipos de movimiento bancario.
    Reemplaza el CharField binario EGRESO/INGRESO del modelo original.
    Permite clasificar: Transferencia, Gasto operativo, Impuesto, Comisión, etc.
    """
    EGRESO  = '0'
    INGRESO = '1'

    FLOW_CHOICES = [
        (EGRESO,  'Egreso'),
        (INGRESO, 'Ingreso'),
    ]

    name        = models.CharField('Nombre', max_length=60)
    flow        = models.CharField('Flujo', max_length=1, choices=FLOW_CHOICES)
    description = models.CharField('Descripción', max_length=150, null=True, blank=True)
    active      = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name        = 'Tipo de movimiento'
        verbose_name_plural = 'Tipos de movimiento'
        ordering            = ['flow', 'name']

    def __str__(self):
        label = dict(self.FLOW_CHOICES).get(self.flow, '')
        return f'[{label}] {self.name}'

    @property
    def is_egreso(self):
        return self.flow == self.EGRESO

    @property
    def is_ingreso(self):
        return self.flow == self.INGRESO


# =============================================================================
# 6. MOVIMIENTOS BANCARIOS
# =============================================================================

class BankMovements(TimeStampedModel):
    """
    Movimiento bancario real — importado del banco o registrado manualmente.

    Cambios vs modelo original:
      + tin              → FK a Tin (empresa dueña, auto-asignada desde Account)
      + movementType     → FK a MovementType (reemplaza transactionType CharField binario)
      + payment_transaction → FK a PaymentTransaction (integración con comprobantes)
      + is_reconciled_with_payment → flag para distinguir conciliaciones automáticas
      + justification    → TextField (era CharField 250)
      + opNumber         → max_length=50 (era 15)
      - transactionType  → eliminado (reemplazado por movementType FK)
      - flagUpdate       → eliminado (TimeStampedModel.modified lo cubre)
    """

    idAccount = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='bank_movements',
        verbose_name='Cuenta bancaria'
    )
    tin = models.ForeignKey(
        Tin, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='bank_movements',
        verbose_name='Empresa',
        help_text='Auto-asignada desde la cuenta al guardar'
    )
    idDoc = models.ForeignKey(
        DocumentsUploaded, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='bank_movements_doc',
        verbose_name='Documento adjunto'
    )
    movementType = models.ForeignKey(
        MovementType, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='movements',
        verbose_name='Tipo de movimiento'
    )

    # ── Integración con comprobantes de pago ──────────────────────────────────
    payment_transaction = models.ForeignKey(
        'PaymentTransaction',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='bank_movements',
        verbose_name='Transacción de pago vinculada',
        help_text='Se asigna automáticamente al confirmar una PaymentTransaction'
    )
    is_reconciled_with_payment = models.BooleanField(
        '¿Conciliado desde pagos?',
        default=False
    )

    # ── Datos del movimiento ──────────────────────────────────────────────────
    date        = models.DateField('Fecha')
    description = models.CharField('Descripción', max_length=100, null=True, blank=True)
    opNumber    = models.CharField('Nro. operación', max_length=50, null=True, blank=True)
    justification = models.TextField('Justificación', null=True, blank=True)

    # ── Partes externas ───────────────────────────────────────────────────────
    originDestination  = models.ForeignKey(
        client, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='bank_movements',
        verbose_name='Origen / Destino'
    )
    expenseSubCategory = models.ForeignKey(
        ExpenseSubCategories, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='Subcategoría gasto'
    )
    incomeSubCategory = models.ForeignKey(
        IncomeSubCategories, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='Subcategoría ingreso'
    )

    # ── Montos ────────────────────────────────────────────────────────────────
    amount           = models.DecimalField('Monto', max_digits=14, decimal_places=2)
    equivalentAmount = models.DecimalField('Monto equivalente', max_digits=14, decimal_places=2, null=True, blank=True)
    balance          = models.DecimalField('Saldo', max_digits=14, decimal_places=2, null=True, blank=True)
    amountReconcilied= models.DecimalField('Monto conciliado', max_digits=14, decimal_places=2, default=0)

    # ── Estado ────────────────────────────────────────────────────────────────
    conciliated = models.BooleanField('Conciliado', default=False)
    pdf_file    = models.FileField('PDF voucher', upload_to='vouchers_pdfs/', null=True, blank=True)

    objects = BankMovementsManager()

    class Meta:
        ordering            = ['date', 'created']
        verbose_name        = 'Movimiento bancario'
        verbose_name_plural = 'Movimientos bancarios'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['conciliated']),
            models.Index(fields=['tin']),
            models.Index(fields=['idAccount']),
            models.Index(fields=['payment_transaction']),
        ]

    def __str__(self):
        nick = self.idAccount.nickName if self.idAccount else '—'
        curr = self.idAccount.get_currency_display() if self.idAccount else ''
        return f"{nick} | {self.opNumber or '—'} | {self.date} | {curr} {self.amount} [{self.amountReconcilied}]"

    def save(self, *args, **kwargs):
        # Auto-asignar Tin desde la cuenta
        if not self.tin_id and self.idAccount_id and self.idAccount.idTin_id:
            self.tin = self.idAccount.idTin
        super().save(*args, **kwargs)

    @property
    def flow(self):
        if self.movementType_id:
            return 'EGRESO' if self.movementType.is_egreso else 'INGRESO'
        return None

    @property
    def pending_reconciliation(self):
        return self.amount - self.amountReconcilied

    @property
    def is_fully_reconciled(self):
        return self.amountReconcilied >= self.amount

    def recalculate_reconciled(self):
        """Recalcula amountReconcilied y el flag conciliated desde Conciliation."""
        result  = Conciliation.objects.SumaMontosConciliadosPorMovimientosOr(self.pk)
        sum_doc = result.get('sumDoc') or Decimal('0')
        sum_mov = result.get('sumMov') or Decimal('0')
        total   = sum_doc + sum_mov
        BankMovements.objects.filter(pk=self.pk).update(
            amountReconcilied=total,
            conciliated=(total >= self.amount)
        )


# =============================================================================
# 7. CONCILIACIONES
# =============================================================================

class Conciliation(TimeStampedModel):
    """
    Reconcilia un movimiento bancario con un documento o con otro movimiento.
    Nueva: campo source para rastrear si fue creada manualmente o desde pagos.
    """

    DOC    = '0'
    MOV    = '1'
    OPBANK = '2'
    IMP    = '3'

    TYPE_CHOICES = [
        (DOC,    'Documento'),
        (MOV,    'Movimiento'),
        (OPBANK, 'Com. Bancarias'),
        (IMP,    'Impuestos'),
    ]

    SOURCE_MANUAL  = 'MANUAL'
    SOURCE_PAYMENT = 'PAYMENT'

    SOURCE_CHOICES = [
        (SOURCE_MANUAL,  'Manual'),
        (SOURCE_PAYMENT, 'Desde pagos'),
    ]

    type = models.CharField('Tipo', max_length=1, choices=TYPE_CHOICES)

    idMovOrigin  = models.ForeignKey(
        BankMovements, on_delete=models.CASCADE,
        related_name='mov_origen', verbose_name='Mov. origen'
    )
    idMovArrival = models.ForeignKey(
        BankMovements, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='mov_destino', verbose_name='Mov. destino'
    )
    idDoc = models.ForeignKey(
        FinancialDocuments, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='doc_conciliation', verbose_name='Documento'
    )

    amountReconcilied = models.DecimalField('Monto conciliado', max_digits=14, decimal_places=2)
    equivalentAmount  = models.DecimalField('Monto equivalente', max_digits=14, decimal_places=3, default=0)
    status            = models.BooleanField('Procesado', default=False)
    source            = models.CharField('Origen', max_length=10, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)

    objects = ConciliationManager()

    class Meta:
        ordering            = ['created']
        verbose_name        = 'Conciliación'
        verbose_name_plural = 'Conciliaciones'
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['status']),
            models.Index(fields=['source']),
        ]

    def __str__(self):
        return f"{self.id} | {self.get_type_display()} | {self.amountReconcilied}"

# =============================================================================
# 8. COMPROBANTES DE PAGO (PaymentDocument)
# =============================================================================

class PaymentDocument(TimeStampedModel):
    """
    Comprobante de pago emitido o recibido.

    Flujos:
      IN  — Cliente → DAV LLC (cobro)
      OUT — Subsidiaria → Proveedor (pago)
      INT — Holding ↔ Subsidiaria (transferencia interna)

    El vínculo con Quote/IntQuote/WorkOrder se infiere desde:
      PaymentAllocation → item → item.idTrafoQuote / idTrafoIntQuote / idWorkOrder
    """

    ACCOUNT_CHOICES = [
        ('ADUANAS',  'Agente de aduana'),
        ('CAJA_CH',  'Caja chica'),
        ('CAJA_GEN', 'Caja general'),
        ('CAJA_VTA', 'Caja general ventas'),
        ('RHE_GEN',  'RHE general'),
        ('ADICIONAL','Adicional'),
        ('PERSONAL', 'Personal'),
        ('PLANILLA', 'Planilla'),
        ('RENTA',    'Renta'),
    ]

    # Identificación
    doc_type   = models.CharField('Tipo', max_length=3, choices=DOC_TYPE_CHOICES, default='FAC')
    doc_number = models.CharField('Número', max_length=50, null=True, blank=True)
    direction  = models.CharField('Dirección', max_length=3, choices=PAYMENT_DIRECTION, default='OUT')

    # Partes
    tin_issuer   = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='docs_issued',   verbose_name='Empresa emisora')
    tin_receiver = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='docs_received', verbose_name='Empresa receptora')
    client       = models.ForeignKey(client, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_docs',  verbose_name='Cliente externo')
    supplier     = models.ForeignKey(supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_docs', verbose_name='Proveedor externo')

    # Fechas
    issue_date    = models.DateField('Fecha de emisión', null=True, blank=True)
    due_date      = models.DateField('Fecha de vencimiento', null=True, blank=True)
    declare_month = models.PositiveSmallIntegerField('Mes declaración', choices=[(i, i) for i in range(1, 13)], null=True, blank=True)
    declare_year  = models.PositiveSmallIntegerField('Año declaración', null=True, blank=True)

    # Montos
    currency       = models.CharField('Moneda', max_length=3, choices=PAYMENT_CURRENCY_CHOICES, default='USD')
    exchange_rate  = models.DecimalField('T.C.', max_digits=10, decimal_places=4, default=1)
    gross_amount   = models.DecimalField('Monto bruto', max_digits=14, decimal_places=2, default=0)
    tax_amount     = models.DecimalField('IGV / IVA', max_digits=14, decimal_places=2, default=0)
    net_amount     = models.DecimalField('Monto neto', max_digits=14, decimal_places=2, default=0)
    paid_amount    = models.DecimalField('Pagado', max_digits=14, decimal_places=2, default=0)
    pending_amount = models.DecimalField('Pendiente', max_digits=14, decimal_places=2, default=0)

    # Estado
    status     = models.CharField('Estado', max_length=10, choices=DOC_STATUS_CHOICES, default='PENDING')
    annotation = models.CharField('Anotación', max_length=10, choices=ANNOTATION_CHOICES, null=True, blank=True)

    # Detracciones / retenciones
    has_detraction    = models.BooleanField('¿Detracción?', default=False)
    detraction_amount = models.DecimalField('Monto detracción', max_digits=14, decimal_places=2, default=0)
    has_retention     = models.BooleanField('¿Retención?', default=False)
    retention_amount  = models.DecimalField('Monto retención', max_digits=14, decimal_places=2, default=0)

    # Contabilidad
    account_category  = models.CharField('Categoría contable', max_length=10, choices=ACCOUNT_CHOICES, null=True, blank=True)
    cost_center       = models.CharField('Centro de costo', max_length=50, null=True, blank=True)
    short_description = models.CharField('Descripción corta', max_length=150, null=True, blank=True)
    description       = models.TextField('Descripción detallada', null=True, blank=True)

    # Archivos
    xml_file = models.FileField('XML', upload_to='payment_docs/xml/', null=True, blank=True)
    pdf_file = models.FileField('PDF', upload_to='payment_docs/pdf/', null=True, blank=True)

    # Auditoría
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_docs_created')

    objects = PaymentDocumentManager()

    class Meta:
        verbose_name        = 'Comprobante de pago'
        verbose_name_plural = 'Comprobantes de pago'
        ordering            = ['-issue_date', '-created']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['direction']),
            models.Index(fields=['tin_issuer']),
            models.Index(fields=['tin_receiver']),
            models.Index(fields=['issue_date']),
        ]

    def __str__(self):
        return f"{self.get_doc_type_display()} {self.doc_number or '—'} | {self.currency} {self.gross_amount}"

    def save(self, *args, **kwargs):
        if not self.net_amount:
            self.net_amount = self.gross_amount - self.tax_amount
        self.pending_amount = self.net_amount - self.paid_amount
        if self.status not in ('CANCELLED', 'REVERSED'):
            if self.paid_amount >= self.net_amount > 0:
                self.status = 'PAID'
            elif self.paid_amount > 0:
                self.status = 'PARTIAL'
            else:
                self.status = 'PENDING'
        super().save(*args, **kwargs)

    def recalculate_paid(self):
        total = self.transaction_lines.filter(
            transaction__status='CONFIRMED'
        ).aggregate(s=Sum('amount_applied'))['s'] or 0
        self.paid_amount = total
        self.save()

    # Traversal helpers (sin FK extra en BD)
    @property
    def related_quotes(self):
        return set(
            a.item.idTrafoQuote
            for a in self.allocations.select_related('item__idTrafoQuote').all()
            if a.item.idTrafoQuote_id
        )

    @property
    def related_int_quotes(self):
        return set(
            a.item.idTrafoIntQuote
            for a in self.allocations.select_related('item__idTrafoIntQuote').all()
            if a.item.idTrafoIntQuote_id
        )

    @property
    def related_work_orders(self):
        return set(
            a.item.idWorkOrder
            for a in self.allocations.select_related('item__idWorkOrder').all()
            if a.item.idWorkOrder_id
        )

class PaymentAllocation(TimeStampedModel):
    """
    Asigna un comprobante a un Item específico con monto parcial.
    El pedido (QUO/INT/WO) se infiere desde item → idTrafoQuote / idTrafoIntQuote / idWorkOrder.
    """
    document = models.ForeignKey(PaymentDocument, on_delete=models.CASCADE, related_name='allocations', verbose_name='Comprobante')
    item     = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='payment_allocations', verbose_name='Ítem')
    allocated_amount = models.DecimalField('Monto asignado', max_digits=14, decimal_places=2, default=0)
    notes            = models.CharField('Notas', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name        = 'Asignación de comprobante'
        verbose_name_plural = 'Asignaciones de comprobante'
        unique_together     = [('document', 'item')]

    def __str__(self):
        return f"{self.document} → Item {self.item.seq} ({self.allocated_amount})"

    @property
    def order_context(self):
        item = self.item
        if item.idTrafoQuote_id:
            return ('QUO', item.idTrafoQuote)
        if item.idTrafoIntQuote_id:
            return ('INT', item.idTrafoIntQuote)
        if item.idWorkOrder_id:
            return ('WO', item.idWorkOrder)
        return (None, None)


# =============================================================================
# 9. TRANSACCIONES DE PAGO
# =============================================================================

class PaymentTransaction(TimeStampedModel):
    """
    Movimiento de caja/banco que liquida uno o varios comprobantes.

    Flujo:
      1. Guardado como DRAFT → no afecta comprobantes
      2. confirm() → status=CONFIRMED, actualiza paid_amount en cada documento
      3. Si hay bank_movement vinculado → conciliación automática con Conciliation
    """

    STATUS_TX = [
        ('DRAFT',     'Borrador'),
        ('CONFIRMED', 'Confirmado'),
        ('REVERSED',  'Revertido'),
    ]

    # Datos del pago
    reference        = models.CharField('Referencia / Nro. Op.', max_length=80, null=True, blank=True)
    pay_method       = models.CharField('Método', max_length=10, choices=PAY_METHOD_CHOICES, default='TRANSFER')
    transaction_date = models.DateField('Fecha de pago')
    currency         = models.CharField('Moneda', max_length=3, choices=PAYMENT_CURRENCY_CHOICES, default='USD')
    exchange_rate    = models.DecimalField('T.C.', max_digits=10, decimal_places=4, default=1)
    amount           = models.DecimalField('Monto total', max_digits=14, decimal_places=2)
    reconciled_amount= models.DecimalField('Monto conciliado', max_digits=14, decimal_places=2, default=0)

    # Partes
    tin_payer    = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_paid',     verbose_name='Empresa pagadora')
    tin_receiver = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_received', verbose_name='Empresa receptora')
    client       = models.ForeignKey(client, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_transactions')
    supplier     = models.ForeignKey(supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_transactions')

    # Cuenta bancaria (centro de costo implícito por Tin)
    bank_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='payment_transactions',
        verbose_name='Cuenta bancaria'
    )
    # Movimiento bancario para conciliación automática
    bank_movement = models.ForeignKey(
        BankMovements, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='payment_transactions_linked',
        verbose_name='Movimiento bancario',
        help_text='Opcional: vincula con el movimiento real para conciliación automática'
    )

    notes        = models.TextField('Notas', null=True, blank=True)
    status       = models.CharField('Estado', max_length=10, choices=STATUS_TX, default='DRAFT')
    voucher_file = models.FileField('Voucher', upload_to='payment_tx/', null=True, blank=True)
    created_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_created')

    objects = PaymentTransactionManager()

    class Meta:
        verbose_name        = 'Transacción de pago'
        verbose_name_plural = 'Transacciones de pago'
        ordering            = ['-transaction_date', '-created']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['transaction_date']),
        ]

    def __str__(self):
        return f"TX-{self.id} | {self.transaction_date} | {self.currency} {self.amount}"

    def confirm(self):
        """
        1. status → CONFIRMED
        2. Actualiza paid_amount en cada comprobante vinculado
        3. Si hay bank_movement → crea Conciliation automáticamente
        """
        if self.status == 'CONFIRMED':
            return
        self.status = 'CONFIRMED'
        self.save()
        for line in self.transaction_lines.all():
            line.document.recalculate_paid()
        if self.bank_movement_id:
            self._auto_conciliate()

    def _auto_conciliate(self):
        """
        Crea Conciliation vinculando bank_movement con FinancialDocuments
        que coincidan por doc_number con los comprobantes de las líneas.
        """
        for line in self.transaction_lines.select_related('document').all():
            fin_doc = FinancialDocuments.objects.filter(
                docNumber=line.document.doc_number
            ).first()
            if fin_doc:
                Conciliation.objects.get_or_create(
                    type=Conciliation.DOC,
                    idMovOrigin=self.bank_movement,
                    idDoc=fin_doc,
                    defaults={
                        'amountReconcilied': line.amount_applied,
                        'source': Conciliation.SOURCE_PAYMENT,
                    }
                )

    def reverse(self):
        """Revierte la transacción y recalcula los comprobantes."""
        self.status = 'REVERSED'
        self.save()
        for line in self.transaction_lines.all():
            line.document.recalculate_paid()

class PaymentTransactionLine(TimeStampedModel):
    """Aplica un monto de la transacción a un comprobante específico."""
    transaction    = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, related_name='transaction_lines', verbose_name='Transacción')
    document       = models.ForeignKey(PaymentDocument, on_delete=models.CASCADE, related_name='transaction_lines', verbose_name='Comprobante')
    amount_applied = models.DecimalField('Monto aplicado', max_digits=14, decimal_places=2)
    notes          = models.CharField('Notas', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name        = 'Línea de transacción'
        verbose_name_plural = 'Líneas de transacción'

    def __str__(self):
        return f"{self.transaction} → {self.document} ({self.amount_applied})"

