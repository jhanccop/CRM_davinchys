from django.contrib import admin
#
from .models import Transformer, Inventario

class TransformerAdmin(admin.ModelAdmin):
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

class IventarioAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'date',
        'name',
        'unit',
        'status',
        'location',
    )
    list_filter = ('code', 'status','location',)


admin.site.register(Transformer, TransformerAdmin)
admin.site.register(Inventario, IventarioAdmin)