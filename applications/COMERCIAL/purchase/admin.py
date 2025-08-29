from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    PurchaseOrderInvoice,
    requirements,
    RequestTracking,
    requirementItems,
    requirementsQuotes,
    PettyCash,
    PettyCashItems,
)
## ==================== Invoice DE ORDENES DE COMPRA ======================
class PurchaseOrderInvoiceResource(resources.ModelResource):
    class Meta:
        model = PurchaseOrderInvoice

@admin.register(PurchaseOrderInvoice)
class PurchaseOrderInvoiceAdmin(ImportExportModelAdmin):
    resource_class = PurchaseOrderInvoiceResource

    def get_idSupplier_numberIdClient(self, obj):
        if obj.idSupplier:
            return obj.idSupplier.numberIdSupplier
        return None
    
    list_display = (
        'id',
        'date',
        'idRequirement',
        'get_idSupplier_numberIdClient',
        'typeInvoice',
        'idInvoice',
        'typeCurrency',
        'amount',
        'amountReconcilied',
        'description',
    )
    
    search_fields = ("id",'idInvoice',)
    list_filter = ('idInvoice','idSupplier')
    autocomplete_fields = ['idSupplier',]

## ==================== requirements =====================
class requirementsResource(resources.ModelResource):
    class Meta:
        model = requirements

@admin.register(requirements)
class requirementsAdmin(ImportExportModelAdmin):
    resource_class = requirementsResource

    list_display = (
        'id',
        'created',
        'idPetitioner',
        'description',
        'totalPrice',
        'isPurchaseOrder'
    )
    search_fields = ('idPetitioner',)
    list_filter = ('idPetitioner',)
    #autocomplete_fields = ['idPetitioner',]

## ==================== RequestTracking =====================
class RequestTrackingResource(resources.ModelResource):
    class Meta:
        model = RequestTracking

@admin.register(RequestTracking)
class RequestTrackingAdmin(ImportExportModelAdmin):
    resource_class = RequestTrackingResource

    list_display = (
        'id',
        'idRequirement',
        'status',
        'area'
    )
    search_fields = ('idRequirement',)
    list_filter = ('status',)
    autocomplete_fields = ['idRequirement',]

## ==================== requirementItems =====================
class requirementItemsResource(resources.ModelResource):
    class Meta:
        model = requirementItems

@admin.register(requirementItems)
class requirementItemsAdmin(ImportExportModelAdmin):
    resource_class = requirementItemsResource

    list_display = (
        'id',
        'idRequirement',
        'product',
        'quantity',
        'price',
    )
    search_fields = ('idRequirement',)
    list_filter = ('idRequirement',)
    autocomplete_fields = ['idRequirement',]

## ==================== CAJA CHICA =====================
class PettyCashResource(resources.ModelResource):
    class Meta:
        model = PettyCash

@admin.register(PettyCash)
class PettyCashAdmin(ImportExportModelAdmin):
    resource_class = PettyCashResource

    list_display = (
        'id',
        'created',
        'idPetitioner',
        'description',
        'currency',
        'totalPrice'
    )
    search_fields = ('idPetitioner',)
    list_filter = ('idPetitioner',)
    #autocomplete_fields = ['idPetitioner',]

## ==================== CAJA CHICA Items =====================
class PettyCashItemsResource(resources.ModelResource):
    class Meta:
        model = PettyCashItems

@admin.register(PettyCashItems)
class PettyCashItemsAdmin(ImportExportModelAdmin):
    resource_class = PettyCashItems

    list_display = (
        'id',
        'idPettyCash',
        'product',
        'quantity',
        'price',
    )
    #search_fields = ('idPettyCash',)
    list_filter = ('idPettyCash',)
    autocomplete_fields = ['idPettyCash',]

## ==================== requirementsQuotes =====================
class requirementsQuotesResource(resources.ModelResource):
    class Meta:
        model = requirementsQuotes

@admin.register(requirementsQuotes)
class requirementsQuotesAdmin(ImportExportModelAdmin):
    resource_class = requirementsQuotesResource

    list_display = (
        'id',
        'idRequirement',
        'idSupplier',
    )
    search_fields = ('idRequirement',)
    list_filter = ('idRequirement',)