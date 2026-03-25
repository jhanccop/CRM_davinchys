



from .models import (
    PaymentDocument, PaymentAllocation,
    PaymentTransaction, PaymentTransactionLine,
    BankMovements,MovementType,
    #ExpenseSubCategories, IncomeSubCategories,
)


"""
FINANTIAL/forms.py  — v3
"""
from decimal import Decimal
from django import forms
from django.forms import inlineformset_factory

from applications.COMERCIAL.sales.models import Items
from applications.cuentas.models import Tin, Account

from .models import (
    PaymentDocument, PaymentAllocation,
    PaymentTransaction, PaymentTransactionLine,
    BankMovements,
    MovementType, ExpenseSubCategories, IncomeSubCategories,
    CostCenter, AccountingAccount, TaxCode, ExchangeRate,
    MonthlyClosure, JournalEntry, JournalEntryLine,
)


# ─────────────────────────────────────────────────────────────────────────────
# Widget factories
# ─────────────────────────────────────────────────────────────────────────────
def _w(**kw): return forms.TextInput(attrs={'class':'form-control',**kw})
def _s(**kw): return forms.Select(attrs={'class':'form-control form-select',**kw})
def _d(**kw): return forms.DateInput(format='%Y-%m-%d', attrs={'class':'form-control datetimepicker text-center text-dark flatpickr-input','placeholder':'',**kw})
def _n(**kw): return forms.NumberInput(attrs={'class':'form-control','step':'0.01',**kw})
def _ta(**kw):return forms.Textarea(attrs={'class':'form-control','rows':3,**kw})
def _cb(**kw):return forms.CheckboxInput(attrs={'class':'form-check-input',**kw})
def _file(**kw):return forms.ClearableFileInput(attrs={'class':'form-control',**kw})


# ─────────────────────────────────────────────────────────────────────────────
# Company-scoped helpers
# ─────────────────────────────────────────────────────────────────────────────
def _get_company(user):
    """Return the Tin company for the user, or None if no employee profile."""
    if user and hasattr(user, 'empleado') and hasattr(user.empleado, 'company'):
        return user.empleado.company
    return None

def _is_holding(user):
    tin = _get_company(user)
    if tin is None:
        return getattr(user, 'is_superuser', False)
    return tin.company_type == Tin.HOLDING

def _tin_qs(user):
    """Tin queryset scoped to the user's company (all if holding/superuser)."""
    tin = _get_company(user)
    if tin and tin.company_type != Tin.HOLDING:
        return Tin.objects.filter(pk=tin.pk)
    return Tin.objects.all().order_by('tinName')

def _account_qs(user):
    """Account queryset scoped to the user's company."""
    tin = _get_company(user)
    if tin and tin.company_type != Tin.HOLDING:
        return Account.objects.filter(idTin=tin, state=True)
    return Account.objects.filter(state=True).select_related('idTin')

def _costcenter_qs(user):
    """CostCenter queryset scoped to the user's company."""
    tin = _get_company(user)
    if tin and tin.company_type != Tin.HOLDING:
        return CostCenter.objects.filter(tin=tin, active=True)
    return CostCenter.objects.filter(active=True)


# =============================================================================
# PaymentDocument
# =============================================================================
class PaymentDocumentForm(forms.ModelForm):

    class Meta:
        model  = PaymentDocument
        fields = [
            'doc_type','doc_number','direction',
            'tin_issuer','tin_receiver','client','supplier',
            'issue_date','due_date','declare_month','declare_year',
            'currency','exchange_rate',
            'gross_amount','tax_amount','net_amount',
            'has_detraction','detraction_amount',
            'has_retention','retention_amount',
            'annotation','account_category','cost_center','tax_code',
            'short_description','description',
            'xml_file','pdf_file',
        ]
        widgets = {
            'doc_type':          _s(),
            'doc_number':        _w(placeholder='E.g. F001-00123'),
            'direction':         _s(),
            'tin_issuer':        _s(),
            'tin_receiver':      _s(),
            'client':            _s(),
            'supplier':          _s(),
            'issue_date':        _d(),
            'due_date':          _d(),
            'declare_month':     _s(),
            'declare_year':      _w(placeholder='2024'),
            'currency':          _s(),
            'exchange_rate':     _n(placeholder='1.000000'),
            'gross_amount':      _n(placeholder='0.00'),
            'tax_amount':        _n(placeholder='0.00'),
            'net_amount':        _n(placeholder='0.00'),
            'has_detraction':    _cb(),
            'detraction_amount': _n(placeholder='0.00'),
            'has_retention':     _cb(),
            'retention_amount':  _n(placeholder='0.00'),
            'annotation':        _s(),
            'account_category':  _s(),
            'cost_center':       _s(),
            'tax_code':          _s(),
            'short_description': _w(placeholder='Resumen del comprobante'),
            'description':       _ta(placeholder='Descripción detallada…'),
            'xml_file':          _file(),
            'pdf_file':          _file(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # Campos siempre opcionales en el form
        for f in ('xml_file','pdf_file','net_amount','detraction_amount',
                  'retention_amount','client','supplier'):
            self.fields[f].required = False

        # Restricción por empresa
        tin_qs = _tin_qs(user)
        self.fields['tin_issuer'].queryset  = tin_qs
        self.fields['tin_receiver'].queryset = tin_qs

        company = _get_company(user)
        if company and not _is_holding(user):
            self.fields['tin_issuer'].initial  = company
            self.fields['tin_receiver'].initial = company

        self.fields['cost_center'].queryset = _costcenter_qs(user)
        self.fields['tax_code'].queryset    = TaxCode.objects.filter(active=True)

    def clean(self):
        cleaned = super().clean()
        gross = cleaned.get('gross_amount') or 0
        tax   = cleaned.get('tax_amount')   or 0
        if not cleaned.get('net_amount'):
            cleaned['net_amount'] = gross - tax

        if cleaned.get('has_detraction') and not (cleaned.get('detraction_amount') or 0):
            self.add_error('detraction_amount','Ingrese el monto de detracción.')
        if cleaned.get('has_retention') and not (cleaned.get('retention_amount') or 0):
            self.add_error('retention_amount','Ingrese el monto de retención.')

        # Si hay tax_code, auto-calcular tax_amount
        tax_code = cleaned.get('tax_code')
        if tax_code and gross and not tax:
            cleaned['tax_amount'] = tax_code.calculate(gross)
            cleaned['net_amount'] = gross - cleaned['tax_amount']

        # Auto-rellenar tipo de cambio desde ExchangeRate
        currency   = cleaned.get('currency')
        issue_date = cleaned.get('issue_date')
        if currency and currency != 'PEN' and issue_date and not cleaned.get('exchange_rate'):
            rate = ExchangeRate.get_rate(currency, 'PEN', issue_date)
            cleaned['exchange_rate'] = rate

        # Validar contraparte según dirección
        direction    = cleaned.get('direction')
        client_v     = cleaned.get('client')
        supplier_v   = cleaned.get('supplier')
        tin_issuer_v = cleaned.get('tin_issuer')
        tin_recv_v   = cleaned.get('tin_receiver')
        if direction == 'IN' and not client_v and not tin_issuer_v:
            self.add_error('client', 'Un comprobante de ingreso requiere cliente externo o empresa emisora.')
        elif direction == 'OUT' and not supplier_v and not tin_recv_v:
            self.add_error('supplier', 'Un comprobante de egreso requiere proveedor externo o empresa receptora.')
        elif direction == 'INT' and (not tin_issuer_v or not tin_recv_v):
            self.add_error('direction', 'Un movimiento interno requiere empresa emisora y empresa receptora.')

        return cleaned


# =============================================================================
# PaymentAllocation inline
# =============================================================================
class PaymentAllocationForm(forms.ModelForm):
    class Meta:
        model   = PaymentAllocation
        fields  = ['item', 'cost_level', 'allocated_amount', 'notes']
        widgets = {
            'item':             _s(),
            'cost_level':       _s(),
            'allocated_amount': _n(placeholder='0.00'),
            'notes':            _w(placeholder='Observación'),
        }

    # Allowed cost_level values for this form instance (set by view for subsidiary users)
    _allowed_levels = None

    def clean(self):
        cleaned     = super().clean()
        item        = cleaned.get('item')
        amount      = cleaned.get('allocated_amount')
        cost_level  = cleaned.get('cost_level', PaymentAllocation.COST_LEVEL_QUO)

        # Server-side enforcement: subsidiary cannot use QUO level
        if self._allowed_levels and cost_level not in self._allowed_levels:
            self.add_error('cost_level', 'No tiene permiso para asignar el nivel de costo seleccionado.')
            return cleaned

        if item and amount and cost_level:
            _COSTS = {
                PaymentAllocation.COST_LEVEL_QUO: item.unitCost,
                PaymentAllocation.COST_LEVEL_INT: item.unitCostInt,
                PaymentAllocation.COST_LEVEL_WO:  item.unitCostWO,
            }
            unit_cost = _COSTS.get(cost_level) or Decimal('0')
            if unit_cost > 0:
                from django.db.models import Sum
                already = PaymentAllocation.objects.filter(
                    item=item, cost_level=cost_level
                ).exclude(
                    pk=self.instance.pk if self.instance.pk else None
                ).aggregate(s=Sum('allocated_amount'))['s'] or Decimal('0')
                disponible = Decimal(str(unit_cost)) - already
                if amount > disponible:
                    self.add_error(
                        'allocated_amount',
                        f'Supera el disponible para el nivel {cost_level}. '
                        f'Costo: {unit_cost} | Ya asignado: {already} | Disponible: {disponible}'
                    )
        return cleaned


PaymentAllocationFormSet = inlineformset_factory(
    PaymentDocument, PaymentAllocation,
    form=PaymentAllocationForm,
    extra=1, can_delete=True,
)


# =============================================================================
# PaymentTransaction
# =============================================================================
class PaymentTransactionForm(forms.ModelForm):

    class Meta:
        model  = PaymentTransaction
        fields = [
            'reference','pay_method','transaction_date',
            'currency','exchange_rate','amount',
            'tin_payer','tin_receiver','client','supplier',
            'bank_account','bank_movement','cost_center',
            'notes','voucher_file',
        ]
        widgets = {
            'reference':        _w(placeholder='Nro. operación / cheque'),
            'pay_method':       _s(),
            'transaction_date': _d(),
            'currency':         _s(),
            'exchange_rate':    _n(placeholder='1.000000'),
            'amount':           _n(placeholder='0.00'),
            'tin_payer':        _s(),
            'tin_receiver':     _s(),
            'client':           _s(),
            'supplier':         _s(),
            'bank_account':     _s(),
            'bank_movement':    _s(),
            'cost_center':      _s(),
            'notes':            _ta(placeholder='Notas adicionales…'),
            'voucher_file':     _file(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ('voucher_file','bank_movement','bank_account','client',
                  'supplier','tin_payer','tin_receiver','cost_center'):
            self.fields[f].required = False
        self.fields['bank_movement'].label = 'Movimiento bancario (para conciliación automática)'

        tin        = _get_company(user)
        is_holding = _is_holding(user)

        # TIN fields — restringidos por empresa
        tin_qs = _tin_qs(user)
        self.fields['tin_payer'].queryset   = tin_qs
        self.fields['tin_receiver'].queryset = tin_qs
        if tin and not is_holding:
            self.fields['tin_payer'].initial   = tin
            self.fields['tin_receiver'].initial = tin

        # Cuenta bancaria, movimientos y centro de costos
        self.fields['bank_account'].queryset  = _account_qs(user)
        self.fields['cost_center'].queryset   = _costcenter_qs(user)
        if is_holding or tin is None:
            self.fields['bank_movement'].queryset = BankMovements.objects.filter(conciliated=False).select_related('idAccount').order_by('-date')
        else:
            self.fields['bank_movement'].queryset = BankMovements.objects.filter(tin=tin, conciliated=False).select_related('idAccount').order_by('-date')

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get('pay_method')
        amount = cleaned.get('amount') or 0

        if amount <= 0:
            self.add_error('amount','El monto debe ser mayor a cero.')

        if method == 'TRANSFER' and not cleaned.get('bank_account'):
            self.add_error('bank_account','Seleccione la cuenta bancaria de origen para una transferencia.')
        if method == 'CHECK' and not (cleaned.get('reference') or '').strip():
            self.add_error('reference','Ingrese el número de cheque en el campo Referencia.')

        # Auto tipo de cambio
        currency = cleaned.get('currency')
        date     = cleaned.get('transaction_date')
        if currency and currency != 'PEN' and date and not cleaned.get('exchange_rate'):
            cleaned['exchange_rate'] = ExchangeRate.get_rate(currency, 'PEN', date)

        return cleaned


# =============================================================================
# PaymentTransactionLine inline — con validación de sobre-pago
# =============================================================================
class PaymentTransactionLineForm(forms.ModelForm):
    # Campo de solo lectura que se muestra en el template para referencia
    doc_pending_display = forms.CharField(required=False, label='Pendiente del comprobante', widget=_w(readonly=True))

    class Meta:
        model   = PaymentTransactionLine
        fields  = ['document','amount_applied','notes']
        widgets = {
            'document':       _s(),
            'amount_applied': _n(placeholder='0.00'),
            'notes':          _w(placeholder='Observación'),
        }

    def clean(self):
        cleaned = super().clean()
        doc    = cleaned.get('document')
        amount = cleaned.get('amount_applied')

        if doc and amount:
            from django.db.models import Sum
            # Pagos ya confirmados excluyendo la transacción actual (si existe)
            qs = doc.transaction_lines.filter(transaction__status='CONFIRMED')
            if self.instance and self.instance.transaction_id:
                qs = qs.exclude(transaction_id=self.instance.transaction_id)
            already = qs.aggregate(s=Sum('amount_applied'))['s'] or Decimal('0')
            disponible = doc.net_amount - already

            if amount > disponible:
                self.add_error(
                    'amount_applied',
                    f'Supera el pendiente del comprobante. '
                    f'Neto: {doc.net_amount} | Ya pagado: {already} | Disponible: {disponible}'
                )

            # Advertencia visual (no bloquea) si el monto iguala o supera el 95%
            if disponible > 0 and amount > disponible * Decimal('0.95') and amount <= disponible:
                # Se pasa como info al template via cleaned_data
                cleaned['_warn_near_full'] = True

        return cleaned


PaymentTransactionLineFormSet = inlineformset_factory(
    PaymentTransaction, PaymentTransactionLine,
    form=PaymentTransactionLineForm,
    extra=1, can_delete=True,
)


# =============================================================================
# BankMovements
# =============================================================================
class BankMovementsForm(forms.ModelForm):

    class Meta:
        model  = BankMovements
        fields = [
            'idAccount','movementType','date','description',
            'opNumber','originDestination',
            'expenseSubCategory','incomeSubCategory',
            'cost_center',
            'amount','equivalentAmount','justification',
            'payment_transaction','pdf_file',
        ]
        widgets = {
            'idAccount':          _s(),
            'movementType':       _s(),
            'date':               _d(),
            'description':        _w(placeholder='Descripción del movimiento'),
            'opNumber':           _w(placeholder='Nro. operación bancaria'),
            'originDestination':  _s(),
            'expenseSubCategory': _s(),
            'incomeSubCategory':  _s(),
            'cost_center':        _s(),
            'amount':             _n(placeholder='0.00'),
            'equivalentAmount':   _n(placeholder='0.00'),
            'justification':      _ta(placeholder='Justificación contable…'),
            'payment_transaction':_s(),
            'pdf_file':           _file(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ('pdf_file','payment_transaction','equivalentAmount','cost_center'):
            self.fields[f].required = False

        self.fields['idAccount'].queryset   = _account_qs(user)
        self.fields['cost_center'].queryset = _costcenter_qs(user)
        self.fields['movementType'].queryset = MovementType.objects.filter(active=True)

    def clean(self):
        cleaned = super().clean()
        account = cleaned.get('idAccount')
        date    = cleaned.get('date')
        # Validar período bloqueado antes de guardar
        if account and date:
            if MonthlyClosure.is_period_locked(account, date):
                raise forms.ValidationError(
                    f'El período {date.strftime("%m/%Y")} está cerrado para la cuenta '
                    f'{account.nickName}. Solicite la reapertura al responsable financiero.'
                )
        return cleaned


# =============================================================================
# MonthlyClosure
# =============================================================================
class MonthlyClosureForm(forms.ModelForm):
    class Meta:
        model  = MonthlyClosure
        fields = ['account','tin','period_year','period_month','opening_balance','notes']
        widgets = {
            'account':        _s(),
            'tin':            _s(),
            'period_year':    _w(placeholder='2024'),
            'period_month':   _s(),
            'opening_balance':_n(placeholder='0.00'),
            'notes':          _ta(placeholder='Observaciones del cierre…'),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        tin        = _get_company(user)
        is_holding = _is_holding(user)
        self.fields['account'].queryset = _account_qs(user)
        self.fields['tin'].queryset     = _tin_qs(user)
        if not is_holding and tin:
            self.fields['tin'].initial = tin

    def clean(self):
        cleaned = super().clean()
        account = cleaned.get('account')
        year    = cleaned.get('period_year')
        month   = cleaned.get('period_month')
        if account and year and month:
            exists = MonthlyClosure.objects.filter(
                account=account, period_year=year, period_month=month
            ).exclude(pk=self.instance.pk if self.instance.pk else None).exists()
            if exists:
                raise forms.ValidationError(
                    f'Ya existe un cierre para esta cuenta en {month}/{year}.'
                )
        return cleaned


class ReopenClosureForm(forms.Form):
    reason = forms.CharField(
        label='Motivo de reapertura',
        widget=_ta(placeholder='Justifique la reapertura del período…'),
        min_length=20,
        help_text='Mínimo 20 caracteres — queda registrado para auditoría.'
    )


# =============================================================================
# ExchangeRate
# =============================================================================
class ExchangeRateForm(forms.ModelForm):
    class Meta:
        model  = ExchangeRate
        fields = ['from_currency','to_currency','rate_date','rate','source']
        widgets = {
            'from_currency': _s(),
            'to_currency':   _s(),
            'rate_date':     _d(),
            'rate':          _n(placeholder='3.750000'),
            'source':        _w(placeholder='SBS, SUNAT, Manual…'),
        }


# =============================================================================
# TaxCode
# =============================================================================
class TaxCodeForm(forms.ModelForm):
    class Meta:
        model  = TaxCode
        fields = ['code','name','tax_type','rate','accounting_account','applies_to_doc_types','active']
        widgets = {
            'code':              _w(placeholder='T01'),
            'name':              _w(placeholder='IGV 18%'),
            'tax_type':          _s(),
            'rate':              _n(placeholder='18.0000'),
            'accounting_account':_s(),
            'applies_to_doc_types':_w(placeholder='FAC,BOL — vacío=todos'),
        }


# =============================================================================
# CostCenter
# =============================================================================
class CostCenterForm(forms.ModelForm):
    class Meta:
        model  = CostCenter
        fields = ['code','name','description','tin','responsible','valid_from','valid_to','active']
        widgets = {
            'code':        _w(placeholder='CC-001'),
            'name':        _w(placeholder='Nombre del centro'),
            'description': _ta(placeholder='Descripción…'),
            'tin':         _s(),
            'responsible': _s(),
            'valid_from':  _d(),
            'valid_to':    _d(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        tin        = _get_company(user)
        is_holding = _is_holding(user)
        self.fields['tin'].queryset = _tin_qs(user)
        if not is_holding and tin:
            self.fields['tin'].initial = tin


# =============================================================================
# AccountingAccount (Plan de cuentas)
# =============================================================================
class AccountingAccountForm(forms.ModelForm):
    class Meta:
        model  = AccountingAccount
        fields = ['code','name','account_type','currency','description','bank_account','active']
        widgets = {
            'code':         _w(placeholder='4211'),
            'name':         _w(placeholder='IGV por pagar'),
            'account_type': _s(),
            'currency':     _s(),
            'description':  _ta(placeholder='Descripción contable…'),
            'bank_account': _s(),
        }


# =============================================================================
# JournalEntry manual
# =============================================================================
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model  = JournalEntry
        fields = ['reference','entry_date','period_year','period_month',
                  'currency','description','tin','cost_center']
        widgets = {
            'reference':    _w(placeholder='REF-001'),
            'entry_date':   _d(),
            'period_year':  _w(placeholder='2024'),
            'period_month': _s(),
            'currency':     _s(),
            'description':  _w(placeholder='Descripción del asiento'),
            'tin':          _s(),
            'cost_center':  _s(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        tin        = _get_company(user)
        is_holding = _is_holding(user)
        self.fields['tin'].queryset        = _tin_qs(user)
        self.fields['cost_center'].queryset = _costcenter_qs(user)
        if not is_holding and tin:
            self.fields['tin'].initial = tin


class JournalEntryLineForm(forms.ModelForm):
    class Meta:
        model   = JournalEntryLine
        fields  = ['account','debit','credit','description','cost_center','tax_code']
        widgets = {
            'account':     _s(),
            'debit':       _n(placeholder='0.00'),
            'credit':      _n(placeholder='0.00'),
            'description': _w(placeholder='Descripción de la partida'),
            'cost_center': _s(),
            'tax_code':    _s(),
        }


JournalEntryLineFormSet = inlineformset_factory(
    JournalEntry, JournalEntryLine,
    form=JournalEntryLineForm,
    extra=2, can_delete=True,
)


# =============================================================================
# Bank Statement CSV Import
# =============================================================================
def _int(**kw):
    return forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', **kw})


class BankStatementImportForm(forms.Form):
    account     = forms.ModelChoiceField(
        queryset=Account.objects.filter(state=True).select_related('idTin'),
        label='Cuenta bancaria', widget=_s(),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = _account_qs(user)
    csv_file    = forms.FileField(label='Archivo CSV / TXT', widget=_file())
    date_col    = forms.IntegerField(initial=0, label='Columna fecha (0-indexada)',  min_value=0, widget=_int())
    desc_col    = forms.IntegerField(initial=1, label='Columna descripción',         min_value=0, widget=_int())
    amount_col  = forms.IntegerField(initial=2, label='Columna monto',               min_value=0, widget=_int())
    debit_col   = forms.IntegerField(required=False, label='Columna cargo (opcional)',  min_value=0, widget=_int())
    credit_col  = forms.IntegerField(required=False, label='Columna abono (opcional)', min_value=0, widget=_int())
    date_format = forms.CharField(initial='%d/%m/%Y', label='Formato de fecha', max_length=20,
                                  widget=_w(placeholder='%d/%m/%Y'))
    delimiter   = forms.ChoiceField(
        choices=[(',', 'Coma (,)'), (';', 'Punto y coma (;)'), ('\t', 'Tab'), ('|', 'Pipe (|)')],
        initial=',', label='Separador', widget=_s(),
    )
    skip_rows   = forms.IntegerField(initial=1, label='Filas a omitir (cabecera)', min_value=0, widget=_int())


# =============================================================================
# Dashboard filter
# =============================================================================
class DashboardFilterForm(forms.Form):
    tin = forms.ModelChoiceField(
        queryset=Tin.objects.all().order_by('tinName'),
        required=False, label='Empresa', widget=_s(),
    )
    direction = forms.ChoiceField(
        choices=[('','Todos')] + list(PaymentDocument._meta.get_field('direction').choices),
        required=False, label='Dirección', widget=_s(),
    )
    status = forms.ChoiceField(
        choices=[('','Todos')] + list(PaymentDocument._meta.get_field('status').choices),
        required=False, label='Estado', widget=_s(),
    )
    currency = forms.ChoiceField(
        choices=[('','Todas')] + list(PaymentDocument._meta.get_field('currency').choices),
        required=False, label='Moneda', widget=_s(),
    )
    date_from = forms.DateField(required=False, label='Desde', widget=_d())
    date_to   = forms.DateField(required=False, label='Hasta',  widget=_d())
    search    = forms.CharField(required=False, label='Buscar', widget=_w(placeholder='Nro. doc, descripción…'))
    cost_center = forms.ModelChoiceField(
        queryset=CostCenter.objects.filter(active=True),
        required=False, label='Centro de costos', widget=_s(),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        tin        = _get_company(user)
        is_holding = _is_holding(user)
        self.fields['tin'].queryset         = _tin_qs(user)
        self.fields['cost_center'].queryset = _costcenter_qs(user)
        # Subsidiaria: ocultar el selector de empresa (solo ve la suya)
        if not is_holding and tin:
            self.fields['tin'].widget = forms.HiddenInput()
            self.fields['tin'].initial = tin
