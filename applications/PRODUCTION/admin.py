from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Trafos,
)

## ==================== CATALOGO TRANSFORMADORES =====================
class TrafosResource(resources.ModelResource):
    class Meta:
        model = Trafos

@admin.register(Trafos)
class TrafosAdmin(ImportExportModelAdmin):
    resource_class = TrafosResource

    list_display = (
        'id',
        'KVA',
        'idSupplier',
        'HV',
        'LV'

    )
    search_fields = ('idSupplier',)
    list_filter = ('idSupplier',)
    #autocomplete_fields = ['idPetitioner',]
