from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import  Incomes

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
