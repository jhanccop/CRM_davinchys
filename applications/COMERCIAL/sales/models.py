from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from applications.cuentas.models import Tin, Account # COMPAÑIAS PROPIETARIAS
#from applications.clientes.models import Cliente
from applications.COMERCIAL.stakeholders.models import client, supplier # Clientes
from applications.LOGISTICA.transport.models import Container
from django.core.exceptions import ValidationError


from .managers import (
    IncomesManager,
    quotesManager,
    QuoteTrackingManager,
    #TrafoManager
)

class quotes(TimeStampedModel):
    """
        COTIZACIONES DE FABRICACION
    """
    idClient = models.ForeignKey(client, on_delete=models.CASCADE, null=True, blank=True,related_name="quote_client")
    idTinReceiving = models.ForeignKey(Tin, on_delete=models.CASCADE, null=True, blank=True,related_name="company_receiving")
    idTinExecuting = models.ForeignKey(Tin, on_delete=models.CASCADE, null=True, blank=True,related_name="company_executing")
    shortDescription = models.CharField(
        'Descripción',
        max_length = 100,
        null = True, 
        blank = True,
    )

    # === CATEGORIA MONEDA ====
    PEN = '0'
    USD = '1'
    EUR = '2'

    CURRENCY_CHOICES = [
        (PEN,'PEN'),
        (USD,'USD'),
        (EUR,'EUR'),
    ]

    currency = models.CharField(
        'Moneda',
        max_length = 1, 
        choices = CURRENCY_CHOICES,
        null = True,
        blank = True
    )

    initialAmount = models.DecimalField(
        'Monto inicial', 
        max_digits=10, 
        decimal_places=2,
        default=0,
        null = True,
        blank = True
    )

    amount = models.DecimalField(
        'Monto', 
        max_digits=10, 
        decimal_places=2,
        default=0,
        null = True,
        blank = True
    )

    dateOrder = models.DateField(
        'Fecha de solicitud',
        null=True,
        blank=True
    )

    deadline = models.DateField(
        'Fecha de entrega',
        null=True,
        blank=True
    )

    # METHOD PAYMENT
    CASH = "1"
    CREDIT = "0"

    PAY_METHOD_CHOICES = [
        (CASH, 'Contado'),
        (CREDIT, 'Credito'),
    ]

    payMethod = models.CharField(
        'Método de pago',
        default="0",
        max_length=1, 
        choices=PAY_METHOD_CHOICES,
        null=True,
        blank=True
    )

    isPO = models.BooleanField("Es PO?",default = False)

    poNumber = models.CharField(
        'PO number',
        max_length = 10, 
        null = True,
        blank = True
    )

    objects = quotesManager()

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
    
    def __str__(self):
        return f"QUO-{self.id} | {self.idClient}"

class Trafo(TimeStampedModel):
    """
        TRANSFORMADORES INDIVIDUALES
    """

    drawing_file = models.FileField(upload_to='drawing_docss/',null=True,blank=True)

    #  ========== TIPO ==========
    #  PHASE 
    MONO = "0"
    THREE = "1"
    PHASE_CHOICES = (
        (MONO, 'Single-phase'),
        (THREE, 'Three-phase'),
    )
    PHASE_NICK = {
        MONO: 'SP',
        THREE: 'TP',
    }
    PHASE = models.CharField(
        'PHASE',
        max_length=2,
        choices=PHASE_CHOICES,
        blank=True, 
        null=True
    )
    
    def get_PHASE_nick(self):
        return self.PHASE_NICK.get(self.PHASE, '-')

    #  COOLING 
    ONAN = "0"
    ONAF = "1"
    KNAN = "2"
    KNAF = "3"
    AN = "4"
    AF = "5"
    OFAN = "6"
    OFAF = "7"
    ONWF = "8"
    OFWF = "9"
    KNAN_KNAF = "10"
    OFWONAN_ONAFF = "11"

    COOLING_CHOICES = (
        (ONAN, 'ONAN'),
        (ONAF, 'ONAF'),
        (KNAN, 'KNAN'),
        (KNAF, 'KNAF'),
        (AN, 'AN'),
        (AF, 'AF'),
        (OFAN, 'OFAN'),
        (OFAF, 'OFAF'),
        (ONWF, 'ONWF'),
        (OFWF, 'OFWF'),
        (KNAN_KNAF, 'KNAN/KNAF'),
        (OFWONAN_ONAFF, 'OFWONAN/ONAFF'),
    )

    COOLING_NICK = {
        ONAN: 'MO',
        ONAF: 'MO',
        KNAN: 'VM',
        KNAF: 'VM',
        AN: '',
        AF: '',
        OFAN: '',
        OFAF: '',
        ONWF: '',
        OFWF: '',
        KNAN_KNAF: 'VM',
        OFWONAN_ONAFF: 'MO',
    }

    COOLING = models.CharField(
        'COOLING',
        max_length=2,
        choices=COOLING_CHOICES,
        blank=True, 
        null=True
    )
    
    def get_COOLING_nick(self):
        return self.COOLING_NICK.get(self.COOLING, '-')
    
    #  MOUNTING 
    POLE = "0"
    PEDESTAL = "1"
    PLATFORM = "2"
    UNDERGROUND = "3"
    SUBSTATION = "4"

    MOUNTING_CHOICES = (
        (POLE, 'Pole'),
        (PEDESTAL, 'Pad'),
        (PLATFORM, 'Platform'),
        (UNDERGROUND, 'Underground'),
        (SUBSTATION, 'Substation'),
    )
    
    MOUNTING_NICK = {
        POLE: 'PM',
        PEDESTAL: 'PAD',
        PLATFORM: 'PLA',
        UNDERGROUND: 'UND',
        SUBSTATION: 'SUB',
    }

    MOUNTING = models.CharField(
        'MOUNTING TYPE',
        max_length=2,
        choices=MOUNTING_CHOICES,
        blank=True, 
        null=True
    )
    
    def get_MOUNTING_nick(self):
        return self.MOUNTING_NICK.get(self.MOUNTING, '-')
    
    # ========== CARACTERITICAS TECNICAS ==========
    #  KVA 
    KVA_CHOICES = (
        ('0', '75'),
        ('1', '100'),
        ('2', '150'),
        ('3', '167'),
        ('4', '225'),
        ('5', '250'),
        ('6', '300'),
        ('7', '500'),
        ('8', '750'),
        ('9', '1000'),
        ('10', '1500'),
        ('11', '2000'),
        ('12', '2000/2300'),
        ('13', '2500'),
        ('14', '2600'),
        ('15', '3000'),
        ('16', '3000/3750'),
        ('17', '3750'),
        ('18', '5000'), 
    )
    KVA = models.CharField(
        'kVA CAPACITY',
        max_length=2,
        choices=KVA_CHOICES,
        blank=True, 
        null=True
    )

    #  HIGH VOLTAGE 
    HV_CHOICES = (
        ('0', '4160'),
        ('1', '7200'),
        ('2', '8320'),
        ('3', '12470'),
        ('4', '13200'),
        ('5', '13800'),
        ('6', '14400'),
        ('7', '21600'),
        ('8', '22860'),
        ('9', '23960'),
        ('10', '24940'),
        ('11', '34500'),
        ('12', '2400Delta X 7200Delta X 4160GY/2400 X 12470GY/7200'),
        ('13', '12470 X 24940'),
        ('14', '14400 X 7200'),
        ('15', '34500 GrdY/19920')
    )
    HV = models.CharField(
        'HV',
        max_length=2,
        choices=HV_CHOICES,
        blank=True, 
        null=True
    )

    #  LOW VOLTAGE 
    LV_CHOICES = (
        ('0', '240/120'),
        ('1', '480Y/277'),
        ('2', '208Y/120'),
        ('3', '4160Y/2400'),
        ('4', '277/480Y'),
        ('5', '277'),
        ('6', '480'),
        ('7', '208'),
        ('8', '480/240')
    )
    LV = models.CharField(
        'LV',
        max_length=2,
        choices=LV_CHOICES,
        blank=True, 
        null=True
    )

    #  FREQUENCY 
    HZ_CHOICES = (
        ('0', '50'),
        ('1', '60'),
    )
    HZ = models.CharField(
        'FREQUENCY',
        max_length=2,
        choices=HZ_CHOICES,
        blank=True, 
        null=True
    )

    #  WINDING 
    WINDING_CHOICES = (
        ('0', 'Al'),
        ('1', 'Cu'),
    )
    WINDING = models.CharField(
        'WINDING',
        max_length=2,
        choices=WINDING_CHOICES,
        blank=True, 
        null=True
    )

    #  CONNECTION 
    CONNECTION_CHOICES = (
        ('0', 'Dyn1'),
        ('1', 'Dyn11'),
        ('2', 'Yyn0'),
        ('3', 'YNyn0'),
        ('4', 'Dzn0'),
        ('5', 'Yd11'),
        ('6', 'lio'),
        ('7', 'Dyn1/YNyn0'),
    )
    CONNECTION = models.CharField(
        'CONNECTION',
        max_length=2,
        choices=CONNECTION_CHOICES,
        blank=True, 
        null=True
    )

    #  STANDARD 
    STANDARD_CHOICES = (
        ('0', 'IEEE C57.12.00'), # subestaciones
        ('1', 'IEEE C57.12.20'), # monofasicos aéreos
        ('2', 'IEEE C57.12.21'), # monofasicos tipo pedestal
        ('3', 'IEEE C57.12.34'), # pedestales
        ('4', 'IEEE C57.12.38'), # 
    )
    STANDARD = models.CharField(
        'STANDARD',
        max_length=2,
        choices=STANDARD_CHOICES,
        blank=True, 
        null=True
    )

    #objects = TrafoManager()

    def delete(self, *args, **kwargs):
        """
        Elimina todos los archivos asociados al modelo antes de eliminar el registro
        """
        
        # Eliminar drawing_file
        if self.drawing_file:
            self.drawing_file.delete(save=False)
        
        super(Items, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Transformador'
        verbose_name_plural = 'Transformadores'

    def __str__(self):
        return f"DT{self.PHASE_NICK.get(self.PHASE, '')}{self.COOLING_NICK.get(self.COOLING, '')}{self.MOUNTING_NICK.get(self.MOUNTING, '')} {self.get_KVA_display()} - {self.id}"

class Items(TimeStampedModel):
    """
        Items INDIVIDUALES
    """
    idContainer = models.ForeignKey(Container, on_delete=models.CASCADE, null=True, blank=True, related_name = "item_container")

    # ========== DATOS COMERCIALES ==========
    idTrafoQuote = models.ForeignKey(quotes, on_delete=models.CASCADE, null=True, blank=True, related_name = "item_Quote")
    idTrafo = models.ForeignKey(Trafo, on_delete=models.CASCADE, null=True, blank=True, related_name = "item_Quote")
    seq = models.CharField(
        "Serial",
        max_length=25,
        blank=True,
        null=True,
        unique=True
    )
    unitCost = models.DecimalField(
        'Costo unitario', 
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True,
    )

    fat_file = models.FileField(upload_to='fats_docss/',null=True,blank=True)
    plate_file = models.FileField(upload_to='plate_docss/',null=True,blank=True)
    plateB_file = models.FileField(upload_to='plate_docss/',null=True,blank=True)

    def delete(self, *args, **kwargs):
        """
        Elimina todos los archivos asociados al modelo antes de eliminar el registro
        """
        # Eliminar fat_file
        if self.fat_file:
            self.fat_file.delete(save=False)
        
        # Eliminar plate_file
        if self.plate_file:
            self.plate_file.delete(save=False)

        if self.plateB_file:
            self.plateB_file.delete(save=False)
        
        super(Items, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return f"{self.idTrafo} - {self.seq} "
   
class ItemTracking(TimeStampedModel):
    """
        SEGUIMIENTO A ITEMS INDIVIDUALES
    """
    idItem = models.ForeignKey(Items, on_delete = models.CASCADE, null=True, blank = True, related_name="itemTracking")
    
    SOLICITADO = '0'
    FABRICADO = '1'
    ENRUTA = '2'
    ENDESTINO = '3'
    ENTREGADO = '4'

    STATE_CHOICES = [
        (SOLICITADO, 'Required'),
        (FABRICADO, 'Assembled'),
        (ENRUTA, 'On the way'),
        (ENDESTINO, 'At destination'),
        (ENTREGADO, 'Delivered'),
    ]

    statusItem = models.CharField(
        'Estado de orden',
        max_length=2,
        choices=STATE_CHOICES,
        null = True,
        blank = True,
       # default=SOLICITADO
    )

    statusPlate = models.CharField(
        'Estado de placa',
        max_length=2,
        choices=STATE_CHOICES,
        null = True,
        blank = True,
        #default=SOLICITADO
    )

    #objects = QuoteTrackingManager()

    class Meta:
        verbose_name = 'Seguimiento de Transformador'
        verbose_name_plural = 'Tracking TRansformadores'
    
    def __str__(self):
        return f"{self.idItem} | {self.get_statusItem_display()} | {self.get_statusPlate_display()}"

class ItemImage(TimeStampedModel):
    """Modelo para almacenar múltiples imágenes de un Item"""
    item = models.ForeignKey(
        'Items', 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(
        upload_to='item_images/',
        verbose_name='Imagen del producto'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden de visualización'
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name='Imagen principal'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-is_main', '-created_at']
        verbose_name = 'Imagen del Item'
        verbose_name_plural = 'Imágenes del Item'
    
    def __str__(self):
        return f"Imagen {self.order} - {self.item.seq}"
    
    def save(self, *args, **kwargs):
        # Validar que no haya más de 5 imágenes por item
        if not self.pk:
            existing_count = ItemImage.objects.filter(item=self.item).count()
            if existing_count >= 5:
                raise ValidationError('No se pueden agregar más de 5 imágenes por producto')
        
        # Si esta imagen es principal, quitar el flag de las demás
        if self.is_main:
            ItemImage.objects.filter(item=self.item).update(is_main=False)
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Eliminar el archivo físico
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

class QuoteTracking(TimeStampedModel):
    """ Modelo de seguimiento de cotzaciones de fabricacion """
    # AREAS DE REQUERIMIENTO
    CLIENTE = '0'
    COMERCIAL = '1'
    FINANZAS = '2'
    PRODUCCION = '3'
    GERENCIA = '4'
    LOGISTICA = '5'

    AREAS_TRACKING_CHOICES = [
        (CLIENTE, 'Cliente'),
        (COMERCIAL, 'Comercial - documentos'),
        (PRODUCCION, 'Producción - técnico'),
        (FINANZAS, 'Finanzas'),
        (GERENCIA, 'Gerencia'),
        (LOGISTICA, 'Logistica'),
    ]

    # ESTADOS DE REQUERIMIENTO - COMERCIAL fINANZAS 
    ESPERA = '0'
    RECIBIDO = '1'  #ROJO
    APROBADO = '2'  #verde
    RECHAZADO = '3' # GRIS
    OBSERVADO = '4' # GRIS

    PO = '13'

    # ESTADO ORDEN DE COMPRA
    SOLICITADO = '5'    # APROBADA PPOR TODAS LAS INSTACIAS LISTAS PARA ADQUIRIR
    PRODUCCION = '6'
    CONTROLDECALIDAD = '7'
    EMBALADO = '8'
    ENTRANSPORTE = '9'
    FACTURADA = '10'        # DERIVADA PARA SER PAGADA, ENTRA A LA LISTA DE CUENTAS POR PAGAR
    PAGOPARCIAL = '10'      # DERIVADA PARA SER PAGADA, ENTRA A LA LISTA DE CUENTAS POR PAGAR
    PAGOTOTAL = '11'        # DERIVADA PARA SER PAGADA, ENTRA A LA LISTA DE CUENTAS POR PAGAR
    COMPLETADO = '12'
    
    STATE_CHOICES = [
        (ESPERA, 'Creado'),
        (RECIBIDO, 'Recibido'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (OBSERVADO, 'Observado'),

        (SOLICITADO, 'Solicitado'),
        (PRODUCCION, 'Enviado a proveedores'),
        (CONTROLDECALIDAD, 'Cotizado por proveedores'),
        (EMBALADO, 'Parcailmente recepcionado'),
        (ENTRANSPORTE, 'Recepción total'),
        (FACTURADA, 'Facturado'),
        (PAGOPARCIAL, 'Pago parcial'),
        (PAGOTOTAL, 'Pagol total'),

        (COMPLETADO, 'Completado'),
    ]

    idquote = models.ForeignKey(quotes, on_delete = models.CASCADE, null=True, blank = True)

    status = models.CharField(
        'Estado de orden',
        max_length=2,
        choices=STATE_CHOICES,
        null = True,
        blank = True
    )

    area = models.CharField(
        'Area de seguimiento',
        max_length = 2, 
        choices = AREAS_TRACKING_CHOICES,
        null = True,
        blank = True
    )

    objects = QuoteTrackingManager()

    class Meta:
        verbose_name = 'seguimiento de requerimiento'
        verbose_name_plural = 'Tracking Cotizaciones'
    
    def __str__(self):
        return f"{self.idquote} | {self.get_status_display()} | {self.get_area_display()}"

class POvouchers(TimeStampedModel): 
    """
        voucher de requerimientos    
    """
    idQuote = models.ForeignKey(quotes, on_delete=models.CASCADE, null=True, blank=True)
    idAccount = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True) # id account
    date = models.DateField(
        'Fecha de emisión',
        null=True,
        blank=True
    )

    # MONEDA
    SOLES = '0'
    DOLARES = '1'
    EUROS = '2'

    TYPE_CURRENCY_CHOISES = [
        (SOLES, "PEN"),
        (DOLARES, "USD"),
        (EUROS, "EUR"),
    ]

    typeCurrency = models.CharField(
        'Moneda de Operación',
        max_length = 1, 
        choices = TYPE_CURRENCY_CHOISES,
        null = True,
        blank = True
    )

    shortDescription = models.CharField(
        'Descripción corta',
        max_length = 150,
        null = True, 
        blank = True,
    )

    amount = models.DecimalField(
        'Monto bruto', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    pdf_file = models.FileField(upload_to='POvouchers_pdfs/',null=True,blank=True)

    def delete(self, *args, **kwargs):
        self.pdf_file.delete()
        super(POvouchers, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['created']
        verbose_name = 'Voucher de recepcion de PO'
        verbose_name_plural = 'Todos los voucher de recepcion de PO'

    def __str__(self):
        return f"{self.idQuote} | {self.date} | {self.id}"

class POinvoice(TimeStampedModel):
    """ Facturas de PO """
    # TYPES
    FACTURA = '0'
    RHE = '1'
    DOCEXTERIOR = '2'
    

    TYPE_INVOICE_CHOISES = [
        (FACTURA, "Factura"),
        (RHE, "RHE"),
        (DOCEXTERIOR, "Doc del exterior"),
    ]
    
    typeInvoice = models.CharField(
        'Tipo de Doc. Emisor',
        max_length = 2, 
        choices = TYPE_INVOICE_CHOISES,
        null=True,
        blank=True
    )

     # STATUS DOC
    NOANULADO = '0'
    ANULADO = '1'
    REVERTIDO = '2'

    DOC_STATUS_CHOICES = [
        (NOANULADO, 'No Anulado'),
        (ANULADO, 'Anulado'),
        (REVERTIDO, 'Revertido'),
    ]

    doc_status = models.CharField(
        'Estado Doc. Emitido',
        max_length = 1, 
        choices = DOC_STATUS_CHOICES,
        null=True,
        blank=True
    )

    # MONEDA
    SOLES = '0'
    DOLARES = '1'
    EUROS = '2'

    TYPE_CURRENCY_CHOISES = [
        (SOLES, "PEN"),
        (DOLARES, "USD"),
        (EUROS, "EUR"),
    ]

    typeCurrency = models.CharField(
        'Moneda de Operación',
        max_length = 1, 
        choices = TYPE_CURRENCY_CHOISES,
        null = True,
        blank = True
    )
    
    # STATUS FACTURA / GUIA DE REMISION / RHE
    NOREQUIERE = '0'
    PENDIENTE = '1'
    COMPLETADO = '2'

    STATUS_CHOISES = [
        (NOREQUIERE, "No requiere"),
        (PENDIENTE, "Pendiente"),
        (COMPLETADO, "Completado"),
    ]
   
    # SUB CATEGORIES ANNOTATIONS
    ANTICIPO = '0'
    PAGOFINAL = '1'
    TOTAL = '2'
    
    ANNOTATION_CHOISES = [
            (ANTICIPO, "anticipo"),
            (PAGOFINAL, "pago final"),
            (TOTAL, "total"),
        ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name="POinvoice_user",
        null=True,
        blank=True
    )

    month_dec = models.PositiveIntegerField(
        "Mes de declaración",
        choices=[(i, i) for i in range(1, 13)],
        null=True,
        blank=True
    )
    year_dec = models.PositiveIntegerField(
        "Año de declaración",
        null=True,
        blank=True
    )

    date = models.DateField(
        'Fecha de emisión',
        null=True,
        blank=True
    )

    detraction = models.CharField(
        'Detracción - Factura',
        max_length = 1, 
        choices = STATUS_CHOISES, 
        default = "0"
    )

    shippingGuide = models.CharField(
        'Guia de remisión - Factura',
        max_length = 1, 
        choices = STATUS_CHOISES, 
        default="0"
    )

    retention = models.CharField(
        'Retención - RHE',
        max_length = 1, 
        choices = STATUS_CHOISES, 
        default = "0"
    )

    annotation = models.CharField(
        'Anotaciones',
        max_length = 2, 
        choices = ANNOTATION_CHOISES,
        null=True,
        blank=True
    )

    description = models.TextField(
        'Descripción',
        null = True, 
        blank = True,
    )

    shortDescription = models.CharField(
        'Descripción corta',
        max_length = 150,
        null = True, 
        blank = True,
    )

    amount = models.DecimalField(
        'Monto bruto', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    incomeTax = models.DecimalField(
        'Impuesto', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    netAmount = models.DecimalField(
        'Monto neto', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    pendingNetPayment = models.DecimalField(
        'Monto Neto Pendiente de Pago', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    equivalentAmount = models.DecimalField(
        'Monto equivalente', 
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )

    amountReconcilied = models.DecimalField(
        'Monto conciliado', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )
    
    idTin = models.ForeignKey(Tin, on_delete=models.CASCADE, null=True, blank=True)
    idClient= models.ForeignKey(client, on_delete=models.CASCADE, null=True, blank=True)

    idQuote = models.ForeignKey(quotes, on_delete=models.CASCADE, null=True, blank=True)
    
    xml_file = models.FileField(upload_to='purchaseDocs_xlms/',null=True,blank=True)
    pdf_file = models.FileField(upload_to='requirementsInvoice_pdfs/',null=True,blank=True)

    #objects = requirementsInvoiceManager()
    
    class Meta:
        ordering = ['created']
        verbose_name = 'Invoice de PO'
        verbose_name_plural = 'Invoices de POs'

    def __str__(self):
        return f"{self.idQuote} | {self.idTin} | {self.idClient}"

class Incomes(TimeStampedModel):

    # STATUS DOC
    RECIBIDO = '0'
    ATENDIDO = '1'
    COMPLETADO = '2'

    TRACK_STATUS_CHOISES = [
        (RECIBIDO, "Recibido"),
        (ATENDIDO, "Contabilidad"),
        (COMPLETADO, "Completado"),
    ]
    
    # TYPES
    FACTURA = '0'
    DOCEXTERIOR = '2'
    IMPUESTO = '3'
    NOTACREDITO = '5'
    LIQ = '10'
    PERCEPCION = '11'
    OTROS = "12"
    BOLETA = '13'

    TYPE_INVOICE_CHOISES = [
        (FACTURA, "Factura"),
        (DOCEXTERIOR, "Doc del exterior"),
        (IMPUESTO, "Impuesto"),
        (NOTACREDITO, "Nota de credito"),
        (LIQ, "Liquidacion"),
        (PERCEPCION, "percepcion"),
        (OTROS, "Otros"),
        (BOLETA,"Boleta de venta"),
    ]
    
    typeInvoice = models.CharField(
        'Tipo de Doc. Emisor',
        max_length = 2, 
        choices = TYPE_INVOICE_CHOISES,
        null=True,
        blank=True
    )

    # STATUS DOC
    NOANULADO = '0'
    ANULADO = '1'
    REVERTIDO = '2'

    DOC_STATUS_CHOICES = [
        (NOANULADO, 'No Anulado'),
        (ANULADO, 'Anulado'),
        (REVERTIDO, 'Revertido'),
    ]

    doc_status = models.CharField(
        'Estado Doc. Emitido',
        max_length = 1, 
        choices = DOC_STATUS_CHOICES,
        null=True,
        blank=True
    )

    # DOC TYPE
    RUC = '0'
    TIN = '1'
    DNI = '2'
    CEX = '2'

    DOC_EMISOR_CHOICES = [
        (RUC, 'RUC'),
        (TIN, 'TIN'),
        (DNI, 'DNI'),
        (CEX, 'Carnet de Extranjería'),
    ]

    doc_emisor = models.CharField(
        'Tipo de Doc. Emisor',
        max_length = 1, 
        choices = DOC_EMISOR_CHOICES,
        null=True,
        blank=True
    )
    
    # MONEDA
    SOLES = '0'
    DOLARES = '1'
    EUROS = '2'

    TYPE_CURRENCY_CHOISES = [
        (SOLES, "PEN"),
        (DOLARES, "USD"),
        (EUROS, "EUR"),
    ]

    typeCurrency = models.CharField(
        'Moneda de Operación',
        max_length = 1, 
        choices = TYPE_CURRENCY_CHOISES,
        null = True,
        blank = True
    )
    
    # STATUS FACTURA / GUIA DE REMISION / RHE
    NOREQUIERE = '0'
    PENDIENTE = '1'
    COMPLETADO = '2'

    STATUS_CHOISES = [
        (NOREQUIERE, "No requiere"),
        (PENDIENTE, "Pendiente"),
        (COMPLETADO, "Completado"),
    ]
   
    # SUB CATEGORIES ANNOTATIONS
    ANTICIPO = '0'
    PAGOFINAL = '1'
    TOTAL = '2'
    
    ANNOTATION_CHOISES = [
            (ANTICIPO, "anticipo"),
            (PAGOFINAL, "pago final"),
            (TOTAL, "total"),
        ]
    
     # SUB CATEGORIES CONTABILIDAD
    AG_AD = '0'
    CCH = '1'
    GEN = '2'
    GEN_V = '3'
    G_RHE = '4'
    ADD = '5'
    PER = '6'
    PL = '7'
    RENTA = '8'

    CONTABILIDAD_CHOISES = [
        (AG_AD, "Agente de aduana"),
        (CCH, "Caja chica"),
        (GEN, "Caja General"),
        (GEN_V, "Caja General ventas"),
        (G_RHE, "RHE general"),
        (ADD, "Adicional"),
        (PER, "Personal"),
        (PL, "PL"),
        (RENTA, "renta"),
    ]
    
    # =========== MODELS ===============

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name="incomes_user",
        null=True,
        blank=True
    )

    month_dec = models.PositiveIntegerField(
        "Mes de declaración",
        choices=[(i, i) for i in range(1, 13)],
        null=True,
        blank=True
    )

    year_dec = models.PositiveIntegerField(
        "Año de declaración",
        null=True,
        blank=True
    )

    date = models.DateField(
        'Fecha de emisión',
        null=True,
        blank=True
    )
    idTin = models.ForeignKey(Tin, on_delete=models.CASCADE, null=True, blank=True)
    idClient = models.ForeignKey(client, on_delete=models.CASCADE, null=True, blank=True)
    
    idInvoice = models.CharField(
        'Id de comprobante',
        max_length = 50,
        unique = False,
        null = True, 
        blank = True,
    )

    detraction = models.CharField(
        'Detracción - Factura',
        max_length = 1, 
        choices = STATUS_CHOISES, 
        default = "0"
    )

    shippingGuide = models.CharField(
        'Guia de remisión - Factura',
        max_length = 1, 
        choices = STATUS_CHOISES, 
        default="0"
    )

    retention = models.CharField(
        'Retención - RHE',
        max_length = 1, 
        choices = STATUS_CHOISES, 
        default = "0"
    )

    annotation = models.CharField(
        'Anotaciones',
        max_length = 2, 
        choices = ANNOTATION_CHOISES,
        null=True,
        blank=True
    )

    contabilidad = models.CharField(
        'Sub Categoria contabilidad',
        max_length = 2, 
        choices=CONTABILIDAD_CHOISES,
        null=True,
        blank=True
    )

    description = models.TextField(
        'Descripción',
        null = True, 
        blank = True,
    )

    shortDescription = models.CharField(
        'Descripción corta',
        max_length = 150,
        null = True, 
        blank = True,
    )

    declareFlag = models.BooleanField("Declaracion?",default=True)

    amount = models.DecimalField(
        'Monto bruto', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    incomeTax = models.DecimalField(
        'Impuesto', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    netAmount = models.DecimalField(
        'Monto neto', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    pendingNetPayment = models.DecimalField(
        'Monto Neto Pendiente de Pago', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    equivalentAmount = models.DecimalField(
        'Monto equivalente', 
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )

    amountReconcilied = models.DecimalField(
        'Monto conciliado', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    trackDoc = models.CharField(
        'Seguimiento del documento',
        max_length = 1, 
        choices = TRACK_STATUS_CHOISES,
        null=True,
        blank=True,
        default = RECIBIDO
    )
    
    xml_file = models.FileField(upload_to='salesDocs_xlms/',null=True,blank=True)
    pdf_file = models.FileField(upload_to='salesDocs_pdfs/',null=True,blank=True)

    objects = IncomesManager()

    def delete(self, *args, **kwargs):
        self.pdf_file.delete()
        super(Incomes, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['created']
        verbose_name = 'Documento de venta'
        verbose_name_plural = 'Documentos de ventas'

    def __str__(self):
        return f"{self.idInvoice} | {self.get_month_dec_display()}-{self.year_dec} | {self.get_typeCurrency_display()} {self.amount} [{self.get_typeCurrency_display()} {self.amountReconcilied}] | {self.idClient}"
        #return f"{self.idInvoice}"
    