from datetime import date, timedelta, datetime
from django.db.models import OuterRef, Subquery, Prefetch

from django.db import models


class TrafoQuoteManager(models.Manager):
    def ListaCotizacionesPorRuc(self, intervalo, company):
        from .models import QuoteTraking, Trafos
        Intervals = intervalo.split(' to ')
        intervals = [datetime.strptime(dt, "%Y-%m-%d") for dt in Intervals]

        # Creación de rango de fechas
        rangeDate = [intervals[0] - timedelta(days=1), None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days=1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days=1)

        # Subconsulta para obtener el último QuoteTraking de cada cotización
        last_tracking_subquery = QuoteTraking.objects.filter(
            idTrafoQuote=OuterRef('pk')
        ).order_by('-created')

        # Prefetch para optimizar la carga de los productos Trafos
        trafos_prefetch = Prefetch(
            'trafo_Quote',
            queryset=Trafos.objects.all(),
            to_attr='productos'
        )

        # Consulta principal con annotate para el último tracking y prefetch para los trafos
        result = self.filter(
            dateOrder__range=rangeDate,
            idTin__id=company
        ).order_by("-id").annotate(
            ultimo_evento=Subquery(last_tracking_subquery.values('event')[:1]),
            ultimo_evento_fecha=Subquery(last_tracking_subquery.values('created')[:1]),
            ultimo_evento_display=Subquery(last_tracking_subquery.values('event')[:1])
        ).prefetch_related(trafos_prefetch)

        return result
    
class TrafoQuoteManager0(models.Manager):
    def ListaCotizacionesPorRuc(self,intervalo,company):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = self.filter(
            dateOrder__range = rangeDate,
            idTin__id = company
        ).order_by("-id")
        return result
