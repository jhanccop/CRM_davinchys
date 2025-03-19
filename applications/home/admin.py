from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
  ContainerTracking,
)

## ==================== Transactions =====================
class ContainerTrackingResource(resources.ModelResource):
    class Meta:
        model = ContainerTracking

@admin.register(ContainerTracking)
class ContainerTrackingAdmin(ImportExportModelAdmin):
    resource_class = ContainerTrackingResource
    list_display = (
        'id',
        'trackingNumber',
        'status'
    )
    search_fields = ('status',)
    list_filter = ('trackingNumber','status')