import pandas as pd
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Count, Q, Sum
from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DeleteView,
    UpdateView
)

from django.urls import reverse_lazy

from applications.actividades.models import Trafos, RestDays, DailyTasks
from applications.COMERCIAL.purchase.models import RequestTracking
from applications.RRHH.models import Local, Empleado, Documento, Permiso, RegistroAsistencia, Feriados

# forms
from applications.actividades.forms import TrafoForm

from django.contrib.auth.mixins import LoginRequiredMixin
#
from .models import ContainerTracking

from .forms import TrackingForm

from dateutil.relativedelta import relativedelta
import calendar

class HomeView(TemplateView):
    template_name = "home/home.html"

class unauthorizedView(TemplateView):
    template_name = "home/unauthorizedView.html"

class EnterTrackingNumberView(ListView):
    template_name = "home/enter-tracking-number.html"
    context_object_name = 'order'

    def get_queryset(self):
        order = self.request.GET.get("order", '')
        payload = {}
        payload["order"] = order
        payload["tracking"] = ContainerTracking.objects.searchOrder(order = order)
        return payload

class TrackingListView(LoginRequiredMixin,ListView):
    template_name = "home/list-tracking-number.html"
    context_object_name = 'order'
    model = ContainerTracking

class TrackingCreateView(LoginRequiredMixin, CreateView):
    template_name = "home/add-tracking-number.html"
    model = ContainerTracking
    form_class = TrackingForm
    success_url = reverse_lazy('home_app:list-tracking-number')

class TrackingEditView(LoginRequiredMixin, UpdateView):
    template_name = "home/edit-tracking-number.html"
    model = ContainerTracking
    form_class = TrackingForm
    success_url = reverse_lazy('home_app:list-tracking-number')

class TrackingDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "home/delete-tracking-number.html"
    model = ContainerTracking
    success_url = reverse_lazy('home_app:list-tracking-number')

class QuoteView(CreateView):
    template_name = "home/quote-with-us.html"
    model = Trafos
    form_class = TrafoForm
    success_url = reverse_lazy('home_app:home')

class PanelHomeView(LoginRequiredMixin,ListView):
    """
        - numero de solicitudes pendientes por aprobar (sumario total )
        - lista mis solicitudes de desembolso
        - lista de solicitudes de permisos
        - Dias laborados en el mes
        - Horas extra acumulada en el mes
        - Horas extra totales acumuladas

        - dias de permisos solicitado en el mes
        - dias de permiso totales

        - dias de vacaciones acumulado (tomado como referencia desde la contratacion)
    """
    template_name = "home/main.html"
    context_object_name = 'data'

    def get_queryset(self):
        userId = self.request.user
        userArea = userId.position
        dateSelected = self.request.GET.get("Kword", '')
        
        date_range = pd.date_range(userId.startDate, pd.Timestamp.now().date(), freq='MS')

        months = [date.strftime("%Y - %m") for date in date_range]

        if dateSelected == None or dateSelected == "":
            dateSelect = months[-1].split(" - ")
            monthSelected = int(dateSelect[1])
            yearSelected = int(dateSelect[0])
            dateSelected = months[-1]
        else:
            dateSelect = dateSelected.split(" - ")
            monthSelected = int(dateSelect[1])
            yearSelected = int(dateSelect[0])

        payload = {}

        payload['listMonths'] = months
        payload["monthSelected"] = dateSelected

        # Numero de dias laborados en el mes por usuario
        payload["nDays"] = DailyTasks.objects.DaysByMonthByUser(userId,yearSelected,monthSelected)

        # Numero de PERMISOS LABORALES acumulados por usuario por mes
        payload["nRestDays"] = RestDays.objects.getRestDaysByMonthByUser(yearSelected,monthSelected,userId)

        # Numero de requerimientos de compra o desembolsos pendientes por AREA O CARGO
        #payload["PaymentReq"] = PaymentRequest.objects.ListasPendientesPagoPorArea(area=userArea)
        #payload["PaymentReq"] = PaymentRequest.objects.getListOfPaymentRequestByArea(area=userArea)
        payload["PaymentReq"] = RequestTracking.objects.getListRequestByArea(area=userArea)

        # Lista de PERMISOS LABORALES SOLICITADOS AL AREA
        payload["RestDaysReq"] = RestDays.objects.getListOfRestPermitsByArea(area=userArea)

        # Mi Lista requerimientos de compra o desembolsos por mes y por usuario
        #payload["listPaymentReq"] = PaymentRequest.objects.getMyListPaymentRequestForMonth(userId,yearSelected,monthSelected)

        # Mi Lista de PERMISOS LABORALES por mes y por usuario
        payload["listRestDayReq"] = RestDays.objects.getMyListRestDaysForMonth(userId,yearSelected,monthSelected)

        #payload["docs"] = Documentations.objects.docs_publics(intervalo=intervalDate) # falta 

        return payload

# ===========================MY ESPACE ===========================

class myEspaceView(LoginRequiredMixin, TemplateView):
    """Vista principal del dashboard de bienvenida"""
    template_name = 'home/myspace.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        empleado = user.empleado
        
        # Obtener período seleccionado
        periodo = self.request.GET.get('periodo', 'mes_actual')
        fecha_inicio, fecha_fin = self._calcular_rango_fechas(periodo)
        
        # Información personal
        context['user'] = user
        context['periodo_seleccionado'] = periodo
        
        # Métricas de asistencia
        metricas = self._calcular_metricas_asistencia(empleado, fecha_inicio, fecha_fin)
        context.update(metricas)
        
        # Registro del día actual
        context['registro_hoy'] = self._obtener_registro_hoy(empleado)
        context['horas_extra1_registradas'] = self._obtener_horas_extra_hoy(empleado, '1')
        context['horas_extra2_registradas'] = self._obtener_horas_extra_hoy(empleado, '2')
        
        # Documentos
        context['porcentaje_documentos'] = empleado.documento_set.porcentaje_completado(empleado.id)
        context['documentos'] = empleado.documento_set.all()[:5]
        
        # Permisos
        context['permisos'] = empleado.permiso_set.all()[:5]

        # Locales
        idCompañia = self.request.user.company
        context['locales'] = Local.objects.obtenerLocalPorCompañia(idCompañia)
        
        return context
    
    def _calcular_rango_fechas(self, periodo):
        hoy = timezone.now().date()
        
        if periodo == 'mes_anterior':
            # Mes anterior
            primer_dia_mes_actual = hoy.replace(day=1)
            ultimo_dia_mes_anterior = primer_dia_mes_actual - timedelta(days=1)
            primer_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)
            return primer_dia_mes_anterior, ultimo_dia_mes_anterior
        elif periodo == 'semestre':
            # Últimos 6 meses
            fecha_fin = hoy
            fecha_inicio = hoy - timedelta(days=180)
            return fecha_inicio, fecha_fin
        else:  # mes_actual
            # Mes actual
            primer_dia_mes = hoy.replace(day=1)
            ultimo_dia_mes = hoy.replace(day=calendar.monthrange(hoy.year, hoy.month)[1])
            return primer_dia_mes, ultimo_dia_mes
    
    def _calcular_metricas_asistencia(self, empleado, fecha_inicio, fecha_fin):
        # Obtener todos los registros de asistencia en el período
        registros = empleado.registroasistencia_set.filtrar_por_fecha(fecha_inicio, fecha_fin)
        
        # Calcular días laborables (lunes a viernes, excluyendo feriados)
        from applications.RRHH.models import Feriados
        dias_laborables = self._calcular_dias_laborables(fecha_inicio, fecha_fin)
        
        # Días laborados (registros con jornada regular)
        dias_laborados = registros.filter(jornada_diaria='0').values('fecha').distinct().count()
        
        # Horas extra
        horas_extra1 = registros.filter(jornada_diaria='1').aggregate(
            total=Sum('horas')
        )['total'] or 0
        
        horas_extra2 = registros.filter(jornada_diaria='2').aggregate(
            total=Sum('horas')
        )['total'] or 0
        
        # Días con permisos
        from applications.RRHH.models import Permiso
        dias_permiso = Permiso.objects.filter(
            empleado=empleado,
            fecha_inicio__lte=fecha_fin,
            fecha_fin__gte=fecha_inicio,
            estado='1'  # Aprobado
        ).count()
        
        # Días ausentes (días laborables - días laborados - días permiso aprobados)
        dias_ausentes = max(0, dias_laborables - dias_laborados - dias_permiso)
        
        return {
            'dias_laborables': dias_laborables,
            'dias_laborados': dias_laborados,
            'dias_ausentes': dias_ausentes,
            'dias_permiso': dias_permiso,
            'horas_extra1': horas_extra1,
            'horas_extra2': horas_extra2,
        }
    
    def _calcular_dias_laborables(self, fecha_inicio, fecha_fin):
        from applications.RRHH.models import Feriados
        
        # Obtener feriados en el rango
        feriados = Feriados.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).values_list('fecha', flat=True)
        
        # Calcular días laborables (lunes a viernes excluyendo feriados)
        dias_laborables = 0
        current_date = fecha_inicio
        
        while current_date <= fecha_fin:
            # Lunes=0, Domingo=6
            if current_date.weekday() < 5 and current_date not in feriados:
                dias_laborables += 1
            current_date += timedelta(days=1)
        
        return dias_laborables
    
    def _obtener_registro_hoy(self, empleado):
        hoy = timezone.now().date()
        return empleado.registroasistencia_set.filter(
            fecha=hoy,
            jornada_diaria='0'  # Jornada regular
        ).first()
    
    def _obtener_horas_extra_hoy(self, empleado, tipo_extra):
        hoy = timezone.now().date()
        return empleado.registroasistencia_set.filter(
            fecha=hoy,
            jornada_diaria=tipo_extra  # '1' para HE1, '2' para HE2
        ).exists()
