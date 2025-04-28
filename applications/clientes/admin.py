from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Contacto, Cliente, CuentasBancarias #, Provider

#class ClientAdmin(ImportExportMixin,admin.ModelAdmin):
#    list_display = (
#        'tradeName',
#        'ruc',
#        'phoneNumber',
#        'contact',
#        'webPage',
#        'email'
#    )
#    search_fields = ('tradeName', )
#    list_filter = ('tradeName',)

class ContactoAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'last_name',
        'email',
        'phoneNumber'
    )
    #search_fields = ('country', 'businessName', )
    list_filter = ('full_name',)

#admin.site.register(Cliente, ClientAdmin)
#
admin.site.register(Contacto, ContactoAdmin)

## ==================== Cliente =====================
class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente

@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    resource_class = ClienteResource
    list_display = (
        'id',
        'tradeName',
        'ruc',
        'phoneNumber',
        'contact',
        'webPage',
        'email'
    )
    search_fields = ('tradeName','ruc',)

## ==================== CuentasBancarias =====================
class CuentasBancariasResource(resources.ModelResource):
    class Meta:
        model = CuentasBancarias

@admin.register(CuentasBancarias)
class CuentasBancariasAdmin(ImportExportModelAdmin):
    resource_class = CuentasBancariasResource
    list_display = (
        'id',
        'idClient',
        'bankName',
        'typeAccount',
        'typeCurrency',
        'account'
    )
    autocomplete_fields = ['idClient']
    search_fields = ('idClient__ruc','idClient__tradeName','account','typeAccount')