from django.contrib import admin

from .models import (
  Transactions,
  InternalTransfers,
  BankMovements,
  BankReconciliation,
  DocumentsUploaded
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
        'description',
        'transactionType',
        'amount',
        'balance',
        'amountReconcilied',
        'opNumber',
    )
    search_fields = ('transactionType','idAccount')
    list_filter = ('transactionType','idAccount')

class BankReconciliationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'get_BankMovements',
        'idClient',
        'typeInvoice',
        'idInvoice',
        'description',
    )
    def get_BankMovements(self, obj):
        return "\n".join([str(p) for p in obj.idBankMovements.all()])
    
    search_fields = ('idBankMovements','idClient')
    list_filter = ('idBankMovements','idClient')

class DocumentsUploadedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'idAccount',
        'fileName',
    )
    list_filter = ('idAccount',)

admin.site.register(BankReconciliation, BankReconciliationAdmin)
admin.site.register(BankMovements, BankMovementsAdmin)
admin.site.register(DocumentsUploaded, DocumentsUploadedAdmin)


admin.site.register(Transactions, TransactionsAdmin)
admin.site.register(InternalTransfers, InternalTransfersAdmin)