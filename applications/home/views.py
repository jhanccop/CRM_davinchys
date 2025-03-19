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
from applications.actividades.models import Trafos
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
    template_name = "home/main.html"
    context_object_name = 'data'

    def get_queryset(self):
        userId = self.request.user
        userArea = userId.position
        intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())
        payload = {}
        payload["nRequest"] = RequestList.objects.ListasPendientes(area=userArea)
        payload["docs"] = Documentations.objects.docs_publics(intervalo=intervalDate)
        return payload

        
