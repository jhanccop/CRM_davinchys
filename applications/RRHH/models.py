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
    PermisoManager,
    LocalManager
)

from applications.cuentas.models import Tin

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
        (HEXTRA1, 'HE1 18:01 - 21:00'),
        (HEXTRA2, 'HE2 21:01 - 23:59 y 00:00 - 06:00'),
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
    ubicacion = models.CharField('Local', max_length=1, null=True, blank=True, default = "0")
    
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
        unique_together = ['empleado', 'fecha', 'hora_inicio', 'jornada_horaria']
        ordering = ['-fecha', '-hora_inicio']
        verbose_name = 'Asistencia'
        verbose_name_plural = "Registro de asistencia"

    def es_fin_de_semana(self):
        """Determina si la fecha es fin de semana (sábado o domingo)"""
        return self.fecha.weekday() in [5, 6]  # 5 = sábado, 6 = domingo

    def es_feriado(self):
        """Determina si la fecha es feriado consultando el modelo Feriados"""
        try:
            from .models import Feriados
            return Feriados.objects.filter(fecha=self.fecha).exists()
        except:
            return False

    def determinar_jornada_horaria(self, hora_time):
        """
        Determina la jornada horaria según la hora proporcionada:
        - REGULAR: 09:00 - 18:00
        - HEXTRA1: 18:01 - 21:00
        - HEXTRA2: 21:01 - 23:59 y 00:00 - 06:00
        """
        hora = hora_time.hour
        minuto = hora_time.minute
        
        # Convertir a minutos desde medianoche para comparación precisa
        tiempo_minutos = hora * 60 + minuto
        
        # Definir rangos en minutos
        inicio_regular = 9 * 60  # 09:00 = 540 minutos
        fin_regular = 18 * 60    # 18:00 = 1080 minutos
        fin_hextra1 = 21 * 60    # 21:00 = 1260 minutos
        fin_hextra2_noche = 6 * 60  # 06:00 = 360 minutos
        
        # Jornada regular: 09:00 - 18:00
        if inicio_regular <= tiempo_minutos <= fin_regular:
            return self.REGULAR
        
        # Horas extra tipo 1: 18:01 - 21:00
        elif fin_regular < tiempo_minutos <= fin_hextra1:
            return self.HEXTRA1
        
        # Horas extra tipo 2: 21:01 - 23:59 y 00:00 - 06:00
        elif tiempo_minutos > fin_hextra1 or tiempo_minutos <= fin_hextra2_noche:
            return self.HEXTRA2
        
        # Período no cubierto: 06:01 - 08:59 (antes del inicio de jornada regular)
        else:
            return self.REGULAR

    def determinar_jornada_diaria(self):
        """
        Determina la jornada diaria según el tipo de día:
        - FERIADO: prioridad máxima
        - FINDESEMANA: si es sábado o domingo
        - LABORABLE: por defecto
        """
        if self.es_feriado():
            return self.FERIADO
        elif self.es_fin_de_semana():
            return self.FINDESEMANA
        else:
            return self.LABORABLE

    def determinar_jornadas_completas(self):
        """
        Determina ambas jornadas automáticamente
        """
        jornada_horaria = self.REGULAR
        jornada_diaria = self.determinar_jornada_diaria()
        
        # Determinar jornada horaria solo si hay hora de inicio
        if self.hora_inicio:
            jornada_horaria = self.determinar_jornada_horaria(self.hora_inicio)
        
        return jornada_horaria, jornada_diaria

    def get_jornada_completa_display(self):
        """Retorna el display completo de ambas jornadas"""
        display_horaria = dict(self.TIPO_JORNADA_HORARIA).get(self.jornada_horaria, '')
        display_diaria = dict(self.TIPO_JORNADA_DIARIA).get(self.jornada_diaria, '')
        
        return f"{display_horaria} - {display_diaria}"

    def necesita_aprobacion(self):
        """
        Determina si el registro requiere aprobación:
        - LABORABLE + REGULAR: No requiere aprobación
        - Cualquier otra combinación: Requiere aprobación
        """
        return not (self.jornada_diaria == self.LABORABLE and self.jornada_horaria == self.REGULAR)

    def calcular_horas_laboradas(self):
        """
        Calcula las horas laboradas
        """
        if not self.hora_inicio or not self.hora_final:
            return 0.0

        inicio_dt = datetime.combine(self.fecha, self.hora_inicio)
        fin_dt = datetime.combine(self.fecha, self.hora_final)

        # Si la hora final es menor que la inicial, asumimos que es del día siguiente
        if self.hora_final <= self.hora_inicio:
            fin_dt += timedelta(days=1)

        # Determinar ambas jornadas automáticamente
        self.jornada_horaria, self.jornada_diaria = self.determinar_jornadas_completas()

        diferencia = fin_dt - inicio_dt
        horas_totales = diferencia.total_seconds() / 3600
        return round(horas_totales, 2)

    def clean(self):
        if self.hora_inicio and self.hora_final:
            if self.hora_final <= self.hora_inicio:
                raise ValidationError('Hora final debe ser mayor que hora inicio')

    def save(self, *args, **kwargs):
        self.full_clean()
        
        # Determinar las jornadas automáticamente antes de guardar
        if self.fecha:
            self.jornada_horaria, self.jornada_diaria = self.determinar_jornadas_completas()
            
            # Gestionar estado según necesidad de aprobación
            if not self.necesita_aprobacion():
                self.estado = self.PROCESADO
                self.aprobado_por = None
            elif self.necesita_aprobacion() and self.estado == self.PROCESADO:
                # Si requiere aprobación pero está como procesado, cambiar a pendiente
                self.estado = self.PENDIENTE
        
        if self.hora_inicio and self.hora_final:
            self.horas = self.calcular_horas_laboradas()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.empleado} - {self.fecha} ({self.get_jornada_completa_display()})"

    # Métodos utilitarios para facilitar el filtrado
    @property
    def es_jornada_especial(self):
        """Indica si es una jornada que requiere aprobación especial"""
        return self.necesita_aprobacion()

    @property
    def es_horario_regular(self):
        """Indica si es horario regular"""
        return self.jornada_horaria == self.REGULAR

    @property
    def es_dia_laborable(self):
        """Indica si es día laborable normal"""
        return self.jornada_diaria == self.LABORABLE

    @property
    def es_dia_especial(self):
        """Indica si es feriado o fin de semana"""
        return self.jornada_diaria in [self.FERIADO, self.FINDESEMANA]

    @property
    def es_horario_extra(self):
        """Indica si es horario extra (HEXTRA1 o HEXTRA2)"""
        return self.jornada_horaria in [self.HEXTRA1, self.HEXTRA2]

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
    
