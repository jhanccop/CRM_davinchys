from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from model_utils.models import TimeStampedModel

# local apps
from applications.clientes.models import Cliente
from applications.producto.models import Transformer
from applications.personal.models import Workers
from applications.actividades.models import Commissions, Projects, TrafoOrder
from applications.movimientos.models import ExpenseSubCategories

from .signals import (
  #CreatePurchaseTracking,
  #CreateOrderTracking,
  #CreateServiceTracking,
  UpdateOrders,
  UpdatePurchases,
  UpdateServices,
)

#
from .managers import (
  OrdersManager,
  OrdersTrakManager,

  PaymentRequestManager,
  ListRequestManager
)

class RequestList(TimeStampedModel):

    # === CATEGORIA ESTADO ====
    SOLICITADO = '0'
    ATENDIDO = '1'
    DENEGADO = '2'
    OBSERVADO = '3'
    CREADO = '4'

    STATUS_CHOICES = [
        (SOLICITADO,'Solicitado'),
        (ATENDIDO,'Atendido'),
        (DENEGADO,'Denegado'),
        (OBSERVADO,'Observado'),
        (CREADO,'Creado'),
    ]

    listName = models.CharField("Nombre de lista",max_length=100, null=True, blank=True)
    idPetitioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="lista_solicitante")
    
    tag1 = models.CharField("Adquisiciones",default="0",choices=STATUS_CHOICES,max_length=1,blank=True,null=True)# adquisitions
    dt1 = models.DateTimeField("F. adquisiciones",null=True,blank=True) # adquisiciones

    tag2 = models.CharField("Contabilidad",default="4",choices=STATUS_CHOICES,max_length=1,blank=True,null=True) # contabilidad
    dt2 = models.DateTimeField("F. contabilidad ",null=True,blank=True) # contabilidad

    tag3 = models.CharField("Finanzas",default="4",choices=STATUS_CHOICES,max_length=1,blank=True,null=True) # finanzas
    dt3 = models.DateTimeField("F. gereFinanzasncia",null=True,blank=True) # finanzas

    tag4 = models.CharField("Gerencia",default="4",choices=STATUS_CHOICES,max_length=1,blank=True,null=True) # only tesoreria
    dt4 = models.DateTimeField("F. Gerencia",null=True,blank=True) # ejecutado

    objects = ListRequestManager()

    class Meta:
        verbose_name = 'Lista de solicitudes'
        verbose_name_plural = 'Listas de solicitudes'
    
    def __str__(self):
        return str(self.listName)

class RequestTracking(TimeStampedModel):
    """ Modelo de seguimiento de ordenes """
    
    # estados de pedido
    SOLICITADO = '0'
    APROBADO = '1'
    CONCILIADO = '2'
    CANCELADO = '3'

    #
    STATE_CHOICES = [
        (SOLICITADO, 'solicitado'),
        (APROBADO, 'aprobado'),
        (CONCILIADO, 'conciliado'),
        (CANCELADO, 'cancelado'),
    ]

    idOrder = models.IntegerField("Id Requerimiento",null=True,blank=True)
    dateChange = models.DateTimeField(
        'Fecha y hora',
    )
    orderState = models.CharField(
        'Estado de orden',
        max_length=1,
        choices=STATE_CHOICES,
        #unique=True
    )
    amountAssigned = models.DecimalField(
        'Monto asignado', 
        max_digits=10, 
        decimal_places=2,
        default=0
    )

    objects = OrdersTrakManager()

    class Meta:
        verbose_name = 'seguimiento de requerimiento'
        verbose_name_plural = 'seguimientos de requerimientos'
    
    def __str__(self):
        return str(self.orderState)

class PaymentRequest(TimeStampedModel):
    """ Modelo de requerimiento de pago """
    
    # === CATEGORIA MONEDA ====
    SOLES = '0'
    DOLARES = '1'
    EUROS = '2'

    CURRENCY_CHOICES = [
        (SOLES,'S/.'),
        (DOLARES,'$'),
        (EUROS,'€'),
    ]

    # === CATEGORIA TIPO SOLICITUD ====
    SIMPLE = '0'
    CONTABILIDAD = '1'

    TYPE_REQUEST_CHOICES = [
        (SIMPLE,'simple'),
        (CONTABILIDAD,'contabilidad'),
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

    # === RECEPTOR ====
    CLIENTE = '0'
    INTERMEDIARIO = '1'

    RECEPTOR_CHOICES = [
        (CLIENTE,'cliente'),
        (INTERMEDIARIO,'intermediario'),
    ]
    
    # ==================== models ======================
    idPetitioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="solicitante")
    #idSupervisor = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="autorizantes")
    
    idProvider = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)

    idList = models.ForeignKey(RequestList, on_delete=models.CASCADE, null=True, blank=True,related_name="lista")

    requirementName = models.CharField('Nombre de requerimiento',max_length=150,unique=True,null=True,blank=True)
    quantity = models.PositiveIntegerField('Cantidad', null=True, blank=True)

    amountRequested = models.DecimalField(
        'Monto solicitado', 
        max_digits=10, 
        decimal_places=2,
    )
    amountAssigned = models.DecimalField(
        'Monto asignado', 
        max_digits=10, 
        decimal_places=2,
        default=0
    )

    paymentType = models.ForeignKey(ExpenseSubCategories, on_delete=models.CASCADE, null=True, blank=True)

    currencyType = models.CharField(
        'Moneda',
        max_length = 1, 
        choices = CURRENCY_CHOICES,
        null=True,
        blank=True
    )

    idCommissions = models.ForeignKey(Commissions, on_delete=models.CASCADE, null=True, blank=True)
    idProjects = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, blank=True)
    idTrafoOrder = models.ForeignKey(TrafoOrder, on_delete=models.CASCADE, null=True, blank=True)
    
    deadline = models.DateField(
        'Fecha de entrega',
        null=True,
        blank=True
    )

    typeRequest = models.CharField(
        'Tipo de solicitud',
        max_length=2, 
        choices = TYPE_REQUEST_CHOICES,
        null=True,
        blank=True
    )

    dt0 = models.DateTimeField("F. solicitada",auto_now_add=True) # automatic workers

    tag1 = models.CharField("Ap adquisiciones",default="0",choices=STATUS_CHOICES,max_length=1,blank=True,null=True)# only adquisitions
    dt1 = models.DateTimeField("F. adquisiciones",null=True,blank=True) # adquisiciones

    tag2 = models.CharField("Ap contabilidad",default="4",choices=STATUS_CHOICES,max_length=1,blank=True,null=True) # only contabilidad
    dt2 = models.DateTimeField("F. contabilidad ",null=True,blank=True) # contabilidad

    tag3 = models.CharField("Ap finanzas",default="4",choices=STATUS_CHOICES,max_length=1,blank=True,null=True) # only finanzas
    dt3 = models.DateTimeField("F. finanzas",null=True,blank=True) # finanzas

    tag4 = models.CharField("Ap desembolsado",default="4",choices=STATUS_CHOICES,max_length=1,blank=True,null=True) # only tesoreria
    dt4 = models.DateTimeField("F. desembolso",null=True,blank=True) # ejecutado

    observations = models.CharField("Observaciones", default="Ninguna",max_length=100, null=True, blank=True)

    pdf_file = models.FileField(upload_to='cotizaciones_pdfs/',null=True,blank=True)

    objects = PaymentRequestManager()

    def delete(self, *args, **kwargs):
        self.pdf_file.delete()
        super(PaymentRequest, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Requerimiento de pago'
        verbose_name_plural = 'Requerimientos de pagos'
    
    def __str__(self):
        return str(self.requirementName)

# signals para seguimiento de compras
#post_save.connect(CreatePurchaseTracking, sender = PurchaseOrders)

# signals para seguimiento de ordenes
#post_save.connect(CreateOrderTracking, sender = Orders)

# signals para seguimiento de servicios
#post_save.connect(CreateServiceTracking, sender = ServiceOrders)

# ======================== UPDATE ORDENES ========================
# signals para seguimiento de compras
#post_save.connect(UpdateOrders, sender = OrderTracking)
