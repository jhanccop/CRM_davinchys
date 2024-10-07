from django.contrib import admin

from .models import (
  Transactions,
  InternalTransfers,
  BankMovements,
  Documents,
  DocumentsUploaded,
  Conciliation
)

class TransactionsAdmin(admin.ModelAdmin):
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

class InternalTransfersAdmin(admin.ModelAdmin):
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

class BankMovementsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'idAccount',
        'date',
        'get_docs',
        'description',
        'transactionType',
        'amount',
        'balance',
        'amountReconcilied',
        'opNumber',
    )
    def get_docs(self, obj):
        return "\n".join([str(p) for p in obj.idDocs.all()])

    search_fields = ('transactionType','idAccount')
    list_filter = ('transactionType','idAccount')

class DocumentsAdmin(admin.ModelAdmin):
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

class ConciliationAdmin(admin.ModelAdmin):
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

class DocumentsUploadedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'idAccount',
        'fileName',
    )
    list_filter = ('idAccount',)

admin.site.register(Documents, DocumentsAdmin)
admin.site.register(BankMovements, BankMovementsAdmin)
admin.site.register(DocumentsUploaded, DocumentsUploadedAdmin)


admin.site.register(Transactions, TransactionsAdmin)
admin.site.register(InternalTransfers, InternalTransfersAdmin)
admin.site.register(Conciliation, ConciliationAdmin)