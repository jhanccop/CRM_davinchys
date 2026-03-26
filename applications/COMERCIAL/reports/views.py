from datetime import date, timedelta
from datetime import datetime

from django.db.models import Sum

from applications.users.mixins import (
    ComercialMixin,
    AdminClientsPermisoMixin,
)

from django.views.generic import ListView

from applications.COMERCIAL.purchase.models import requirements
from applications.COMERCIAL.sales.models import (
    quotes,
    IntQuotes,
    WorkOrder,
    Items,
)


# ==================== DASHBOARD COMERCIAL ====================
class DashboardView(ComercialMixin, ListView):
    template_name = "COMERCIAL/dashboard/dashboard-comercial.html"
    context_object_name = 'documentos'

    @staticmethod
    def _parse_range(intervalo):
        parts = intervalo.split(' to ')
        dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in parts]
        start = dates[0] - timedelta(days=1)
        end   = dates[-1] + timedelta(days=1)
        return start, end

    def get_queryset(self, **kwargs):
        intervalDate = self.request.GET.get("dateKword", '')
        if not intervalDate or intervalDate == "today":
            intervalDate = (
                str(date.today() - timedelta(days=120)) + " to " + str(date.today())
            )

        date_range = self._parse_range(intervalDate)

        # ── Tablas principales (con anotaciones de tracking) ──
        requerimientos = requirements.objects.ListaOrdenesdeCompra(intervalo=intervalDate)
        pedidos        = quotes.objects.ListaPOs(intervalo=intervalDate)

        # ── KPIs desde las tablas ya filtradas ───────────────
        req_list       = list(requerimientos)
        req_total      = len(req_list)
        req_completados = sum(1 for r in req_list if r.lastStatus == '12')
        req_pendientes  = req_total - req_completados

        po_list         = list(pedidos)
        pos_total       = len(po_list)
        pos_completadas = sum(1 for p in po_list if p.lastStatus == '12')
        pos_activas     = pos_total - pos_completadas

        # ── KPIs simples (conteos directos) ──────────────────
        qs_all = quotes.objects.filter(created__range=date_range)
        total_quotes = qs_all.filter(isPO=False).count()

        # Monto acumulado de POs en el período
        pos_pen = (
            qs_all.filter(isPO=True, currency='0')
            .aggregate(t=Sum('amount'))['t'] or 0
        )
        pos_usd = (
            qs_all.filter(isPO=True, currency='1')
            .aggregate(t=Sum('amount'))['t'] or 0
        )

        total_intquotes = IntQuotes.objects.filter(created__range=date_range).count()
        total_wo        = WorkOrder.objects.filter(created__range=date_range).count()

        # Items con algún evento de seguimiento en el período
        items_en_proceso = Items.objects.filter(
            itemTracking__statusItem__in=['1', '2', '3']
        ).distinct().count()
        items_entregados = Items.objects.filter(
            itemTracking__statusItem='4'
        ).distinct().count()

        return {
            "intervalDate":     intervalDate,
            "requerimientos":   requerimientos,
            "pedidos":          pedidos,
            # KPIs
            "total_quotes":     total_quotes,
            "pos_total":        pos_total,
            "pos_activas":      pos_activas,
            "pos_completadas":  pos_completadas,
            "pos_pen":          pos_pen,
            "pos_usd":          pos_usd,
            "total_intquotes":  total_intquotes,
            "total_wo":         total_wo,
            "items_en_proceso": items_en_proceso,
            "items_entregados": items_entregados,
            "req_total":        req_total,
            "req_pendientes":   req_pendientes,
            "req_completados":  req_completados,
        }
