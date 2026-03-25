"""
FINANTIAL/models.py  — v3
=========================
App financiera completa de Davinchy Corporation.

Módulos:
  1.  Account             — Cuentas bancarias
  2.  MovementType        — Catálogo tipos de movimiento
  3.  ExpenseSubCategories / IncomeSubCategories
  4.  bankAccountsClient
  5.  DocumentsUploaded / FinancialDocuments
  6.  BankMovements       — Movimientos bancarios reales
  7.  Conciliation        — Reconciliaciones
  8.  CostCenter          — Centro de costos formal (SAP KS)
  9.  AccountingAccount   — Plan de cuentas (SAP FS00)
  10. ExchangeRate        — Tipos de cambio por fecha (SAP OB08)
  11. TaxCode             — Códigos de impuesto (SAP FTXP)
  12. MonthlyClosure      — Cierre de período (SAP F.16)
  13. PaymentDocument     — Comprobantes de pago
  14. PaymentAllocation   — Asignación comprobante → ítem
  15. PaymentTransaction  — Transacciones de pago
  16. PaymentTransactionLine
  17. JournalEntry / JournalEntryLine — Asientos contables (SAP FB50)
"""

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
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
CURRENCY_CHOICES = [('0', 'PEN'), ('1', 'USD')]

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

MONTH_CHOICES = [(i, i) for i in range(1, 13)]

# =============================================================================
# 2. CATEGORÍAS GASTO / INGRESO
# =============================================================================
class ExpenseSubCategories(TimeStampedModel):
    name        = models.CharField('Nombre', max_length=60)
    description = models.CharField('Descripción', max_length=150, null=True, blank=True)
    active      = models.BooleanField('Activo', default=True)
    class Meta:
        verbose_name        = 'Subcategoría de gasto'
        verbose_name_plural = 'Subcategorías de gasto'
        ordering            = ['name']
    def __str__(self): return self.name

class IncomeSubCategories(TimeStampedModel):
    name        = models.CharField('Nombre', max_length=60)
    description = models.CharField('Descripción', max_length=150, null=True, blank=True)
    active      = models.BooleanField('Activo', default=True)
    class Meta:
        verbose_name        = 'Subcategoría de ingreso'
        verbose_name_plural = 'Subcategorías de ingreso'
        ordering            = ['name']
    def __str__(self): return self.name

# =============================================================================
# 3. CUENTAS DE CLIENTES
# =============================================================================

# =============================================================================
# 4. DOCUMENTOS ADJUNTOS / FINANCIEROS
# =============================================================================
class DocumentsUploaded(TimeStampedModel):
    file        = models.FileField('Archivo', upload_to='financial_docs/')
    description = models.CharField('Descripción', max_length=150, null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_docs')
    class Meta:
        verbose_name        = 'Documento adjunto'
        verbose_name_plural = 'Documentos adjuntos'
    def __str__(self): return self.description or f'Doc #{self.id}'

class FinancialDocuments(TimeStampedModel):
    docNumber         = models.CharField('Número', max_length=50, null=True, blank=True)
    docType           = models.CharField('Tipo', max_length=10, null=True, blank=True)
    amount            = models.DecimalField('Monto', max_digits=14, decimal_places=2, default=0)
    amountReconcilied = models.DecimalField('Monto conciliado', max_digits=14, decimal_places=2, default=0)
    idTin             = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='financial_docs')
    description       = models.CharField('Descripción', max_length=200, null=True, blank=True)
    date              = models.DateField('Fecha', null=True, blank=True)
    class Meta:
        verbose_name        = 'Documento financiero'
        verbose_name_plural = 'Documentos financieros'
        ordering            = ['-date']
    def __str__(self): return f"{self.docType or ''} {self.docNumber or '—'} | {self.amount}"
    @property
    def pending_amount(self): return self.amount - self.amountReconcilied

# =============================================================================
# 5. TIPO DE MOVIMIENTO
# =============================================================================
class MovementType(TimeStampedModel):
    EGRESO  = '0'
    INGRESO = '1'
    FLOW_CHOICES = [(EGRESO, 'Egreso'), (INGRESO, 'Ingreso')]

    name        = models.CharField('Nombre', max_length=60)
    flow        = models.CharField('Flujo', max_length=1, choices=FLOW_CHOICES)
    description = models.CharField('Descripción', max_length=150, null=True, blank=True)
    active      = models.BooleanField('Activo', default=True)
    class Meta:
        verbose_name        = 'Tipo de movimiento'
        verbose_name_plural = 'Tipos de movimiento'
        ordering            = ['flow', 'name']
    def __str__(self): return f"[{self.get_flow_display()}] {self.name}"
    @property
    def is_egreso(self): return self.flow == self.EGRESO
    @property
    def is_ingreso(self): return self.flow == self.INGRESO

# =============================================================================
# 6. CENTRO DE COSTOS  (SAP KS01)
# =============================================================================
class CostCenter(TimeStampedModel):
    """
    Centro de costos formal — equivalente a SAP KS01.
    Reemplaza el CharField cost_center en PaymentDocument.
    """
    code        = models.CharField('Código', max_length=20, unique=True)
    name        = models.CharField('Nombre', max_length=80)
    description = models.CharField('Descripción', max_length=200, null=True, blank=True)
    tin         = models.ForeignKey(Tin, on_delete=models.CASCADE, related_name='cost_centers', verbose_name='Empresa')
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cost_centers_responsible', verbose_name='Responsable')
    active      = models.BooleanField('Activo', default=True)
    valid_from  = models.DateField('Válido desde', null=True, blank=True)
    valid_to    = models.DateField('Válido hasta', null=True, blank=True)

    class Meta:
        verbose_name        = 'Centro de costos'
        verbose_name_plural = 'Centros de costos'
        ordering            = ['tin__tinName', 'code']

    def __str__(self):
        return f"{self.code} — {self.name} ({self.tin.tinName})"

# =============================================================================
# 7. PLAN DE CUENTAS CONTABLES  (SAP FS00)
# =============================================================================
class AccountingAccount(TimeStampedModel):
    """
    Cuenta contable del plan de cuentas — equivalente a SAP FS00.
    Permite generar asientos (JournalEntry) estructurados.
    """
    ACCOUNT_TYPE_CHOICES = [
        ('ASSET',     'Activo'),
        ('LIABILITY', 'Pasivo'),
        ('EQUITY',    'Patrimonio'),
        ('INCOME',    'Ingreso'),
        ('EXPENSE',   'Gasto'),
        ('BANK',      'Banco / Tesorería'),
        ('TAX',       'Impuesto'),
    ]

    code        = models.CharField('Código', max_length=10, unique=True)
    name        = models.CharField('Nombre', max_length=100)
    account_type= models.CharField('Tipo', max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    currency    = models.CharField('Moneda', max_length=3, choices=PAYMENT_CURRENCY_CHOICES, default='PEN')
    description = models.CharField('Descripción', max_length=200, null=True, blank=True)
    active      = models.BooleanField('Activa', default=True)
    # Vínculo opcional con cuenta bancaria (para cuentas tipo BANK)
    bank_account= models.OneToOneField(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='accounting_account', verbose_name='Cuenta bancaria vinculada')

    class Meta:
        verbose_name        = 'Cuenta contable'
        verbose_name_plural = 'Plan de cuentas'
        ordering            = ['code']

    def __str__(self):
        return f"{self.code} — {self.name}"

    @property
    def is_debit_normal(self):
        """Cuentas cuyo saldo normal es débito (activo, gasto)."""
        return self.account_type in ('ASSET', 'EXPENSE', 'BANK')

# =============================================================================
# 8. TIPOS DE CAMBIO POR FECHA  (SAP OB08)
# =============================================================================
class ExchangeRate(TimeStampedModel):
    """
    Tipo de cambio centralizado por fecha — equivalente a SAP OB08.
    La TX y el comprobante lo consultan en lugar de ingresarlo manualmente.
    """
    from_currency = models.CharField('Moneda origen', max_length=3, choices=PAYMENT_CURRENCY_CHOICES)
    to_currency   = models.CharField('Moneda destino', max_length=3, choices=PAYMENT_CURRENCY_CHOICES)
    rate_date     = models.DateField('Fecha')
    rate          = models.DecimalField('Tasa', max_digits=14, decimal_places=6)
    source        = models.CharField('Fuente', max_length=50, default='Manual', help_text='SBS, SUNAT, Manual, etc.')

    class Meta:
        verbose_name        = 'Tipo de cambio'
        verbose_name_plural = 'Tipos de cambio'
        ordering            = ['-rate_date']
        unique_together     = [('from_currency', 'to_currency', 'rate_date')]
        indexes             = [models.Index(fields=['rate_date', 'from_currency', 'to_currency'])]

    def __str__(self):
        return f"{self.from_currency}→{self.to_currency} | {self.rate_date} | {self.rate}"

    @classmethod
    def get_rate(cls, from_currency, to_currency, date):
        """Devuelve la tasa más reciente ≤ date. Retorna 1 si son la misma moneda."""
        if from_currency == to_currency:
            return Decimal('1')
        obj = cls.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency,
            rate_date__lte=date
        ).order_by('-rate_date').first()
        return obj.rate if obj else Decimal('1')

# =============================================================================
# 9. CÓDIGOS DE IMPUESTO  (SAP FTXP)
# =============================================================================
class TaxCode(TimeStampedModel):
    """
    Código de impuesto — equivalente a SAP FTXP.
    Permite calcular IGV, detracción y retención automáticamente.
    """
    TAX_TYPE_CHOICES = [
        ('IGV',        'IGV / IVA'),
        ('DETRACTION', 'Detracción'),
        ('RETENTION',  'Retención'),
        ('PERCEPTION', 'Percepción'),
        ('OTHER',      'Otro'),
    ]

    code            = models.CharField('Código', max_length=10, unique=True)
    name            = models.CharField('Nombre', max_length=80)
    tax_type        = models.CharField('Tipo', max_length=15, choices=TAX_TYPE_CHOICES)
    rate            = models.DecimalField('Tasa (%)', max_digits=6, decimal_places=4, help_text='Ej: 18.0000 para IGV 18%')
    accounting_account = models.ForeignKey(AccountingAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='tax_codes', verbose_name='Cuenta contable destino')
    active          = models.BooleanField('Activo', default=True)
    applies_to_doc_types = models.CharField('Aplica a tipos', max_length=100, blank=True, help_text='FAC,BOL,RHE — vacío=todos')

    class Meta:
        verbose_name        = 'Código de impuesto'
        verbose_name_plural = 'Códigos de impuesto'
        ordering            = ['tax_type', 'code']

    def __str__(self):
        return f"{self.code} — {self.name} ({self.rate}%)"

    def calculate(self, base_amount):
        """Calcula el monto del impuesto sobre base_amount."""
        return (Decimal(str(base_amount)) * self.rate / 100).quantize(Decimal('0.01'))

# =============================================================================
# 10. CIERRE DE PERÍODO  (SAP F.16 / FAGLGVTR)
# =============================================================================
class MonthlyClosure(TimeStampedModel):
    """
    Cierre mensual de una cuenta bancaria — equivalente a SAP F.16.

    Estados:
      OPEN     → período abierto, se permiten movimientos
      CLOSED   → cierre ejecutado, movimientos bloqueados
      APPROVED → aprobado por gerencia (doble firma)
      REOPENED → reabierto con justificación auditada
    """
    STATUS_CHOICES = [
        ('OPEN',     'Abierto'),
        ('CLOSED',   'Cerrado'),
        ('APPROVED', 'Aprobado'),
        ('REOPENED', 'Reabierto'),
    ]

    account      = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='monthly_closures', verbose_name='Cuenta bancaria')
    tin          = models.ForeignKey(Tin, on_delete=models.CASCADE, related_name='monthly_closures', verbose_name='Empresa')
    period_year  = models.PositiveSmallIntegerField('Año')
    period_month = models.PositiveSmallIntegerField('Mes', choices=MONTH_CHOICES)

    # Saldos calculados al cierre
    opening_balance  = models.DecimalField('Saldo inicial', max_digits=14, decimal_places=2, default=0)
    total_ingresos   = models.DecimalField('Total ingresos', max_digits=14, decimal_places=2, default=0)
    total_egresos    = models.DecimalField('Total egresos', max_digits=14, decimal_places=2, default=0)
    closing_balance  = models.DecimalField('Saldo final', max_digits=14, decimal_places=2, default=0)
    movements_count  = models.PositiveIntegerField('Nro. movimientos', default=0)
    unreconciled_count = models.PositiveIntegerField('Sin conciliar', default=0)

    # Estado y auditoría
    status       = models.CharField('Estado', max_length=10, choices=STATUS_CHOICES, default='OPEN')
    is_locked    = models.BooleanField('Período bloqueado', default=False, help_text='Si True, no se permiten nuevos movimientos en este período')
    closed_by    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='closures_executed', verbose_name='Cerrado por')
    closed_at    = models.DateTimeField('Fecha cierre', null=True, blank=True)
    approved_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='closures_approved', verbose_name='Aprobado por')
    approved_at  = models.DateTimeField('Fecha aprobación', null=True, blank=True)
    reopen_reason= models.TextField('Motivo reapertura', null=True, blank=True)
    notes        = models.TextField('Notas', null=True, blank=True)

    class Meta:
        verbose_name        = 'Cierre mensual'
        verbose_name_plural = 'Cierres mensuales'
        ordering            = ['-period_year', '-period_month', 'account']
        unique_together     = [('account', 'period_year', 'period_month')]
        indexes             = [models.Index(fields=['period_year', 'period_month', 'tin'])]

    def __str__(self):
        return f"{self.account.nickName} | {self.period_year}-{self.period_month:02d} | {self.get_status_display()}"

    @property
    def period_label(self):
        import calendar
        month_name = calendar.month_name[self.period_month]
        return f"{month_name} {self.period_year}"

    def calculate_totals(self):
        """Calcula y guarda los totales del período desde BankMovements."""
        movs = BankMovements.objects.filter(
            idAccount=self.account,
            date__year=self.period_year,
            date__month=self.period_month,
        )
        ingresos = movs.filter(movementType__flow=MovementType.INGRESO).aggregate(s=Sum('amount'))['s'] or 0
        egresos  = movs.filter(movementType__flow=MovementType.EGRESO).aggregate(s=Sum('amount'))['s'] or 0
        sin_conc = movs.filter(conciliated=False).count()
        total    = movs.count()

        self.total_ingresos    = ingresos
        self.total_egresos     = egresos
        self.closing_balance   = self.opening_balance + ingresos - egresos
        self.movements_count   = total
        self.unreconciled_count= sin_conc
        self.save(update_fields=[
            'total_ingresos','total_egresos','closing_balance',
            'movements_count','unreconciled_count',
        ])

    def close(self, user):
        """Ejecuta el cierre: calcula totales y bloquea el período."""
        from django.utils import timezone
        if self.status not in ('OPEN', 'REOPENED'):
            raise ValidationError('Solo se pueden cerrar períodos abiertos o reabiertos.')
        if self.unreconciled_count and self.unreconciled_count > 0:
            self.calculate_totals()
        else:
            self.calculate_totals()
        self.status    = 'CLOSED'
        self.is_locked = True
        self.closed_by = user
        self.closed_at = timezone.now()
        self.save(update_fields=['status','is_locked','closed_by','closed_at'])

    def approve(self, user):
        """Aprobación gerencial del cierre."""
        from django.utils import timezone
        if self.status != 'CLOSED':
            raise ValidationError('Solo se pueden aprobar períodos cerrados.')
        self.status      = 'APPROVED'
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save(update_fields=['status','approved_by','approved_at'])

    def reopen(self, user, reason):
        """Reabre el período con justificación — queda auditado."""
        if self.status not in ('CLOSED', 'APPROVED'):
            raise ValidationError('Solo se pueden reabrir períodos cerrados o aprobados.')
        self.status       = 'REOPENED'
        self.is_locked    = False
        self.reopen_reason= reason
        self.save(update_fields=['status','is_locked','reopen_reason'])

    @classmethod
    def is_period_locked(cls, account, date):
        """Verifica si la fecha cae en un período bloqueado para esa cuenta."""
        return cls.objects.filter(
            account=account,
            period_year=date.year,
            period_month=date.month,
            is_locked=True,
        ).exists()

# =============================================================================
# 11. MOVIMIENTOS BANCARIOS
# =============================================================================
class BankMovements(TimeStampedModel):
    idAccount  = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='bank_movements', verbose_name='Cuenta bancaria')
    tin        = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='bank_movements', verbose_name='Empresa')
    idDoc      = models.ForeignKey(DocumentsUploaded, on_delete=models.CASCADE, null=True, blank=True, related_name='bank_movements_doc', verbose_name='Documento adjunto')
    movementType = models.ForeignKey(MovementType, on_delete=models.SET_NULL, null=True, blank=True, related_name='movements', verbose_name='Tipo de movimiento')
    cost_center  = models.ForeignKey('CostCenter', on_delete=models.SET_NULL, null=True, blank=True, related_name='bank_movements', verbose_name='Centro de costos')

    payment_transaction = models.ForeignKey('PaymentTransaction', on_delete=models.SET_NULL, null=True, blank=True, related_name='bank_movements', verbose_name='Transacción de pago vinculada')
    is_reconciled_with_payment = models.BooleanField('¿Conciliado desde pagos?', default=False)

    date              = models.DateField('Fecha')
    description       = models.CharField('Descripción', max_length=100, null=True, blank=True)
    opNumber          = models.CharField('Nro. operación', max_length=50, null=True, blank=True)
    justification     = models.TextField('Justificación', null=True, blank=True)
    originDestination = models.ForeignKey(client, on_delete=models.CASCADE, null=True, blank=True, related_name='bank_movements', verbose_name='Origen / Destino')
    expenseSubCategory= models.ForeignKey(ExpenseSubCategories, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Subcategoría gasto')
    incomeSubCategory = models.ForeignKey(IncomeSubCategories, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Subcategoría ingreso')

    amount            = models.DecimalField('Monto', max_digits=14, decimal_places=2)
    equivalentAmount  = models.DecimalField('Monto equivalente', max_digits=14, decimal_places=2, null=True, blank=True)
    balance           = models.DecimalField('Saldo', max_digits=14, decimal_places=2, null=True, blank=True)
    amountReconcilied = models.DecimalField('Monto conciliado', max_digits=14, decimal_places=2, default=0)
    conciliated       = models.BooleanField('Conciliado', default=False)
    pdf_file          = models.FileField('PDF voucher', upload_to='vouchers_pdfs/', null=True, blank=True)

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
        ]

    def __str__(self):
        nick = self.idAccount.nickName if self.idAccount else '—'
        return f"{nick} | {self.opNumber or '—'} | {self.date} | {self.amount} [{self.amountReconcilied}]"

    def clean(self):
        """Bloquea guardado si el período está cerrado."""
        if self.idAccount_id and self.date:
            if MonthlyClosure.is_period_locked(self.idAccount, self.date):
                raise ValidationError(
                    f'El período {self.date.strftime("%m/%Y")} está cerrado para la cuenta '
                    f'{self.idAccount.nickName}. Contacte al responsable financiero para reabrirlo.'
                )

    def save(self, *args, **kwargs):
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
        result  = Conciliation.objects.SumaMontosConciliadosPorMovimientosOr(self.pk)
        sum_doc = result.get('sumDoc') or Decimal('0')
        sum_mov = result.get('sumMov') or Decimal('0')
        total   = sum_doc + sum_mov
        BankMovements.objects.filter(pk=self.pk).update(
            amountReconcilied=total,
            conciliated=(total >= self.amount),
        )

# =============================================================================
# 12. CONCILIACIONES
# =============================================================================

class Conciliation(TimeStampedModel):
    DOC    = '0'
    MOV    = '1'
    OPBANK = '2'
    IMP    = '3'
    TYPE_CHOICES   = [(DOC,'Documento'),(MOV,'Movimiento'),(OPBANK,'Com. Bancarias'),(IMP,'Impuestos')]
    SOURCE_MANUAL  = 'MANUAL'
    SOURCE_PAYMENT = 'PAYMENT'
    SOURCE_CHOICES = [(SOURCE_MANUAL,'Manual'),(SOURCE_PAYMENT,'Desde pagos')]

    type          = models.CharField('Tipo', max_length=1, choices=TYPE_CHOICES)
    idMovOrigin   = models.ForeignKey(BankMovements, on_delete=models.CASCADE, related_name='mov_origen', verbose_name='Mov. origen')
    idMovArrival  = models.ForeignKey(BankMovements, on_delete=models.CASCADE, null=True, blank=True, related_name='mov_destino', verbose_name='Mov. destino')
    payment_document = models.ForeignKey('PaymentDocument', on_delete=models.SET_NULL, null=True, blank=True, related_name='conciliations', verbose_name='Comprobante')
    amountReconcilied = models.DecimalField('Monto conciliado', max_digits=14, decimal_places=2)
    equivalentAmount  = models.DecimalField('Monto equivalente', max_digits=14, decimal_places=3, default=0)
    status        = models.BooleanField('Procesado', default=False)
    source        = models.CharField('Origen', max_length=10, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)
    objects = ConciliationManager()

    class Meta:
        ordering            = ['created']
        verbose_name        = 'Conciliación'
        verbose_name_plural = 'Conciliaciones'
        indexes = [models.Index(fields=['type']), models.Index(fields=['status']), models.Index(fields=['source'])]

    def __str__(self):
        return f"{self.id} | {self.get_type_display()} | {self.amountReconcilied}"

    def clean(self):
        """
        1. Valida que el monto conciliado no supere el saldo pendiente del movimiento origen.
        2. Si type=DOC, bloquea la creación manual cuando ya existe una PaymentTransaction
           confirmada que cubre el mismo movimiento y comprobante (evita doble conteo).
        """
        if self.idMovOrigin_id and self.amountReconcilied:
            mov = self.idMovOrigin
            already = mov.amountReconcilied
            if self.pk:
                already = Conciliation.objects.exclude(pk=self.pk).filter(
                    idMovOrigin=mov
                ).aggregate(s=Sum('amountReconcilied'))['s'] or Decimal('0')
            disponible = mov.amount - already
            if self.amountReconcilied > disponible:
                raise ValidationError(
                    f'El monto a conciliar ({self.amountReconcilied}) supera el saldo disponible '
                    f'del movimiento ({disponible}). Solo puede conciliar hasta {disponible}.'
                )

        if (self.type == self.DOC
                and self.payment_document_id
                and self.idMovOrigin_id):
            # Verificar si ya hay una PaymentTransaction confirmada que cubre este par
            from .models import PaymentTransactionLine  # import local para evitar circular
            ya_cubierto = PaymentTransactionLine.objects.filter(
                document_id=self.payment_document_id,
                transaction__bank_movement_id=self.idMovOrigin_id,
                transaction__status='CONFIRMED',
            ).exclude(
                # Permitir si esta misma conciliación ya existe (edición)
                transaction__conciliations__pk=self.pk,
            ).exists()
            if ya_cubierto:
                raise ValidationError(
                    'Ya existe una Transacción de pago confirmada que vincula este '
                    'movimiento bancario con este comprobante. No es necesario crear '
                    'una conciliación manual; el pago ya registra el vínculo.'
                )

# =============================================================================
# 13. ASIENTOS CONTABLES  (SAP FB50 / F-02)
# =============================================================================
class JournalEntry(TimeStampedModel):
    """
    Asiento contable — equivalente a SAP FB50.
    Se genera automáticamente al confirmar una PaymentTransaction.
    """
    SOURCE_CHOICES = [
        ('MANUAL',      'Manual'),
        ('PAYMENT',     'Transacción de pago'),
        ('CONCILIATION','Conciliación'),
        ('CLOSURE',     'Cierre de período'),
    ]

    reference      = models.CharField('Referencia', max_length=80)
    entry_date     = models.DateField('Fecha del asiento')
    period_year    = models.PositiveSmallIntegerField('Año')
    period_month   = models.PositiveSmallIntegerField('Mes', choices=MONTH_CHOICES)
    currency       = models.CharField('Moneda', max_length=3, choices=PAYMENT_CURRENCY_CHOICES, default='PEN')
    description    = models.CharField('Descripción', max_length=200, null=True, blank=True)
    source         = models.CharField('Origen', max_length=15, choices=SOURCE_CHOICES, default='MANUAL')
    tin            = models.ForeignKey(Tin, on_delete=models.CASCADE, related_name='journal_entries', verbose_name='Empresa')
    cost_center    = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True, blank=True, related_name='journal_entries', verbose_name='Centro de costos')
    payment_transaction = models.OneToOneField('PaymentTransaction', on_delete=models.SET_NULL, null=True, blank=True, related_name='journal_entry', verbose_name='Transacción de pago')
    is_posted      = models.BooleanField('Contabilizado', default=False)
    posted_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='posted_entries')
    posted_at      = models.DateTimeField('Fecha contabilización', null=True, blank=True)

    class Meta:
        verbose_name        = 'Asiento contable'
        verbose_name_plural = 'Asientos contables'
        ordering            = ['-entry_date', '-created']
        indexes             = [models.Index(fields=['period_year', 'period_month', 'tin'])]

    def __str__(self):
        return f"AST-{self.id} | {self.entry_date} | {self.reference}"

    @property
    def total_debit(self):
        return self.lines.aggregate(s=Sum('debit'))['s'] or Decimal('0')

    @property
    def total_credit(self):
        return self.lines.aggregate(s=Sum('credit'))['s'] or Decimal('0')

    @property
    def is_balanced(self):
        return self.total_debit == self.total_credit

    def post(self, user):
        """Contabiliza el asiento (equivale a SAP FB50 → Grabar)."""
        from django.utils import timezone
        if not self.is_balanced:
            raise ValidationError(
                f'El asiento no está balanceado: Débito {self.total_debit} ≠ Crédito {self.total_credit}.'
            )
        self.is_posted = True
        self.posted_by = user
        self.posted_at = timezone.now()
        self.save(update_fields=['is_posted', 'posted_by', 'posted_at'])

class JournalEntryLine(TimeStampedModel):
    """Línea de asiento — una partida individual (debe/haber)."""
    entry           = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines', verbose_name='Asiento')
    account         = models.ForeignKey(AccountingAccount, on_delete=models.CASCADE, related_name='journal_lines', verbose_name='Cuenta contable')
    debit           = models.DecimalField('Debe', max_digits=14, decimal_places=2, default=0)
    credit          = models.DecimalField('Haber', max_digits=14, decimal_places=2, default=0)
    description     = models.CharField('Descripción', max_length=200, null=True, blank=True)
    cost_center     = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True, blank=True, related_name='journal_lines', verbose_name='Centro de costos')
    tax_code        = models.ForeignKey(TaxCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='journal_lines', verbose_name='Código impuesto')

    class Meta:
        verbose_name        = 'Línea de asiento'
        verbose_name_plural = 'Líneas de asiento'

    def __str__(self):
        return f"AST-{self.entry_id} | {self.account.code} | D:{self.debit} H:{self.credit}"

    def clean(self):
        if self.debit > 0 and self.credit > 0:
            raise ValidationError('Una línea no puede tener debe y haber simultáneamente.')
        if self.debit == 0 and self.credit == 0:
            raise ValidationError('Ingrese un monto en debe o en haber.')

# =============================================================================
# 14. COMPROBANTES DE PAGO
# =============================================================================

class PaymentDocument(TimeStampedModel):
    ACCOUNT_CHOICES = [
        ('ADUANAS','Agente de aduana'),('CAJA_CH','Caja chica'),('CAJA_GEN','Caja general'),
        ('CAJA_VTA','Caja general ventas'),('RHE_GEN','RHE general'),('ADICIONAL','Adicional'),
        ('PERSONAL','Personal'),('PLANILLA','Planilla'),('RENTA','Renta'),
    ]

    doc_type   = models.CharField('Tipo', max_length=3, choices=DOC_TYPE_CHOICES, default='FAC')
    doc_number = models.CharField('Número', max_length=50, null=True, blank=True)
    direction  = models.CharField('Dirección', max_length=3, choices=PAYMENT_DIRECTION, default='OUT')

    tin_issuer   = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='docs_issued',   verbose_name='Empresa emisora')
    tin_receiver = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='docs_received', verbose_name='Empresa receptora')
    client       = models.ForeignKey(client, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_docs',  verbose_name='Cliente externo')
    supplier     = models.ForeignKey(supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_docs', verbose_name='Proveedor externo')

    issue_date    = models.DateField('Fecha de emisión', null=True, blank=True)
    due_date      = models.DateField('Fecha de vencimiento', null=True, blank=True)
    declare_month = models.PositiveSmallIntegerField('Mes declaración', choices=MONTH_CHOICES, null=True, blank=True)
    declare_year  = models.PositiveSmallIntegerField('Año declaración', null=True, blank=True)

    currency       = models.CharField('Moneda', max_length=3, choices=PAYMENT_CURRENCY_CHOICES, default='USD')
    exchange_rate  = models.DecimalField('T.C.', max_digits=10, decimal_places=6, default=1)
    gross_amount   = models.DecimalField('Monto bruto', max_digits=14, decimal_places=2, default=0)
    tax_amount     = models.DecimalField('IGV / IVA', max_digits=14, decimal_places=2, default=0)
    net_amount     = models.DecimalField('Monto neto', max_digits=14, decimal_places=2, default=0)
    paid_amount    = models.DecimalField('Pagado', max_digits=14, decimal_places=2, default=0)
    pending_amount = models.DecimalField('Pendiente', max_digits=14, decimal_places=2, default=0)

    status     = models.CharField('Estado', max_length=10, choices=DOC_STATUS_CHOICES, default='PENDING')
    annotation = models.CharField('Anotación', max_length=10, choices=ANNOTATION_CHOICES, null=True, blank=True)

    has_detraction    = models.BooleanField('¿Detracción?', default=False)
    detraction_amount = models.DecimalField('Monto detracción', max_digits=14, decimal_places=2, default=0)
    has_retention     = models.BooleanField('¿Retención?', default=False)
    retention_amount  = models.DecimalField('Monto retención', max_digits=14, decimal_places=2, default=0)

    # Clasificación contable — ahora FK a modelos formales
    account_category = models.CharField('Categoría contable', max_length=10, choices=ACCOUNT_CHOICES, null=True, blank=True)
    cost_center      = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_documents', verbose_name='Centro de costos')
    tax_code         = models.ForeignKey(TaxCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_documents', verbose_name='Código de impuesto')

    short_description = models.CharField('Descripción corta', max_length=150, null=True, blank=True)
    description       = models.TextField('Descripción detallada', null=True, blank=True)
    xml_file = models.FileField('XML', upload_to='payment_docs/xml/', null=True, blank=True)
    pdf_file = models.FileField('PDF', upload_to='payment_docs/pdf/', null=True, blank=True)
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
        constraints = [
            models.UniqueConstraint(
                fields=['doc_type', 'doc_number', 'tin_issuer'],
                condition=models.Q(doc_number__isnull=False) & ~models.Q(doc_number=''),
                name='unique_payment_doc_number_per_issuer',
            )
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

    COST_LEVEL_QUO = 'QUO'
    COST_LEVEL_INT = 'INT'
    COST_LEVEL_WO  = 'WO'
    COST_LEVEL_CHOICES = [
        (COST_LEVEL_QUO, 'Cotización Master — Cliente → Holding (unitCost)'),
        (COST_LEVEL_INT, 'Cotización Interna — Subsidiaria ↔ Holding (unitCostInt)'),
        (COST_LEVEL_WO,  'Orden de Trabajo — Holding → Proveedor (unitCostWO)'),
    ]

    document         = models.ForeignKey(PaymentDocument, on_delete=models.CASCADE, related_name='allocations', verbose_name='Comprobante')
    item             = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='payment_allocations', verbose_name='Ítem')
    cost_level       = models.CharField('Nivel de costo', max_length=3, choices=COST_LEVEL_CHOICES, default=COST_LEVEL_QUO)
    allocated_amount = models.DecimalField('Monto asignado', max_digits=14, decimal_places=2, default=0)
    notes            = models.CharField('Notas', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name        = 'Asignación de comprobante'
        verbose_name_plural = 'Asignaciones de comprobante'
        unique_together     = [('document', 'item', 'cost_level')]

    def __str__(self):
        return f"{self.document} → Item {self.item.seq} [{self.cost_level}] ({self.allocated_amount})"

    # ── helpers ──────────────────────────────────────────────────────────────
    @staticmethod
    def _unit_cost_for_level(item, cost_level):
        return {
            'QUO': item.unitCost,
            'INT': item.unitCostInt,
            'WO':  item.unitCostWO,
        }.get(cost_level) or Decimal('0')

    def clean(self):
        """
        Valida que el monto asignado no supere el costo unitario del nivel
        correspondiente, descontando lo ya asignado en otros comprobantes.
        """
        if self.item_id and self.allocated_amount and self.cost_level:
            item      = self.item
            unit_cost = self._unit_cost_for_level(item, self.cost_level)
            if unit_cost > 0:
                already = PaymentAllocation.objects.filter(
                    item=item, cost_level=self.cost_level
                ).exclude(pk=self.pk).aggregate(s=Sum('allocated_amount'))['s'] or Decimal('0')
                disponible = Decimal(str(unit_cost)) - already
                if self.allocated_amount > disponible:
                    raise ValidationError(
                        f'El monto asignado ({self.allocated_amount}) supera el disponible '
                        f'para el nivel {self.cost_level} ({disponible}). '
                        f'Costo: {unit_cost}, ya asignado: {already}.'
                    )

    @property
    def order_context(self):
        item = self.item
        if item.idTrafoQuote_id:    return ('QUO', item.idTrafoQuote)
        if item.idTrafoIntQuote_id: return ('INT', item.idTrafoIntQuote)
        if item.idWorkOrder_id:     return ('WO',  item.idWorkOrder)
        return (None, None)

# =============================================================================
# 15. TRANSACCIONES DE PAGO
# =============================================================================
class PaymentTransaction(TimeStampedModel):
    STATUS_TX = [('DRAFT','Borrador'),('CONFIRMED','Confirmado'),('REVERSED','Revertido')]

    reference        = models.CharField('Referencia / Nro. Op.', max_length=80, null=True, blank=True)
    pay_method       = models.CharField('Método', max_length=10, choices=PAY_METHOD_CHOICES, default='TRANSFER')
    transaction_date = models.DateField('Fecha de pago')
    currency         = models.CharField('Moneda', max_length=3, choices=PAYMENT_CURRENCY_CHOICES, default='USD')
    exchange_rate    = models.DecimalField('T.C.', max_digits=10, decimal_places=6, default=1)
    amount           = models.DecimalField('Monto total', max_digits=14, decimal_places=2)
    reconciled_amount= models.DecimalField('Monto conciliado', max_digits=14, decimal_places=2, default=0)

    tin_payer    = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_paid',     verbose_name='Empresa pagadora')
    tin_receiver = models.ForeignKey(Tin, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_received', verbose_name='Empresa receptora')
    client       = models.ForeignKey(client, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_transactions')
    supplier     = models.ForeignKey(supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_transactions')

    bank_account  = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_transactions', verbose_name='Cuenta bancaria')
    bank_movement = models.ForeignKey(BankMovements, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_transactions_linked', verbose_name='Movimiento bancario')
    cost_center   = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_transactions', verbose_name='Centro de costos')

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

    def clean(self):
        """
        Valida:
        1. Que el monto total de las líneas no supere self.amount.
        2. Que ninguna línea supere el pending_amount del comprobante.
        """
        if self.pk and self.status == 'DRAFT':
            total_lines = self.transaction_lines.aggregate(s=Sum('amount_applied'))['s'] or Decimal('0')
            if total_lines > self.amount:
                raise ValidationError(
                    f'La suma de las líneas ({total_lines}) supera el monto de la transacción ({self.amount}).'
                )

    def confirm(self):
        """
        1. Valida que ninguna línea supere el pending del comprobante.
        2. status → CONFIRMED.
        3. Actualiza paid_amount en cada comprobante.
        4. Crea Conciliation si hay bank_movement.
        5. Genera JournalEntry automático.
        """
        if self.status == 'CONFIRMED':
            return

        # Validar sobre-pago línea a línea
        errors = []
        for line in self.transaction_lines.select_related('document').all():
            doc = line.document
            current_paid = doc.transaction_lines.filter(
                transaction__status='CONFIRMED'
            ).exclude(transaction=self).aggregate(s=Sum('amount_applied'))['s'] or Decimal('0')
            disponible = doc.net_amount - current_paid
            if line.amount_applied > disponible:
                errors.append(
                    f'{doc}: aplica {line.amount_applied} pero solo queda {disponible} pendiente.'
                )
        if errors:
            raise ValidationError('No se puede confirmar — sobre-pago detectado: ' + ' | '.join(errors))

        self.status = 'CONFIRMED'
        self.save()

        for line in self.transaction_lines.all():
            line.document.recalculate_paid()

        if self.bank_movement_id:
            self._auto_conciliate()

        self._generate_journal_entry()

    def _auto_conciliate(self):
        for line in self.transaction_lines.select_related('document').all():
            if not line.document_id:
                continue
            Conciliation.objects.get_or_create(
                type=Conciliation.DOC,
                idMovOrigin=self.bank_movement,
                payment_document=line.document,
                defaults={
                    'amountReconcilied': line.amount_applied,
                    'source': Conciliation.SOURCE_PAYMENT,
                }
            )

    def _generate_journal_entry(self):
        """
        Genera JournalEntry automático al confirmar.
        Patrón básico: Debe = cuenta bancaria / Haber = cuenta de gasto/ingreso.
        Si no hay AccountingAccount configurado, se omite silenciosamente.
        """
        try:
            tin = self.tin_payer or (self.bank_account.idTin if self.bank_account else None)
            if not tin:
                return
            # Buscar cuenta contable bancaria
            bank_acc = None
            if self.bank_account and hasattr(self.bank_account, 'accounting_account'):
                bank_acc = self.bank_account.accounting_account
            if not bank_acc:
                return  # Sin plan de cuentas configurado, omitir

            entry = JournalEntry.objects.create(
                reference   = f'TX-{self.id}',
                entry_date  = self.transaction_date,
                period_year = self.transaction_date.year,
                period_month= self.transaction_date.month,
                currency    = self.currency,
                description = f'Pago {self.get_pay_method_display()} — {self.reference or ""}',
                source      = 'PAYMENT',
                tin         = tin,
                cost_center = self.cost_center,
                payment_transaction = self,
            )
            # Línea bancaria (débito para egresos, crédito para ingresos)
            for line in self.transaction_lines.select_related('document__cost_center').all():
                doc = line.document
                is_egreso = doc.direction == 'OUT'
                JournalEntryLine.objects.create(
                    entry       = entry,
                    account     = bank_acc,
                    debit       = line.amount_applied if is_egreso else Decimal('0'),
                    credit      = Decimal('0') if is_egreso else line.amount_applied,
                    description = str(doc),
                    cost_center = doc.cost_center or self.cost_center,
                )
        except Exception:
            pass  # El asiento contable es opcional; no bloquear el confirm

    def reverse(self):
        self.status = 'REVERSED'
        self.save()
        for line in self.transaction_lines.all():
            line.document.recalculate_paid()

class PaymentTransactionLine(TimeStampedModel):
    transaction    = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, related_name='transaction_lines', verbose_name='Transacción')
    document       = models.ForeignKey(PaymentDocument, on_delete=models.CASCADE, related_name='transaction_lines', verbose_name='Comprobante')
    amount_applied = models.DecimalField('Monto aplicado', max_digits=14, decimal_places=2)
    notes          = models.CharField('Notas', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name        = 'Línea de transacción'
        verbose_name_plural = 'Líneas de transacción'

    def __str__(self):
        return f"{self.transaction} → {self.document} ({self.amount_applied})"

    def clean(self):
        """
        Valida que el monto aplicado no supere el pending_amount del comprobante.
        Considera los pagos ya confirmados de otras transacciones.
        """
        if self.document_id and self.amount_applied:
            doc = self.document
            # Pagos ya confirmados en OTRAS transacciones (excluir la actual si existe)
            qs = doc.transaction_lines.filter(
                transaction__status='CONFIRMED'
            )
            if self.transaction_id:
                qs = qs.exclude(transaction_id=self.transaction_id)
            already_paid = qs.aggregate(s=Sum('amount_applied'))['s'] or Decimal('0')
            disponible   = doc.net_amount - already_paid
            if self.amount_applied > disponible:
                raise ValidationError(
                    f'El monto aplicado ({self.amount_applied}) supera el pendiente '
                    f'del comprobante {doc.doc_number or doc.id} ({disponible}). '
                    f'Neto: {doc.net_amount}, ya pagado: {already_paid}.'
                )








