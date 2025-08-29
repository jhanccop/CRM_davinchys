from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import supplier, client, clientContact, supplierContact

## ==================== CONTACT SUPPLIER =====================
class supplierContactResource(resources.ModelResource):
    class Meta:
        model = supplierContact

@admin.register(supplierContact)
class supplierContactAdmin(ImportExportModelAdmin):
    resource_class = supplierContactResource
    list_display = (
        'name',
        'last_name',
        'email',
        'phoneNumber',
        'supplier_contact'
    )
    search_fields = ('supplier_contact',)

## ==================== SUPPLIER =====================
class supplierResource(resources.ModelResource):
    class Meta:
        model = supplier

@admin.register(supplier)
class supplierAdmin(ImportExportModelAdmin):
    resource_class = supplierResource
    list_display = (
        'id',
        'tradeName',
        'numberIdSupplier',
        'typeDocument',
        'location',
        'country',
        'brandName'
    )
    search_fields = ('tradeName','numberIdSupplier',)

## ==================== CONTACT CLIENT =====================
class clientContactResource(resources.ModelResource):
    class Meta:
        model = clientContact

@admin.register(clientContact)
class clientContactAdmin(ImportExportModelAdmin):
    resource_class = clientContactResource
    list_display = (
        'name',
        'last_name',
        'email',
        'phoneNumber'
    )
    #search_fields = ('tradeName','numberIdSupplier',)

## ==================== CLIENT =====================
class clientResource(resources.ModelResource):
    class Meta:
        model = client

@admin.register(client)
class clientAdmin(ImportExportModelAdmin):
    resource_class = clientResource
    list_display = (
        'id',
        'tradeName',
        'numberIdClient',
        'typeDocument',
        'location',
        'country',
        'brandName'
    )
    search_fields = ('tradeName','numberIdClient',)
