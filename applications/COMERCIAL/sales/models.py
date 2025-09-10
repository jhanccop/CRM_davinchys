from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from applications.cuentas.models import Tin, Account # COMPAÑIAS PROPIETARIAS
from applications.clientes.models import Cliente
from applications.COMERCIAL.stakeholders.models import client # Clientes


from .managers import (
    IncomesManager,
    quotesManager,
    QuoteTrackingManager
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

    objects = quotesManager()

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
    
    def __str__(self):
        return f"QUO-{self.id} | {self.idClient}"

class Trafos(TimeStampedModel):
    """
        Catalogo de Transformadores
    """
    from applications.LOGISTICA.transport.models import Container
    
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

    idTrafoQuote = models.ForeignKey(quotes, on_delete=models.CASCADE, null=True, blank=True, related_name = "trafo_Quote")
    idContainer = models.ForeignKey(Container, on_delete=models.CASCADE, null=True, blank=True, related_name = "container")

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

    serialNumber = models.CharField(
        'Número serial',
        max_length = 20,
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

    #objects = TrafosManager()

    class Meta:
        verbose_name = 'Trafos'
        verbose_name_plural = 'Trafos'

    def __str__(self):
        return f"{self.serialNumber} | {self.get_KVA_display()} | {self.get_LV_display()}"

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
        verbose_name_plural = 'seguimientos de requerimientos'
    
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
    