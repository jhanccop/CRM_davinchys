from django.contrib import admin

from .models import (

  RequestTracking,
  PaymentRequest
)

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


admin.site.register(PaymentRequest, PaymentRequestAdmin)
admin.site.register(RequestTracking, RequestTrackingAdmin)