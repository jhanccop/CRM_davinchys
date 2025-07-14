from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import supplier

## ==================== Cliente =====================
class supplierResource(resources.ModelResource):
    class Meta:
        model = supplier

@admin.register(supplier)
class supplierAdmin(ImportExportModelAdmin):
    resource_class = supplierResource
    list_display = (
        'id',
        'tradeName',
        'idSupplier',
        'typeDocument',
        'locationClient',
        'country',
        'brandName'
    )
    search_fields = ('tradeName','idSupplier',)