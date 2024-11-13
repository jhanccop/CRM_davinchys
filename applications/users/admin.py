from django.contrib import admin

from .models import User, Documentations

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'last_name',
        'position',
        'condition'
    )
    list_filter = ('position',)

class DocumentationsAdmin(admin.ModelAdmin):
    list_display = (
        'idUser',
        'typeDoc',
        'sumary',
    )
    list_filter = ('typeDoc',)

admin.site.register(User, UserAdmin)
admin.site.register(Documentations, DocumentationsAdmin)
