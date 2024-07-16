from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Contacto, Cliente #, Provider

class ClientAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = (
        'tradeName',
        'ruc',
        'phoneNumber',
        'contact',
        'webPage',
        'email'
    )
    search_fields = ('tradeName', )
    list_filter = ('tradeName',)

class ContactoAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'last_name',
        'email',
        'phoneNumber'
    )
    #search_fields = ('country', 'businessName', )
    list_filter = ('full_name',)

admin.site.register(Cliente, ClientAdmin)
#
admin.site.register(Contacto, ContactoAdmin)