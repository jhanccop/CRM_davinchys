# Django
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    View,
)
# local
from applications.users.mixins import AlmacenPermisoMixin
#
from .models import Transformer, Inventario
from .forms import TransformerForm
from applications.utils import render_to_pdf

# ===================== TRANSFORMADOR =========================

class TransformadorListView(ListView):
    template_name = "producto/lista_transformadores.html"
    context_object_name = 'transformador'
    model = Transformer

class TransformadorCreateView(CreateView):
    template_name = "producto/crear_transformadores.html"
    model = Transformer
    form_class = TransformerForm
    success_url = reverse_lazy('producto_app:transformador-lista')

class TransformadorDeleteView(DeleteView):
    template_name = "producto/eliminar_transformadores.html"
    model = Transformer
    success_url = reverse_lazy('producto_app:transformador-lista')

class TransformadorUpdateView(UpdateView):
    template_name = "producto/editar_transformadores.html"
    model = Transformer
    form_class = TransformerForm
    success_url = reverse_lazy('producto_app:transformador-lista')

class TransformadorDetailView(DetailView):
    template_name = "producto/detalle_transformador.html"
    model = Transformer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #
        return context
    
# ===================== INVENTARIO =========================
class InventarioListView(ListView):
    template_name = "producto/lista_inventario.html"
    context_object_name = 'inventario'
    paginate_by = 1
    model = Inventario


# =============================
"""
class ProductListView(AlmacenPermisoMixin, ListView):
    template_name = "producto/lista.html"
    context_object_name = 'productos'

    def get_queryset(self):
        kword = self.request.GET.get("kword", '')
        order = self.request.GET.get("order", '')
        queryset = Product.objects.buscar_producto(kword, order)
        return queryset

class ProductCreateView(AlmacenPermisoMixin, CreateView):
    template_name = "producto/form_producto.html"
    form_class = ProductForm
    success_url = reverse_lazy('producto_app:producto-lista')


class ProductUpdateView(AlmacenPermisoMixin, UpdateView):
    template_name = "producto/form_producto.html"
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('producto_app:producto-lista')



class ProductDeleteView(AlmacenPermisoMixin, DeleteView):
    template_name = "producto/delete.html"
    model = Product
    success_url = reverse_lazy('producto_app:producto-lista')


class ProductDetailView(AlmacenPermisoMixin, DetailView):
    template_name = "producto/detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #
        context["ventas_mes"] = SaleDetail.objects.ventas_mes_producto(
            self.kwargs['pk']
        )
        return context


class ProductDetailViewPdf(AlmacenPermisoMixin, View):
    
    def get(self, request, *args, **kwargs):
        producto = Product.objects.get(id=self.kwargs['pk'])
        data = {
            'product': producto,
            'ventas_mes': SaleDetail.objects.ventas_mes_producto(self.kwargs['pk'])
        }
        pdf = render_to_pdf('producto/detail-print.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class FiltrosProductListView(AlmacenPermisoMixin, ListView):
    template_name = "producto/filtros.html"
    context_object_name = 'productos'

    def get_queryset(self):

        queryset = Product.objects.filtrar(
            kword=self.request.GET.get("kword", ''),
            date_start=self.request.GET.get("date_start", ''),
            date_end=self.request.GET.get("date_end", ''),
            provider=self.request.GET.get("provider", ''),
            marca=self.request.GET.get("marca", ''),
            order=self.request.GET.get("order", ''),
        )
        return queryset
"""    


    

