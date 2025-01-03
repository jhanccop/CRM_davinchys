from datetime import date, datetime,timedelta

from django.db.models import OuterRef, Subquery, Count, F, Sum
from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models

class TrafoTrackingManager(models.Manager):
    def obtenerTrack(self,idTrack):
        return self.filter(idOrder = idTrack.id).order_by('dateChange')
    
    def ListOrdersTrack(self):
        #sq = Item.objects.filter(category=OuterRef('category')).order_by('-pubdate')  # deferred execution
        #Item.objects.filter(pk=Subquery(sq.values('pk')[:1]))
        Today = date.today()
        sq = self.filter(
            dateChange__gte = Today - timedelta(days = 30),
            idOrder=OuterRef('idOrder')
        ).order_by('-dateChange')
        payload = self.filter(pk=Subquery(sq.values('pk')[:1])).order_by('idOrder')

        return payload
    
class TrafoOrderManager(models.Manager):
    
    def listar_pedidos(self):
        from .models import OrderTracking
        Today = date.today()
        orders = self.filter(
            dateOrder__gte = Today - timedelta(days = 30),
        ).all().order_by('-dateOrder')
        print(orders)
        allOrders = []
        for order in orders:
            payload = {}

            lastStatus = OrderTracking.objects.filter(idOrder = order.id).order_by('dateChange').last()
            print("---****",lastStatus,order.idOrder)
            payload["id"] = order.id
            payload["idOrder"] = order.idOrder
            payload["idClient"] = order.idClient
            payload["idTransformer"] = order.idTransformer
            payload["dateOrder"] = order.dateOrder
            payload["idAttendant"] = order.idAttendant
            payload["IdOrderState"] = lastStatus

            allOrders.append(payload)
        return allOrders
    
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
    
    def listarPedidos(self):
        Today = date.today()
        orders = self.filter(
            dateOrder__gte = Today - timedelta(days = 30),
        ).order_by('id')

        return orders
    
class DailyTasksManager(models.Manager):
    def MiListarPorIntervalo(self,user,interval,type):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        if type == "2":
            result = self.filter(
                date__range = rangeDate,
                user = user
            ).order_by("-date")
        else:
            result = self.filter(
                date__range = rangeDate,
                user = user,
                is_overTime = False
            ).order_by("-date")
        return result
    
    def MiListarPorIntervaloHorasExtra(self,user,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = self.filter(
                date__range = rangeDate,
                user = user,
                is_overTime = True
            ).values(
                'date',
                'endTime',
                'startTime',
                'id',
                'activity'
            ).annotate(
                delta = F('endTime')-F('startTime')
            ).order_by("-date")

        return result
    
    def MiListarPorIntervaloHorasExtraAcc(self,user,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = self.filter(
                date__range = rangeDate,
                user = user,
                is_overTime = True
            ).values(
                'endTime',
                'startTime',
            ).annotate(
                delta = F('endTime')-F('startTime')
            ).aggregate(
            acc = Sum('delta')
        )

        return result
    
    def MiListarPorIntervaloDias(self,user,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = self.filter(
                date__range = rangeDate,
                user = user,
                is_overTime = False
            ).values(
                'date',
            ).distinct().aggregate(dias = Count("date"))

        return result
    
class TrafoQuoteManager(models.Manager):
    def CotizacionPorId(self,id):
        return self.get(id=id)
    
    def ListarPorIntervalo(self,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        if len(intervals) == 1:
            lista = self.filter(
                created__gte = intervals[0] - timedelta(days = 1),
            ).order_by('-created')
            return lista
        else:
            lista = self.filter(
                created__range=(intervals[0],intervals[1]+timedelta(days=1)),
            ).order_by('-created')
            return lista
    
class TrafosManager(models.Manager):
    def TrafoPorId(self,id):
        return self.get(id=id)
    
    def ListaPorCotizaciones(self,quote):
        ids = self.filter(
            idQuote__id = quote
        )
        #result = ids.values('idQuote').annotate(
        #    provider =  ArrayAgg('provider'),
        #)
        return ids
    
class TrafoTaskManager(models.Manager):
    def ListaTareasPorCotizacion(self,id):
        result = self.filter(
            idTrafoQuote = id
        )
        return result
    
class SuggestionBoxManager(models.Manager):
    def MiListaDeSugerencias(self,user):
        result = self.filter(
            user = user
        )
        return result