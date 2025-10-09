from django.db import models
from datetime import timedelta, datetime, time
from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone

class RegistroAsistenciaManager0(models.Manager):
    def ObtenerAssitenciaPorRangoCompaniaTipo(self, idCompany, intervalo, TypeKword):
        """
        Lista de asistencia por rango - compañia - tipo
        """
        Intervals = intervalo.split(' to ')
        intervals = [datetime.strptime(dt, "%Y-%m-%d") for dt in Intervals]

        # Creacion de rango de fechas
        rangeDate = [intervals[0] - timedelta(days=1), None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days=1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days=1)

        if TypeKword == "-1" or TypeKword == "":
            return self.filter(
                created__range=rangeDate,
                empleado__user__company__id=idCompany,
            )
        else:
            return self.filter(
                created__range=rangeDate,
                empleado__user__company__id=idCompany,
                jornada=TypeKword
            )
    
    def en_periodo(self, fecha_inicio, fecha_fin):
        return self.filter(fecha__range=[fecha_inicio, fecha_fin])
    
    def metricas_asistencia(self, fecha_inicio, fecha_fin):
        return self.en_periodo(fecha_inicio, fecha_fin).aggregate(
            total_registros=Count('id'),
            total_horas_extra1=Sum('horas', filter=Q(jornada='1')),
            total_horas_extra2=Sum('horas', filter=Q(jornada='2'))
        )

class LocalManager(models.Manager):
    def obtenerLocalPorCompañia(self, idCompany):
        """
        Lista de locales compañia
        """
        
        return self.filter(
            idCompany = idCompany,
        )

class RegistroAsistenciaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('empleado', 'aprobado_por')
    
    def filtrar_por_fecha(self, fecha_inicio, fecha_fin):
        """
        Filtra registros por rango de fechas
        """
        queryset = self.get_queryset()
        
        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            queryset = queryset.filter(fecha__gte=fecha_inicio)
        elif fecha_fin:
            queryset = queryset.filter(fecha__lte=fecha_fin)
            
        return queryset
    
    def por_empleado(self, empleado_id):
        """Filtra por empleado específico"""
        return self.get_queryset().filter(empleado_id=empleado_id)
    
    def por_estado(self, estado):
        """Filtra por estado"""
        return self.get_queryset().filter(estado=estado)
    
    # ================ MY ESPACE ================
    def asistencia_por_empleado_periodo(self, empleado_id, fecha_inicio, fecha_fin):
        """Obtiene asistencia de un empleado en un periodo específico"""
        return self.filter(
            empleado_id=empleado_id,
            fecha__range=[fecha_inicio, fecha_fin]
        )
    
    def tiene_asistencia_hoy(self, empleado_id):
        """Verifica si el empleado ya registró asistencia hoy"""
        hoy = timezone.now().date()
        return self.filter(
            empleado_id=empleado_id,
            fecha=hoy
        ).exists()
    
    def tiene_horas_extra_hoy(self, empleado_id):
        """Verifica si el empleado ya registró horas extra hoy"""
        hoy = timezone.now().date()
        return self.filter(
            empleado_id=empleado_id,
            fecha=hoy,
            jornada__in=['1', '2']  # HEXTRA1 y HEXTRA2
        ).exists()

class DashboardManager(models.Manager):
    def en_periodo(self, fecha_inicio, fecha_fin):
        return self.filter(fecha__range=[fecha_inicio, fecha_fin])
    
    def metricas_asistencia(self, fecha_inicio, fecha_fin):
        return self.en_periodo(fecha_inicio, fecha_fin).aggregate(
            total_registros=Count('id'),
            horas_extra1=Count('id', filter=Q(jornada='1')),
            horas_extra2=Count('id', filter=Q(jornada='2'))
        )
    
class EmpleadoManager(models.Manager):
    def activos(self):
        return self.filter(activo=True)
    
    def por_departamento(self, departamento_id):
        return self.filter(departamento_id=departamento_id, activo=True)
    
    def metricas_dashboard(self):
        return self.filter(activo=True).aggregate(
            total=Count('id'),
            con_contrato=Count('id', filter=Q(tipo_contrato__isnull=False)),
            promedio_salario=Avg('salario_base')
        )

class PermisoManager(models.Manager):
    def permisos_por_estado(self):
        """Agrupa permisos por estado"""
        return self.values('estado').annotate(
            total=Count('id')
        ).order_by('estado')
    
    def permisos_ultimo_mes(self):
        """Permisos del último mes"""
        inicio_mes = timezone.now().date().replace(day=1)
        return self.filter(fecha_solicitud__gte=inicio_mes)
    
    # ================ MY ESPACE ================
    def por_empleado(self, empleado_id):
        """Obtiene todos los permisos de un empleado"""
        return self.filter(empleado_id=empleado_id)
    
    def contadores_estado_empleado(self, empleado_id):
        """Obtiene contadores de permisos por estado para un empleado"""
        return self.filter(empleado_id=empleado_id).aggregate(
            total=Count('id'),
            pendientes=Count('id', filter=Q(estado='0')),
            aprobados=Count('id', filter=Q(estado='1')),
            rechazados=Count('id', filter=Q(estado='2'))
        )

class DocumentoManager(models.Manager):
    def ObtenerDocumentoPorRangoCompaniaTipo(self, idCompany, intervalo, TypeKword):
        """
        Lista de documentos por rango - compañia - tipo
        """
        Intervals = intervalo.split(' to ')
        intervals = [datetime.strptime(dt, "%Y-%m-%d") for dt in Intervals]

        # Creacion de rango de fechas
        rangeDate = [intervals[0] - timedelta(days=1), None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days=1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days=1)

        if TypeKword == "-1" or TypeKword == "":
            return self.filter(
                created__range=rangeDate,
                empleado__user__company__id=idCompany,
            )
        else:
            return self.filter(
                created__range=rangeDate,
                empleado__user__company__id=idCompany,
                tipo=TypeKword
            )
    
    def documentos_completos_empleado(self, empleado_id):
        tipos = ['0', '1', '2', '3', '4']  # Boleta, Contrato, CV, Identificación, Certificación
        return {
            tipo: self.filter(empleado_id=empleado_id, tipo=tipo).exists()
            for tipo in tipos
        }
    
    def porcentaje_completado(self, empleado_id):
        tipos_requeridos = ['0', '1', '2']  # Boleta, Contrato, CV como requeridos
        documentos = self.filter(empleado_id=empleado_id, tipo__in=tipos_requeridos)
        tipos_presentes = documentos.values_list('tipo', flat=True).distinct()
        return (len(tipos_presentes) / len(tipos_requeridos)) * 100 if tipos_requeridos else 0
    
# ================ MIS DOCUMENTOS ================
    def ObtenerDocumentoPorUserTipo(self, idUser, TypeKword):
        """
        Lista de documentos ususario y- tipo
        """
        if TypeKword == "-1" or TypeKword == "":
            return self.filter(
                empleado__user__id=idUser,
            )
        else:
            return self.filter(
                empleado__user__id=idUser,
                tipo=TypeKword
            )