from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings

from model_utils.models import TimeStampedModel

from django.utils import timezone
from datetime import datetime, date, time, timedelta
from django.core.exceptions import ValidationError

from .managers import (
    RegistroAsistenciaManager,
    EmpleadoManager,
    DocumentoManager,
    PermisoManager
)

class Departamento(TimeStampedModel):
    nombre = models.CharField(max_length=100)
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

class RegistroAsistencia(TimeStampedModel):
    LOCAL1 = "0"
    LOCAL2 = "1"
    LOCAL3 = "2"
    REMOTO = "3"
    OTROLOCAL = "4"
    TIPO_LOCAL = [
        (LOCAL1, 'Shell'),
        (LOCAL2, 'Colon'),
        (LOCAL3, 'Planta'),
        (REMOTO, 'Remoto'),
        (OTROLOCAL, 'Otro'),
    ]

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

    REGULAR = "0"
    HEXTRA1 = "1"
    HEXTRA2 = "2"
    FERIADO = "3"
    REFRIGERIO = "4"
    OTRAJORNADA = "5"
    TIPO_JORNADA = [
        (REGULAR, 'Reg 9:00 - 18:00'),
        (HEXTRA1, 'HE1 18:01 - 21:59'),
        (HEXTRA2, 'HE2 22:00 - 05:59'),
        (FERIADO, 'Feriado'),
        (REFRIGERIO, 'Refrigerio'),
        (OTRAJORNADA, 'Otro'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField('Fecha')
    hora_inicio = models.TimeField('Hora inicio', null=True, blank=True)
    hora_final = models.TimeField('Hora final', null=True, blank=True)
    ubicacion = models.CharField('Local', max_length=1, choices=TIPO_LOCAL)
    jornada = models.CharField('Jornada', max_length=1, choices=TIPO_JORNADA,
                               default=REGULAR, blank=True)
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

    objects = RegistroAsistenciaManager()  # o tu RegistroAsistenciaManager si lo tienes

    class Meta:
        indexes = [
            models.Index(fields=['empleado', 'fecha']),
            models.Index(fields=['fecha', 'jornada']),
        ]
        unique_together = ['empleado', 'fecha', 'hora_inicio', 'jornada']
        ordering = ['-fecha', '-hora_inicio']
        verbose_name = 'Asistencia'
        verbose_name_plural = "Registro de asistencia"

    def clean(self):
        if self.hora_inicio and self.hora_final:
            if self.hora_final <= self.hora_inicio:
                raise ValidationError('Hora final debe ser mayor que hora inicio')

    def determinar_jornada_por_hora(self, hora_time):
        """
        Determina el tipo de jornada según la hora proporcionada
        """
        hora = hora_time.hour
        if 18 <= hora <= 21:
            return self.HEXTRA1
        elif hora >= 22 or hora <= 6:
            return self.HEXTRA2
        else:
            return self.REGULAR

    def calcular_horas_laboradas(self):
        """
        Calcula las horas laboradas considerando los diferentes rangos de jornada
        """
        if not self.hora_inicio or not self.hora_final:
            return 0.0

        inicio_dt = datetime.combine(self.fecha, self.hora_inicio)
        fin_dt = datetime.combine(self.fecha, self.hora_final)

        # Si la hora final es menor que la inicial, asumimos que es del día siguiente
        if self.hora_final <= self.hora_inicio:
            fin_dt += timedelta(days=1)

        # Determinar jornada
        jornada_inicio = self.determinar_jornada_por_hora(self.hora_inicio)
        jornada_fin = self.determinar_jornada_por_hora(self.hora_final)

        if jornada_inicio == self.HEXTRA2 or jornada_fin == self.HEXTRA2:
            self.jornada = self.HEXTRA2
        elif jornada_inicio == self.HEXTRA1 or jornada_fin == self.HEXTRA1:
            self.jornada = self.HEXTRA1
        else:
            self.jornada = self.REGULAR

        diferencia = fin_dt - inicio_dt
        horas_totales = diferencia.total_seconds() / 3600
        return round(horas_totales, 2)

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.hora_inicio and self.hora_final:
            self.horas = self.calcular_horas_laboradas()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.empleado} - {self.fecha} ({self.get_jornada_display()})"

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
    
