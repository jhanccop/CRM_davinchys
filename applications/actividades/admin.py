from django.contrib import admin

from .models import Commissions, Projects, DailyTasks, TrafoQuote, Trafos, TrafoTask, SuggestionBox

class CommissionsAdmin(admin.ModelAdmin):
    list_display = (
        'commissionName',
        'startDate',
        'endDate',
        'place',
        'status',
    )
    search_fields = ('commissionName','status',)
    list_filter = ('status',)

class ProjectsAdmin(admin.ModelAdmin):
    list_display = (
        'projectName',
        'startDate',
        'endDate',
        'status',
    )
    search_fields = ('projectName','status',)
    list_filter = ('status',)

class DailyTasksAdmin(admin.ModelAdmin):
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

class SuggestionBoxAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'created',
        'area',
        'suggestion'
    )
    search_fields = ('area',)
    list_filter = ('area',)

class TrafoQuoteAdmin(admin.ModelAdmin):
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

class TrafoTasksAdmin(admin.ModelAdmin):
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

class TrafosAdmin(admin.ModelAdmin):
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

admin.site.register(Commissions, CommissionsAdmin)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(DailyTasks, DailyTasksAdmin)
admin.site.register(SuggestionBox, SuggestionBoxAdmin)

admin.site.register(TrafoQuote, TrafoQuoteAdmin)
admin.site.register(Trafos, TrafosAdmin)
admin.site.register(TrafoTask, TrafoTasksAdmin)