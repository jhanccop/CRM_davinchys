from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Trafos
from .forms import TrafosForm, TrafosFilterForm

class TrafosListView(LoginRequiredMixin, ListView):
    model = Trafos
    template_name = 'PRODUCCION/catalogo/trafos_list.html'
    context_object_name = 'trafos'
    #paginate_by = 2
    
    def get_queryset(self):
        queryset = Trafos.objects.all().select_related('idSupplier')
        
        # Filtros
        form = TrafosFilterForm(self.request.GET)
        if form.is_valid():
            KVA = form.cleaned_data.get('KVA')
            TYPE = form.cleaned_data.get('TYPE')
            MOUNTING = form.cleaned_data.get('MOUNTING')
            
            if KVA:
                queryset = queryset.filter(KVA=KVA)
            if TYPE:
                queryset = queryset.filter(TYPE=TYPE)
            if MOUNTING:
                queryset = queryset.filter(MOUNTING=MOUNTING)
        
        # Búsqueda
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(idSupplier__name__icontains=search) |
                Q(KVA__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TrafosFilterForm(self.request.GET)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class TrafosCreateView(LoginRequiredMixin, CreateView):
    model = Trafos
    form_class = TrafosForm
    template_name = 'PRODUCCION/catalogo/trafos_new.html'
    success_url = reverse_lazy('produccion_app:trafos-lista')
    
    def form_valid(self, form):
        form.instance.idUser = self.request.user
        return super().form_valid(form)

class TrafosDetailView(LoginRequiredMixin, DetailView):
    model = Trafos
    template_name = 'PRODUCCION/catalogo/trafos_detail.html'
    context_object_name = 'trafo'

class TrafosUpdateView(LoginRequiredMixin, UpdateView):
    model = Trafos
    form_class = TrafosForm
    template_name = 'PRODUCCION/catalogo/trafos_new.html'
    success_url = reverse_lazy('produccion_app:trafos-lista')
    
    def form_valid(self, form):
        form.instance.idUser = self.request.user
        return super().form_valid(form)

class TrafosDeleteView(LoginRequiredMixin, DeleteView):
    model = Trafos
    template_name = 'PRODUCCION/catalogo/trafos_confirm_delete.html'
    success_url = reverse_lazy('produccion_app:trafos-lista')