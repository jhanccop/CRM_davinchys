from django.contrib import admin

from .models import (

  RequestTracking,
  PaymentRequest,
  RequestList
)

class RequestListAdmin(admin.ModelAdmin):
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

class PaymentRequestAdmin(admin.ModelAdmin):
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

class RequestTrackingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'idOrder',
        'dateChange',
        'amountAssigned',
        'orderState',
    )
    search_fields = ('orderState',)

admin.site.register(RequestList, RequestListAdmin)
admin.site.register(PaymentRequest, PaymentRequestAdmin)
admin.site.register(RequestTracking, RequestTrackingAdmin)