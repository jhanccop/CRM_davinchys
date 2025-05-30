from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
  FinancialDocuments,
  OthersDocuments,
)

## ==================== FinancialDocuments =====================
class FinancialDocumentsResource(resources.ModelResource):
    class Meta:
        model = FinancialDocuments

@admin.register(FinancialDocuments)
class FinancialDocumentsAdmin(ImportExportModelAdmin):
    resource_class = FinancialDocumentsResource

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