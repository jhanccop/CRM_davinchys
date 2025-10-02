from django.db import models
from datetime import date, timedelta, datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import TruncDate,LastValue,Abs, TruncMonth

from django.db.models import Sum, Max, DateField,F, Q, CharField, When, Value, Case, When, FloatField
from django.db.models import OuterRef, Subquery

# ======================= REQUERIMIENTOS =======================
class requirementsManager(models.Manager):
    def ListaRequerimientosPorUsuario(self,intervalo,idPetitioner):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        from applications.COMERCIAL.purchase.models import RequestTracking
        last_tracking_subquery = RequestTracking.objects.filter(
            idRequirement=OuterRef('pk')
        ).order_by('-created').values('status', 'area')[:1]

        # Consulta principal que obtiene los requirements con su último estado y área
        result = self.filter(
            created__range=rangeDate,
            idPetitioner__id=idPetitioner
        ).annotate(
            lastStatus=Subquery(last_tracking_subquery.values('status')),
            lastArea=Subquery(last_tracking_subquery.values('area'))
        ).order_by('-created')
            

        return result

    def ListaRequerimientosForBoss(self,intervalo):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        from applications.COMERCIAL.purchase.models import RequestTracking
        last_tracking_subquery = RequestTracking.objects.filter(
            idRequirement=OuterRef('pk')
        ).order_by('-created').values('status', 'area')[:1]

        # Consulta principal que obtiene los requirements con su último estado y área
        result = self.filter(
            created__range=rangeDate,
        ).annotate(
            lastStatus=Subquery(last_tracking_subquery.values('status')),
            lastArea=Subquery(last_tracking_subquery.values('area'))
        ).order_by('-created')
            
        return result

    def obtenerRequerimientoPorId(self,id):
        return self.get(id = id)

    def ListaOrdenesdeCompra(self,intervalo):
        """
            Lista de ordenes de compra
        """

        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        from applications.COMERCIAL.purchase.models import RequestTracking
        last_tracking_subquery = RequestTracking.objects.filter(
            idRequirement=OuterRef('pk')
        ).order_by('-created').values('status', 'area')[:1]

        STATE_CHOICES = RequestTracking.STATE_CHOICES

        result = self.filter(
            created__range=rangeDate,
            isPurchaseOrder = True
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

    # ========================== MANAGER LOGISTICOS ==========================

    def ListaRequerimientosPorArea(self,intervalo,idArea):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        from applications.COMERCIAL.purchase.models import RequestTracking
        last_tracking_subquery = RequestTracking.objects.filter(
            idRequirement=OuterRef('pk')
        ).order_by('-created').values('status', 'area')[:1]

        # Consulta principal que obtiene los requirements con su último estado y área
        result = self.filter(
            created__range = rangeDate,
            idPetitioner__position = idArea
        ).annotate(
            lastStatus=Subquery(last_tracking_subquery.values('status')),
            lastArea=Subquery(last_tracking_subquery.values('area'))
        ).order_by('-created')
            
        return result
    

class requestTrackingManager(models.Manager):
    def obtenerTrackingPorIdRequerimiento(self,id):
        return self.filter(idRequirement = id).order_by("-id")

    def getListRequestByArea(self, area):
        """
        Obtener los requerimientos solicitados al aera
        """
        if area == "1": # 1 MANAGER AREA
            result =  self.filter(
                status = "1", # RECIBIDO
            )
            return result
        elif area == "2": # GERENCIA
            result =  self.filter(
                status = "1", # RECIBIDO
            )
            return result
        elif area == "3": # COMPRAS
            result =  self.filter(
                status = "1", # RECIBIDO
            )
            return result
        elif area == "4": # CONTABILIDAD
            result =  self.filter(
                status = "1", # RECIBIDO
            )
            return result
        elif area == "3": # 0 ADMINISTRADOR
            result =  self.filter(
                Q(tag4="0") | Q(tag4="1")
            )
            return result

class requirementItemsManager(models.Manager):
    def obtenerTrackingPorIdRequerimiento(self,id):
        return self.filter(idRequirement = id).order_by("-id")

# ======================= CAJA CHICA =======================
class PettyCashManager(models.Manager):
    def ListaCajaChicaPorUsuario(self,intervalo,idPetitioner):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = self.filter(
            created__range=rangeDate,
            idPetitioner__id=idPetitioner
        ).order_by('-created')
        
        return result

    def obtenerCajaChicaPorId(self,id):
        return self.get(id = id)

class PettyCashItemsManager(models.Manager):
    def obtenerPettyCashItemsPorId(self,id):
        return self.filter(idPettyCash = id).order_by("-id")
 
# ======================= DOCS =======================
class requirementsInvoiceManager(models.Manager):
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
            tin = ArrayAgg('idSupplier__tradeName'),
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
