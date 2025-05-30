import pandas as pd
from datetime import date, timedelta

from django.shortcuts import render
from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DeleteView,
    UpdateView
)

from django.urls import reverse_lazy

# models
from applications.movimientos.models import DocumentsUploaded
from applications.users.models import Documentations
from applications.actividades.models import Trafos, RestDays, DailyTasks
from applications.pedidos.models import PaymentRequest, RequestList

# forms
from applications.actividades.forms import TrafoForm

from django.contrib.auth.mixins import LoginRequiredMixin
#
from .models import ContainerTracking

from .forms import TrackingForm

class HomeView(TemplateView):
    template_name = "home/home.html"

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
        payload["PaymentReq"] = PaymentRequest.objects.getListOfPaymentRequestByArea(area=userArea)

        # Lista de de pPERMISOS LABORALES SOLICITADOS AL AREA
        payload["RestDaysReq"] = RestDays.objects.getListOfRestPermitsByArea(area=userArea)

        # Mi Lista requerimientos de compra o desembolsos por mes y por usuario
        payload["listPaymentReq"] = PaymentRequest.objects.getMyListPaymentRequestForMonth(userId,yearSelected,monthSelected)

        # Mi Lista de PERMISOS LABORALES por mes y por usuario
        payload["listRestDayReq"] = RestDays.objects.getMyListRestDaysForMonth(userId,yearSelected,monthSelected)

        #payload["docs"] = Documentations.objects.docs_publics(intervalo=intervalDate) # falta 

        return payload

        
