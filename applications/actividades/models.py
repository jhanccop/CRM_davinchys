from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel

from applications.clientes.models import Cliente
from applications.producto.models import Transformer
from applications.personal.models import Workers

from applications.cuentas.models import Tin

from django.db import transaction
from decimal import Decimal

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .managers import (
  TrafoOrderManager,
  TrafoTrackingManager,

  DailyTasksManager,
  RestDaysManager,

  TrafoQuoteManager,
  TrafosManager,
  TrafoTaskManager,
  SuggestionBoxManager
)

class TrafoTracking(TimeStampedModel):
    """ Modelo de seguimiento de ordenes """
    
    # estados de pedido
    CREADO = '0'
    FABRICADO = '1'
    ENVIADO = '2'
    COMPLETADO = '3'
    CANCELADO = '4'

    #
    STATE_CHOICES = [
        (CREADO, 'Creado'),
        (FABRICADO, 'Fabricado'),
        (ENVIADO, 'Enviado'),
        (COMPLETADO, 'Completado'),
        (CANCELADO, 'Cancelado'),
    ]

    idOrder = models.IntegerField("Id Orders",null=True,blank=True)
    dateChange = models.DateTimeField(
        'Fecha',
    )
    orderState = models.CharField(
        'Estado de orden',
        max_length=1,
        choices=STATE_CHOICES,
        #unique=True
    )

    objects = TrafoTrackingManager()

    class Meta:
        verbose_name = 'pedido seguimiento '
        verbose_name_plural = 'pedidos seguimientos '

    def get_short_name(self):
        return self.idOrder
    
    def get_full_name(self):
        return self.idClient
    
    def __str__(self):
        return str(self.orderState)

class TrafoOrder(TimeStampedModel):
    """ Modelo de ordenes """

    idOrder = models.CharField('Id orden',max_length=100,unique=True,null=True,blank=True)
    idClient = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    idTransformer = models.ForeignKey(Transformer, on_delete=models.CASCADE, null=True, blank=True)
    
    dateOrder = models.DateField(
        'Fecha de pedido',
    )
    deadline = models.DateField(
        'Fecha de entrega',
    )

    amount = models.DecimalField(
        'Costo', 
        max_digits=10, 
        decimal_places=2
    )
    numberUnits = models.PositiveIntegerField('Numero de unidades', null=True, blank=True)
    idAttendant = models.ForeignKey(Workers, on_delete=models.CASCADE, null=True, blank=True)
    
    IdOrderState = models.CharField("Estado de orden",default = "0", max_length=25,null=True,blank=True)

    objects = TrafoOrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def get_short_name(self):
        return self.idOrder
    
    def get_full_name(self):
        return self.idClient
    
    def __str__(self):
        return str(self.idOrder)

class Commissions(TimeStampedModel):

    # ESTADOS 
    ACTIVO = '0'
    CULMINADO = '1'
    PAUSADO = '2'
    SUSPENDIDO = '3'
    CANCELADO = '4'

    #
    STATUS_CHOICES = [
        (ACTIVO, 'Activo'),
        (CULMINADO, 'Culminado'),
        (PAUSADO, 'Pausado'),
        (SUSPENDIDO, 'Suspendido'),
        (CANCELADO, 'Cancelado'),
    ]

    commissionName = models.CharField(
        'Nombre de comision',
        max_length=100,
        null=True,
        blank=True,
    )

    place = models.CharField(
        'Lugar',
        max_length=100,
        null=True,
        blank=True,
    )

    startDate = models.DateField(
        'Fecha de incio',
    )
    endDate = models.DateField(
        'Fecha de finalizacion',
    )

    workers = models.ManyToManyField(settings.AUTH_USER_MODEL)

    status = models.CharField(
        'Estado',
        max_length=50, 
        choices=STATUS_CHOICES, 
        blank=True
    )

    description = models.TextField(
        'Descripcion',
        blank = True,
    )

    #objects = SaleManager()

    class Meta:
        verbose_name = 'Comision de trabajo'
        verbose_name_plural = 'Comisiones de trabajo'

    def __str__(self):
        return str(self.commissionName)

class Projects(TimeStampedModel):

     # ESTADOS 
    ACTIVO = '0'
    CULMINADO = '1'
    PAUSADO = '2'
    SUSPENDIDO = '3'
    CANCELADO = '4'

    #
    STATUS_CHOICES = [
        (ACTIVO, 'Activo'),
        (CULMINADO, 'Culminado'),
        (PAUSADO, 'Pausado'),
        (SUSPENDIDO, 'Suspendido'),
        (CANCELADO, 'Cancelado'),
    ]

    projectName = models.CharField(
        'Nombre de projecto',
        max_length=100,
        null=True,
        blank=True,
    )
    startDate = models.DateField(
        'Fecha de incio',
    )
    endDate = models.DateField(
        'Fecha de finalizacion',
    )

    workers = models.ManyToManyField(settings.AUTH_USER_MODEL)

    status = models.CharField(
        'Estado',
        max_length=50, 
        choices=STATUS_CHOICES, 
        blank=True
    )

    description = models.TextField(
        'Descripcion',
        blank=True,
    )

    #objects = SaleManager()

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return str(self.projectName)

#class AssignedTasks(TimeStampedModel):

class AssignedTasks(TimeStampedModel):
    # TIPO DE JORNADA 
    ENPROCESO = '0'
    CULMINADO = '1'
    CANCELADO = '2'
    ENESPERA = '3'

    #
    STATUS_CHOICES = [
        (ENPROCESO, 'en proceso'),
        (CULMINADO, 'culminado'),
        (CANCELADO, 'cancelado'),
        (ENESPERA, 'en espera'),
    ]

    activity = models.CharField(
        'Actividad',
        null=False,
        blank=False,
    )
    startDate = models.DateField(
        'Fecha de incio',
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    endDate = models.DateField(
        'Fecha de finalizacion',
    )
    status = models.CharField(
        'Estado',
        max_length=1, 
        choices=STATUS_CHOICES,
        null=True,
        blank=True
    )
    comentary = models.CharField(
        'comentario',
        null=False,
        blank=False,
    )

    #objects = SaleManager()

    class Meta:
        verbose_name = 'Tarea asignada'
        verbose_name_plural = 'Tareas asignadas'

    def __str__(self):
        return str(self.activity)

# ================= RRHH ================
class RestDays(TimeStampedModel):
    # TIPO DE PERMISO 
    PARTICULAR = '0'
    DESCANSOMEDICO = '1'
    VACACIONES = '2'
    MATERNIDAD = '3'
    OTROS = '4'

    #
    TYPE_CHOICES = [
        (PARTICULAR, 'Permiso particular'),
        (DESCANSOMEDICO, 'Descanso médico'),
        (VACACIONES, 'Vacaciones'),
        (MATERNIDAD, 'Maternidad'),
        (OTROS, 'Otro'),
    ]

    # === CATEGORIA ESTADO ====
    ESPERA = '0'
    ACEPTADO = '1'
    DENEGADO = '2'
    OBSERVADO = '3'
    CREADO = '4'

    STATUS_CHOICES = [
        (ESPERA,'espera'),
        (ACEPTADO,'aceptado'),
        (DENEGADO,'denegado'),
        (OBSERVADO,'observado'),
        (CREADO,'creado'),
    ]

    # ------------- models -------------
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
    )

    type = models.CharField(
        'Tipo de permiso',
        max_length=1, 
        choices=TYPE_CHOICES,
        null=True,
        blank=True,
        default="0",
    )

    hours = models.DecimalField(
        'Horas',
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=3
    )

    days = models.IntegerField(
        'Dias',
        null=True,
        blank=True,
        default=0
    )

    isCompensated = models.BooleanField(
        "Compensación necesaria",
        default=True
    )

    hoursCompensated = models.IntegerField(
        "Horas compensados",
        null=True,
        blank=True,
        default=0
    )

    daysCompensated = models.IntegerField(
        "Dias compensados",
        null=True,
        blank=True,
        default=0
    )

    startDate = models.DateField(
        'Fecha de inicio',
        null=True,
        blank=True,
    )
    endDate = models.DateField(
        'Fecha de término',
        null=True,
        blank=True,
    )

    motive = models.TextField(
        'Motivo',
        null=True,
        blank=True,
    )

    tag1 = models.CharField("Ap RRHH",default="0",choices=STATUS_CHOICES,max_length=1,blank=True,null=True)# only adquisitions
    dt1 = models.DateTimeField("F. RRHH",null=True,blank=True) # adquisiciones

    tag2 = models.CharField("VB Gerencia",default="4",choices=STATUS_CHOICES,max_length=1,blank=True,null=True) # only contabilidad
    dt2 = models.DateTimeField("F. Gerencia ",null=True,blank=True) # contabilidad

    pdf_file = models.FileField(upload_to='descansos_pdfs/',null=True,blank=True)

    objects = RestDaysManager()

    class Meta:
        verbose_name = 'Descanso'
        verbose_name_plural = 'Descansos'

    def __str__(self):
        return f"{self.user} | {self.startDate} | {self.get_type_display()}"

class DailyTasks(TimeStampedModel):

    # TIPO DE JORNADA 
    JORNADAREGULAR = '0'
    HORASEXTRA = '1'
    FERIADO = '2'
    OTROS = '3'
    COMPENSACION = '4'

    #
    TYPE_CHOICES = [
        (JORNADAREGULAR, 'Jornada diaria'),
        (HORASEXTRA, 'Horas extra'),
        (FERIADO, 'Feriado'),
        (COMPENSACION, 'Compensación'),
        (OTROS, 'Otro'),
    ]

    # CLASE DE ACTIVIDAD 
    INSPECCION = '0'
    MANTENIMIENTO = '1'
    PRODUCCION = '2'
    CONTROLDECALIDAD = '3'
    TRANSPORTE = '4'
    LOGISTICA = '5'

    DOCUMENTACION = '6'
    REUNION = '7'
    MARKETING = '8'
    PLANIFICACION = '9'
    FINANZAS = '10'
    CONTABILIDAD = '11'
    REPRESENTACION = '12'
    AUDITORIA = '13'

    DESARROLLO = '14'
    TESTING = '15'

    ADUANAS = '16'
    OTRO = '17'
    
    #
    WORK_CHOICES = [
        (INSPECCION, 'Inspección'),
        (MANTENIMIENTO, 'Mantenimiento'),
        (PRODUCCION, 'Producción'),
        (CONTROLDECALIDAD, 'Control de calidad'),
        (TRANSPORTE, 'Transporte'),
        (LOGISTICA, 'Logistica'),

        (DOCUMENTACION, 'Documentación'),
        (REUNION, 'Reunión'),
        (MARKETING, 'Marketing'),
        (PLANIFICACION, 'Planificación'),
        (FINANZAS, 'Finanzas'),
        (CONTABILIDAD, 'Contabilidad'),
        (REPRESENTACION, 'Representación'),
        (AUDITORIA, 'Auditoria'),

        (DESARROLLO, 'Desarrollo'),
        (TESTING, 'Testing'),

        (ADUANAS, 'Aduanas'),
        (OTRO, 'Otro'),

    ]

    # ------------- models -------------
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
    )

    date = models.DateField(
        'Fecha',
    )

    activity = models.TextField(
        'Actividad',
        null=True,
        blank=True,
    )

    type = models.CharField(
        'Tipo de jornada',
        max_length=1, 
        choices=TYPE_CHOICES,
        null=True,
        blank=True,
        default="0",
    )

    task = models.CharField(
        'Tipo de actividad',
        max_length=2, 
        choices=WORK_CHOICES,
        null=True,
        blank=True,
        default="7",
    )

    overTime = models.DecimalField(
        'Horas extra',
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=3
    )

    hours = models.DecimalField(
        'Horas',
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
    )

    idTin = models.ForeignKey(Tin, on_delete = models.CASCADE, null=True, blank=True, related_name="DialyTaskTin")
    rest_day = models.ForeignKey(RestDays, on_delete = models.CASCADE, null=True, blank=True, related_name="compensations")
    trafoOrder = models.ForeignKey(TrafoOrder, on_delete = models.CASCADE, null=True, blank=True)
    commissions = models.ForeignKey(Commissions, on_delete = models.CASCADE, null=True, blank=True)
    projects = models.ForeignKey(Projects, on_delete = models.CASCADE, null=True, blank=True)
    assignedTasks = models.ForeignKey(AssignedTasks, on_delete = models.CASCADE, null=True, blank=True)
    

    objects = DailyTasksManager()

    class Meta:
        verbose_name = 'Tarea diaria'
        verbose_name_plural = 'Tareas diarias'

    def __str__(self):
        return str(self.user) + " - " + str(self.date)

# ================= COTIZACIONES ================
class TrafoQuote(TimeStampedModel):

    CONDITION_CHOICES = (
        ('0', 'recibida'),
        ('1', 'enviada'),
        ('2', 'aprobada'),
    )

    # ESTADO DE COTIZACION
    ESPERA = '0'
    COMPLETADO = '1'
    CANCELADO = '2'
    OBSERVADO = '3'
    CREADO = '4'

    #
    STATUS_CHOICES = [
        (CREADO, 'creado'),
        (ESPERA, 'espera'),
        (COMPLETADO, 'completado'),
        (OBSERVADO, 'observado'),
        (CANCELADO, 'cancelado'),
    ]

    # ESTADO DE PO
    NOPO = '0'
    PO = '1'

    PO_STATUS_CHOICES = [
        (NOPO, 'no PO'),
        (PO, 'PO'),
    ]

     # ESTADO DE FABRICACION
    RECIBIDO = '0'
    MATERIALES = '1'
    FABRICADO = '2'
    TRANSPORTEINTERNO = '3'
    TRANSPORTEMARITIMO = '4'
    ARRIBADO = '5'
    ENTREGADO = '6'

    #
    TRAKING_CHOICES = [
        (RECIBIDO, 'recibido'),
        (MATERIALES, 'insumos'),
        (FABRICADO, 'fabricado'),
        (TRANSPORTEINTERNO, 'transporte interno'),
        (TRANSPORTEMARITIMO, 'transporte maritimo'),
        (ARRIBADO, 'arribado'),
        (ENTREGADO, 'entregado'),
    ]

    idQuote = models.CharField('RFQ Number',max_length=100,unique=True)
    idClient = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="cliente")
    userClient = models.CharField("Cliente",max_length=20,null=True,blank=True)
    dateOrder = models.DateField(
        'Fecha de pedido',
    )
    deadline = models.DateField(
        'Fecha de entrega',
        null=True,
        blank=True
    )
    idAttendant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    q1 = models.CharField(
        'Recibido',
        max_length=1,
        default="0",
        choices=STATUS_CHOICES,
    )
    q2 = models.CharField(
        'Cotizacion',
        max_length=1,
        default="4",
        choices=STATUS_CHOICES,
    )
    q3 = models.CharField(
        'Respuesta de cliente',
        max_length=1,
        default="4",
        choices=STATUS_CHOICES,
    )
    q4 = models.CharField(
        'Atendido',
        max_length=1,
        default="4",
        choices=STATUS_CHOICES,
    )

    dt1 = models.DateTimeField("dt1",null=True,blank=True)
    dt2 = models.DateTimeField("dt2",null=True,blank=True)
    dt3 = models.DateTimeField("dt3",null=True,blank=True)
    dt4 = models.DateTimeField("dt4",null=True,blank=True)

    poStatus = models.CharField(
        'Estado PO',
        default="0",
        max_length=1, 
        choices=PO_STATUS_CHOICES,
        null=True,
        blank=True
    )

    trakingStatus = models.CharField(
        'Seguimiento',
        default="0",
        max_length=1, 
        choices=TRAKING_CHOICES,
        null=True,
        blank=True
    )

    description = models.TextField("Description",null=True,blank=True)

    condition = models.CharField(
        'Condicion',
        max_length=1,
        default="0",
        choices=CONDITION_CHOICES,
        blank=True, 
        null=True
    )

    objects = TrafoQuoteManager()

    def __str__(self):
        return str(self.idQuote)

class TrafoTask(TimeStampedModel):
    idTrafoQuote = models.ForeignKey(TrafoQuote, on_delete=models.CASCADE)
    nameTask = models.CharField("Tarea",max_length=100)
    #workers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    location = models.CharField("Ubicacion",max_length=100, blank=True, null=True)
    start_date = models.DateField("Fecha de inicio", blank=True, null=True)
    end_date = models.DateField("Fecha finalizacion", blank=True, null=True)
    progress = models.IntegerField("Progreso",default=0)
    depend = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_milestone = models.BooleanField(default=False) 

    objects = TrafoTaskManager()

    class Meta:
        verbose_name = 'Tarea orden'
        verbose_name_plural = 'Tareas ordenes'

    def __str__(self):
        return f"{self.idTrafoQuote} | {self.nameTask}"
    
# ======================== TRAFOS ======================
class Trafos(TimeStampedModel):
    """
        Catalogo de Transformadores
    """
    KVA_CHOICES = (
        ('0', '15'),
        ('1', '30'),
        ('2', '75'),
        ('3', '100'),
        ('4', '167'),
        ('5', '200'),
        ('6', '250'),
        ('7', '400'),
        ('8', '500'),
        ('9', '600'),
        ('10', '750'),
        ('11', '1000'),
        ('12', '1500'),
        ('13', '2000'), 
    )

    HVTAP_CHOICES = (
        ('0', 'K-Tap - HV'),
        ('1', 'Fix HV'),
    )

    KTapHV_CHOICES = (
        ('0', '12700/7200'),
        ('1', '24940/14400'),
    )
    FIXHV_CHOICES = (
        ('0', '7200'),
        ('1', '12470'),
        ('2', '22900'),
    )

    LV_CHOICES = (
        ('0', '120/240'),
        ('1', '277/480'),
    )

    HZ_CHOICES = (
        ('0', '50'),
        ('1', '60'),
    )

    PHASE_CHOICES = (
        ('0', 'Mono-phasic'),
        ('1', 'Three-phasic'),
    )

    MOUNTING_CHOICES = (
        ('0', 'Pole'),
        ('1', 'Standard'),
        ('2', 'Feed Through Pad'),
    )

    COOLING_CHOICES = (
        ('0', 'Oil'),
        ('1', 'Dry'),
    )

    WINDING_CHOICES = (
        ('0', 'Al - Al'),
        ('1', 'Cu - CU'),
    )

    INSULAT_CHOICES = (
        ('0', 'A'),
        ('1', 'E'),
        ('2', 'H'),
    )

    CONNECTION_CHOICES = (
        ('0', 'WEY'),
        ('1', 'DELTA'),
    )

    STANDARD_CHOICES = (
        ('0', 'NMX-116'),
        ('1', 'IEC 61558'),
    )

    TENSION_CHOICES = (
        ('0', '220'),
        ('1', '380'),
        ('2', '400'),
        ('3', '460'),
        ('4', '600'),
        ('5', '10000'),
        ('6', '13800'),
        ('7', '20000'),
        ('8', '22900'),
    )

    TYPE_CHOICES = (
        ('0', 'Seco'),
        ('1', 'Aceite'),
        ('2', 'Pedestal'),
        ('3', 'Integrado'),
        ('4', 'Subestacion'),
        ('5', 'Poste'),
    )

    id = models.AutoField(primary_key=True)

    idQuote = models.ForeignKey(TrafoQuote, on_delete=models.CASCADE, null=True, blank=True)

    provider = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    KVA = models.CharField(
        'kVA CAPACITY',
        max_length=2,
        choices=KVA_CHOICES,
        blank=True, 
        null=True
    )

    HVTAP = models.CharField(
        'HV TAP',
        max_length=2,
        choices=HVTAP_CHOICES,
        blank=True, 
        null=True
    )

    KTapHV = models.CharField(
        'K Tap HV',
        max_length=2,
        choices=KTapHV_CHOICES,
        blank=True, 
        null=True
    )

    FIXHV = models.CharField(
        'FIX HV',
        max_length=2,
        choices=FIXHV_CHOICES,
        blank=True, 
        null=True
    )

    LV = models.CharField(
        'LV',
        max_length=2,
        choices=LV_CHOICES,
        blank=True, 
        null=True
    )

    HZ = models.CharField(
        'HZ',
        max_length=2,
        choices=HZ_CHOICES,
        blank=True, 
        null=True
    )

    TYPE = models.CharField(
        'TYPE',
        max_length=2,
        choices=PHASE_CHOICES,
        blank=True, 
        null=True
    )

    MOUNTING = models.CharField(
        'MOUNTING TYPE',
        max_length=2,
        choices=MOUNTING_CHOICES,
        blank=True, 
        null=True
    )

    COOLING = models.CharField(
        'COOLING',
        max_length=2,
        choices=COOLING_CHOICES,
        blank=True, 
        null=True
    )

    WINDING = models.CharField(
        'WINDING',
        max_length=2,
        choices=WINDING_CHOICES,
        blank=True, 
        null=True
    )

    INSULAT = models.CharField(
        'INSULAT CLASS',
        max_length=2,
        choices=INSULAT_CHOICES,
        blank=True, 
        null=True
    )

    CONNECTION = models.CharField(
        'CONNECTION',
        max_length=2,
        choices=CONNECTION_CHOICES,
        blank=True, 
        null=True
    )

    STANDARD = models.CharField(
        'STANDARD',
        max_length=2,
        choices=STANDARD_CHOICES,
        blank=True, 
        null=True
    )

    quantity = models.IntegerField(
        'Cantidad',
        blank=True,
        null=True,
    )

    unitCost = models.DecimalField(
        'Costo unitario', 
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True,
    )

    objects = TrafosManager()

    class Meta:
        verbose_name = 'Trafos'
        verbose_name_plural = 'Trafos'

    def __str__(self):
        return str(self.KVA) + ' | ' + str(self.LV)
    
class EmailSent(TimeStampedModel): 

    Type_CHOICES = (
        ('0', 'inicial'),
        ('1', 'cotizacion'),
        ('2', 'aprobación'),
    )

    typeMail = models.CharField(
        'Tipo',
        default="0",
        max_length=1, 
        choices=Type_CHOICES,
        null=True,
        blank=True
    )

    idQuote = models.ForeignKey(TrafoQuote,on_delete=models.CASCADE, null=True, blank=True)
    sendFlag = models.BooleanField("Enviado", default=False)
    subject = models.CharField("Subject", max_length=100)
    body = models.TextField("Body")
    sender = models.CharField("Emisor", max_length=100, default="jh")
    recipients = models.CharField("Receptores", max_length=100)

    def __str__(self):
        return str(self.subject) + " - " + str(self.send)

# ================= BUZON DE SUGERENCIAS ================
class SuggestionBox(TimeStampedModel):
    CONTABILIDAD = '1'
    SUPERVISOR_PRODUCCION = '2'
    ADQUISICIONES = '5'
    FINANZAS = '6'
    CONSULTOREXTERNO = '8'

    ROLES_CHOICES = [
        (CONTABILIDAD, 'Contabilidad'),
        (SUPERVISOR_PRODUCCION, 'Supervisor producción'),
        (ADQUISICIONES, 'Adquisiciones'),
        (FINANZAS, 'Finanzas'),
        (CONSULTOREXTERNO, 'Consultor'),
    ]

    # ------------- models -------------
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
    )
    suggestion = models.TextField(
        'Sugerencia',
        null=False,
        blank=False,
    )
    area = models.CharField(
        'Area',
        max_length=1, 
        choices=ROLES_CHOICES, 
        blank=True
    )

    objects = SuggestionBoxManager()

    class Meta:
        verbose_name = 'Sugerencia'
        verbose_name_plural = 'Sugerencias'

    def __str__(self):
        return f"{self.user} - {self.get_area_display()}"

# ======================= SIGNAL REST DAYS =======================
@receiver(pre_save, sender=RestDays)
def update_tag2_when_tag1_approved(sender, instance, **kwargs):
    """
    Actualiza tag2 a 'ESPERA' (0) cuando tag1 cambia a 'ACEPTADO' (1)
    y tag2 estaba en su valor por defecto ('CREADO' - 4)
    """
    if instance.pk:  # Solo para instancias existentes
        try:
            original = RestDays.objects.get(pk=instance.pk)
            
            # Verificar si tag1 cambió a ACEPTADO (1)
            if original.tag1 != instance.tag1 and instance.tag1 == RestDays.ACEPTADO:
                # Si tag2 está en su valor por defecto (CREADO - 4), cambiarlo a ESPERA (0)
                if instance.tag2 == RestDays.CREADO:
                    instance.tag2 = RestDays.ESPERA
                    
        except RestDays.DoesNotExist:
            pass  # Para nuevos registros, no hacemos nada

@receiver(pre_save, sender=RestDays)
def calculate_days_between_dates(sender, instance, **kwargs):
    """
    Calcula el número de días entre startDate y endDate y lo guarda en el campo 'days'.
    Este signal se ejecuta antes de guardar un objeto RestDays.
    """
    try:
        if instance.startDate and instance.endDate:
            # Calcular la diferencia en días
            delta = instance.endDate - instance.startDate
            
            # Asignar el valor al campo 'days' (añadir +1 para incluir ambos días)
            # Por ejemplo: del 10 al 12 son 3 días (10, 11, 12)
            instance.days = delta.days + 1

    except Exception as e:
        print(f"Error al buscar el modelo relacionado: {str(e)}")

def get_actual_days_count(rest_day):
    """
    Función para contar los días únicos correctamente.
    Realizamos una consulta manual para evitar problemas de cache o conteo incorrecto.
    """
    # Obtenemos las fechas únicas y las contamos manualmente
    unique_dates = set(
        DailyTasks.objects.filter(
            rest_day=rest_day,
            type=DailyTasks.COMPENSACION
        ).values_list('date', flat=True)
    )
    
    # Retornamos el número exacto de días únicos
    return len(unique_dates)

@receiver(post_save, sender=DailyTasks)
def update_rest_day_compensation(sender, instance, created, **kwargs):
    """
    Signal para actualizar las hoursCompensated y daysCompensated en RestDays
    cuando se guarda un DailyTasks.
    
    - hoursCompensated: Se copia el valor de hours del RestDay
    - daysCompensated: Se completa con cantidad de DailyTask con el restday respectivo en diferentes días
    """
    # Solo procesar si hay un rest_day asociado y es de tipo compensación
    if instance.rest_day and instance.type == DailyTasks.COMPENSACION:
        rest_day = instance.rest_day
        
        # Copiar el valor de hours de RestDay a hoursCompensated
        # Si hours es None, se asigna 0
        if rest_day.hours is not None:
            hours_compensated = rest_day.hours
        else:
            hours_compensated = 0
            
        # Actualizar hoursCompensated
        rest_day.hoursCompensated = hours_compensated
        
        # Actualizar daysCompensated: contar días distintos con compensaciones
        # Usamos nuestra función personalizada para garantizar un conteo exacto
        days_compensated = get_actual_days_count(rest_day)
        
        rest_day.daysCompensated = days_compensated - 1
        
        # Guardar los cambios sin disparar más signals para evitar recursión
        rest_day.save(update_fields=['hoursCompensated', 'daysCompensated'])

@receiver(post_delete, sender=DailyTasks)
def update_rest_day_compensation_on_delete(sender, instance, **kwargs):
    """
    Signal para actualizar las hoursCompensated y daysCompensated en RestDays
    cuando se elimina un DailyTasks.
    """
    # Solo procesar si había un rest_day asociado y era de tipo compensación
    if instance.rest_day and instance.type == DailyTasks.COMPENSACION:
        rest_day = instance.rest_day
        
        # Mantener hoursCompensated igual al campo hours del RestDay
        if rest_day.hours is not None:
            hours_compensated = rest_day.hours
        else:
            hours_compensated = 0
            
        rest_day.hoursCompensated = hours_compensated
        
        # Recalcular daysCompensated usando nuestra función personalizada
        days_compensated = get_actual_days_count(rest_day)
        rest_day.daysCompensated = days_compensated
        
        # Guardar los cambios con update_fields para evitar recursión
        rest_day.save(update_fields=['hoursCompensated', 'daysCompensated'])