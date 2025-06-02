from django.db import models
from model_utils.models import TimeStampedModel

from applications.clientes.models import Cliente

# Create your models here.
class Quote(TimeStampedModel):
    # QUOTES STATUS
    RECIBIDO = "0"
    RESPONDIDO = "1"
    APROBADO = "2"
    RECHAZADO = "3"

    STATUS_CHOICES = (
        (RECIBIDO, 'Recibido'),
        (RESPONDIDO, 'Respondido'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
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
    tin = models.IntegerField("Tin Number",max_length=20,null=False,blank=True)
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
