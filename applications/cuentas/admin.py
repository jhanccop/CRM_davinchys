from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
#
from .models import Account,ManualAccount,Tin

## ==================== Account =====================
class AccountResource(resources.ModelResource):
    class Meta:
        model = Account

@admin.register(Account)
class AccountAdmin(ImportExportModelAdmin):
    resource_class = AccountResource
    list_display = (
        'id',
        'accountName',
        'accountNumber',
        'nickName',
        'initialAccount',
        'currency',
        'state'
    )
    search_fields = ('nickName','state',)
    list_filter = ('nickName',)

## ==================== Tin =====================
class TinResource(resources.ModelResource):
    class Meta:
        model = Tin

@admin.register(Tin)
class TinAdmin(ImportExportModelAdmin):
    resource_class = TinResource
    list_display = (
        'id',
        'tin',
        'tinName'
    )
    search_fields = ('tin',)
    list_filter = ('tin',)
