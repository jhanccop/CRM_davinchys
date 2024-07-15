from django.contrib import admin

from .models import Commissions, Projects, DailyTasks

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
    autocomplete_fields = ['workers']

class ProjectsAdmin(admin.ModelAdmin):

    list_display = (
        'projectName',
        'startDate',
        'endDate',
        'status',
    )
    search_fields = ('projectName','status',)
    list_filter = ('status',)
    autocomplete_fields = ['workers']

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

admin.site.register(Commissions, CommissionsAdmin)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(DailyTasks, DailyTasksAdmin)
