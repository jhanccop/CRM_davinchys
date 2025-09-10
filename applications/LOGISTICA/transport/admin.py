from django.contrib import admin


from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Container,
)

## ==================== Invoice DE ORDENES DE COMPRA ======================
class ContainerResource(resources.ModelResource):
    class Meta:
        model = Container

@admin.register(Container)
class ContainerAdmin(ImportExportModelAdmin):
    resource_class = ContainerResource

    #def get_idSupplier_numberIdClient(self, obj):
    #    if obj.idSupplier:
    #        return obj.idSupplier.numberIdSupplier
    #    return None
    
    list_display = (
        'id',
        'created',
        'idQuote',
        'idRequirement',
        'containerName',
        'shortDescription',
    )
    
    search_fields = ("id",'idQuote',)
    list_filter = ('idQuote','idRequirement')
    autocomplete_fields = ['idQuote',]
