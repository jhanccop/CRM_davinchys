from datetime import date, datetime,timedelta


from django.db.models import OuterRef, Subquery, Count, F, Sum, Q, ExpressionWrapper, fields, When, Case
from django.db.models.functions import ExtractDay, ExtractYear, Coalesce
from django.db import models
import calendar

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

    def DaysByMonthByUser(self,user_id, year, month):
        """
        Obtiene estadísticas de trabajo mensuales para un usuario específico.
        
        Args:
            user_id: ID del usuario
            year: Año (ej. 2025)
            month: Número del mes (1-12)
            
        Returns:
            dict: Estadísticas de días trabajados, horas extra y días feriados
        """
        # Convertir a enteros si son strings
        year = int(year)
        month = int(month)
        
        # Base query - filtrar por usuario, año y mes
        base_query = self.filter(
            user_id=user_id,
            date__year=year,
            date__month=month
        )
        
        # 1. Total de DÍAS LABORADOS EN EL MES (jornada regular - type '0')
        regular_days = base_query.filter(type="0").values('date').distinct().count()
        
        # 2. Total de HORAS EXTRA en el mes (suma de overTime donde type es '1')
        # Primero verifica si hay registros de horas extra
        overtime_hours_query = base_query.filter(type="1")
        overtime_hours = overtime_hours_query.aggregate(
            total_overtime=Sum('overTime')
        )['total_overtime'] or 0
        
        # También podemos sumar las horas extra en jornadas regulares si tienen valor
        regular_overtime_query = base_query.filter(
            type="2",
            overTime__isnull=False
        )
        regular_overtime = regular_overtime_query.aggregate(
            total_overtime=Sum('overTime')
        )['total_overtime'] or 0
        
        total_overtime = overtime_hours + regular_overtime
        
        # 3. Total de FERIADOS LABORADOS en el mes (type '2')
        holiday_days = base_query.filter(type="2").count()
        
        return {
            'regular_days': regular_days,
            'overtime_hours': float(total_overtime),
            'holiday_days': holiday_days,
            'year': year,
            'month': month,
            'user_id': user_id
        }

class RestDaysManager(models.Manager):

    # ================================
    def _get_month_range(self, year, month):
        """Calcula el primer y último día del mes"""
        last_day = calendar.monthrange(year, month)[1]
        return date(year, month, 1), date(year, month, last_day)
    
    def _get_base_queryset(self, year, month, user_id=None):
        """
        Base queryset para todos los indicadores
        Filtra por mes/año, estado aprobado (tag2=ACEPTADO) y opcionalmente por usuario
        """
        start_date, end_date = self._get_month_range(year, month)
        
        queryset = self.get_queryset().filter(
            tag2=self.model.ACEPTADO,
            startDate__lte=end_date
        ).filter(
            Q(endDate__gte=start_date) | Q(endDate__isnull=True)
        )
        
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
            
        return queryset
    
    def _calculate_duration(self, queryset):
        """
        Calcula la duración en días, considerando casos con endDate vacío
        """
        return queryset.annotate(
            duration_days=Case(
                # Cuando hay endDate, calculamos la diferencia en días
                When(endDate__isnull=False,
                    then=ExpressionWrapper(
                        ExtractDay(F('endDate') - F('startDate')) + 1,
                        output_field=fields.FloatField()
                    )),
                # Cuando no hay endDate, calculamos días basados en horas (8 horas = 1 día)
                When(endDate__isnull=True,
                    then=ExpressionWrapper(
                        F('hours') / 8,
                        output_field=fields.FloatField()
                    )),
                output_field=fields.FloatField()
            )
        )
    
    def _get_monthly_indicators(self, year, month, type_filter=None, user_id=None):
        """
        Método base para indicadores mensuales
        """
        queryset = self._get_base_queryset(year, month, user_id)
        
        if type_filter is not None:
            queryset = queryset.filter(type=type_filter)
        
        queryset = self._calculate_duration(queryset)
        
        return queryset
    
    def get_particular_days_approved(self, year, month, user_id=None):
        """
        Total de días de permisos particulares aprobados
        """
        queryset = self._get_monthly_indicators(
            year, month, self.model.PARTICULAR, user_id
        )
        
        if user_id:
            return queryset.aggregate(
                total_days=Sum('duration_days', output_field=models.FloatField())
            )['total_days'] or 0
        
        return queryset.values(
            'user__id', 'user__username'
        ).annotate(
            total_days=Sum('duration_days', output_field=models.FloatField())
        ).order_by('user__username')
    
    def get_medical_rest_days_approved(self, year, month, user_id=None):
        """
        Total de días de descanso médico aprobados
        """
        queryset = self._get_monthly_indicators(
            year, month, self.model.DESCANSOMEDICO, user_id
        )
        
        if user_id:
            return queryset.aggregate(total_days=Sum('duration_days'))['total_days'] or 0
        
        return queryset.values(
            'user__id', 'user__username'
        ).annotate(
            total_days=Sum('duration_days')
        ).order_by('user__username')
    
    def get_vacation_days_approved(self, year, month, user_id=None):
        """
        Total de días de vacaciones aprobados
        """
        queryset = self._get_monthly_indicators(
            year, month, self.model.VACACIONES, user_id
        )
        
        if user_id:
            return queryset.aggregate(total_days=Sum('duration_days'))['total_days'] or 0
        
        return queryset.values(
            'user__id', 'user__username'
        ).annotate(
            total_days=Sum('duration_days')
        ).order_by('user__username')
    
    def get_maternity_days_approved(self, year, month, user_id=None):
        """
        Total de días de maternidad aprobados
        """
        queryset = self._get_monthly_indicators(
            year, month, self.model.MATERNIDAD, user_id
        )
        
        if user_id:
            return queryset.aggregate(total_days=Sum('duration_days'))['total_days'] or 0
        
        return queryset.values(
            'user__id', 'user__username'
        ).annotate(
            total_days=Sum('duration_days')
        ).order_by('user__username')
    
    def get_compensated_days(self, year, month, user_id=None):
        """
        Total de días con compensación necesaria (isCompensated=True)
        """
        queryset = self._get_base_queryset(year, month, user_id).filter(
            isCompensated=True
        )
        
        queryset = self._calculate_duration(queryset)
        
        if user_id:
            return queryset.aggregate(total_days=Sum('duration_days'))['total_days'] or 0
        
        return queryset.values(
            'user__id', 'user__username'
        ).annotate(
            total_days=Sum('duration_days')
        ).order_by('user__username')
    
    def get_total_compensated_days(self, year, month, user_id=None):
        """
        Total de días compensados (daysCompensated)
        """
        queryset = self._get_base_queryset(year, month, user_id).filter(
            daysCompensated__gt=0
        )
        
        if user_id:
            return queryset.aggregate(total_days=Sum('daysCompensated'))['total_days'] or 0
        
        return queryset.values(
            'user__id', 'user__username'
        ).annotate(
            total_days=Sum('daysCompensated')
        ).order_by('user__username')
    
    def get_compensated_hours(self, year, month, user_id=None):
        """
        Total de horas con compensación necesaria (isCompensated=True)
        """
        queryset = self._get_base_queryset(year, month, user_id).filter(
            isCompensated=True
        )
        
        if user_id:
            return queryset.aggregate(total_hours=Sum('hours'))['total_hours'] or 0
        
        return queryset.values(
            'user__id', 'user__username'
        ).annotate(
            total_hours=Sum('hours')
        ).order_by('user__username')
    
    def get_total_compensated_hours(self, year, month, user_id=None):
        """
        Total de horas compensadas (hoursCompensated)
        """
        queryset = self._get_base_queryset(year, month, user_id).filter(
            hoursCompensated__gt=0
        )
        
        if user_id:
            return queryset.aggregate(total_hours=Sum('hoursCompensated'))['total_hours'] or 0
        
        return queryset.values(
            'user__id', 'user__username'
        ).annotate(
            total_hours=Sum('hoursCompensated')
        ).order_by('user__username')
    
    def getRestDaysByMonthByUser(self, year, month, user_id=None):
        """
        Método que devuelve todos los indicadores en un solo diccionario
        """
        return {
            'particular_days': self.get_particular_days_approved(year, month, user_id),
            'medical_rest_days': self.get_medical_rest_days_approved(year, month, user_id),
            'vacation_days': self.get_vacation_days_approved(year, month, user_id),
            'maternity_days': self.get_maternity_days_approved(year, month, user_id),
            'compensated_days': self.get_compensated_days(year, month, user_id),
            'total_compensated_days': self.get_total_compensated_days(year, month, user_id),
            'compensated_hours': self.get_compensated_hours(year, month, user_id),
            'total_compensated_hours': self.get_total_compensated_hours(year, month, user_id),
        }
    
    # ================================
    
    def getMyListRestDaysForMonth(self, user, year, month):
        """
            Lista de PREMISOS LABORALES SOLICITADOS POR USUARIO DADO UN MES
        """
        month_start = date(year, month, 1)
        if month == 12:
            month_end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(year, month + 1, 1) - timedelta(days=1)

        result = self.filter(
                user=user
            ).filter(
                created__lte = month_end,
                created__gte = month_start
            )
        
        return result
    
    def getRestTimesNoCompensateById(self, user):
        """
            Lista de PREMISOS LABORALES SOLICITADOS POR USUARIO
        """
        result = self.filter(
                user=user,
                isCompensated = True,
                tag2 = "1" # aprobados
            ).filter(
            models.Q(days__gt=models.F('daysCompensated')) | 
            models.Q(hours__gt=models.F('hoursCompensated'))
        )
        
        return result


    def getListOfRestPermitsByArea(self, area):
        """
        Obtener los dias de descanso solicitados al aera
        """

        if area == "9": #  9 recursos humanos
            result =  self.filter(
                Q(tag1="0") | Q(tag1="1")  | Q(tag1="2")
            )
            return result

        elif area == "0": # 0 administrador
            result =  self.filter(
                Q(tag2="0") | Q(tag2="1")  | Q(tag2="2")
            )
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