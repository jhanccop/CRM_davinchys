from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Commissions, Projects, DailyTasks, TrafoQuote, Trafos, TrafoTask, SuggestionBox

## ==================== Commissions =====================
class CommissionsResource(resources.ModelResource):
    class Meta:
        model = Commissions

@admin.register(Commissions)
class CommissionsAdmin(ImportExportModelAdmin):
    resource_class = CommissionsResource
    list_display = (
        'commissionName',
        'startDate',
        'endDate',
        'place',
        'status',
    )
    search_fields = ('commissionName','status',)
    list_filter = ('status',)

## ==================== Projects =====================
class ProjectsResource(resources.ModelResource):
    class Meta:
        model = Projects

@admin.register(Projects)
class ProjectsAdmin(ImportExportModelAdmin):
    resource_class = ProjectsResource
    list_display = (
        'projectName',
        'startDate',
        'endDate',
        'status',
    )
    search_fields = ('projectName','status',)
    list_filter = ('status',)

## ==================== DailyTasks =====================
class DailyTasksResource(resources.ModelResource):
    class Meta:
        model = DailyTasks

@admin.register(DailyTasks)
class DailyTasksAdmin(ImportExportModelAdmin):
    resource_class = DailyTasksResource
    list_display = (
        'user',
        'date',
        'activity',
        'is_overTime',
        'startTime',
        'endTime',
    )
    search_fields = ('is_overTime',)
    list_filter = ('is_overTime',)

## ==================== SuggestionBox =====================
class SuggestionBoxResource(resources.ModelResource):
    class Meta:
        model = SuggestionBox

@admin.register(SuggestionBox)
class SuggestionBoxAdmin(ImportExportModelAdmin):
    resource_class = SuggestionBoxResource
    list_display = (
        'user',
        'created',
        'area',
        'suggestion'
    )
    search_fields = ('area',)
    list_filter = ('area',)

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
        'userClient',
        'dateOrder',
        'deadline',
        'idAttendant',
        'poStatus'
    )
    search_fields = ('idQuote',)
    list_filter = ('poStatus','idAttendant')

## ==================== TrafoTask =====================
class TrafoTaskResource(resources.ModelResource):
    class Meta:
        model = TrafoTask

@admin.register(TrafoTask)
class TrafoTaskAdmin(ImportExportModelAdmin):
    resource_class =TrafoTaskResource
    list_display = (
        'idTrafoQuote',
        'nameTask',
        'start_date',
        'end_date',
        'progress',
        #'dependence',
        'is_milestone',
    )
    search_fields = ('nameTask',)
    list_filter = ('nameTask','idTrafoQuote')

## ==================== Trafos =====================
class TrafosResource(resources.ModelResource):
    class Meta:
        model = Trafos

@admin.register(Trafos)
class TrafosAdmin(ImportExportModelAdmin):
    resource_class = TrafosResource
    list_display = (
        'id',
        'idQuote',
        'provider',
        'KVA',
        'LV',
        'TYPE',
        'MOUNTING',
        'COOLING'
    )
    search_fields = ('MOUNTING',)
    list_filter = ('idQuote','provider')