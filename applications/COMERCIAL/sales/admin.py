from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Incomes,
    quotes,
    QuoteTracking,
    Items,
    ItemImage,
    ItemTracking
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
        'idTinReceiving',
        'idTinExecuting',
        'amount',
        'deadline',
        'isPO'
    )
    search_fields = ('idClient',)
    list_filter = ('idClient',)
    #autocomplete_fields = ['idPetitioner',]

## ==================== ITEMS TRANSFORMADORES =====================
class ItemsResource(resources.ModelResource):
    class Meta:
        model = Items

@admin.register(Items)
class ItemsAdmin(ImportExportModelAdmin):
    resource_class = ItemsResource

    list_display = (
        'id',
        'idTrafoQuote',
        'seq',
        'PHASE',
        'COOLING',
        'MOUNTING',
        'KVA'
    )
    search_fields = ('idTrafoQuote',)
    list_filter = ('idTrafoQuote',)

## ==================== IMAGEN ITEMS TRANSFORMADORES =====================
class ItemImageResource(resources.ModelResource):
    class Meta:
        model = ItemImage

@admin.register(ItemImage)
class ItemImageAdmin(ImportExportModelAdmin):
    resource_class = ItemImageResource

    list_display = (
        'id',
        'item',
        'is_main',
        'description',
    )
    search_fields = ('item',)
    list_filter = ('item',)

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

## ==================== TRACKING ITEMS TRANSFORMADORES =====================
class ItemTrackingResource(resources.ModelResource):
    class Meta:
        model = ItemTracking

@admin.register(ItemTracking)
class ItemTrackingAdmin(ImportExportModelAdmin):
    resource_class = ItemTrackingResource

    list_display = (
        'id',
        'created',
        'idItem',
        'statusItem',
        'statusPlate',
    )
    search_fields = ('statusItem',)
    list_filter = ('statusItem',)
