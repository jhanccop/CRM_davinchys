from django.contrib import admin


from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Container,
    ContainerTracking
)

## ==================== Container =====================
class ContainerResource(resources.ModelResource):
    class Meta:
        model = Container

@admin.register(Container)
class ContainerAdmin(ImportExportModelAdmin):
    resource_class = ContainerResource
    
    list_display = (
        'id',
        'created',
        'netAmount',
        'isOrder',
        'idPetitioner',
    )
    
    search_fields = ("isOrder",)
    list_filter = ('isOrder',)

## ==================== ContainerTracking =====================
class ContainerTrackingResource(resources.ModelResource):
    class Meta:
        model = ContainerTracking

@admin.register(ContainerTracking)
class ContainerTrackingAdmin(ImportExportModelAdmin):
    resource_class = ContainerTrackingResource
    
    list_display = (
        'id',
        'created',
        'idContainer',
        'area',
        'status',
    )
    
    search_fields = ("idContainer",)
    list_filter = ('idContainer',)

