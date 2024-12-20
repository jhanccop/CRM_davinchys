from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
#
from .models import Transformer, Inventario

## ==================== Transformer =====================
class TransformerResource(resources.ModelResource):
    class Meta:
        model = Transformer

@admin.register(Transformer)
class TransformerAdmin(ImportExportModelAdmin):
    resource_class = TransformerResource
    list_display = (
        'barcode',
        'provider',
        'model_name',
        'KVA',
        'HVTAP',
        'KTapHV',
        'FIXHV',
    )
    search_fields = ('MOUNTING', 'COOLING', )
    list_filter = ('MOUNTING', 'COOLING',)

## ==================== Inventario =====================
class InventarioResource(resources.ModelResource):
    class Meta:
        model = Inventario

@admin.register(Inventario)
class InventarioAdmin(ImportExportModelAdmin):
    resource_class = InventarioResource
    list_display = (
        'code',
        'date',
        'name',
        'unit',
        'status',
        'location',
    )
    list_filter = ('code', 'status','location',)