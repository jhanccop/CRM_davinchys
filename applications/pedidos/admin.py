from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
  RequestTracking,
  PaymentRequest,
  RequestList
)

## ==================== RequestTracking =====================
class RequestTrackingResource(resources.ModelResource):
    class Meta:
        model = RequestTracking

@admin.register(RequestTracking)
class RequestTrackingAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'idOrder',
        'dateChange',
        'amountAssigned',
        'orderState',
    )
    search_fields = ('orderState',)

## ==================== PaymentRequest =====================
class PaymentRequestResource(resources.ModelResource):
    class Meta:
        model = PaymentRequest

@admin.register(PaymentRequest)
class PaymentRequestAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'idPetitioner',
        'idProvider',
        'requirementName',
        'quantity',
        'amountRequested',
        'amountAssigned',
        'paymentType',
        'deadline',
    )
    search_fields = ('paymentType',)

## ==================== RequestList =====================
class RequestListResource(resources.ModelResource):
    class Meta:
        model = RequestList

@admin.register(RequestList)
class RequestListAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'created',
        'listName',
        'idPetitioner',
        'tag1',
        'tag2',
        'tag3',
        'tag4',
    )
    search_fields = ('idPetitioner',)