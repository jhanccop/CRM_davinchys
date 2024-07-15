from datetime import date, timedelta, datetime
from django.db.models import Sum, Max, DateField,F, Q
from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models.functions import TruncDate,LastValue,Abs
from applications.cuentas.models import Account

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
        ).order_by("-id")

        return result
    
    def ListaMovimientosPorTipo(self,documentation):
        ids = self.filter(
            #idBankMovements__id__in = movimientos
        )
        result = ids.values('idBankMovements__id').annotate(
            accumulate = Sum("amountReconcilied"),
            per = Abs(Sum("amountReconcilied")*100/F('idBankMovements__amount')),
            tin =  ArrayAgg('idClient__ruc'),
            doc =  ArrayAgg('description'),
            amount = ArrayAgg('amountReconcilied'),
        )
                
        return result
    
class  BankReconciliationManager(models.Manager):
   def ListaDocumentosPorTipo(self,intervalo,tipo):
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
            ).order_by("date")
        else:
           result = self.filter(
                date__range = rangeDate,
                typeInvoice = str(tipo)
            ).order_by("date")

        return result
   
   def ListaConciliacionPorCuenta(self,movimientos):

      ids = self.filter(
         idBankMovements__id__in = movimientos
      )
      result = ids.values('idBankMovements__id').annotate(
         accumulate = Sum("amountReconcilied"),
         per = Abs(Sum("amountReconcilied")*100/F('idBankMovements__amount')),
         tin =  ArrayAgg('idClient__ruc'),
         doc =  ArrayAgg('description'),
         amount = ArrayAgg('amountReconcilied'),
      )
            
      return result


class TransactionsManager(models.Manager):
  def SaldosGeneralPorIntervalo(self,intervalo):
    Intervals = intervalo.split(' to ')
    intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

    # =========== Creacion de rango de fechas ===========
    rangeDate = [intervals[0],None]
    if len(intervals) == 1:
       rangeDate[1] = intervals[0] + timedelta(days = 1)
    else:
        rangeDate[1] = intervals[1] + timedelta(days = 1)
    return self.filter(dateTime__range = rangeDate).order_by("-dateTime")

  def ReportePorCuenta_v0(self,intervalo,moneda,cajaChica):
    Intervals = intervalo.split(' to ')
    intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

    # =========== Creacion de rango de fechas ===========
    rangeDate = [intervals[0] - timedelta(days = 1),None]
    
    if len(intervals) == 1:
       rangeDate[1] = intervals[0] + timedelta(days = 1)
    else:
        rangeDate[1] = intervals[1] + timedelta(days = 1)

    # =========== extraccion de cuentas por moneda (soles o dolares)===========
    cuentas = Account.objects.ListaCuentasGeneral(moneda,cajaChica) # 1: soles

    listPayload = []
    for cuenta in cuentas:
        compilado = {}
        print(cuenta)
        dt = self.filter(
            dateTime__range = rangeDate,
            idAccount__id = cuenta.id
            ).annotate(
                day=TruncDate('dateTime', output_field = DateField()),
            ).values(
                'day'
            ).annotate(
                DateTime=Max('dateTime'),
            ).values('DateTime').order_by('-DateTime')
        
        ddtt = [i["DateTime"] for i in dt]

        saldoFinal = self.filter(
            dateTime__in = ddtt,
            idAccount__currency = moneda,
            idAccount__cajaChica = cajaChica
        ).order_by('-dateTime')

        lista = self.filter(
           dateTime__range = rangeDate,
           idAccount__id = cuenta.id
        ).order_by("-dateTime")

        compilado["Cuenta"] = cuenta
        compilado["SaldoFinal"] = saldoFinal
        compilado["ListaTransaciones"] = lista
        listPayload.append(compilado)
    
    print("compilado",listPayload)
    return listPayload

  def ReportePorCuenta(self,intervalo,cuenta):
    Intervals = intervalo.split(' to ')
    intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

    # =========== Creacion de rango de fechas ===========
    rangeDate = [intervals[0] - timedelta(days = 1),None]
    
    if len(intervals) == 1:
       rangeDate[1] = intervals[0] + timedelta(days = 1)
    else:
        rangeDate[1] = intervals[1] + timedelta(days = 1)

    compilado = {}

    dt = self.filter(
        dateTime__range = rangeDate,
        idAccount__id = cuenta
        ).annotate(
            day=TruncDate('dateTime', output_field = DateField()),
        ).values(
            'day'
        ).annotate(
            DateTime=Max('dateTime'),
        ).values('DateTime').order_by('-DateTime')
    
    ddtt = [i["DateTime"] for i in dt]

    saldoFinalDiario = self.filter(
        dateTime__in = ddtt,
        idAccount__id = cuenta
    ).order_by('-dateTime')

    lista = self.filter(
        dateTime__range = rangeDate,
        idAccount__id = cuenta
    ).order_by("-dateTime")

    PorCategoria = self.filter(
        dateTime__range = rangeDate,
        idAccount__id = cuenta,
        transactionType = "0" # solo egresos
    ).values(
       "category",
    ).annotate(
       acumulate = Sum("amount"),
    ).values("category","acumulate").order_by(
       "category"
    )

    TotalIngresos = self.filter(
        dateTime__range = rangeDate,
        idAccount__id = cuenta,
        transactionType = "1" # solo egresos
    ).aggregate(Sum("amount"))

    TotalEgresos = self.filter(
        dateTime__range = rangeDate,
        idAccount__id = cuenta,
        transactionType = "0" # solo egresos
    ).aggregate(Sum("amount"))

    compilado["Cuenta"] = Account.objects.CuentasById(id = cuenta)
    compilado["saldoFinalDiario"] = saldoFinalDiario
    compilado["ListaTransaciones"] = lista
    compilado["PorCategoria"] = PorCategoria
    compilado["TotalIngresos"] = TotalIngresos
    compilado["TotalEgresos"] = TotalEgresos

    return compilado

  def ReportePorCajaChica(self,intervalo,cuenta):
    from applications.egresos.models import CajaChica
    Intervals = intervalo.split(' to ')
    intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

    # =========== Creacion de rango de fechas ===========
    rangeDate = [intervals[0] - timedelta(days = 1),None]
    
    if len(intervals) == 1:
       rangeDate[1] = intervals[0] + timedelta(days = 1)
    else:
        rangeDate[1] = intervals[1] + timedelta(days = 1)

    compilado = {}

    dt = self.filter(
        dateTime__range = rangeDate,
        idAccount__id = cuenta
        ).annotate(
            day=TruncDate('dateTime', output_field = DateField()),
        ).values(
            'day'
        ).annotate(
            DateTime=Max('dateTime'),
        ).values('DateTime').order_by('-DateTime')
    
    ddtt = [i["DateTime"] for i in dt]

    saldoFinal = self.filter(
        dateTime__in = ddtt,
        idAccount__id = cuenta
    ).order_by('-dateTime')

    lista = self.filter(
        dateTime__range = rangeDate,
        idAccount__id = cuenta
    ).order_by("-dateTime")

    acumulados = CajaChica.objects.filter(
        paymentDate__range = rangeDate,
        idAccount__id = cuenta,
    ).values(
       "subcategory",
    ).annotate(
       acumulate = Sum("amount"),
    ).values("subcategory","acumulate").order_by(
       "subcategory"
    )

    #print("eehhe",acumulados)

    compilado["Cuenta"] = Account.objects.CuentasById(id = cuenta)
    compilado["SaldoFinal"] = saldoFinal
    compilado["ListaTransaciones"] = lista
    compilado["PorCategoria"] = acumulados

    #print(compilado)

    return compilado
    
class InternalTransfersManager(models.Manager):
  
  def ListarPorIntervalo(self,interval):
    Intervals = interval.split(' to ')
    intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

    if len(intervals) == 1:
        lista = self.filter(
            created_at__gte = intervals[0] - timedelta(days = 1),
        ).order_by('-created_at')
        return lista
    else:
        lista = self.filter(
            created_at__range=(intervals[0],intervals[1]+timedelta(days=1)),
        ).order_by('-created_at')
        return lista