from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Workers

## ==================== Transformer =====================
class WorkersResource(resources.ModelResource):
    class Meta:
        model = Workers

@admin.register(Workers)
class WorkersAdmin(ImportExportModelAdmin):
    resource_class = WorkersResource
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
    search_fields = ('idClient',)