from datetime import date, datetime,timedelta

from django.db.models import OuterRef, Subquery, Count, Sum, Q

from django.db import models

class OrdersManager(models.Manager):
    
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
    
class OrdersTrakManager(models.Manager):
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
    
class PurchaseOrdersManager(models.Manager):
    def ListarPorIntervalo(self,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        if len(intervals) == 1:
            lista = self.filter(
                created_at__gte = intervals[0] - timedelta(days = 1),
            ).order_by('IdOrderState')
            return lista
        else:
            lista = self.filter(
                created_at__range=(intervals[0],intervals[1]+timedelta(days=1)),
            ).order_by('IdOrderState')
            return lista
        
    def listarPedidos(self):
        Today = datetime.today()
        orders = self.filter(
            created_at__gte = Today - timedelta(days = 30),
        ).order_by('IdOrderState')

        return orders
    
    def comprasPendientes(self):
        """ Ordenes que falta aprobacion """

        return self.filter(IdOrderState = "0").aggregate(Count("IdOrderState"))
       
class PurchaseTrackingManager(models.Manager):
    def ListOrdersTrack(self):
        Today = date.today()
        sq = self.filter(
            dateChange__gte = Today - timedelta(days = 30),
            idOrder=OuterRef('idOrder')
        ).order_by('-dateChange')
        payload = self.filter(pk=Subquery(sq.values('pk')[:1])).order_by('-idOrder')

        return payload
        
class ServiceOrdersManager(models.Manager):
    def ListarPorIntervalo(self,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        if len(intervals) == 1:
            lista = self.filter(
                created_at__gte = intervals[0] - timedelta(days = 1),
            ).order_by('IdOrderState')
            return lista
        else:
            lista = self.filter(
                created_at__range=(intervals[0],intervals[1]+timedelta(days=1)),
            ).order_by('IdOrderState')
            return lista
        
    def listarPedidos(self):
        Today = datetime.today()
        orders = self.filter(
            created_at__gte = Today - timedelta(days = 30),
        ).order_by('IdOrderState')

        return orders
    
    def serviciosPendientes(self):
        """ Ordenes que falta aprobacion """

        return self.filter(IdOrderState = "0").aggregate(Count("IdOrderState"))
    
class ServiceTrackingManager(models.Manager):
    def ListOrdersTrack(self):
        Today = date.today()
        sq = self.filter(
            dateChange__gte = Today - timedelta(days = 30),
            idOrder=OuterRef('idOrder')
        ).order_by('-dateChange')
        payload = self.filter(pk=Subquery(sq.values('pk')[:1])).order_by('-idOrder')

        return payload

class ListRequestManager(models.Manager):
    def ListaPorId(self,pk):
        result = self.get(
            id = pk
        )

        return result
    def ListasPorIntervalo(self,user,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = self.filter(
            created__range = rangeDate,
            idPetitioner = user
        ).order_by("-created")

        return result
    
    def ListaPorAreaUsuarioTiempo(self,area,user_selected,TimeSelect):
        date = datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')
        
        fil = self.all()
        # FLITRO DE TIEMPO
        if TimeSelect == "1":
            fil = self.filter(
                created__year = year,
                created__month = month
                )
        elif TimeSelect == "2":
            fil = self.filter(
                created__year = year,
                )
            
        # FLITRO DE USUARIO
        if user_selected == "all":
            result = fil.all().order_by("-created")
        else:
            result = fil.filter(
                    idPetitioner = user_selected
                ).order_by("-tag1","-created")
            
        # FLITRO POR AREA Y TAG
        payload = result
        if area == "5":
            payload = payload.filter(Q(tag1 = "0") | Q(tag1 = "1"))
        elif area == "1":
            payload = payload.filter(Q(tag2 = "0") | Q(tag2 = "1"))
        elif area == "6":
            payload = payload.filter(Q(tag3 = "0") | Q(tag3 = "1"))
        elif area == "0":
            payload = payload.filter(Q(tag4 = "0") | Q(tag4 = "1"))

        return payload
    
    def ListasPendientes(self,area):
        if area == "5": # adquisiciones
            result = self.filter(
            tag1 = "0" # pedidos solicitados
            ).aggregate(count = Count("tag1"))
            return result
        elif area == "1": # contabilidad
            result = self.filter(
            tag2="0" # pedidos solicitados
            ).aggregate(count = Count("tag2"))
            return result
        elif area == "6": # finanzas
            result = self.filter(
            tag3="0" # pedidos solicitados
            ).aggregate(count = Count("tag3"))
            return result
        elif area == "0": # gerencia
            result = self.filter(
            tag4="0" # pedidos solicitados
            ).aggregate(count = Count("tag4"))
            return result
        return result
    
    def RequerimientosPendientes(self,area):
        if area == "5": # adquisiciones
            result = self.filter(
            tag1 = "0" # pedidos solicitados
            ).aggregate(count = Count("tag1"))
            return result
        elif area == "1": # contabilidad
            result = self.filter(
            tag2="0" # pedidos solicitados
            ).aggregate(count = Count("tag2"))
            return result
        elif area == "6": # finanzas
            result = self.filter(
            tag3="0" # pedidos solicitados
            ).aggregate(count = Count("tag3"))
            return result
        elif area == "7": # tesoreria
            result = self.filter(
            tag4="0" # pedidos solicitados
            ).aggregate(count = Count("tag4"))
            return result

class PaymentRequestManager(models.Manager):
    def MiListarPorIntervalo(self,user,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = self.filter(
            created__range = rangeDate,
            idPetitioner = user
        ).order_by("-created")

        return result
    
    def ListaPorAreaUsuarioTiempo(self,area,user_selected,TimeSelect):
        date = datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')

        fil = self.all()
        
        if TimeSelect == "1":
            fil = self.filter(
                created__year = year,
                created__month = month
                )
        elif TimeSelect == "2":
            fil = self.filter(
                created__year = year,
                )
                    
        if user_selected == "all":
            if area == "5": # adquisiciones
                result = fil.filter(
                    tag1 = "0",
                ).order_by("-created")
            elif area == "1": # contabilidad
                result = fil.filter(
                    tag2 = "0",
                ).order_by("-created")
            elif area == "6": # finanzas
                result = fil.filter(
                    tag3 = "0",
                ).order_by("-created")
            elif area == "7": # tesoreria
                result = fil.filter(
                    tag4 = "0",
                ).order_by("-created")

        else:
            if area == "5": # adquisiciones
                result = fil.filter(
                    idPetitioner = user_selected,
                    tag1 = "0",
                ).order_by("-created")
            elif area == "1": # contabilidad
                result = fil.filter(
                    idPetitioner = user_selected,
                    tag2 = "0",
                ).order_by("-created")
            elif area == "6": # finanzas
                result = fil.filter(
                    idPetitioner = user_selected,
                    tag3 = "0",
                ).order_by("-created")
            elif area == "7": # tesoreria
                result = fil.filter(
                    idPetitioner = user_selected,
                    tag4 = "0",
                ).order_by("-created")

        return result

    def ListarAprobarPorIntervalo(self,area,user_selected,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = {}

        if user_selected == "all":
            if area == "5": # adquisiciones
                result = self.filter(
                    tag1 = "0",
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "1": # contabilidad
                result = self.filter(
                    tag2 = "0",
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "6": # finanzas
                result = self.filter(
                    tag3 = "0",
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "7": # tesoreria
                result = self.filter(
                    tag4 = "0",
                    created__range = rangeDate,
                ).order_by("-created")

        else:
            if area == "5": # adquisiciones
                result = self.filter(
                    idPetitioner = user_selected,
                    tag1 = "0",
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "1": # contabilidad
                result = self.filter(
                    idPetitioner = user_selected,
                    tag2 = "0",
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "6": # finanzas
                result = self.filter(
                    idPetitioner = user_selected,
                    tag3 = "0",
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "7": # tesoreria
                result = self.filter(
                    idPetitioner = user_selected,
                    tag4 = "0",
                    created__range = rangeDate,
                ).order_by("-created")

        return result
    
    def ListarHistoricoPorIntervalo(self,area,user_selected,interval):
        Intervals = interval.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = {}

        if user_selected == "all":
            if area == "5": # adquisiciones
                result = self.filter(
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "1": # contabilidad
                result = self.filter(
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "6": # finanzas
                result = self.filter(
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "7": # tesoreria
                result = self.filter(
                    created__range = rangeDate,
                ).order_by("-created")

        else:
            if area == "5": # adquisiciones
                result = self.filter(
                    idPetitioner = user_selected,
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "1": # contabilidad
                result = self.filter(
                    idPetitioner = user_selected,
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "6": # finanzas
                result = self.filter(
                    idPetitioner = user_selected,
                    created__range = rangeDate,
                ).order_by("-created")
            elif area == "7": # tesoreria
                result = self.filter(
                    idPetitioner = user_selected,
                    created__range = rangeDate,
                ).order_by("-created")

        return result
    
    def RequerimientosPendientes(self,area):
        if area == "5": # adquisiciones
            result = self.filter(
            tag1 = "0" # pedidos solicitados
            ).aggregate(count = Count("tag1"))
            return result
        elif area == "1": # contabilidad
            result = self.filter(
            tag2="0" # pedidos solicitados
            ).aggregate(count = Count("tag2"))
            return result
        elif area == "6": # finanzas
            result = self.filter(
            tag3="0" # pedidos solicitados
            ).aggregate(count = Count("tag3"))
            return result
        elif area == "7": # tesoreria
            result = self.filter(
            tag4="0" # pedidos solicitados
            ).aggregate(count = Count("tag4"))
            return result
        
    def RequerimientosPorNombreLista(self,pk, area = None):
        if area == "1":
            result = self.filter(
                idList__id=pk,
                tag2 = 0
            ).order_by("-created")
        else:
            result = self.filter(
                idList__id=pk
            ).order_by("-created")
        
        return result
    
    def RequerimientosContabilidadPorId(self,pk):
        result = self.filter(
            idList__id = pk,
            tag2 = "0",
        ).aggregate(n = Count("id"))
        
        return result

