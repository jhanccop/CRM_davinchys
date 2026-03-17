from django.utils import timezone

"""
FINANTIAL/views.py
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q, F
from django.http import JsonResponse
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
)
from .models import (
    PaymentDocument, PaymentAllocation,
    PaymentTransaction, PaymentTransactionLine,
    BankMovements,
)

from applications.cuentas.models import Tin, Account


# =============================================================================
# MIXIN BASE
# =============================================================================
class CompanyContextMixin(LoginRequiredMixin):
    """
    Inyecta en cada vista:
      user_tin   → Tin del usuario (None si superuser sin empleado)
      is_holding → True si holding o superuser

    Segmentación:
      holding    → ve toda la corporación
      subsidiaria → ve solo su Tin
    """

    def _get_user_tin(self):
        user = self.request.user
        if hasattr(user, 'empleado') and hasattr(user.empleado, 'company'):
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
            'tin_issuer', 'tin_receiver', 'client', 'supplier', 'created_by'
        )
        if self._is_holding():
            return qs.all()
        tin = self._get_user_tin()
        return qs.filter(Q(tin_issuer=tin) | Q(tin_receiver=tin)) if tin else qs.none()

    def get_tx_queryset(self):
        qs = PaymentTransaction.objects.select_related(
            'tin_payer', 'tin_receiver', 'client', 'supplier',
            'bank_account__idTin', 'bank_movement', 'created_by'
        )
        if self._is_holding():
            return qs.all()
        tin = self._get_user_tin()
        return qs.filter(Q(tin_payer=tin) | Q(tin_receiver=tin)) if tin else qs.none()

    def get_mov_queryset(self):
        qs = BankMovements.objects.select_related(
            'idAccount__idTin', 'tin', 'movementType',
            'originDestination', 'payment_transaction'
        )
        if self._is_holding():
            return qs.all()
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

        # KPIs comprobantes
        ctx['total_docs']   = doc_qs.count()
        ctx['pending_docs'] = doc_qs.filter(status='PENDING').count()
        ctx['partial_docs'] = doc_qs.filter(status='PARTIAL').count()
        ctx['paid_docs']    = doc_qs.filter(status='PAID').count()

        agg = doc_qs.aggregate(
            total_gross=Sum('gross_amount'),
            total_net=Sum('net_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount'),
        )
        ctx.update({k: v or 0 for k, v in agg.items()})

        # Documentos por dirección
        for d in ('IN', 'OUT', 'INT'):
            ctx[f'docs_{d.lower()}'] = doc_qs.filter(direction=d).aggregate(
                cnt=Count('id'), total=Sum('net_amount'))

        # Últimos pendientes y transacciones
        ctx['recent_pending']      = doc_qs.filter(status__in=['PENDING','PARTIAL']).order_by('-created')[:10]
        ctx['recent_transactions'] = tx_qs.order_by('-transaction_date')[:5]

        # Movimientos bancarios sin conciliar
        ctx['pending_movements'] = mov_qs.filter(conciliated=False).order_by('-date')[:8]

        # Breakdown por empresa (solo holding)
        if ctx['is_holding']:
            ctx['by_tin'] = (
                doc_qs
                .values('tin_issuer__tinName')
                .annotate(cnt=Count('id'), total_net=Sum('net_amount'), total_paid=Sum('paid_amount'))
                .order_by('-total_net')[:8]
            )

        # Cuentas bancarias
        ctx['accounts']    = self._get_user_accounts()
        ctx['filter_form'] = DashboardFilterForm(self.request.GET or None)
        return ctx

# =============================================================================
# PAYMENT DOCUMENT — CRUD
# =============================================================================
class PaymentDocumentListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/document_list.html'
    context_object_name = 'documents'
    paginate_by         = 25

    def get_queryset(self):
        qs = self.get_doc_queryset()
        f  = DashboardFilterForm(self.request.GET or None)
        if f.is_valid():
            cd = f.cleaned_data
            if cd.get('tin'):
                qs = qs.filter(Q(tin_issuer=cd['tin']) | Q(tin_receiver=cd['tin']))
            if cd.get('direction'):
                qs = qs.filter(direction=cd['direction'])
            if cd.get('status'):
                qs = qs.filter(status=cd['status'])
            if cd.get('currency'):
                qs = qs.filter(currency=cd['currency'])
            if cd.get('date_from'):
                qs = qs.filter(issue_date__gte=cd['date_from'])
            if cd.get('date_to'):
                qs = qs.filter(issue_date__lte=cd['date_to'])
            if cd.get('search'):
                q = cd['search']
                qs = qs.filter(
                    Q(doc_number__icontains=q) |
                    Q(short_description__icontains=q) |
                    Q(description__icontains=q)
                )
        return qs.order_by('-issue_date', '-created')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filter_form'] = DashboardFilterForm(self.request.GET or None)
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
            'transaction__bank_account__idTin', 'transaction__bank_movement'
        ).all()
        return ctx

class PaymentDocumentCreateView(CompanyContextMixin, CreateView):
    template_name = 'FINANTIAL/document_form.html'
    form_class    = PaymentDocumentForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['allocation_formset'] = (
            PaymentAllocationFormSet(self.request.POST)
            if self.request.POST else PaymentAllocationFormSet()
        )
        ctx['title']  = 'Registrar Comprobante'
        ctx['action'] = 'create'
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        fs  = ctx['allocation_formset']
        if fs.is_valid():
            doc = form.save(commit=False)
            doc.created_by = self.request.user
            doc.save()
            fs.instance = doc
            fs.save()
            messages.success(self.request, f'Comprobante {doc} registrado.')
            return redirect(reverse('finantial:document-detail', kwargs={'pk': doc.pk}))
        messages.error(self.request, 'Revise los ítems del formulario.')
        return self.render_to_response(ctx)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrija los errores.')
        return super().form_invalid(form)

class PaymentDocumentUpdateView(CompanyContextMixin, UpdateView):
    template_name = 'FINANTIAL/document_form.html'
    form_class    = PaymentDocumentForm

    def get_object(self):
        return get_object_or_404(self.get_doc_queryset(), pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['allocation_formset'] = (
            PaymentAllocationFormSet(self.request.POST, instance=self.object)
            if self.request.POST else PaymentAllocationFormSet(instance=self.object)
        )
        ctx['title']  = f'Editar — {self.object}'
        ctx['action'] = 'update'
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        fs  = ctx['allocation_formset']
        if fs.is_valid():
            doc = form.save()
            fs.instance = doc
            fs.save()
            messages.success(self.request, 'Comprobante actualizado.')
            return redirect(reverse('finantial:document-detail', kwargs={'pk': doc.pk}))
        messages.error(self.request, 'Revise los ítems del formulario.')
        return self.render_to_response(ctx)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrija los errores.')
        return super().form_invalid(form)

class PaymentDocumentDeleteView(CompanyContextMixin, DeleteView):
    template_name       = 'FINANTIAL/document_confirm_delete.html'
    success_url         = reverse_lazy('finantial:document-list')
    context_object_name = 'document'

    def get_object(self):
        return get_object_or_404(self.get_doc_queryset(), pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.warning(self.request, f'Comprobante eliminado.')
        return super().form_valid(form)

# =============================================================================
# PAYMENT TRANSACTION — CRUD
# =============================================================================
class PaymentTransactionListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by         = 25

    def get_queryset(self):
        qs     = self.get_tx_queryset().order_by('-transaction_date', '-created')
        q      = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(Q(reference__icontains=q) | Q(notes__icontains=q))
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q']      = self.request.GET.get('q', '')
        ctx['status'] = self.request.GET.get('status', '')
        return ctx

class PaymentTransactionDetailView(CompanyContextMixin, DetailView):
    template_name       = 'FINANTIAL/transaction_detail.html'
    context_object_name = 'transaction'

    def get_object(self):
        return get_object_or_404(self.get_tx_queryset(), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['lines'] = self.object.transaction_lines.select_related('document').all()
        return ctx

class PaymentTransactionCreateView(CompanyContextMixin, CreateView):
    template_name = 'FINANTIAL/transaction_form.html'
    form_class    = PaymentTransactionForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx    = super().get_context_data(**kwargs)
        doc_qs = self.get_doc_queryset().filter(status__in=['PENDING', 'PARTIAL'])
        ctx['line_formset'] = (
            PaymentTransactionLineFormSet(self.request.POST)
            if self.request.POST else PaymentTransactionLineFormSet()
        )
        for f in ctx['line_formset'].forms:
            f.fields['document'].queryset = doc_qs
        ctx['title']        = 'Registrar Pago'
        ctx['action']       = 'create'
        ctx['pending_docs'] = doc_qs.order_by('-issue_date')[:50]
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        fs  = ctx['line_formset']
        if fs.is_valid():
            tx = form.save(commit=False)
            tx.created_by = self.request.user
            tx.save()
            fs.instance = tx
            fs.save()
            messages.success(self.request, f'TX-{tx.id} guardada como borrador. Confirme para aplicar los pagos.')
            return redirect(reverse('finantial:transaction-detail', kwargs={'pk': tx.pk}))
        messages.error(self.request, 'Revise las líneas del formulario.')
        return self.render_to_response(ctx)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrija los errores.')
        return super().form_invalid(form)

class PaymentTransactionUpdateView(CompanyContextMixin, UpdateView):
    template_name = 'FINANTIAL/transaction_form.html'
    form_class    = PaymentTransactionForm

    def get_object(self):
        return get_object_or_404(self.get_tx_queryset(), pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx    = super().get_context_data(**kwargs)
        doc_qs = self.get_doc_queryset().filter(status__in=['PENDING', 'PARTIAL'])
        ctx['line_formset'] = (
            PaymentTransactionLineFormSet(self.request.POST, instance=self.object)
            if self.request.POST else PaymentTransactionLineFormSet(instance=self.object)
        )
        for f in ctx['line_formset'].forms:
            f.fields['document'].queryset = doc_qs
        ctx['title']  = f'Editar TX-{self.object.id}'
        ctx['action'] = 'update'
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        fs  = ctx['line_formset']
        if fs.is_valid():
            tx = form.save()
            fs.instance = tx
            fs.save()
            messages.success(self.request, 'Transacción actualizada.')
            return redirect(reverse('finantial:transaction-detail', kwargs={'pk': tx.pk}))
        messages.error(self.request, 'Revise las líneas del formulario.')
        return self.render_to_response(ctx)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrija los errores.')
        return super().form_invalid(form)

class PaymentTransactionDeleteView(CompanyContextMixin, DeleteView):
    template_name       = 'FINANTIAL/transaction_confirm_delete.html'
    success_url         = reverse_lazy('finantial:transaction-list')
    context_object_name = 'transaction'

    def get_object(self):
        return get_object_or_404(self.get_tx_queryset(), pk=self.kwargs['pk'])

class ConfirmTransactionView(CompanyContextMixin, View):
    def post(self, request, pk):
        tx = get_object_or_404(self.get_tx_queryset(), pk=pk)
        if tx.status == 'DRAFT':
            tx.confirm()
            messages.success(request, f'TX-{tx.id} confirmada. Comprobantes actualizados.')
        else:
            messages.warning(request, f'TX-{tx.id} ya fue procesada ({tx.get_status_display()}).')
        return redirect(reverse('finantial:transaction-detail', kwargs={'pk': pk}))

# =============================================================================
# BANK MOVEMENTS — CRUD
# =============================================================================
class BankMovementsListView(CompanyContextMixin, ListView):
    template_name       = 'FINANTIAL/movement_list.html'
    context_object_name = 'movements'
    paginate_by         = 30

    def get_queryset(self):
        qs = self.get_mov_queryset().order_by('-date', '-created')
        q  = self.request.GET.get('q')
        account_id   = self.request.GET.get('account')
        conciliated  = self.request.GET.get('conciliated')
        flow         = self.request.GET.get('flow')
        if q:
            qs = qs.filter(
                Q(description__icontains=q) | Q(opNumber__icontains=q)
            )
        if account_id:
            qs = qs.filter(idAccount_id=account_id)
        if conciliated in ('0', '1'):
            qs = qs.filter(conciliated=conciliated == '1')
        if flow in ('0', '1'):
            qs = qs.filter(movementType__flow=flow)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accounts'] = self._get_user_accounts()
        ctx['q']          = self.request.GET.get('q', '')
        ctx['sel_account']   = self.request.GET.get('account', '')
        ctx['sel_conciliated'] = self.request.GET.get('conciliated', '')
        ctx['sel_flow']      = self.request.GET.get('flow', '')
        return ctx

class BankMovementsDetailView(CompanyContextMixin, DetailView):
    template_name       = 'FINANTIAL/movement_detail.html'
    context_object_name = 'movement'

    def get_object(self):
        return get_object_or_404(self.get_mov_queryset(), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['conciliations'] = self.object.mov_origen.select_related(
            'idDoc', 'idMovArrival__idAccount'
        ).all()
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
        mov = form.save()
        messages.success(self.request, f'Movimiento MOV-{mov.id} registrado.')
        return redirect(reverse('finantial:movement-detail', kwargs={'pk': mov.pk}))

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
        mov = form.save()
        messages.success(self.request, 'Movimiento actualizado.')
        return redirect(reverse('finantial:movement-detail', kwargs={'pk': mov.pk}))

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
            'idTrafo', 'idTrafoQuote', 'idTrafoIntQuote', 'idWorkOrder'
        ).prefetch_related('payment_allocations__document')

        if not ctx['is_holding']:
            tin = ctx['user_tin']
            if tin:
                items_qs = items_qs.filter(
                    Q(idTrafoQuote__idTinReceiving=tin) |
                    Q(idTrafoIntQuote__idTinReceiving=tin) |
                    Q(idWorkOrder__idTinReceiving=tin)
                )

        if quote_id:
            items_qs = items_qs.filter(idTrafoQuote_id=quote_id)
        if int_quote_id:
            items_qs = items_qs.filter(idTrafoIntQuote_id=int_quote_id)
        if wo_id:
            items_qs = items_qs.filter(idWorkOrder_id=wo_id)

        enriched = []
        for item in items_qs:
            allocs         = list(item.payment_allocations.all())
            confirmed_paid = sum(a.allocated_amount for a in allocs if a.document.status == 'PAID') or 0
            partial_paid   = sum(a.allocated_amount for a in allocs if a.document.status == 'PARTIAL') or 0
            unit_cost      = item.unitCost or item.unitCostInt or item.unitCostWO or 0
            coverage       = float(confirmed_paid / unit_cost * 100) if unit_cost else 0

            if item.idTrafoQuote_id:
                order_type, order_obj = 'QUO', item.idTrafoQuote
            elif item.idTrafoIntQuote_id:
                order_type, order_obj = 'INT', item.idTrafoIntQuote
            elif item.idWorkOrder_id:
                order_type, order_obj = 'WO', item.idWorkOrder
            else:
                order_type, order_obj = None, None

            enriched.append({
                'item':           item,
                'order_type':     order_type,
                'order_obj':      order_obj,
                'unit_cost':      unit_cost,
                'confirmed_paid': confirmed_paid,
                'partial_paid':   partial_paid,
                'coverage_pct':   round(coverage, 1),
                'pending':        max(float(unit_cost) - float(confirmed_paid), 0),
                'allocations':    allocs,
            })

        ctx['enriched_items']     = enriched
        ctx['summary_total_cost'] = sum(e['unit_cost'] for e in enriched)
        ctx['summary_paid_full']  = sum(1 for e in enriched if e['coverage_pct'] >= 100)
        ctx['summary_no_docs']    = sum(1 for e in enriched if not e['allocations'])
        ctx['quotes']             = quotes.objects.all().order_by('-created')[:50]
        ctx['int_quotes']         = IntQuotes.objects.all().order_by('-created')[:50]
        ctx['work_orders']        = WorkOrder.objects.all().order_by('-created')[:50]
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
        item      = get_object_or_404(Items, pk=pk)
        unit_cost = float(item.unitCost or item.unitCostInt or item.unitCostWO or 0)
        allocated = float(
            item.payment_allocations.filter(
                document__status__in=['PAID', 'PARTIAL']
            ).aggregate(s=Sum('allocated_amount'))['s'] or 0
        )
        return JsonResponse({
            'unit_cost': unit_cost,
            'allocated': allocated,
            'pending':   max(unit_cost - allocated, 0),
        })