from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
  ExpenseSubCategories,
  IncomeSubCategories,
  BankMovements,
  DocumentsUploaded,
  Conciliation,
)


## ==================== ExpenseSubCategories =====================
class ExpenseSubCategoriesResource(resources.ModelResource):
    class Meta:
        model = ExpenseSubCategories

@admin.register(ExpenseSubCategories)
class ExpenseSubCategoriesAdmin(ImportExportModelAdmin):
    resource_class = ExpenseSubCategoriesResource
    list_display = (
        'id',
        'nameSubCategoy',
        'category',
    )
    search_fields = ('category',)

## ==================== IncomeSubCategories =====================
class IncomeSubCategoriesResource(resources.ModelResource):
    class Meta:
        model = IncomeSubCategories

@admin.register(IncomeSubCategories)
class IncomeSubCategoriesAdmin(ImportExportModelAdmin):
    resource_class = IncomeSubCategoriesResource
    list_display = (
        'id',
        'nameSubCategoy',
    )
    search_fields = ('nameSubCategoy',)

## ==================== BankMovements =====================
class BankMovementsResource(resources.ModelResource):
    class Meta:
        model = BankMovements

@admin.register(BankMovements)
class BankMovementsAdmin(ImportExportModelAdmin):
    resource_class = BankMovementsResource
    list_display = (
        'id',
        'idAccount',
        'date',
        #'get_docs',
        'description',
        'transactionType',
        #'expenseSubCategory',
        #'incomeSubCategory',
        'amount',
        'balance',
        'amountReconcilied',
        'opNumber',
    )
    #def get_docs(self, obj):
    #    return "\n".join([str(p) for p in obj.idDocs.all()])

    search_fields = ("id",'opNumber','date')
    list_filter = ('transactionType','idAccount')
    autocomplete_fields = ['originDestination']


## ==================== DocumentsUploaded =====================
class DocumentsUploadedResource(resources.ModelResource):
    class Meta:
        model = DocumentsUploaded

@admin.register(DocumentsUploaded)
class DocumentsUploadedAdmin(ImportExportModelAdmin):
    resource_class = DocumentsUploadedResource
    list_display = (
        'id',
        'created',
        'idAccount',
        'fileName',
    )
    search_fields = ('status',)
    list_filter = ('idAccount',)

## ==================== Conciliation =====================
class ConciliationResource(resources.ModelResource):
    class Meta:
        model = Conciliation

@admin.register(Conciliation)
class ConciliationAdmin(ImportExportModelAdmin):
    resource_class = ConciliationResource
    
    list_display = (
        'id',
        'amountReconcilied',
        'equivalentAmount',
        'status',
        'type',
        'idMovOrigin',
        'idMovArrival',
        'idDoc',
    )
    
    search_fields = (
        "id",
        'status',
        'type',
        'idDoc__idInvoice'
    )
    list_filter = ('status','type')
    autocomplete_fields = ['idMovOrigin','idDoc','idMovArrival']

admin.site.site_header = "Administrador Davinchys"
admin.site.site_title = "Administrador Davinchys"
admin.site.index_title = "Bienvenido al Panel de Administración"