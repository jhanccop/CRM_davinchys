from django.contrib import admin

from .models import Workers

class WorkersAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'last_name',
        'email',
        'phoneNumber',
        'area',
        'gender',
        'condition',
        'date_entry',
    )
    search_fields = ('idClient',) #search_fields = ('idClient__businessName',)

admin.site.register(Workers, WorkersAdmin)