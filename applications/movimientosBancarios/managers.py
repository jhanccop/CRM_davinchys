from datetime import date, timedelta, datetime
from django.db.models import Sum,F, Q, Count, When, Case, When, FloatField, DecimalField, ExpressionWrapper, IntegerField
from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models.functions import TruncDate,LastValue,Abs, TruncMonth, Now, ExtractDay
from applications.cuentas.models import Account


from collections import defaultdict

from decimal import Decimal

today = date.today()

class DocumentsUploadedManager(models.Manager):
    def MontosHistorico(self,intervalo,cuenta):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = self.filter(
            created__range = rangeDate,
            idAccount__id = cuenta
        ).order_by("created")

        return result

    def idLastDocument(self):
       return self.all().order_by('-modified').last()
    
    def ListaNArchivos(self,N):
       payload = self.all().order_by('-created')[:5]
       return payload
 
class BankMovementsManager(models.Manager):
    def BusquedaRegistros(self,idAccount,balance,opNumber):
       result = self.filter(idAccount=idAccount).filter(balance=balance).filter(opNumber=opNumber)
       return result.exists()
    
    def ListaMovimientosPorDocumentos(self,docs):
       result = self.filter(idDocs__in = docs)
       return result

    def MovimientosPorId(self,id):
       return self.filter(id = id).annotate(per = F("amountReconcilied") * 100 / F("amount"),diff =  F("amount") - F("amountReconcilied"))[0]
    
    def SumaDocsPorId(self,id):
        #from .models import Conciliation

        #result = Conciliation.objects.SumaMontosPorIdMov(idMovOrigin = id)
        #result = self.filter(id = id).annotate(sum = Sum("idDocs__amountReconcilied"))
        return 0

    def SumaMovsPorId(self,id):
       result = self.filter(id = id).aggregate(sum = Sum("idMovement__amountReconcilied"))
       return result

    def ListaMovimientosPorCuenta(self,intervalo,cuenta):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)
        result = self.filter(
            date__range = rangeDate,
            idAccount__id = cuenta
        ).annotate(
            #per = (F("amountReconcilied")/F("amount")) * 100,
            per = Case(
                When(amount = 0, then = 0.0),
                default=(F("amountReconcilied")/F("amount")) * 100,
                output_field=FloatField()
            ),
            days_since_date=ExtractDay(Now() - F('date'))
            
        ).order_by("-id")
        return result

    def ResumenMovimientosPorCuenta(self,intervalo,cuenta):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)
            
        result = self.filter(
            date__range = rangeDate,
            idAccount__id = cuenta,
        ).aggregate(
            egresos = Sum("amount", filter=Q(transactionType = "0")),
            ingresos = Sum("amount", filter=Q(transactionType = "1")),
            balance = F("ingresos") - F("egresos")
        )
        return result
    
    def EgresosMovimientosPorCuenta(self,intervalo,cuenta):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)
        result = self.filter(
            date__range = rangeDate,
            idAccount__id = cuenta,
            transactionType = "0"
        ).aggregate(
            total = Sum("amount")
        )
        return result
    
    def ObtenerSaldo(self,cuenta):
       result = self.filter(idAccount__id=cuenta).values("balance").last()
       return result
    
    def ListaMovimientosPorTipo(self,documentation):
        ids = self.filter(
            #idBankMovements__id__in = movimientos
        )
        result = ids.values('idBankMovements__id').annotate(
            accumulate = Sum("amountReconcilied"),
            per = Case(
                When(idBankMovements__amount = 0, then = 0),
                default=Abs(Sum("amountReconcilied")*100/F('idBankMovements__amount'))
            ),
            tin =  ArrayAgg('idClient__ruc'),
            doc =  ArrayAgg('description'),
            amount = ArrayAgg('amountReconcilied'),
        )
        return result
    
    def ConciliacionPorMontosPorCuentaPorIntervalo(self,intervalo,cuenta):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)
            
        result = self.filter(
            date__range = rangeDate,
            idAccount__id = cuenta
        ).aggregate(
            sumAmount = Sum("amount"),
            sumConciliation = Sum("amountReconcilied"),
            sumPending = F("sumAmount") - F("sumConciliation"),

            countAmount = Count("amount"),
            countConciliation = Count("amountReconcilied",filter=Q(amountReconcilied__gt = 0)),
            countPending = F("countAmount") - F("countConciliation"),
        )
        return result
    
    def FlujoDeCajaPorCuenta(self,intervalo,cuenta, idi, ide):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)
            
        result = self.filter(
                date__range = rangeDate,
                idAccount__id = cuenta
            ).annotate(
                month=TruncMonth('created')
            ).values(
                'month','incomeSubCategory','expenseSubCategory'
            ).annotate(
                #labels = F("incomeSubCategory"),
                #total_income= Sum('amount',filter=Q(incomeSubCategory__in = ids)),
                total_income = Sum('amount',filter=Q(incomeSubCategory__in = idi)),
                total_expense = Sum('amount',filter=Q(expenseSubCategory__in = ide)),
            ).order_by('-month','incomeSubCategory')
        return result

    def GetMonths(self,intervalo,cuenta):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)
            
        result = self.filter(
                date__range = rangeDate,
                idAccount__id = cuenta
            ).annotate(
                month=TruncMonth('created')
            ).values(
                'month'
            ).distinct('month').order_by('month')
        return result

    def GetExpenses(self,intervalo,cuenta, ide):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)
            
        results = self.filter(
                date__range = rangeDate,
                idAccount__id = cuenta
            ).annotate(
                month =TruncMonth('created'),
                name = F("expenseSubCategory__nameSubCategoy")
            ).values(
                'month','expenseSubCategory__nameSubCategoy'
            ).annotate(
                expense = Sum('amount',filter=Q(expenseSubCategory__in = ide)),
            ).order_by('month','expenseSubCategory')
        resultado = defaultdict(dict)

        for result in results:
            #if result['income'] == None:
            #    continue
            month = result['month'].strftime('%Y-%m')
            name = result['expenseSubCategory__nameSubCategoy']
            expense = result['expense']
            resultado[month][name] = expense

        print(resultado)
        
        return dict(resultado)

    def GetIncomes(self,intervalo,cuenta, idi):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)
            
        results = self.filter(
                date__range = rangeDate,
                idAccount__id = cuenta
            ).annotate(
                month =TruncMonth('created'),
                name = F("incomeSubCategory__nameSubCategoy")
            ).values(
                'month','incomeSubCategory__nameSubCategoy'
            ).annotate(
                income = Sum('amount',filter=Q(incomeSubCategory__in = idi)),
            ).order_by('month','incomeSubCategory')
        resultado = defaultdict(dict)

        for result in results:
            #if result['income'] == None:
            #    continue
            month = result['month'].strftime('%Y-%m')
            name = result['incomeSubCategory__nameSubCategoy']
            income = result['income']
            resultado[month][name] = income

        print(resultado)
        
        return dict(resultado)
    
    # ================================== WEEKLY REPORT ===================================
    def ListaMovimientosPorCuentaPorRangoPorTipo(self,id,sDate,eDate,type):
        result = self.filter(
            idAccount__id = id,
            date__range=[sDate, eDate],
            transactionType = type
        )
        return result
    
class ConciliationManager(models.Manager):
    def SumaMontosPorIdMov(self,idMovOrigin):
        result = self.filter(
            idMovOrigin = idMovOrigin
        ).aggregate(
           sum =Sum("amountReconcilied")
        )
        return result
       
    def SumaMontosConciliadosPorMovimientosOr(self,idMovOrigin):
        result = self.filter(
            idMovOrigin = idMovOrigin
        ).aggregate(
           sum =Sum("amountReconcilied")
        )
        return result
    
    def SumaMontosConciliadosPorMovimientosDest(self,idMovArrival):
            
        result = self.filter(idMovArrival = idMovArrival).aggregate(
            sum = Sum(
                Case(
                    When(
                        idMovArrival__idAccount__currency = F('idMovOrigin__idAccount__currency'),
                        then=F('amountReconcilied')
                    ),
                    default=F('equivalentAmount'),
                    output_field=DecimalField()
                )
            )
        )

        print(result)
        return result
    
    def SumaMontosConciliadosPorDocumentos(self,idDoc):
        #print("manager",1)
        #result = self.filter(
        #    idDoc = idDoc
        #).aggregate(
        #   sum =Sum("amountReconcilied")
        #)
        #return result
    
        #result =  self.filter(
        #        idDoc = idDoc
        #    ).values(
        #    'idDoc'
        #    ).annotate(
        #        # suma de montos de documentos segun movimiento origen
        #        sum=Sum(
        #            Case(
        #                When(idMovOrigin__idAccount__currency=F('idDoc__typeCurrency'), then=F('amountReconcilied')),
        #                default=F('equivalentAmount'),
        #                output_field=DecimalField()
        #            )
        #        ),
        #)
        
        result = self.filter(idDoc = idDoc).aggregate(
            sum = Sum(
                Case(
                    When(
                        idDoc__typeCurrency=F('idMovOrigin__idAccount__currency'),
                        then=F('amountReconcilied')
                    ),
                    default=F('equivalentAmount'),
                    output_field=DecimalField()
                )
            )
        )

        print(result)
        
        return result
    
    def SumaMontosEquivalentesConciliadosPorDocumentos(self,idDoc):
        #print("manager",10)
        #result = self.filter(
        #    idDoc = idDoc
        #    ).aggregate(
        #    sum =Sum("equivalentAmount")
        #    )
        #return result
    
        result =  self.filter(
                idDoc = idDoc
            ).values(
            'idDoc'
            ).annotate(
                # suma de montos de documentos segun movimiento origen
                sum=Sum(
                    Case(
                        When(idMovOrigin__idAccount__currency=F('idDoc__typeCurrency'), then=F('amountReconcilied')),
                        default=F('equivalentAmount'),
                        output_field=DecimalField()
                    )
                ),

            )
        
        return result[0]

