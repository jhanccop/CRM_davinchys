"""
pagos_app/forms.py
"""
from django import forms
from django.forms import inlineformset_factory

from applications.COMERCIAL.sales.models import Items
from applications.cuentas.models import Tin, Account

"""
FINANTIAL/forms.py
"""
from django import forms
from django.forms import inlineformset_factory

from .models import (
    PaymentDocument, PaymentAllocation,
    PaymentTransaction, PaymentTransactionLine,
    BankMovements,MovementType,
    #ExpenseSubCategories, IncomeSubCategories,
)


# ─────────────────────────────────────────────────────────────────────────────
# Widget factories
# ─────────────────────────────────────────────────────────────────────────────
def _w(**kw):
    return forms.TextInput(attrs={'class': 'form-control form-control-sm', **kw})

def _s(**kw):
    return forms.Select(attrs={'class': 'form-select form-select-sm', **kw})

def _d(**kw):
    return forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date', **kw})

def _n(**kw):
    return forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01', **kw})

def _ta(**kw):
    return forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, **kw})

def _cb(**kw):
    return forms.CheckboxInput(attrs={'class': 'form-check-input', **kw})

def _file(**kw):
    return forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm', **kw})


# ─────────────────────────────────────────────────────────────────────────────
# PaymentDocument
# ─────────────────────────────────────────────────────────────────────────────
class PaymentDocumentForm(forms.ModelForm):

    class Meta:
        model  = PaymentDocument
        fields = [
            'doc_type', 'doc_number', 'direction',
            'tin_issuer', 'tin_receiver', 'client', 'supplier',
            'issue_date', 'due_date', 'declare_month', 'declare_year',
            'currency', 'exchange_rate',
            'gross_amount', 'tax_amount', 'net_amount',
            'has_detraction', 'detraction_amount',
            'has_retention',  'retention_amount',
            'annotation', 'account_category', 'cost_center',
            'short_description', 'description',
            'xml_file', 'pdf_file',
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
            'exchange_rate':     _n(placeholder='1.0000'),
            'gross_amount':      _n(placeholder='0.00'),
            'tax_amount':        _n(placeholder='0.00'),
            'net_amount':        _n(placeholder='0.00'),
            'has_detraction':    _cb(),
            'detraction_amount': _n(placeholder='0.00'),
            'has_retention':     _cb(),
            'retention_amount':  _n(placeholder='0.00'),
            'annotation':        _s(),
            'account_category':  _s(),
            'cost_center':       _w(placeholder='Centro de costo'),
            'short_description': _w(placeholder='Resumen del comprobante'),
            'description':       _ta(placeholder='Descripción detallada…'),
            'xml_file':          _file(),
            'pdf_file':          _file(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # Preseleccionar empresa para usuarios de subsidiaria
        if user and hasattr(user, 'empleado') and hasattr(user.empleado, 'company'):
            company = user.empleado.company
            if company.company_type != company.HOLDING:
                self.fields['tin_issuer'].initial  = company
                self.fields['tin_receiver'].initial = company

        self.fields['xml_file'].required  = False
        self.fields['pdf_file'].required  = False
        self.fields['net_amount'].required = False

    def clean(self):
        cleaned = super().clean()
        gross = cleaned.get('gross_amount') or 0
        tax   = cleaned.get('tax_amount')   or 0
        if not cleaned.get('net_amount'):
            cleaned['net_amount'] = gross - tax
        if cleaned.get('has_detraction') and not (cleaned.get('detraction_amount') or 0):
            self.add_error('detraction_amount', 'Ingrese el monto de detracción.')
        if cleaned.get('has_retention') and not (cleaned.get('retention_amount') or 0):
            self.add_error('retention_amount', 'Ingrese el monto de retención.')
        return cleaned


# ─────────────────────────────────────────────────────────────────────────────
# PaymentAllocation inline
# ─────────────────────────────────────────────────────────────────────────────
class PaymentAllocationForm(forms.ModelForm):
    class Meta:
        model   = PaymentAllocation
        fields  = ['item', 'allocated_amount', 'notes']
        widgets = {
            'item':             _s(),
            'allocated_amount': _n(placeholder='0.00'),
            'notes':            _w(placeholder='Observación'),
        }


PaymentAllocationFormSet = inlineformset_factory(
    PaymentDocument, PaymentAllocation,
    form=PaymentAllocationForm,
    extra=1, can_delete=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# PaymentTransaction
# ─────────────────────────────────────────────────────────────────────────────
class PaymentTransactionForm(forms.ModelForm):

    class Meta:
        model  = PaymentTransaction
        fields = [
            'reference', 'pay_method', 'transaction_date',
            'currency', 'exchange_rate', 'amount',
            'tin_payer', 'tin_receiver', 'client', 'supplier',
            'bank_account', 'bank_movement',
            'notes', 'voucher_file',
        ]
        widgets = {
            'reference':        _w(placeholder='Nro. operación / cheque'),
            'pay_method':       _s(),
            'transaction_date': _d(),
            'currency':         _s(),
            'exchange_rate':    _n(placeholder='1.0000'),
            'amount':           _n(placeholder='0.00'),
            'tin_payer':        _s(),
            'tin_receiver':     _s(),
            'client':           _s(),
            'supplier':         _s(),
            'bank_account':     _s(),
            'bank_movement':    _s(),
            'notes':            _ta(placeholder='Notas adicionales…'),
            'voucher_file':     _file(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher_file'].required  = False
        self.fields['bank_movement'].required = False
        self.fields['bank_movement'].label    = 'Movimiento bancario (para conciliación automática)'

        tin = None
        if user and hasattr(user, 'empleado') and hasattr(user.empleado, 'company'):
            tin = user.empleado.company

        is_holding = (tin is None) or (tin.company_type == Tin.HOLDING)

        if is_holding:
            self.fields['bank_account'].queryset  = Account.objects.filter(state=True).select_related('idTin')
            self.fields['bank_movement'].queryset = BankMovements.objects.filter(
                conciliated=False
            ).select_related('idAccount').order_by('-date')
        else:
            self.fields['bank_account'].queryset  = Account.objects.filter(idTin=tin, state=True)
            self.fields['bank_movement'].queryset = BankMovements.objects.filter(
                tin=tin, conciliated=False
            ).select_related('idAccount').order_by('-date')


# ─────────────────────────────────────────────────────────────────────────────
# PaymentTransactionLine inline
# ─────────────────────────────────────────────────────────────────────────────
class PaymentTransactionLineForm(forms.ModelForm):
    class Meta:
        model   = PaymentTransactionLine
        fields  = ['document', 'amount_applied', 'notes']
        widgets = {
            'document':       _s(),
            'amount_applied': _n(placeholder='0.00'),
            'notes':          _w(placeholder='Observación'),
        }


PaymentTransactionLineFormSet = inlineformset_factory(
    PaymentTransaction, PaymentTransactionLine,
    form=PaymentTransactionLineForm,
    extra=1, can_delete=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# Dashboard filters
# ─────────────────────────────────────────────────────────────────────────────
class DashboardFilterForm(forms.Form):
    tin = forms.ModelChoiceField(
        queryset=Tin.objects.all().order_by('tinName'),
        required=False, label='Empresa', widget=_s(),
    )
    direction = forms.ChoiceField(
        choices=[('', 'Todos')] + list(PaymentDocument._meta.get_field('direction').choices),
        required=False, label='Dirección', widget=_s(),
    )
    status = forms.ChoiceField(
        choices=[('', 'Todos')] + list(PaymentDocument._meta.get_field('status').choices),
        required=False, label='Estado', widget=_s(),
    )
    currency = forms.ChoiceField(
        choices=[('', 'Todas')] + list(PaymentDocument._meta.get_field('currency').choices),
        required=False, label='Moneda', widget=_s(),
    )
    date_from = forms.DateField(required=False, label='Desde', widget=_d())
    date_to   = forms.DateField(required=False, label='Hasta',  widget=_d())
    search    = forms.CharField(
        required=False, label='Buscar',
        widget=_w(placeholder='Nro. doc, descripción…'),
    )


# ─────────────────────────────────────────────────────────────────────────────
# BankMovements form (para uso en vistas de movimientos bancarios)
# ─────────────────────────────────────────────────────────────────────────────
class BankMovementsForm(forms.ModelForm):

    class Meta:
        model  = BankMovements
        fields = [
            'idAccount', 'movementType', 'date', 'description',
            'opNumber', 'originDestination',
            'expenseSubCategory', 'incomeSubCategory',
            'amount', 'equivalentAmount', 'justification',
            'payment_transaction', 'pdf_file',
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
            'amount':             _n(placeholder='0.00'),
            'equivalentAmount':   _n(placeholder='0.00'),
            'justification':      _ta(placeholder='Justificación contable…'),
            'payment_transaction':_s(),
            'pdf_file':           _file(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pdf_file'].required          = False
        self.fields['payment_transaction'].required = False
        self.fields['equivalentAmount'].required  = False

        tin = None
        if user and hasattr(user, 'empleado') and hasattr(user.empleado, 'company'):
            tin = user.empleado.company

        is_holding = (tin is None) or (tin.company_type == Tin.HOLDING)

        if not is_holding and tin:
            self.fields['idAccount'].queryset = Account.objects.filter(idTin=tin, state=True)
        else:
            self.fields['idAccount'].queryset = Account.objects.filter(state=True).select_related('idTin')

        self.fields['movementType'].queryset = MovementType.objects.filter(active=True)