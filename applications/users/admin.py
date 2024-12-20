from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import User, Documentations

## ==================== user =====================
class UserResource(resources.ModelResource):
    class Meta:
        model = User

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = (
        'id',
        'full_name',
        'last_name',
        'position',
        'condition'
    )
    list_filter = ('position',)

## ==================== user =====================
class DocumentationsResource(resources.ModelResource):
    class Meta:
        model = Documentations

@admin.register(Documentations)
class DocumentationsAdmin(ImportExportModelAdmin):
    resource_class = DocumentationsResource
    list_display = (
        'idUser',
        'typeDoc',
        'sumary',
    )
    list_filter = ('typeDoc',)