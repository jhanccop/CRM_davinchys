from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel

from applications.clientes.models import Cliente
from applications.producto.models import Transformer
from applications.personal.models import Workers


from .managers import (
  TrafoOrderManager,
  TrafoTrackingManager,
  DailyTasksManager
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
    
    