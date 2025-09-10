from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Incomes,
    quotes,
    Trafos,
    QuoteTracking
)

## ==================== ExpensesDocuments =====================
class IncomesResource(resources.ModelResource):
    class Meta:
        model = Incomes

@admin.register(Incomes)
class IncomesAdmin(ImportExportModelAdmin):
    resource_class = IncomesResource

    def get_client_ruc(self, obj):
        if obj.idClient:
            return obj.idClient.ruc
        return None
    
    list_display = (
        'id',
        'date',
        'get_client_ruc',
        'typeInvoice',
        'idInvoice',
        'typeCurrency',
        'amount',
        'amountReconcilied',
        'description',
    )
    
    search_fields = ("id",'idInvoice',)
    list_filter = ('idInvoice','idClient')
    autocomplete_fields = ['idClient',]


## ==================== QUOTES =====================
class quotesResource(resources.ModelResource):
    class Meta:
        model = quotes

@admin.register(quotes)
class quotesAdmin(ImportExportModelAdmin):
    resource_class = quotesResource

    list_display = (
        'id',
        'created',
        'idClient',
        'amount',
        'deadline',
        'isPO'
    )
    search_fields = ('idClient',)
    list_filter = ('idClient',)
    #autocomplete_fields = ['idPetitioner',]

## ==================== TRANSFORMADORES =====================
class TrafosResource(resources.ModelResource):
    class Meta:
        model = Trafos

@admin.register(Trafos)
class TrafosAdmin(ImportExportModelAdmin):
    resource_class = TrafosResource

    list_display = (
        'id',
        'idTrafoQuote',
        'KVA',
        'HVTAP',
        'serialNumber',
        'quantity',
        'unitCost',
    )
    search_fields = ('idTrafoQuote',)
    list_filter = ('idTrafoQuote',)
    #autocomplete_fields = ['idPetitioner',]

## ==================== TRACKING QUOTES =====================
class QuoteTrackingResource(resources.ModelResource):
    class Meta:
        model = QuoteTracking

@admin.register(QuoteTracking)
class QuoteTrackingAdmin(ImportExportModelAdmin):
    resource_class = QuoteTrackingResource

    list_display = (
        'id',
        'created',
        'idquote',
        'area',
        'status',
    )
    search_fields = ('idquote',)
    list_filter = ('idquote',)
    #autocomplete_fields = ['idPetitioner',]

