from django.db import models, transaction
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.db.models import Q

from model_utils.models import TimeStampedModel

from django.utils import timezone
from datetime import datetime, date, time, timedelta
from django.core.exceptions import ValidationError

from .managers import (
    RegistroAsistenciaManager,
    EmpleadoManager,
    DocumentoManager,
    PermisoManager,
    LocalManager
)

from applications.cuentas.models import Tin

class Departamento(TimeStampedModel):
    # TIPO DE USUARIOS
    ADMINISTRADOR = '0'
    COMERCIAL = '1'
    FINANZAS = '2'
    PRODUCCION = '3'
    GERENCIA = '4'
    LOGISTICA = '5'
    RECURSOSHUMANOS = '6'
    CONSULTOREXTERNO = '7'
    CEOGLOBAL = '8'
    TI = '9'
    
    #
    AREA_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (COMERCIAL, 'Comercial'),
        (FINANZAS, 'Finanzas'),
        (PRODUCCION, 'Producción'),
        (GERENCIA, 'Gerencia'),
        (LOGISTICA, 'Logística'),
        (RECURSOSHUMANOS, 'Recursos humanos'),
        (CONSULTOREXTERNO, 'Consultor externo'),
        (CEOGLOBAL, 'CEO general'),
        (TI, 'TI'),
    ]

    idArea = models.CharField(
        'Area',
        max_length=1, 
        choices=AREA_CHOICES, 
        blank=True
    )

    nombre = models.CharField(max_length=100,null=True,blank=True)
    descripcion = models.TextField(blank=True)
    jefe_departamento = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='departamentos_jefe')
    
    def __str__(self):
        return self.nombre
    
class Empleado(TimeStampedModel):
    FIJO = "0"
    TEMPORAL = "1"
    PRACTICAS = "2"
    FORMACION = "3"
    TIPO_CONTRATO = [
        (FIJO, 'Contrato Fijo'),
        (TEMPORAL, 'Contrato Temporal'),
        (PRACTICAS, 'Prácticas'),
        (FORMACION, 'Formación'),
    ]

    PEN = "0"
    USD = "1"
    EUR = "2"
    TIPO_MONEDA = [
        (PEN, 'PEN'),
        (USD, 'USD'),
        (EUR, 'EUR'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='empleado')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    fecha_contratacion = models.DateField("Fecha de ingreso",blank=True)
    tipo_contrato = models.CharField("Tipo de contrato",max_length=1,choices=TIPO_CONTRATO,default=FIJO,blank=True)
    moneda = models.CharField("Moneda",max_length=1, choices=TIPO_MONEDA,default=PEN)
    salario_base = models.DecimalField("Salario",max_digits=10, decimal_places=2,blank=True)
    telefono = models.CharField("Telefono",max_length=15, blank=True)
    direccion = models.TextField("Direccion",blank=True)
    fecha_nacimiento = models.DateField("F. Nacimiento",null=True, blank=True)
    activo = models.BooleanField("Esta activo?",default=True)

    objects = EmpleadoManager()

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
    
    def __str__(self):
        return f"{self.user} - {self.departamento}"
    
class ContactoEmergencia(TimeStampedModel):
    HERMANO = "0"
    PADRES = "1"
    CONYUGE = "2"
    OTRO = "3"
    TIPO_PARENTESCO = [
        (HERMANO, 'Hermano/a'),
        (PADRES, 'Padre o madre'),
        (CONYUGE, 'Cónyuge'),
        (OTRO, 'otro'),
    ]
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='contactos_emergencia')
    nombre = models.CharField("APellidos y Nombres",max_length=150,blank=True)
    parentesco = models.CharField("Parentesco",max_length=1,choices=TIPO_PARENTESCO,blank=True)
    telefono = models.CharField("Teléfono",max_length=15,blank=True)
    email = models.EmailField("Correo",blank=True)
    direccion = models.TextField("Dirección",blank=True)
    principal = models.BooleanField("Es principal?",default=False,blank=True)
    
    class Meta:
        verbose_name = 'Contacto de emergencia'
        verbose_name_plural = "Contactos de Emergencia"
    
    def __str__(self):
        return f"{self.nombre} ({self.parentesco}) - {self.empleado}"

class Feriados(TimeStampedModel):
    fecha = models.DateField('Fecha')
    Nombre = models.CharField('Nombre feriado', max_length=25, blank=True)
    def __str__(self):
        return f"{self.fecha} - {self.Nombre}"

class Local(TimeStampedModel):
    nombreLocal = models.CharField('Nombre Local', max_length=20)
    idCompany = models.ForeignKey(Tin, on_delete=models.CASCADE)
    descripcion = models.CharField('Descripción', max_length=50, blank=True, null=True)

    objects = LocalManager() 

    def __str__(self):
        return f"{self.nombreLocal} - {self.idCompany}"

class RegistroAsistencia(TimeStampedModel):

    PENDIENTE = "0"
    APROBADO = "1"
    RECHAZADO = "2"
    PROCESADO = "3"
    TIPO_ESTADOS = [
        (PENDIENTE, 'Pendiente'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (PROCESADO, 'Procesado'),
    ]

    # JORNADA HORARIA (según hora del día)
    REGULAR = "0"
    HEXTRA1 = "1"
    HEXTRA2 = "2"
    TIPO_JORNADA_HORARIA = [
        (REGULAR, 'Reg 9:00 - 18:00'),
        (HEXTRA1, 'HE1 18:01 - 22:00'),
        (HEXTRA2, 'HE2 22:01 - 23:59 y 00:00 - 06:00'),
    ]

    # JORNADA DIARIA (según tipo de día)
    LABORABLE = "0"
    FERIADO = "1"
    FINDESEMANA = "2"
    TIPO_JORNADA_DIARIA = [
        (LABORABLE, 'Día Laborable'),
        (FERIADO, 'Feriado'),
        (FINDESEMANA, 'Fin de semana'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='registro_asistencia')
    fecha = models.DateField('Fecha')
    hora_inicio = models.TimeField('Hora inicio', null=True, blank=True)
    hora_final = models.TimeField('Hora final', null=True, blank=True)
    idLocal = models.ForeignKey(Local, on_delete=models.CASCADE, null=True, blank=True)
    ubicacion = models.CharField('Local', max_length=1, null=True, blank=True, default="0")
    
    # Campos separados para jornada horaria y diaria
    jornada_horaria = models.CharField(
        'Tipo de Jornada Horaria', 
        max_length=1, 
        choices=TIPO_JORNADA_HORARIA,
        default=REGULAR, 
        blank=True
    )
    jornada_diaria = models.CharField(
        'Tipo de Jornada Diaria', 
        max_length=1, 
        choices=TIPO_JORNADA_DIARIA,
        default=LABORABLE, 
        blank=True
    )
    
    observaciones = models.TextField('Observaciones', blank=True)

    # Campos calculados
    horas = models.DecimalField("Horas laboradas", max_digits=4, decimal_places=2,
                                editable=False, null=True, blank=True)

    # Control y auditoría
    estado = models.CharField(max_length=1, choices=TIPO_ESTADOS, default=PENDIENTE)
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     null=True, blank=True,
                                     related_name="asistencia_aprobacion")

    objects = RegistroAsistenciaManager() 

    class Meta:
        indexes = [
            models.Index(fields=['empleado', 'fecha']),
            models.Index(fields=['fecha', 'jornada_horaria']),
            models.Index(fields=['fecha', 'jornada_diaria']),
        ]
        ordering = ['-fecha', '-hora_inicio']
        verbose_name = 'Asistencia'
        verbose_name_plural = "Registro de asistencia"

    def __str__(self):
        horaria = dict(self.TIPO_JORNADA_HORARIA).get(self.jornada_horaria, '')
        diaria = dict(self.TIPO_JORNADA_DIARIA).get(self.jornada_diaria, '')
        return f"{self.empleado} - {self.fecha} {self.hora_inicio}-{self.hora_final} ({horaria} / {diaria})"

    # Propiedades utilitarias
    @property
    def es_jornada_especial(self):
        return self.necesita_aprobacion()

    @property
    def es_horario_regular(self):
        return self.jornada_horaria == self.REGULAR

    @property
    def es_dia_laborable(self):
        return self.jornada_diaria == self.LABORABLE

    @property
    def es_dia_especial(self):
        return self.jornada_diaria in [self.FERIADO, self.FINDESEMANA]

    @property
    def es_horario_extra(self):
        return self.jornada_horaria in [self.HEXTRA1, self.HEXTRA2]
    

    def clean(self):
        """
        Valida que no existan registros superpuestos para el mismo empleado
        en la misma fecha con rangos de horas que se solapen.
        """
        super().clean()
        
        # Validar que hora_inicio y hora_final existan
        if not self.hora_inicio or not self.hora_final:
            raise ValidationError({
                'hora_inicio': 'Debe especificar hora de inicio.',
                'hora_final': 'Debe especificar hora de fin.'
            })
        
        # Validar que hora_final sea mayor que hora_inicio
        if self.hora_final <= self.hora_inicio:
            raise ValidationError({
                'hora_final': 'La hora final debe ser mayor que la hora de inicio.'
            })
        
        # Buscar registros superpuestos
        registros_superpuestos = self._obtener_registros_superpuestos()
        
        if registros_superpuestos.exists():
            # Obtener detalles del primer registro superpuesto para el mensaje
            registro = registros_superpuestos.first()
            raise ValidationError(
                f'Ya existe un registro para {self.empleado} el {self.fecha} '
                f'entre {registro.hora_inicio} y {registro.hora_final} que se superpone '
                f'con el horario ingresado ({self.hora_inicio} - {self.hora_final}).'
            )

    def _obtener_registros_superpuestos(self):
        """
        Obtiene registros que se superponen en fecha y horario para el mismo empleado.
        
        La lógica de superposición:
        - Dos rangos [A_inicio, A_fin] y [B_inicio, B_fin] se superponen si:
          A_inicio < B_fin AND B_inicio < A_fin
        """
        # Query base: mismo empleado y misma fecha
        queryset = RegistroAsistencia.objects.filter(
            empleado=self.empleado,
            fecha=self.fecha
        )
        
        # Excluir el registro actual si está siendo editado
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)
        
        # Filtrar registros con horas que se superponen
        # Condición: hora_inicio < otro.hora_final AND otro.hora_inicio < hora_final
        registros_superpuestos = queryset.filter(
            Q(hora_inicio__lt=self.hora_final) & 
            Q(hora_final__gt=self.hora_inicio)
        )
        
        return registros_superpuestos

    def save(self, *args, **kwargs):
        """
        Ejecuta validación completa antes de guardar.
        """
        # Ejecutar validación
        self.full_clean()
        super().save(*args, **kwargs)
    
class ActividadDiaria(TimeStampedModel):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField('Fecha')
    descripcion = models.TextField('Descripción')
    horas_trabajadas = models.DecimalField('Horas',max_digits=4, decimal_places=2)
    proyecto = models.CharField('proyecto',max_length=100, blank=True)
    completada = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Actividad'
        verbose_name_plural = "Actividades"
    
    def __str__(self):
        return f"{self.empleado} - {self.fecha}"

class Permiso(TimeStampedModel):
    VACACIONES = "0"
    ENFERMEDAD = "1"
    PERSONAL = "2"
    MATERNIDAD = "3"
    PATERNIDAD = "4"
    TIPO_PERMISO = [
        (VACACIONES, 'Vacaciones'),
        (ENFERMEDAD, 'Enfermedad'),
        (PERSONAL, 'Personal'),
        (MATERNIDAD, 'Maternidad'),
        (PATERNIDAD, 'Paternidad'),
    ]
    
    PENDIENTE = "0"
    APROBADO = "1"
    RECHAZADO = "2"
    ESTADO_PERMISO = [
        (PENDIENTE, 'Pendiente'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.CharField('Tipo de permiso',max_length=20, choices=TIPO_PERMISO,default=PERSONAL)
    fecha_inicio = models.DateField('Fecha de inicio')
    fecha_fin = models.DateField('Fecha de finalización')
    horas = models.DecimalField("Horas",decimal_places=2,max_digits=4)
    estado = models.CharField("Estado",max_length=10, choices=ESTADO_PERMISO, default='PENDIENTE')
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_aprobacion = models.DateTimeField("Fecha de aprobación",null=True, blank=True)
    
    objects = PermisoManager()
    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = "Permisos "
    
    def __str__(self):
        return f"{self.empleado} - {self.tipo} ({self.estado})"

class Documento(TimeStampedModel):
    BOLETA = "0"
    CONTRATO = "1"
    CV = "2"
    IDENTIFICACION = "3"
    CERTIFICACION = "4"
    OTRO = "5"
    TIPO_DOCUMENTO = [
        (BOLETA, 'Boleta de Pago'),
        (CONTRATO, 'Contrato'),
        (CV, 'Curriculum Vitae'),
        (IDENTIFICACION, 'Identificación'),
        (CERTIFICACION, 'Certificación'),
        (OTRO, 'Otro'),
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.CharField("Tipo de documento",max_length=20, choices=TIPO_DOCUMENTO)
    nombre = models.CharField("Nombre de documento",max_length=200)
    archivo = models.FileField(
        upload_to='documentos/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'png'])]
    )
    fecha_documento = models.DateField("Fecha de emisión")
    descripcion = models.TextField("Descripción del documento",blank=True)
    
    objects = DocumentoManager()

    class Meta:
        ordering = ['-fecha_documento']
    
    def __str__(self):
        return f"{self.empleado} - {self.tipo} - {self.nombre}"
    
