
"""
FINANTIAL/views.py  — v3
"""
import csv
import io
from datetime import date, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Sum, Count, Q, F, Avg, OuterRef, Subquery
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView,
    DeleteView, TemplateView, View,
)

from .forms import (
    PaymentDocumentForm, PaymentAllocationFormSet,
    PaymentTransactionForm, PaymentTransactionLineFormSet,
    DashboardFilterForm, BankMovementsForm,
    MonthlyClosureForm, ReopenClosureForm,
    ExchangeRateForm, TaxCodeForm, CostCenterForm,
    AccountingAccountForm, JournalEntryForm, JournalEntryLineFormSet,
    BankStatementImportForm,
)
from .models import (
    PaymentDocument, PaymentAllocation,
    PaymentTransaction, PaymentTransactionLine,
    BankMovements, MovementType,
    CostCenter, AccountingAccount, ExchangeRate, TaxCode,
    MonthlyClosure, JournalEntry, JournalEntryLine,
    MONTH_CHOICES,
)

from applications.cuentas.models import Account, Tin

# =============================================================================
# MIXIN BASE
# =============================================================================
class CompanyContextMixin(LoginRequiredMixin):

    def _get_user_tin(self):
        user = self.request.user
        if hasattr(user,'empleado') and hasattr(user.empleado,'company'):
            return user.empleado.company
        return None

    def _is_holding(self):
        tin = self._get_user_tin()
        if tin is None:
            return self.request.user.is_superuser
        return tin.company_type == Tin.HOLDING

    def _get_user_accounts(self):
        tin = self._get_user_tin()
        if self._is_holding() or tin is None:
            return Account.objects.filter(state=True).select_related('idTin').order_by('idTin__tinName')
        return Account.objects.filter(idTin=tin, state=True)

    def get_doc_queryset(self):
        qs = PaymentDocument.objects.select_related(
            'tin_issuer','tin_receiver','client','supplier','created_by','cost_center','tax_code'
        )
        if self._is_holding(): return qs.all()
        tin = self._get_user_tin()
        return qs.filter(Q(tin_issuer=tin)|Q(tin_receiver=tin)) if tin else qs.none()

    def get_tx_queryset(self):
        qs = PaymentTransaction.objects.select_related(
            'tin_payer','tin_receiver','client','supplier',
            'bank_account__idTin','bank_movement','cost_center','created_by'
        )
        if self._is_holding(): return qs.all()
        tin = self._get_user_tin()
        return qs.filter(Q(tin_payer=tin)|Q(tin_receiver=tin)) if tin else qs.none()

    def get_mov_queryset(self):
        qs = BankMovements.objects.select_related(
            'idAccount__idTin','tin','movementType','originDestination','payment_transaction','cost_center'
        )
        if self._is_holding(): return qs.all()
        tin = self._get_user_tin()
        return qs.filter(tin=tin) if tin else qs.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_tin']   = self._get_user_tin()
        ctx['is_holding'] = self._is_holding()
        return ctx


# =============================================================================
# DASHBOARD
# =============================================================================
class PaymentDashboardView(CompanyContextMixin, TemplateView):
    template_name = 'FINANTIAL/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx    = super().get_context_data(**kwargs)
        doc_qs = self.get_doc_queryset()
        tx_qs  = self.get_tx_queryset()
        mov_qs = self.get_mov_queryset()

        ctx['total_docs']   = doc_qs.count()
        ctx['pending_docs'] = doc_qs.filter(status='PENDING').count()
        ctx['partial_docs'] = doc_qs.filter(status='PARTIAL').count()
        ctx['paid_docs']    = doc_qs.filter(status='PAID').count()

        agg = doc_qs.aggregate(
            total_gross=Sum('gross_amount'), total_net=Sum('net_amount'),
            total_paid=Sum('paid_amount'),   total_pending=Sum('pending_amount'),
        )
        ctx.update({k: v or 0 for k, v in agg.items()})

        for d in ('IN','OUT','INT'):
            ctx[f'docs_{d.lower()}'] = doc_qs.filter(direction=d).aggregate(
                cnt=Count('id'), total=Sum('net_amount'))

        ctx['recent_pending']      = doc_qs.filter(status__in=['PENDING','PARTIAL']).order_by('-created')[:10]
        ctx['recent_transactions'] = tx_qs.order_by('-transaction_date')[:5]
        ctx['pending_movements']   = mov_qs.filter(conciliated=False).order_by('-date')[:8]

        if ctx['is_holding']:
            ctx['by_tin'] = (
                doc_qs.values('tin_issuer__tinName')
                .annotate(cnt=Count('id'), total_net=Sum('net_amount'), total_paid=Sum('paid_amount'))
                .order_by('-total_net')[:8]
            )

        ctx['accounts']         = self._get_user_accounts()
        ctx['filter_form']      = DashboardFilterForm(self.request.GET or None, user=self.request.user)

        # Alertas de cierre próximo (períodos que cierran este mes)
        import datetime
        today = datetime.date.today()
        ctx['open_closures'] = MonthlyClosure.objects.filter(
            status='OPEN', period_year=today.year, period_month=today.month
        ).select_related('account','tin')[:5]

        # Tipo de cambio del día
        ctx['today_rate'] = ExchangeRate.objects.filter(
            from_currency='USD', to_currency='PEN',
            rate_date__lte=today
        ).order_by('-rate_date').first()

        return ctx


# =============================================================================
# DOCUMENT CRUD — con mixin compartido
# =============================================================================
class _DocFormMixin(CompanyContextMixin):
    template_name = 'FINANTIAL/document_form.html'
    form_class    = PaymentDocumentForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    # cost_level → PaymentDocument.direction mapping
    _LEVEL_TO_DIRECTION = {'QUO': 'IN', 'INT': 'INT', 'WO': 'OUT'}

    def _get_formset(self, instance=None, prefill_item=None, prefill_cost_level=None):
        if not hasattr(self, '_fs'):
            kwargs = dict(
                data  = self.request.POST  if self.request.method == 'POST' else None,
                files = self.request.FILES if self.request.method == 'POST' else None,
            )
            if instance:
                kwargs['instance'] = instance
            # Pre-populate the first extra form when arriving from item-tracking
            if self.request.method == 'GET' and prefill_item:
                kwargs['initial'] = [{
                    'item':       prefill_item,
                    'cost_level': prefill_cost_level or 'QUO',
                }]
            fs = PaymentAllocationFormSet(**kwargs)
            # Restrict cost_level choices: subsidiary users cannot see/assign QUO level
            if not self._is_holding():
                from .models import PaymentAllocation as _PA
                allowed     = [_PA.COST_LEVEL_INT, _PA.COST_LEVEL_WO]
                sub_choices = [(k, v) for k, v in _PA.COST_LEVEL_CHOICES if k in allowed]
                for form in fs.forms:
                    form.fields['cost_level'].choices = sub_choices
                    form._allowed_levels = allowed
            self._fs = fs
        return self._fs

    def _formset_errors_msg(self, fs):
        errs = []
        for i, row_errors in enumerate(fs.errors):
            for field, msgs in row_errors.items():
                label = 'Ítem' if field == '__all__' else field
                errs.append(f'Fila {i+1} · {label}: {", ".join(msgs)}')
        errs += list(fs.non_form_errors())
        return ' | '.join(errs) if errs else 'Revise los ítems asignados.'

    def _form_errors_msg(self, form):
        errs = []
        for field, msgs in form.errors.items():
            if field == '__all__':
                errs += list(msgs)
            else:
                label = form.fields[field].label if field in form.fields else field
                errs.append(f'{label}: {", ".join(msgs)}')
        return ' | '.join(errs) if errs else 'Por favor corrija los errores del formulario.'


class PaymentDocumentListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/document_list.html'
    context_object_name = 'documents'
    paginate_by         = 25

    def get_queryset(self):
        qs = self.get_doc_queryset()
        f  = DashboardFilterForm(self.request.GET or None, user=self.request.user)
        if f.is_valid():
            cd = f.cleaned_data
            if cd.get('tin'):
                qs = qs.filter(Q(tin_issuer=cd['tin'])|Q(tin_receiver=cd['tin']))
            if cd.get('direction'): qs = qs.filter(direction=cd['direction'])
            if cd.get('status'):    qs = qs.filter(status=cd['status'])
            if cd.get('currency'):  qs = qs.filter(currency=cd['currency'])
            if cd.get('date_from'): qs = qs.filter(issue_date__gte=cd['date_from'])
            if cd.get('date_to'):   qs = qs.filter(issue_date__lte=cd['date_to'])
            if cd.get('cost_center'): qs = qs.filter(cost_center=cd['cost_center'])
            if cd.get('search'):
                q = cd['search']
                qs = qs.filter(
                    Q(doc_number__icontains=q)|Q(short_description__icontains=q)|Q(description__icontains=q)
                )
        return qs.order_by('-issue_date','-created')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filter_form'] = DashboardFilterForm(self.request.GET or None, user=self.request.user)
        return ctx


class PaymentDocumentDetailView(CompanyContextMixin, DetailView):
    template_name       = 'FINANTIAL/document_detail.html'
    context_object_name = 'document'

    def get_object(self):
        return get_object_or_404(self.get_doc_queryset(), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        doc = self.object
        ctx['allocations'] = doc.allocations.select_related('item__idTrafo').all()
        ctx['tx_lines']    = doc.transaction_lines.select_related(
            'transaction__bank_account__idTin','transaction__bank_movement'
        ).all()
        # Advertencia de sobre-pago
        ctx['overpaid'] = doc.paid_amount > doc.net_amount
        return ctx


class PaymentDocumentCreateView(_DocFormMixin, CreateView):

    def _get_prefill(self):
        """Return (item_pk, cost_level) from GET params, or (None, None)."""
        item_pk    = self.request.GET.get('item')
        cost_level = self.request.GET.get('cost_level', 'QUO').upper()
        if cost_level not in ('QUO', 'INT', 'WO'):
            cost_level = 'QUO'
        return item_pk, cost_level

    def get_initial(self):
        initial = super().get_initial()
        item_pk, cost_level = self._get_prefill()
        if item_pk:
            initial['direction'] = self._LEVEL_TO_DIRECTION.get(cost_level, 'IN')
        return initial

    def get_context_data(self, **kwargs):
        item_pk, cost_level = self._get_prefill()
        ctx = super().get_context_data(**kwargs)
        ctx['allocation_formset'] = self._get_formset(
            prefill_item=item_pk, prefill_cost_level=cost_level
        )
        ctx['title']             = 'Registrar Comprobante'
        ctx['action']            = 'create'
        # Pass to template so JS can auto-activate flow button & show info banner
        ctx['prefill_item_pk']   = item_pk
        ctx['prefill_cost_level']= cost_level
        ctx['prefill_direction'] = self._LEVEL_TO_DIRECTION.get(cost_level, '') if item_pk else ''
        # Load item info for the banner
        if item_pk:
            from applications.COMERCIAL.sales.models import Items
            try:
                ctx['prefill_item_obj'] = Items.objects.select_related(
                    'idTrafo', 'idTrafoQuote', 'idTrafoIntQuote', 'idWorkOrder'
                ).get(pk=item_pk)
            except Items.DoesNotExist:
                ctx['prefill_item_obj'] = None
        return ctx

    def form_valid(self, form):
        fs = self._get_formset()
        if fs.is_valid():
            doc = form.save(commit=False)
            doc.created_by = self.request.user
            doc.save()
            fs.instance = doc
            fs.save()
            messages.success(self.request, f'Comprobante {doc} registrado correctamente.')
            return redirect(reverse('finantial:document-detail', kwargs={'pk': doc.pk}))
        messages.error(self.request, f'Errores en ítems: {self._formset_errors_msg(fs)}')
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, self._form_errors_msg(form))
        return self.render_to_response(self.get_context_data(form=form))


class PaymentDocumentUpdateView(_DocFormMixin, UpdateView):
    def get_object(self):
        return get_object_or_404(self.get_doc_queryset(), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['allocation_formset'] = self._get_formset(instance=self.object)
        ctx['title']  = f'Editar — {self.object}'
        ctx['action'] = 'update'
        return ctx

    def form_valid(self, form):
        fs = self._get_formset(instance=self.object)
        if fs.is_valid():
            doc = form.save()
            fs.instance = doc
            fs.save()
            messages.success(self.request, 'Comprobante actualizado correctamente.')
            return redirect(reverse('finantial:document-detail', kwargs={'pk': doc.pk}))
        messages.error(self.request, f'Errores en ítems: {self._formset_errors_msg(fs)}')
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, self._form_errors_msg(form))
        return self.render_to_response(self.get_context_data(form=form))


class PaymentDocumentDeleteView(CompanyContextMixin, DeleteView):
    template_name       = 'FINANTIAL/document_confirm_delete.html'
    success_url         = reverse_lazy('finantial:document-list')
    context_object_name = 'document'

    def get_object(self):
        return get_object_or_404(self.get_doc_queryset(), pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.warning(self.request, 'Comprobante eliminado.')
        return super().form_valid(form)


# =============================================================================
# TRANSACTION CRUD — con mixin compartido
# =============================================================================
class _TxFormMixin(CompanyContextMixin):
    template_name = 'FINANTIAL/transaction_form.html'
    form_class    = PaymentTransactionForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def _get_line_formset(self, instance=None):
        if not hasattr(self, '_lfs'):
            kwargs = dict(
                data  = self.request.POST  if self.request.method == 'POST' else None,
                files = self.request.FILES if self.request.method == 'POST' else None,
            )
            if instance:
                kwargs['instance'] = instance
            self._lfs = PaymentTransactionLineFormSet(**kwargs)
        return self._lfs

    def _apply_doc_queryset(self, fs):
        doc_qs = self.get_doc_queryset().filter(status__in=['PENDING','PARTIAL'])
        for f in fs.forms:
            f.fields['document'].queryset = doc_qs
        return doc_qs

    def _formset_errors_msg(self, fs):
        errs = []
        for i, row_errors in enumerate(fs.errors):
            for field, msgs in row_errors.items():
                label = 'Línea' if field == '__all__' else field
                errs.append(f'Fila {i+1} · {label}: {", ".join(msgs)}')
        errs += list(fs.non_form_errors())
        return ' | '.join(errs) if errs else 'Revise las líneas.'

    def _form_errors_msg(self, form):
        errs = []
        for field, msgs in form.errors.items():
            if field == '__all__':
                errs += list(msgs)
            else:
                label = form.fields[field].label if field in form.fields else field
                errs.append(f'{label}: {", ".join(msgs)}')
        return ' | '.join(errs) if errs else 'Por favor corrija los errores.'


class PaymentTransactionListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by         = 25

    def get_queryset(self):
        qs = self.get_tx_queryset().order_by('-transaction_date','-created')
        qs = qs.select_related('cost_center')
        # Annotate with journal_entry id (safe: None if no journal entry exists)
        qs = qs.annotate(
            journal_entry_id=Subquery(
                JournalEntry.objects.filter(payment_transaction=OuterRef('pk')).values('pk')[:1]
            )
        )
        q         = self.request.GET.get('q')
        status    = self.request.GET.get('status')
        date_from = self.request.GET.get('date_from')
        date_to   = self.request.GET.get('date_to')
        if q:         qs = qs.filter(Q(reference__icontains=q)|Q(notes__icontains=q))
        if status:    qs = qs.filter(status=status)
        try:
            if date_from: qs = qs.filter(transaction_date__gte=date_from)
            if date_to:   qs = qs.filter(transaction_date__lte=date_to)
        except Exception:
            pass
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q']         = self.request.GET.get('q','')
        ctx['status']    = self.request.GET.get('status','')
        ctx['date_from'] = self.request.GET.get('date_from','')
        ctx['date_to']   = self.request.GET.get('date_to','')
        return ctx


class PaymentTransactionDetailView(CompanyContextMixin, DetailView):
    template_name       = 'FINANTIAL/transaction_detail.html'
    context_object_name = 'transaction'

    def get_object(self):
        return get_object_or_404(self.get_tx_queryset(), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['lines'] = self.object.transaction_lines.select_related('document').all()
        # Alertas de sobre-pago por línea
        warnings = []
        for line in ctx['lines']:
            doc = line.document
            if line.amount_applied > doc.pending_amount:
                warnings.append(
                    f'{doc.doc_number or doc.id}: aplicado {line.amount_applied} > pendiente {doc.pending_amount}'
                )
        ctx['overpay_warnings'] = warnings
        # Asiento contable vinculado si existe
        ctx['journal_entry'] = getattr(self.object, 'journal_entry', None)
        return ctx


class PaymentTransactionCreateView(_TxFormMixin, CreateView):
    def get_context_data(self, **kwargs):
        ctx    = super().get_context_data(**kwargs)
        fs     = self._get_line_formset()
        doc_qs = self._apply_doc_queryset(fs)
        ctx['line_formset'] = fs
        ctx['title']        = 'Registrar Pago'
        ctx['action']       = 'create'
        ctx['pending_docs'] = doc_qs.order_by('-issue_date')[:50]
        return ctx

    def form_valid(self, form):
        fs = self._get_line_formset()
        self._apply_doc_queryset(fs)
        if fs.is_valid():
            tx = form.save(commit=False)
            tx.created_by = self.request.user
            tx.save()
            fs.instance = tx
            fs.save()
            messages.success(self.request, f'TX-{tx.id} guardada como borrador. Confirme para aplicar los pagos.')
            return redirect(reverse('finantial:transaction-detail', kwargs={'pk': tx.pk}))
        messages.error(self.request, f'Errores en líneas: {self._formset_errors_msg(fs)}')
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, self._form_errors_msg(form))
        return self.render_to_response(self.get_context_data(form=form))


class PaymentTransactionUpdateView(_TxFormMixin, UpdateView):
    def get_object(self):
        return get_object_or_404(self.get_tx_queryset(), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx    = super().get_context_data(**kwargs)
        fs     = self._get_line_formset(instance=self.object)
        doc_qs = self._apply_doc_queryset(fs)
        ctx['line_formset'] = fs
        ctx['title']        = f'Editar TX-{self.object.id}'
        ctx['action']       = 'update'
        ctx['pending_docs'] = doc_qs.order_by('-issue_date')[:50]
        return ctx

    def form_valid(self, form):
        fs = self._get_line_formset(instance=self.object)
        self._apply_doc_queryset(fs)
        if fs.is_valid():
            tx = form.save()
            fs.instance = tx
            fs.save()
            messages.success(self.request, 'Transacción actualizada.')
            return redirect(reverse('finantial:transaction-detail', kwargs={'pk': tx.pk}))
        messages.error(self.request, f'Errores en líneas: {self._formset_errors_msg(fs)}')
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, self._form_errors_msg(form))
        return self.render_to_response(self.get_context_data(form=form))


class PaymentTransactionDeleteView(CompanyContextMixin, DeleteView):
    template_name       = 'FINANTIAL/transaction_confirm_delete.html'
    success_url         = reverse_lazy('finantial:transaction-list')
    context_object_name = 'transaction'

    def get_object(self):
        return get_object_or_404(self.get_tx_queryset(), pk=self.kwargs['pk'])


class ConfirmTransactionView(CompanyContextMixin, View):
    def post(self, request, pk):
        tx = get_object_or_404(self.get_tx_queryset(), pk=pk)
        if tx.status != 'DRAFT':
            messages.warning(request, f'TX-{tx.id} ya fue procesada ({tx.get_status_display()}).')
            return redirect(reverse('finantial:transaction-detail', kwargs={'pk': pk}))
        try:
            tx.confirm()
            messages.success(request, f'TX-{tx.id} confirmada. Comprobantes actualizados.')
            if hasattr(tx, 'journal_entry'):
                messages.info(request, f'Asiento contable AST-{tx.journal_entry.id} generado automáticamente.')
        except ValidationError as e:
            messages.error(request, f'No se pudo confirmar: {e.message}')
        return redirect(reverse('finantial:transaction-detail', kwargs={'pk': pk}))


# =============================================================================
# BANK MOVEMENTS CRUD
# =============================================================================
class BankMovementsListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/movement_list.html'
    context_object_name = 'movements'
    paginate_by         = 30

    def get_queryset(self):
        qs = self.get_mov_queryset().order_by('-date','-created')
        q           = self.request.GET.get('q')
        account_id  = self.request.GET.get('account')
        conciliated = self.request.GET.get('conciliated')
        flow        = self.request.GET.get('flow')
        date_from   = self.request.GET.get('date_from')
        date_to     = self.request.GET.get('date_to')
        if q:          qs = qs.filter(Q(description__icontains=q)|Q(opNumber__icontains=q))
        if account_id: qs = qs.filter(idAccount_id=account_id)
        if conciliated in ('0','1'): qs = qs.filter(conciliated=conciliated=='1')
        if flow in ('0','1'):        qs = qs.filter(movementType__flow=flow)
        try:
            if date_from: qs = qs.filter(date__gte=date_from)
            if date_to:   qs = qs.filter(date__lte=date_to)
        except Exception:
            pass
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accounts']        = self._get_user_accounts()
        ctx['q']               = self.request.GET.get('q','')
        ctx['sel_account']     = self.request.GET.get('account','')
        ctx['sel_conciliated'] = self.request.GET.get('conciliated','')
        ctx['sel_flow']        = self.request.GET.get('flow','')
        ctx['date_from']       = self.request.GET.get('date_from','')
        ctx['date_to']         = self.request.GET.get('date_to','')
        return ctx


class BankMovementsDetailView(CompanyContextMixin, DetailView):
    template_name       = 'FINANTIAL/movement_detail.html'
    context_object_name = 'movement'

    def get_object(self):
        return get_object_or_404(self.get_mov_queryset(), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['conciliations'] = self.object.mov_origen.select_related('idDoc','idMovArrival__idAccount').all()
        return ctx


class BankMovementsCreateView(CompanyContextMixin, CreateView):
    template_name = 'FINANTIAL/movement_form.html'
    form_class    = BankMovementsForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title']  = 'Registrar Movimiento'
        ctx['action'] = 'create'
        return ctx

    def form_valid(self, form):
        try:
            mov = form.save()
            messages.success(self.request, f'Movimiento MOV-{mov.id} registrado.')
            return redirect(reverse('finantial:movement-detail', kwargs={'pk': mov.pk}))
        except ValidationError as e:
            messages.error(self.request, str(e.message))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrija los errores.')
        return super().form_invalid(form)


class BankMovementsUpdateView(CompanyContextMixin, UpdateView):
    template_name = 'FINANTIAL/movement_form.html'
    form_class    = BankMovementsForm

    def get_object(self):
        return get_object_or_404(self.get_mov_queryset(), pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title']  = f'Editar MOV-{self.object.id}'
        ctx['action'] = 'update'
        return ctx

    def form_valid(self, form):
        try:
            mov = form.save()
            messages.success(self.request, 'Movimiento actualizado.')
            return redirect(reverse('finantial:movement-detail', kwargs={'pk': mov.pk}))
        except ValidationError as e:
            messages.error(self.request, str(e.message))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrija los errores.')
        return super().form_invalid(form)


class BankMovementsDeleteView(CompanyContextMixin, DeleteView):
    template_name       = 'FINANTIAL/movement_confirm_delete.html'
    success_url         = reverse_lazy('finantial:movement-list')
    context_object_name = 'movement'

    def get_object(self):
        return get_object_or_404(self.get_mov_queryset(), pk=self.kwargs['pk'])


# =============================================================================
# MONTHLY CLOSURE  (SAP F.16)
# =============================================================================
class MonthlyClosureListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/closure_list.html'
    context_object_name = 'closures'
    paginate_by         = 20

    def get_queryset(self):
        qs = MonthlyClosure.objects.select_related('account','tin','closed_by','approved_by')
        if not self._is_holding():
            tin = self._get_user_tin()
            if tin: qs = qs.filter(tin=tin)
        year  = self.request.GET.get('year')
        month = self.request.GET.get('month')
        status= self.request.GET.get('status')
        if year:   qs = qs.filter(period_year=year)
        if month:  qs = qs.filter(period_month=month)
        if status: qs = qs.filter(status=status)
        return qs.order_by('-period_year','-period_month','account')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accounts'] = self._get_user_accounts()
        ctx['sel_year']   = self.request.GET.get('year','')
        ctx['sel_month']  = self.request.GET.get('month','')
        ctx['sel_status'] = self.request.GET.get('status','')
        ctx['meses'] = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun','Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        return ctx


class MonthlyClosureDetailView(CompanyContextMixin, DetailView):
    template_name       = 'FINANTIAL/closure_detail.html'
    context_object_name = 'closure'
    model               = MonthlyClosure

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        c   = self.object
        # Movimientos del período
        ctx['movements'] = BankMovements.objects.filter(
            idAccount=c.account, date__year=c.period_year, date__month=c.period_month
        ).select_related('movementType','originDestination').order_by('date')
        ctx['unreconciled'] = ctx['movements'].filter(conciliated=False)
        ctx['reopen_form'] = ReopenClosureForm() if c.status in ('CLOSED','APPROVED') else None
        return ctx


class MonthlyClosureCreateView(CompanyContextMixin, CreateView):
    template_name = 'FINANTIAL/closure_form.html'
    form_class    = MonthlyClosureForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Crear Período de Cierre'
        return ctx

    def form_valid(self, form):
        closure = form.save()
        messages.success(self.request, f'Período {closure.period_label} creado.')
        return redirect(reverse('finantial:closure-detail', kwargs={'pk': closure.pk}))


class CloseMonthView(CompanyContextMixin, View):
    """Ejecuta el cierre del período."""
    def post(self, request, pk):
        closure = get_object_or_404(MonthlyClosure, pk=pk)
        try:
            closure.close(request.user)
            messages.success(request,
                f'Período {closure.period_label} cerrado. '
                f'{closure.movements_count} movimientos, '
                f'{closure.unreconciled_count} sin conciliar. '
                f'Saldo final: {closure.closing_balance}.'
            )
            if closure.unreconciled_count > 0:
                messages.warning(request,
                    f'Hay {closure.unreconciled_count} movimiento(s) sin conciliar en el período cerrado.'
                )
        except ValidationError as e:
            messages.error(request, str(e.message))
        return redirect(reverse('finantial:closure-detail', kwargs={'pk': pk}))


class ApproveClosureView(CompanyContextMixin, View):
    """Aprobación gerencial del cierre."""
    def post(self, request, pk):
        closure = get_object_or_404(MonthlyClosure, pk=pk)
        try:
            closure.approve(request.user)
            messages.success(request, f'Período {closure.period_label} aprobado por {request.user}.')
        except ValidationError as e:
            messages.error(request, str(e.message))
        return redirect(reverse('finantial:closure-detail', kwargs={'pk': pk}))


class ReopenClosureView(CompanyContextMixin, View):
    """Reapertura del período con justificación."""
    def post(self, request, pk):
        closure = get_object_or_404(MonthlyClosure, pk=pk)
        form    = ReopenClosureForm(request.POST)
        if form.is_valid():
            try:
                closure.reopen(request.user, form.cleaned_data['reason'])
                messages.warning(request,
                    f'Período {closure.period_label} reabierto. '
                    f'Queda registrado para auditoría.'
                )
            except ValidationError as e:
                messages.error(request, str(e.message))
        else:
            messages.error(request, 'El motivo de reapertura es requerido (mínimo 20 caracteres).')
        return redirect(reverse('finantial:closure-detail', kwargs={'pk': pk}))


# =============================================================================
# JOURNAL ENTRIES  (SAP FB50)
# =============================================================================
class JournalEntryListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/journal_list.html'
    context_object_name = 'entries'
    paginate_by         = 25

    def get_queryset(self):
        qs = JournalEntry.objects.select_related('tin','cost_center','payment_transaction')
        if not self._is_holding():
            tin = self._get_user_tin()
            if tin: qs = qs.filter(tin=tin)
        is_posted = self.request.GET.get('posted')
        date_from = self.request.GET.get('date_from')
        date_to   = self.request.GET.get('date_to')
        if is_posted in ('0','1'): qs = qs.filter(is_posted=is_posted=='1')
        try:
            if date_from: qs = qs.filter(entry_date__gte=date_from)
            if date_to:   qs = qs.filter(entry_date__lte=date_to)
        except Exception:
            pass
        return qs.order_by('-entry_date','-created')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['date_from'] = self.request.GET.get('date_from','')
        ctx['date_to']   = self.request.GET.get('date_to','')
        return ctx


class JournalEntryDetailView(CompanyContextMixin, DetailView):
    template_name       = 'FINANTIAL/journal_detail.html'
    context_object_name = 'entry'
    model               = JournalEntry

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['lines']      = self.object.lines.select_related('account','cost_center','tax_code').all()
        ctx['is_balanced']= self.object.is_balanced
        return ctx


class JournalEntryCreateView(CompanyContextMixin, CreateView):
    template_name = 'FINANTIAL/journal_form.html'
    form_class    = JournalEntryForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not hasattr(self, '_jlfs'):
            self._jlfs = (
                JournalEntryLineFormSet(self.request.POST)
                if self.request.method == 'POST'
                else JournalEntryLineFormSet()
            )
        ctx['line_formset'] = self._jlfs
        ctx['title']  = 'Nuevo Asiento Contable'
        ctx['action'] = 'create'
        return ctx

    def form_valid(self, form):
        if not hasattr(self, '_jlfs'):
            self._jlfs = JournalEntryLineFormSet(self.request.POST)
        fs = self._jlfs
        if fs.is_valid():
            entry = form.save()
            fs.instance = entry
            fs.save()
            messages.success(self.request, f'Asiento AST-{entry.id} creado.')
            return redirect(reverse('finantial:journal-detail', kwargs={'pk': entry.pk}))
        messages.error(self.request, 'Revise las líneas del asiento.')
        return self.render_to_response(self.get_context_data(form=form))


class PostJournalEntryView(CompanyContextMixin, View):
    """Contabiliza el asiento (equivale a SAP 'Grabar')."""
    def post(self, request, pk):
        entry = get_object_or_404(JournalEntry, pk=pk)
        if entry.is_posted:
            messages.warning(request, 'El asiento ya fue contabilizado.')
        else:
            try:
                entry.post(request.user)
                messages.success(request, f'Asiento AST-{entry.id} contabilizado.')
            except ValidationError as e:
                messages.error(request, str(e.message))
        return redirect(reverse('finantial:journal-detail', kwargs={'pk': pk}))


# =============================================================================
# SAP CATALOG VIEWS — ExchangeRate, TaxCode, CostCenter, AccountingAccount
# =============================================================================
class ExchangeRateListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/exchangerate_list.html'
    context_object_name = 'rates'
    paginate_by         = 30
    queryset            = ExchangeRate.objects.all().order_by('-rate_date')


class ExchangeRateCreateView(CompanyContextMixin, CreateView):
    template_name = 'FINANTIAL/catalog_form.html'
    form_class    = ExchangeRateForm
    success_url   = reverse_lazy('finantial:exchangerate-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title']   = 'Nuevo Tipo de Cambio'
        ctx['back_url']= reverse_lazy('finantial:exchangerate-list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de cambio registrado.')
        return super().form_valid(form)


class TaxCodeListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/taxcode_list.html'
    context_object_name = 'codes'
    queryset            = TaxCode.objects.select_related('accounting_account').order_by('tax_type','code')


class TaxCodeCreateView(CompanyContextMixin, CreateView):
    template_name = 'FINANTIAL/catalog_form.html'
    form_class    = TaxCodeForm
    success_url   = reverse_lazy('finantial:taxcode-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title']   = 'Nuevo Código de Impuesto'
        ctx['back_url']= reverse_lazy('finantial:taxcode-list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Código de impuesto registrado.')
        return super().form_valid(form)


class CostCenterListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/costcenter_list.html'
    context_object_name = 'cost_centers'

    def get_queryset(self):
        qs = CostCenter.objects.select_related('tin','responsible')
        if not self._is_holding():
            tin = self._get_user_tin()
            if tin: qs = qs.filter(tin=tin)
        return qs.order_by('tin__tinName','code')


class CostCenterCreateView(CompanyContextMixin, CreateView):
    template_name = 'FINANTIAL/catalog_form.html'
    form_class    = CostCenterForm
    success_url   = reverse_lazy('finantial:costcenter-list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title']   = 'Nuevo Centro de Costos'
        ctx['back_url']= reverse_lazy('finantial:costcenter-list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Centro de costos registrado.')
        return super().form_valid(form)


class AccountingAccountListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/chart_of_accounts.html'
    context_object_name = 'accounts'
    queryset            = AccountingAccount.objects.select_related('bank_account').order_by('code')


class AccountingAccountCreateView(CompanyContextMixin, CreateView):
    template_name = 'FINANTIAL/catalog_form.html'
    form_class    = AccountingAccountForm
    success_url   = reverse_lazy('finantial:chart-of-accounts')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title']   = 'Nueva Cuenta Contable'
        ctx['back_url']= reverse_lazy('finantial:chart-of-accounts')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Cuenta contable registrada.')
        return super().form_valid(form)


# =============================================================================
# ITEM TRACKING
# =============================================================================
class ItemTrackingView(CompanyContextMixin, TemplateView):
    template_name = 'FINANTIAL/item_tracking.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from applications.COMERCIAL.sales.models import Items, quotes, IntQuotes, WorkOrder

        quote_id     = self.request.GET.get('quote')
        int_quote_id = self.request.GET.get('int_quote')
        wo_id        = self.request.GET.get('work_order')

        items_qs = Items.objects.select_related(
            'idTrafo','idTrafoQuote','idTrafoIntQuote','idWorkOrder'
        ).prefetch_related('payment_allocations__document')

        if not ctx['is_holding']:
            tin = ctx['user_tin']
            if tin:
                items_qs = items_qs.filter(
                    Q(idTrafoQuote__idTinReceiving=tin)|
                    Q(idTrafoIntQuote__idTinReceiving=tin)|
                    Q(idWorkOrder__idTinReceiving=tin)
                )

        if quote_id:     items_qs = items_qs.filter(idTrafoQuote_id=quote_id)
        if int_quote_id: items_qs = items_qs.filter(idTrafoIntQuote_id=int_quote_id)
        if wo_id:        items_qs = items_qs.filter(idWorkOrder_id=wo_id)

        def _level_data(allocs_by_level, unit_cost):
            """Compute coverage metrics for a single cost level."""
            if not unit_cost:
                return None
            unit_cost = Decimal(str(unit_cost))
            paid_docs    = [a for a in allocs_by_level if a.document.status in ('PAID', 'PARTIAL')]
            confirmed    = sum(a.allocated_amount for a in paid_docs) or Decimal('0')
            total_assigned = sum(a.allocated_amount for a in allocs_by_level) or Decimal('0')
            coverage     = float(confirmed / unit_cost * 100) if unit_cost else 0
            return {
                'unit_cost':      unit_cost,
                'confirmed_paid': confirmed,
                'coverage_pct':   round(min(coverage, 100), 1),
                'pending':        max(unit_cost - confirmed, Decimal('0')),
                'allocations':    allocs_by_level,
                'overpay_alert':  total_assigned > unit_cost,
                'total_assigned': total_assigned,
            }

        enriched = []
        for item in items_qs:
            all_allocs = list(item.payment_allocations.select_related('document').all())

            quo_allocs = [a for a in all_allocs if a.cost_level == 'QUO']
            int_allocs = [a for a in all_allocs if a.cost_level == 'INT']
            wo_allocs  = [a for a in all_allocs if a.cost_level == 'WO']

            level_quo = _level_data(quo_allocs, item.unitCost)
            level_int = _level_data(int_allocs, item.unitCostInt)
            level_wo  = _level_data(wo_allocs,  item.unitCostWO)

            # Subsidiary users: hide QUO level (Cliente→Holding margin is HOLDING-only)
            if not ctx['is_holding']:
                level_quo = None

            has_any_alloc = bool(all_allocs)
            any_overpay   = any(lv['overpay_alert'] for lv in (level_quo, level_int, level_wo) if lv)
            all_covered   = all(
                lv['coverage_pct'] >= 100
                for lv in (level_quo, level_int, level_wo) if lv
            ) if (level_quo or level_int or level_wo) else False

            enriched.append({
                'item':         item,
                'level_quo':    level_quo,
                'level_int':    level_int,
                'level_wo':     level_wo,
                'has_any_alloc': has_any_alloc,
                'any_overpay':  any_overpay,
                'all_covered':  all_covered,
            })

        ctx['enriched_items']    = enriched
        ctx['summary_paid_full'] = sum(1 for e in enriched if e['all_covered'])
        ctx['summary_no_docs']   = sum(1 for e in enriched if not e['has_any_alloc'])
        ctx['summary_overpay']   = sum(1 for e in enriched if e['any_overpay'])
        # Per-level independent totals (no agregado entre niveles — son flujos distintos)
        ctx['summary_quo_cost']  = sum(e['level_quo']['unit_cost']      for e in enriched if e['level_quo'])
        ctx['summary_quo_paid']  = sum(e['level_quo']['confirmed_paid'] for e in enriched if e['level_quo'])
        ctx['summary_int_cost']  = sum(e['level_int']['unit_cost']      for e in enriched if e['level_int'])
        ctx['summary_int_paid']  = sum(e['level_int']['confirmed_paid'] for e in enriched if e['level_int'])
        ctx['summary_wo_cost']   = sum(e['level_wo']['unit_cost']       for e in enriched if e['level_wo'])
        ctx['summary_wo_paid']   = sum(e['level_wo']['confirmed_paid']  for e in enriched if e['level_wo'])
        tin = ctx['user_tin']
        if ctx['is_holding'] or not tin:
            ctx['quotes']      = quotes.objects.all().order_by('-created')[:50]
            ctx['int_quotes']  = IntQuotes.objects.all().order_by('-created')[:50]
            ctx['work_orders'] = WorkOrder.objects.all().order_by('-created')[:50]
        else:
            ctx['quotes']      = quotes.objects.filter(idTinReceiving=tin).order_by('-created')[:50]
            ctx['int_quotes']  = IntQuotes.objects.filter(idTinReceiving=tin).order_by('-created')[:50]
            ctx['work_orders'] = WorkOrder.objects.filter(idTinReceiving=tin).order_by('-created')[:50]
        ctx['selected_quote']     = quote_id
        ctx['selected_int_quote'] = int_quote_id
        ctx['selected_wo']        = wo_id
        return ctx


# =============================================================================
# AJAX
# =============================================================================
class ItemPendingAmountView(CompanyContextMixin, View):
    def get(self, request, pk):
        from applications.COMERCIAL.sales.models import Items
        item = get_object_or_404(Items, pk=pk)

        def _level(lvl, unit_cost):
            alloc = float(
                item.payment_allocations.filter(cost_level=lvl).aggregate(
                    s=Sum('allocated_amount'))['s'] or 0
            )
            conf = float(
                item.payment_allocations.filter(
                    cost_level=lvl, document__status__in=['PAID', 'PARTIAL']
                ).aggregate(s=Sum('allocated_amount'))['s'] or 0
            )
            pending = max(unit_cost - alloc, 0)
            return {'unit_cost': unit_cost, 'allocated': alloc,
                    'confirmed': conf, 'pending': pending,
                    'overpay': alloc > unit_cost}

        uc_quo = float(item.unitCost    or 0)
        uc_int = float(item.unitCostInt or 0)
        uc_wo  = float(item.unitCostWO  or 0)

        quo_data = _level('QUO', uc_quo)
        int_data = _level('INT', uc_int)
        wo_data  = _level('WO',  uc_wo)

        return JsonResponse({
            'unit_cost_quo': uc_quo,
            'unit_cost_int': uc_int,
            'unit_cost_wo':  uc_wo,
            'quo_data': quo_data,
            'int_data': int_data,
            'wo_data':  wo_data,
        })


class DocumentPendingAmountView(CompanyContextMixin, View):
    """AJAX: devuelve el monto pendiente de un PaymentDocument."""
    def get(self, request, pk):
        doc = get_object_or_404(self.get_doc_queryset(), pk=pk)
        return JsonResponse({
            'net_amount':     float(doc.net_amount),
            'paid_amount':    float(doc.paid_amount),
            'pending_amount': float(doc.pending_amount),
            'status':         doc.status,
            'overpay':        doc.paid_amount > doc.net_amount,
        })


class ExchangeRateAPIView(CompanyContextMixin, View):
    """AJAX: devuelve el tipo de cambio más reciente para una fecha."""
    def get(self, request):
        from_cur = request.GET.get('from','USD')
        to_cur   = request.GET.get('to','PEN')
        date_str = request.GET.get('date')
        if date_str:
            import datetime
            try:
                d = datetime.date.fromisoformat(date_str)
                rate = ExchangeRate.get_rate(from_cur, to_cur, d)
                return JsonResponse({'rate': float(rate), 'found': rate != Decimal('1')})
            except ValueError:
                pass
        return JsonResponse({'rate': 1.0, 'found': False})


# =============================================================================
# MEDIA PRIORIDAD — Antigüedad de cartera (AR Aging)
# =============================================================================
class ARAgingView(CompanyContextMixin, TemplateView):
    template_name = 'FINANTIAL/ar_aging.html'

    def get_context_data(self, **kwargs):
        ctx   = super().get_context_data(**kwargs)
        today = date.today()

        pending = self.get_doc_queryset().filter(
            status__in=['PENDING', 'PARTIAL'],
        ).select_related('client', 'supplier', 'tin_issuer', 'tin_receiver')

        not_due = []
        b0_30   = []
        b31_60  = []
        b61_90  = []
        b90plus = []
        no_date = []

        for doc in pending:
            if not doc.due_date:
                no_date.append(doc)
                continue
            days = (today - doc.due_date).days
            if days <= 0:
                not_due.append(doc)
            elif days <= 30:
                b0_30.append(doc)
            elif days <= 60:
                b31_60.append(doc)
            elif days <= 90:
                b61_90.append(doc)
            else:
                b90plus.append(doc)

        def _total(lst):
            return sum(d.pending_amount for d in lst)

        ctx.update({
            'today':       today,
            'not_due':     not_due,     'total_not_due':  _total(not_due),
            'b0_30':       b0_30,       'total_0_30':     _total(b0_30),
            'b31_60':      b31_60,      'total_31_60':    _total(b31_60),
            'b61_90':      b61_90,      'total_61_90':    _total(b61_90),
            'b90plus':     b90plus,     'total_90plus':   _total(b90plus),
            'no_date':     no_date,     'total_no_date':  _total(no_date),
            'grand_total': _total(not_due + b0_30 + b31_60 + b61_90 + b90plus + no_date),
        })
        return ctx


# =============================================================================
# MEDIA PRIORIDAD — Flujo de caja proyectado
# =============================================================================
class CashFlowView(CompanyContextMixin, TemplateView):
    template_name = 'FINANTIAL/cashflow.html'

    def get_context_data(self, **kwargs):
        ctx   = super().get_context_data(**kwargs)
        today = date.today()

        base_qs = self.get_doc_queryset().filter(status__in=['PENDING', 'PARTIAL'])

        # Vencidos
        overdue = base_qs.filter(due_date__lt=today)
        overdue_in  = overdue.filter(direction='IN' ).aggregate(s=Sum('pending_amount'))['s'] or Decimal('0')
        overdue_out = overdue.filter(direction='OUT').aggregate(s=Sum('pending_amount'))['s'] or Decimal('0')

        # Próximos 90 días en tramos
        periods = [
            ('0 – 30 días',  today,               today + timedelta(days=30)),
            ('31 – 60 días', today + timedelta(31), today + timedelta(60)),
            ('61 – 90 días', today + timedelta(61), today + timedelta(90)),
        ]
        periods_data = []
        for label, start, end in periods:
            qs = base_qs.filter(due_date__gte=start, due_date__lte=end)
            in_amt  = qs.filter(direction='IN' ).aggregate(s=Sum('pending_amount'))['s'] or Decimal('0')
            out_amt = qs.filter(direction='OUT').aggregate(s=Sum('pending_amount'))['s'] or Decimal('0')
            periods_data.append({
                'label':   label,
                'in_amt':  in_amt,
                'out_amt': out_amt,
                'net':     in_amt - out_amt,
                'docs':    list(qs.order_by('due_date')[:15]),
            })

        ctx.update({
            'today':        today,
            'overdue_in':   overdue_in,
            'overdue_out':  overdue_out,
            'overdue_net':  overdue_in - overdue_out,
            'overdue_docs': list(overdue.order_by('due_date')[:20]),
            'periods_data': periods_data,
        })
        return ctx


# =============================================================================
# BAJA PRIORIDAD — Importación de extracto bancario CSV
# =============================================================================
class BankStatementImportView(CompanyContextMixin, TemplateView):
    template_name = 'FINANTIAL/import_statement.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = BankStatementImportForm(user=self.request.user)
        return ctx

    def post(self, request, *args, **kwargs):
        form = BankStatementImportForm(request.POST, request.FILES, user=request.user)
        ctx  = self.get_context_data(**kwargs)
        ctx['form'] = form

        if not form.is_valid():
            return self.render_to_response(ctx)

        cd        = form.cleaned_data
        account   = cd['account']
        delimiter = cd['delimiter']
        date_fmt  = cd['date_format']
        date_col  = cd['date_col']
        desc_col  = cd['desc_col']
        amt_col   = cd['amount_col']
        deb_col   = cd.get('debit_col')
        cre_col   = cd.get('credit_col')
        skip      = cd['skip_rows']

        default_egreso  = MovementType.objects.filter(flow=MovementType.EGRESO,  active=True).first()
        default_ingreso = MovementType.objects.filter(flow=MovementType.INGRESO, active=True).first()

        content  = cd['csv_file'].read().decode('utf-8-sig')
        reader   = csv.reader(io.StringIO(content), delimiter=delimiter)
        created, errors = [], []

        for i, row in enumerate(reader, 1):
            if i <= skip:
                continue
            try:
                from datetime import datetime as _dt
                tx_date = _dt.strptime(row[date_col].strip(), date_fmt).date()
                desc    = row[desc_col].strip()

                if deb_col is not None and cre_col is not None:
                    deb = Decimal(row[deb_col].strip().replace(',', '') or '0')
                    cre = Decimal(row[cre_col].strip().replace(',', '') or '0')
                    amount     = deb if deb > 0 else cre
                    is_egreso  = deb > 0
                else:
                    raw    = row[amt_col].strip().replace(',', '')
                    amount = abs(Decimal(raw))
                    is_egreso = Decimal(raw) < 0

                mov_type = default_egreso if is_egreso else default_ingreso
                bm = BankMovements(
                    idAccount=account,
                    date=tx_date,
                    description=desc,
                    amount=amount,
                    movementType=mov_type,
                    balance=Decimal('0'),
                    equivalentAmount=Decimal('0'),
                    amountReconcilied=Decimal('0'),
                )
                bm.full_clean()
                bm.save()
                created.append({'date': tx_date, 'desc': desc, 'amount': amount, 'type': 'E' if is_egreso else 'I'})
            except Exception as e:
                errors.append(f'Fila {i}: {e}')

        ctx['created'] = created
        ctx['errors']  = errors
        if created:
            messages.success(request, f'{len(created)} movimientos importados correctamente.')
        if errors:
            messages.warning(request, f'{len(errors)} filas con errores.')
        return self.render_to_response(ctx)


# =============================================================================
# BAJA PRIORIDAD — Exportación PLE SUNAT
# =============================================================================
class PLEExportView(CompanyContextMixin, TemplateView):
    """GET sin parámetros → formulario de selección.
       GET con ?tipo=&anio=&mes= → descarga el archivo TXT."""
    template_name = 'FINANTIAL/ple_export.html'

    def get(self, request, *args, **kwargs):
        tipo = request.GET.get('tipo')
        if tipo in ('14', '8'):
            return self._download(request, tipo)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['years']  = range(date.today().year - 2, date.today().year + 1)
        ctx['months'] = MONTH_CHOICES
        ctx['cur_year']  = date.today().year
        ctx['cur_month'] = date.today().month
        return ctx

    def _download(self, request, tipo):
        try:
            year  = int(request.GET.get('anio',  date.today().year))
            month = int(request.GET.get('mes',   date.today().month))
        except (ValueError, TypeError):
            year, month = date.today().year, date.today().month

        tin = self._get_user_tin()
        qs  = PaymentDocument.objects.filter(declare_year=year, declare_month=month)
        if tin and not self._is_holding():
            qs = qs.filter(Q(tin_issuer=tin) | Q(tin_receiver=tin))

        if tipo == '14':
            qs       = qs.filter(direction='IN')
            filename = f'LE{year}{month:02d}00140100001100CR.txt'
        else:
            qs       = qs.filter(direction='OUT')
            filename = f'LE{year}{month:02d}00080100001100CR.txt'

        output = io.StringIO()
        writer = csv.writer(output, delimiter='|', lineterminator='\r\n')

        for n, doc in enumerate(qs.select_related('tin_issuer', 'client', 'supplier'), 1):
            if tipo == '14':
                ruc   = doc.client.numberIdClient if doc.client else ''
                name  = doc.client.tradeName if doc.client else ''
            else:
                ruc   = doc.supplier.numberIdClient if doc.supplier else ''
                name  = doc.supplier.tradeName if doc.supplier else ''

            writer.writerow([
                f'{year}{month:02d}00',
                str(n).zfill(8),
                doc.issue_date.strftime('%d/%m/%Y') if doc.issue_date else '',
                doc.due_date.strftime('%d/%m/%Y')   if doc.due_date   else '',
                doc.doc_type,
                '',                          # Serie
                doc.doc_number or '',
                '6',                         # Tipo doc identidad (RUC=6)
                ruc,
                name,
                f'{doc.gross_amount:.2f}',
                f'{doc.tax_amount:.2f}',
                '0.00',                      # ISC
                '0.00',                      # ICBPER
                '0.00',                      # Otros tributos
                f'{doc.net_amount:.2f}',
                doc.currency,
                f'{doc.exchange_rate:.3f}',
                '',                          # Ref. doc modificado
                '',
                '1',                         # Estado (1=anotado)
            ])

        response = HttpResponse(output.getvalue(), content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


# =============================================================================
# BAJA PRIORIDAD — Estado de resultados (P&L)
# =============================================================================
class ProfitLossView(CompanyContextMixin, TemplateView):
    template_name = 'FINANTIAL/profit_loss.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            year  = int(self.request.GET.get('anio',  date.today().year))
            month = int(self.request.GET.get('mes',   0))
        except (ValueError, TypeError):
            year, month = date.today().year, 0

        tin = self._get_user_tin()
        je_qs = JournalEntry.objects.filter(period_year=year, is_posted=True)
        if month:
            je_qs = je_qs.filter(period_month=month)
        if tin and not self._is_holding():
            je_qs = je_qs.filter(tin=tin)

        lines = JournalEntryLine.objects.filter(entry__in=je_qs).select_related('account')

        income_lines  = lines.filter(account__account_type='INCOME')
        expense_lines = lines.filter(account__account_type='EXPENSE')

        total_income  = (income_lines.aggregate( s=Sum('credit'))['s'] or Decimal('0')) - \
                        (income_lines.aggregate( s=Sum('debit')) ['s'] or Decimal('0'))
        total_expense = (expense_lines.aggregate(s=Sum('debit')) ['s'] or Decimal('0')) - \
                        (expense_lines.aggregate(s=Sum('credit'))['s'] or Decimal('0'))
        net_profit    = total_income - total_expense

        income_by_account  = income_lines.values(
            'account__code', 'account__name'
        ).annotate(total=Sum('credit') - Sum('debit')).order_by('account__code')

        expense_by_account = expense_lines.values(
            'account__code', 'account__name'
        ).annotate(total=Sum('debit') - Sum('credit')).order_by('account__code')

        ctx.update({
            'year':               year,
            'month':              month,
            'months':             MONTH_CHOICES,
            'years':              range(date.today().year - 3, date.today().year + 1),
            'total_income':       total_income,
            'total_expense':      total_expense,
            'net_profit':         net_profit,
            'income_by_account':  income_by_account,
            'expense_by_account': expense_by_account,
        })
        return ctx