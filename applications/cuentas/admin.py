from django.contrib import admin
#
from .models import Account,ManualAccount

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'accountName',
        'accountNumber',
        'nickName',
        'accountBalance',
        'currency',
        'state'
    )
    search_fields = ('nickName','state',)
    list_filter = ('nickName',)

class ManualAccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'idAcount',
        'realBalance',
    )
    list_filter = ('idAcount',)

admin.site.register(Account, AccountAdmin)
admin.site.register(ManualAccount, ManualAccountAdmin)
