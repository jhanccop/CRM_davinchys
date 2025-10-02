from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *

## ==================== Departamento =====================
class DepartamentoResource(resources.ModelResource):
    class Meta:
        model = Departamento
        import_id_fields = ['id']

@admin.register(Departamento)
class EmpleadoResource(ImportExportModelAdmin):
    resource_class = DepartamentoResource
    list_display = (
        'id',
        'nombre',
        'descripcion',
        'jefe_departamento',
    )
    search_fields = ('nombre',)
    list_filter = ('nombre',)


## ==================== Empleado =====================
class EmpleadoResource(resources.ModelResource):
    class Meta:
        model = Empleado
        import_id_fields = ['id']

@admin.register(Empleado)
class EmpleadoAdmin(ImportExportModelAdmin):
    resource_class = EmpleadoResource
    list_display = (
        'id',
        'user',
        'departamento',
        'fecha_contratacion',
        'tipo_contrato',
        'salario_base',
        'activo',
    )
    search_fields = ('user__username', 'departamento__nombre')
    list_filter = ('departamento', 'tipo_contrato', 'activo')

## ==================== ContactoEmergencia =====================
class ContactoEmergenciaResource(resources.ModelResource):
    class Meta:
        model = ContactoEmergencia
        import_id_fields = ['id']

@admin.register(ContactoEmergencia)
class ContactoEmergenciaAdmin(ImportExportModelAdmin):
    resource_class = ContactoEmergenciaResource
    list_display = (
        'id',
        'empleado',
        'nombre',
        'parentesco',
        'telefono',
        'principal',
    )
    search_fields = ('empleado__user__username', 'nombre', 'parentesco', 'telefono')
    list_filter = ('parentesco', 'principal', 'empleado__departamento')

## ==================== RegistroAsistencia =====================
class RegistroAsistenciaResource(resources.ModelResource):
    class Meta:
        model = RegistroAsistencia
        import_id_fields = ['id']

@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(ImportExportModelAdmin):
    resource_class = RegistroAsistenciaResource
    list_display = (
        'id',
        'empleado',
        'fecha',
        'hora_inicio',
        'hora_final',
        'ubicacion',
        'jornada',
        'horas',
        'estado'
    )
    search_fields = ('empleado__user__username', 'ubicacion')
    list_filter = ('jornada', 'fecha', 'empleado__departamento')
    date_hierarchy = 'fecha'

## ==================== DIAS FERIADOS =====================
class FeriadosResource(resources.ModelResource):
    class Meta:
        model = Feriados
        import_id_fields = ['id']

@admin.register(Feriados)
class FeriadosAdmin(ImportExportModelAdmin):
    resource_class = FeriadosResource
    list_display = (
        'id',
        'fecha',
        'Nombre'
    )
    date_hierarchy = 'fecha'

## ==================== ActividadDiaria =====================
class ActividadDiariaResource(resources.ModelResource):
    class Meta:
        model = ActividadDiaria
        import_id_fields = ['id']

@admin.register(ActividadDiaria)
class ActividadDiariaAdmin(ImportExportModelAdmin):
    resource_class = ActividadDiariaResource
    list_display = (
        'id',
        'empleado',
        'fecha',
        'proyecto',
        'horas_trabajadas',
        'completada',
    )
    search_fields = ('empleado__user__username', 'proyecto', 'descripcion')
    list_filter = ('completada', 'fecha', 'empleado__departamento')
    date_hierarchy = 'fecha'

## ==================== Permiso =====================
class PermisoResource(resources.ModelResource):
    class Meta:
        model = Permiso
        import_id_fields = ['id']

@admin.register(Permiso)
class PermisoAdmin(ImportExportModelAdmin):
    resource_class = PermisoResource
    list_display = (
        'id',
        'empleado',
        'tipo',
        'fecha_inicio',
        'fecha_fin',
        'estado',
    )
    search_fields = ('empleado__user__username', 'tipo', 'motivo')
    list_filter = ('tipo', 'estado', 'empleado__departamento')
    date_hierarchy = 'fecha_inicio'

## ==================== Documento =====================
class DocumentoResource(resources.ModelResource):
    class Meta:
        model = Documento
        import_id_fields = ['id']

@admin.register(Documento)
class DocumentoAdmin(ImportExportModelAdmin):
    resource_class = DocumentoResource
    list_display = (
        'id',
        'empleado',
        'tipo',
        'nombre',
        'fecha_documento',
    )
    search_fields = ('empleado__user__username', 'nombre', 'tipo')
    list_filter = ('tipo', 'fecha_documento')
    date_hierarchy = 'fecha_documento'
