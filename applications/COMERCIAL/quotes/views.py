from datetime import date, timedelta

from django.views.generic import (
    CreateView,
    ListView
)
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import TrafoQuote, Trafos
from .forms import TrafoQuoteForm, TrafoForm
from applications.cuentas.models import Account

TrafosFormSet = inlineformset_factory(TrafoQuote, Trafos, form=TrafoForm, extra=1)

# ================= COTIZACIONES ========================
class CreateTrafoQuoteView(CreateView):
    model = TrafoQuote
    form_class = TrafoQuoteForm
    template_name = 'COMERCIAL/quotes/crear-cotizacion.html'
    success_url = reverse_lazy('comercial_app:lista-cotizaciones')  # Ajusta esto a tu URL de listado
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['trafos_formset'] = TrafosFormSet(self.request.POST, prefix='trafos')
        else:
            context['trafos_formset'] = TrafosFormSet(prefix='trafos')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        trafos_formset = context['trafos_formset']
        if trafos_formset.is_valid():
            self.object = form.save()
            trafos_formset.instance = self.object
            trafos_formset.save()
            return redirect('success_url')  # Redirigir a una URL de éxito
        return self.render_to_response(self.get_context_data(form=form))

class TrafoQuoteListView(ListView):
    template_name = 'COMERCIAL/quotes/lista-cotizaciones.html'
    context_object_name = 'quote'
    
    def get_queryset(self,**kwargs):
        compania_id = self.request.session.get('compania_id')
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 90)) + " to " + str(date.today())

        quotes = TrafoQuote.objects.ListaCotizacionesPorRuc(intervalo = intervalDate, company = compania_id)
        payload = {}
        payload["intervalDate"] = intervalDate
        payload["listQuotes"] = quotes
        return payload
    
class QuoteView(CreateView):
    template_name = "home/quote-with-us.html"
    model = Trafos
    form_class = TrafoForm
    success_url = reverse_lazy('home_app:home')