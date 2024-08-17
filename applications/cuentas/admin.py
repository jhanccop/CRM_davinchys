from django.contrib import admin
#
from .models import Account,ManualAccount,Tin

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

class TinAdmin(admin.ModelAdmin):
    list_display = (
        'tin',
        'tinName'
    )
    search_fields = ('tin',)
    list_filter = ('tin',)

class ManualAccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'idAcount',
        'realBalance',
    )
    list_filter = ('idAcount',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Tin, TinAdmin)
admin.site.register(ManualAccount, ManualAccountAdmin)
