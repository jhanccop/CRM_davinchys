from django.db import models
from datetime import date, timedelta, datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import TruncDate,LastValue,Abs, TruncMonth

from django.db.models import Sum, Max, CharField,F, Q, Count, When, Value, Case, When, FloatField
from django.db.models import OuterRef, Subquery, Prefetch

class IncomesManager(models.Manager):
    def ListaDocumentosPorTipo(self,intervalo,tipo,compania_id):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        if tipo == 5:
            result = self.filter(
                date__range = rangeDate,
                idTin__id = compania_id
            ).annotate(
                per=Case(
                    When(amount=0, then=Value(0)),  # Si amount es 0, devuelve 0
                    default=(F("amountReconcilied") * 100) / F("amount"),
                    output_field=FloatField()
                ),
                #per = (F("amountReconcilied")/F("amount")) * 100,
            ).order_by("date")
        else:
            result = self.filter(
                date__range = rangeDate,
                idTin__id = compania_id,
                typeInvoice = str(tipo)
            ).annotate(
                per=Case(
                    When(amount=0, then=Value(0)),  # Si amount es 0, devuelve 0
                    default=(F("amountReconcilied") * 100) / F("amount"),
                    output_field=FloatField()
                ),
                #per = (F("amountReconcilied")/F("amount")) * 100,
            ).order_by("date")

        return result

    def ListaConciliacionPorCuenta(self,movimientos):
        ids = self.filter(
            idBankMovements__id__in = movimientos
        )
        result = ids.values('idBankMovements__id').annotate(
            accumulate = Sum("amountReconcilied"),
            per = Abs(Sum("amountReconcilied")*100/F('idBankMovements__amount')),
            amount = ArrayAgg('amountReconcilied'),
            tin = ArrayAgg('idClient__tradeName'),
            doc =  ArrayAgg('description'),
            pdf =  ArrayAgg('pdf_file'),
        )
        return result
    
    def ListaConciliacionPorIdMovimiento(self,movimiento):
        result = self.filter(
            idBankMovements__id = movimiento
        ).order_by("date")
        return result
    
    def ListaConciliacionSumaPorIdMovimiento(self,movimiento):
        result = self.filter(
            idBankMovements__id = movimiento
        ).values(
           "amountReconcilied"
        ).aggregate(tot = Sum("amountReconcilied"))
        return result
    
    def SumaConciliadaPorIdDocumento(self,id):
        result = self.filter(
            id = id 
            ).aggregate(suma = Sum("amountReconcilied"))
        return result
    
    def DocumentosPorId(self,id):
       return self.filter(id = id).annotate(per = F("amountReconcilied") * 100 / F("amount"),diff =  F("amount") - F("amountReconcilied"))[0]

    def DocumentosPorRUC(self,ruc):
       return self.filter(idClient__ruc = ruc).order_by("created")
    
class quotesManager(models.Manager):
    def ListaPOs(self,intervalo):
        """
            Lista de PO
        """

        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        from applications.COMERCIAL.sales.models import QuoteTracking
        last_tracking_subquery = QuoteTracking.objects.filter(
            idquote=OuterRef('pk')
        ).order_by('-created').values('status', 'area')[:1]

        STATE_CHOICES = QuoteTracking.STATE_CHOICES

        result = self.filter(
            created__range=rangeDate,
            isPO = True
        ).annotate(
            lastStatus=Subquery(last_tracking_subquery.values('status')),
            lastArea=Subquery(last_tracking_subquery.values('area')),
            lastStatusDisplay=Case(
                *[When(lastStatus=status, then=Value(display)) 
                for status, display in STATE_CHOICES],
                default=Value(''),
                output_field=CharField()
            )
        ).order_by('-created')

        return result

    def ListaCotizacionesPorRuc(self, intervalo, company):
        from .models import Items, QuoteTracking
        Intervals = intervalo.split(' to ')
        intervals = [datetime.strptime(dt, "%Y-%m-%d") for dt in Intervals]

        # Creación de rango de fechas
        rangeDate = [intervals[0] - timedelta(days=1), None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days=1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days=1)

        # Subconsulta para obtener el último QuoteTraking de cada cotización
        last_tracking_subquery = QuoteTracking.objects.filter(
            idquote=OuterRef('pk')
        ).order_by('-created')

        # CORRECCIÓN: Usar el related_name correcto
        #items_prefetch = Prefetch(
        #    'item_Quote',  # ← Este es el related_name correcto
        #    queryset=Items.objects.select_related('idTrafo'),  # Optimizar con select_related
        #    to_attr='items'
        #)

        # Consulta principal con annotate para el último tracking y prefetch para los items
        result = self.filter(
            created__range=rangeDate,
            idTinReceiving__id=company
        ).order_by("-id").annotate(
            ultimo_evento=Subquery(last_tracking_subquery.values('status')[:1]),
            ultimo_evento_fecha=Subquery(last_tracking_subquery.values('created')[:1]),
            ultimo_evento_display=Case(
                *[When(quotetracking__status=value, then=Value(display)) 
                for value, display in QuoteTracking.STATE_CHOICES],
                default=Value('Desconocido'),
                output_field=CharField()
            ),
            ultimo_area_display=Case(
                *[When(quotetracking__area=value, then=Value(display)) 
                for value, display in QuoteTracking.AREAS_TRACKING_CHOICES],
                default=Value('Desconocido'),
                output_field=CharField()
            )
        )#.prefetch_related(items_prefetch).distinct()  # Agregar distinct para evitar duplicados

        return result
    
    def ListaPOPorRuc(self, intervalo, company, isPO):
        from .models import Items, QuoteTracking
        Intervals = intervalo.split(' to ')
        intervals = [datetime.strptime(dt, "%Y-%m-%d") for dt in Intervals]

        # Creación de rango de fechas
        rangeDate = [intervals[0] - timedelta(days=1), None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days=1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days=1)

        # Subconsulta para obtener el último QuoteTraking de cada cotización
        last_tracking_subquery = QuoteTracking.objects.filter(
            idquote = OuterRef('pk')
        ).order_by('-created')

        # Prefetch para optimizar la carga de los productos Trafos
        items_prefetch = Prefetch(
            'item_Quote',  # ← Este es el related_name correcto
            queryset=Items.objects.select_related('idTrafo'),  # Optimizar con select_related
            to_attr='items'
        )

        # Consulta principal con annotate para el último tracking y prefetch para los trafos
        result = self.filter(
            created__range = rangeDate,
            idTinReceiving__id = company,
            isPO = isPO
        ).order_by("-id").annotate(
            ultimo_evento = Subquery(last_tracking_subquery.values('status')[:1]),
            ultimo_evento_fecha=Subquery(last_tracking_subquery.values('created')[:1]),
            ultimo_evento_display=Case(
                *[When(quotetracking__status=value, then=Value(display)) 
                for value, display in QuoteTracking.STATE_CHOICES],
                default=Value('Desconocido'),
                output_field=CharField()
            ),
            ultimo_area_display=Case(
                *[When(quotetracking__area=value, then=Value(display)) 
                for value, display in QuoteTracking.AREAS_TRACKING_CHOICES],
                default=Value('Desconocido'),
                output_field=CharField()
            )
        ).prefetch_related(items_prefetch)

        return result
    

class QuoteTrackingManager(models.Manager):
    def UltimoEstadoTracking(self,idQuote):
        result = self.filter(
            idquote__id = idQuote
        ).last()
        return result

#class TrafoManager(models.Manager):