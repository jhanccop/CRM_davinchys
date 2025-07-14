from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import  TrafoQuote, Trafos, QuoteTraking

## ==================== Quote traking =====================
class QuoteTrakingResource(resources.ModelResource):
    class Meta:
        model = QuoteTraking

@admin.register(QuoteTraking)
class QuoteTrakingAdmin(ImportExportModelAdmin):
    resource_class = QuoteTrakingResource
    list_display = (
        'id',
        'idTrafoQuote',
        'event',
    )
    search_fields = ('idTrafoQuote',)
    list_filter = ('idTrafoQuote','event')

## ==================== TrafoQuote =====================
class TrafoQuoteResource(resources.ModelResource):
    class Meta:
        model = TrafoQuote

@admin.register(TrafoQuote)
class TrafoQuoteAdmin(ImportExportModelAdmin):
    resource_class = TrafoQuoteResource
    list_display = (
        'id',
        'idQuote',
        'idClient',
        'dateOrder',
        'deadline',
        'idAttendant',
        'poStatus'
    )
    search_fields = ('idQuote',)
    list_filter = ('poStatus','idAttendant')

## ==================== Trafos =====================
class TrafosResource(resources.ModelResource):
    class Meta:
        model = Trafos

@admin.register(Trafos)
class TrafosAdmin(ImportExportModelAdmin):
    resource_class = TrafosResource
    list_display = (
        'id',
        'idTrafoQuote',
        'KVA',
        'LV',
        'TYPE',
        'MOUNTING',
        'COOLING'
    )
    search_fields = ('MOUNTING',)
    list_filter = ('idTrafoQuote',)