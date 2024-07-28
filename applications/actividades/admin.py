from django.contrib import admin

from .models import Commissions, Projects, DailyTasks, TrafoQuote, Trafos

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
        'type',
        'startTime',
        'endTime',
    )
    search_fields = ('type',)
    list_filter = ('type',)

class TrafoQuoteAdmin(admin.ModelAdmin):
    list_display = (
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

admin.site.register(TrafoQuote, TrafoQuoteAdmin)
admin.site.register(Trafos, TrafosAdmin)
