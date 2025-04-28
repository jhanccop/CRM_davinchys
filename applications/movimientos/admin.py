from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
  Transactions,
  InternalTransfers,
  ExpenseSubCategories,
  IncomeSubCategories,
  BankMovements,
  Documents,
  DocumentsUploaded,
  Conciliation
)

## ==================== Transactions =====================
class TransactionsResource(resources.ModelResource):
    class Meta:
        model = Transactions

@admin.register(Transactions)
class TransactionsAdmin(ImportExportModelAdmin):
    resource_class = TransactionsResource
    list_display = (
        'id',
        'dateTime',
        'category',
        'idTransaction',
        'transactionName',
        'amount',
        'currency',
        'balance',
        'idAccount'
    )
    search_fields = ('category','idAccount')
    list_filter = ('category','idAccount')

## ==================== InternalTransfers =====================
class InternalTransfersResource(resources.ModelResource):
    class Meta:
        model = InternalTransfers

@admin.register(InternalTransfers)
class InternalTransfersAdmin(ImportExportModelAdmin):
    resource_class = InternalTransfersResource
    list_display = (
        'id',
        'created_at',
        'idSourceAcount',
        'SourceAmount',
        'idDestinationAcount',
        'DestinationAmount',
        'opNumber',
    )
    search_fields = ('idSourceAcount','SourceAmount')

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
        'get_docs',
        'description',
        'transactionType',
        #'expenseSubCategory',
        #'incomeSubCategory',
        'amount',
        'balance',
        'amountReconcilied',
        'opNumber',
    )
    def get_docs(self, obj):
        return "\n".join([str(p) for p in obj.idDocs.all()])

    search_fields = ('opNumber','date')
    list_filter = ('transactionType','idAccount')
    autocomplete_fields = ['originDestination']

## ==================== Documents =====================
class DocumentsResource(resources.ModelResource):
    class Meta:
        model = Documents

@admin.register(Documents)
class DocumentsAdmin(ImportExportModelAdmin):
    resource_class = DocumentsResource
    list_display = (
        'id',
        'date',
        'idClient',
        'typeInvoice',
        'idInvoice',
        'description',
    )
    
    search_fields = ('idClient',)
    list_filter = ('idClient',)

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
        'status',
        'type',
        'idMovOrigin',
        'idMovArrival',
        'idDoc',
    )
    
    search_fields = ('idMovOrigin',)
    list_filter = ('type',)

admin.site.site_header = "Administrador Davinchys"
admin.site.site_title = "Administrador Davinchys"
admin.site.index_title = "Bienvenido al Panel de Administración"