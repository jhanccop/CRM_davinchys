from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
  FinancialDocuments,
  OthersDocuments,
  RawsFilesRHE
)

## ==================== MASIVO RawsFilesRHE =====================
class RawsFilesRHEResource(resources.ModelResource):
    class Meta:
        model = RawsFilesRHE

@admin.register(RawsFilesRHE)
class RawsFilesRHEAdmin(ImportExportModelAdmin):
    resource_class = RawsFilesRHEResource

    def get_client_ruc(self, obj):
        if obj.idClient:
            return obj.idClient.ruc
        return None
    
    list_display = (
        'id',
        'created',
        'archivo',
        'status',
    )
    
    search_fields = ("id",'created',)
    list_filter = ('created',)
    #autocomplete_fields = ['idClient',]

## ==================== FinancialDocuments =====================
class FinancialDocumentsResource(resources.ModelResource):
    class Meta:
        model = FinancialDocuments

@admin.register(FinancialDocuments)
class FinancialDocumentsAdmin(ImportExportModelAdmin):
    resource_class = FinancialDocumentsResource

    def get_client_ruc(self, obj):
        if obj.idClient:
            return obj.idClient.numberIdClient
        return None
    
    def get_supplier_ruc(self, obj):
        if obj.idSupplier:
            return obj.idSupplier.numberIdSupplier
        return None
    
    list_display = (
        'id',
        'date',
        'get_client_ruc',
        'get_supplier_ruc',
        'typeInvoice',
        'idInvoice',
        'typeCurrency',
        'expenseFlag',
        'amount',
        'amountReconcilied',
        'description',
    )
    
    search_fields = ("id",'idInvoice','expenseFlag')
    list_filter = ('idInvoice','expenseFlag')
    autocomplete_fields = ['idClient','idSupplier']

## ==================== OthersDocuments =====================
class OthersDocumentsResource(resources.ModelResource):
    class Meta:
        model = OthersDocuments

@admin.register(OthersDocuments)
class OthersDocumentsAdmin(ImportExportModelAdmin):
    resource_class = OthersDocumentsResource
    list_display = (
        'id',
        'date',
        'idFinacialDocuments',
        'description',
        'idOtherDocument'
    )
    
    search_fields = ('idFinacialDocuments',)
    list_filter = ('idFinacialDocuments',)