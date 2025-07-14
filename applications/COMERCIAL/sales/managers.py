from django.db import models
from datetime import date, timedelta, datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import TruncDate,LastValue,Abs, TruncMonth

from django.db.models import Sum, Max, DateField,F, Q, Count, When, Value, Case, When, FloatField


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
    