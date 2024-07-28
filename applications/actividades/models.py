from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel

from applications.clientes.models import Cliente
from applications.producto.models import Transformer
from applications.personal.models import Workers


from .managers import (
  TrafoOrderManager,
  TrafoTrackingManager,
  DailyTasksManager,

  TrafoQuoteManager,
  TrafosManager
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

class DailyTasks(TimeStampedModel):
    # TIPO DE JORNADA 
    JORNADA = '0'
    SOBRETIEMPO = '1'
    OTRO = '2'

    #
    TYPE_CHOICES = [
        (JORNADA, 'jornada diaria'),
        (SOBRETIEMPO, 'horas extra'),
        (OTRO, 'otro'),
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
        null=False,
        blank=False,
    )
    
    type = models.CharField(
        'Tipo de jornada',
        max_length=1, 
        choices=TYPE_CHOICES,
        null=True,
        blank=True
    )
    startTime = models.TimeField(
        'Hora de inicio',
        null=True,
        blank=True,
    )
    endTime = models.TimeField(
        'Hora de termino',
        null=True,
        blank=True,
    )

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
