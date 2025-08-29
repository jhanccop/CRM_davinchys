from sre_parse import CATEGORIES
from unicodedata import category
from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from applications.cuentas.models import Tin # COMPAÑIAS PROPIETARIAS
#from applications.COMERCIAL.suppliers.models import supplier # PROVEEDORES
from applications.COMERCIAL.stakeholders.models import supplier # PROVEEDORES

from .managers import (
    requirementsInvoiceManager,
    requirementsManager,
    requestTrackingManager,
    requirementItemsManager,

    PettyCashManager,
    PettyCashItemsManager,
)

class requirements(TimeStampedModel):

    idPetitioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="requirements_user")

    description = models.CharField(
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

    totalPrice = models.DecimalField(
        'Precio total', 
        max_digits=10, 
        decimal_places=2,
        default=0,
        null = True,
        blank = True
    )

    isPurchaseOrder = models.BooleanField("Es orden de compra?",default = False)

    objects = requirementsManager()

    class Meta:
        verbose_name = 'Requerimiento'
        verbose_name_plural = 'Requerimientos'
    
    def __str__(self):
        return f"REQ-{self.id} | {self.idPetitioner}"

class RequestTracking(TimeStampedModel):
    """ Modelo de seguimiento de requerimientos """
    # AREAS DE REQUERIMIENTO
    USER = '0'
    AREAMANAGER = '10'
    GERENCIA = '4'
    COMPRAS = '1'
    CONTABILIDAD = '8'
    FINANZAS = '5'

    AREAS_TRACKING_CHOICES = [
        (USER, 'Usuario'),
        (AREAMANAGER, 'Area Manager'),
        (GERENCIA, 'Gerencia'),
        (COMPRAS, 'Compras'),
        (CONTABILIDAD, 'Contabilidad'),
        (FINANZAS, 'Finanzas'),
    ]

    # ESTADOS DE REQUERIMIENTO
    CREADO = '0'
    RECIBIDO = '1'
    APROBADO = '2'
    RECHAZADO = '3'
    OBSERVADO = '4'

    # ESTADO OREDEN DE COMPRA
    SOLICITADO = '5'    # APROBADA PPOR TODAS LAS INSTACIAS LISTAS PARA ADQUIRIR
    ENVIADOPROVEEDOR = '6'
    COTIZACIONRECIBIDA = '7'
    BIENPARCIALRECIBIDO = '8'
    BIENTOTALRECIBIDO = '9'
    FACTURADA = '10'        # DERIVADA PARA SER PAGADA, ENTRA A LA LISTA DE CUENTAS POR PAGAR
    PAGOPARCIAL = '10'      # DERIVADA PARA SER PAGADA, ENTRA A LA LISTA DE CUENTAS POR PAGAR
    PAGOTOTAL = '11'        # DERIVADA PARA SER PAGADA, ENTRA A LA LISTA DE CUENTAS POR PAGAR
    COMPLETADO = '12'
    
    STATE_CHOICES = [
        (CREADO, 'Creado'),
        (RECIBIDO, 'Recibido'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (OBSERVADO, 'Observado'),

        (SOLICITADO, 'Solicitado'),
        (ENVIADOPROVEEDOR, 'Enviado a proveedores'),
        (COTIZACIONRECIBIDA, 'Cotizado por proveedores'),
        (BIENPARCIALRECIBIDO, 'Parcailmente recepcionado'),
        (BIENTOTALRECIBIDO, 'Recepción total'),
        (FACTURADA, 'Facturado'),
        (PAGOPARCIAL, 'Pago parcial'),
        (PAGOTOTAL, 'Pagol total'),

        (COMPLETADO, 'Completado'),
    ]

    idRequirement = models.ForeignKey(requirements, on_delete = models.CASCADE, null=True, blank = True)

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

    objects = requestTrackingManager()

    class Meta:
        verbose_name = 'seguimiento de requerimiento'
        verbose_name_plural = 'seguimientos de requerimientos'
    
    def __str__(self):
        return f"{self.idRequirement} | {self.get_status_display()} | {self.get_area_display()}"

class requirementItems(TimeStampedModel):
    idRequirement = models.ForeignKey(requirements, on_delete=models.CASCADE, null=True, blank=True, related_name="requirementItems_requirement")
    quantity = models.PositiveIntegerField('Cantidad', null=True, blank=True)

    price = models.DecimalField(
        'Precio unitario', 
        max_digits=10, 
        decimal_places=2,
        default=0,
        null = True,
        blank = True
    )

    product = models.CharField(
        'Producto',
        max_length = 150,
        null = True, 
        blank = True,
    )

    objects = requirementItemsManager()

    class Meta:
        ordering = ['created']
        verbose_name = 'Item de requerimiento'
        verbose_name_plural = 'Items de requerimientos'

    def __str__(self):
        return f"{self.idRequirement} | {self.quantity} | {self. price}"

class PettyCash(TimeStampedModel):
    idPetitioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="PettyCash_user")

    description = models.CharField(
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

    totalPrice = models.DecimalField(
        'Precio total', 
        max_digits=10, 
        decimal_places=2,
        default=0,
        null = True,
        blank = True
    )

    objects = PettyCashManager()

    class Meta:
        verbose_name = 'Caja chica'
        verbose_name_plural = 'Todo caja chica'
    
    def __str__(self):
        return f"CCH-{self.id} | {self.idPetitioner}"

class PettyCashItems(TimeStampedModel):
    idPettyCash = models.ForeignKey(PettyCash, on_delete=models.CASCADE, null=True, blank=True, related_name="requirementItems_requirement")
    quantity = models.PositiveIntegerField('Cantidad', null=True, blank=True)

    price = models.DecimalField(
        'Precio', 
        max_digits=10, 
        decimal_places=2,
        default=0,
        null = True,
        blank = True
    )

    product = models.CharField(
        'Producto',
        max_length = 150,
        null = True, 
        blank = True,
    )

    # === CATEGORIA GASTO ====
    TRANSPORTE = '0'
    ENVIOS = '1'
    ALIMENTACION = '2'
    COMUNICACIONES = '3'
    OTROS = '4'

    EXPENSE_CATEGORIES_CHOICES = [
        (TRANSPORTE, 'Transporte'),
        (ENVIOS, 'Envíos'),
        (ALIMENTACION, 'Alimentación'),
        (COMUNICACIONES, 'Comunicaciones'),
        (OTROS, 'Otros'),
    ]

    category = models.CharField(
        'Categoria',
        max_length = 1, 
        choices = EXPENSE_CATEGORIES_CHOICES,
        null = True,
        blank = True
    )

    objects = PettyCashItemsManager()

    class Meta:
        ordering = ['created']
        verbose_name = 'Item de caja chica'
        verbose_name_plural = 'Items de caja chica'

    def __str__(self):
        return f"{self.idPettyCash} | {self.quantity} {self. price}"

class QuoteSuppliers(TimeStampedModel): 
    """ Envio de contizaciones """
    
    idRequirement = models.ForeignKey(requirements, on_delete=models.CASCADE, null=True, blank=True)
    idProvider = models.ManyToManyField(supplier)
    message = models.TextField(
        'Mensaje',
        null = True,
        blank = True
    )
    class Meta:
        ordering = ['created']
        verbose_name = 'Envio de cotizacion'
        verbose_name_plural = 'Envio de cotizacion a proveedores'

    def __str__(self):
        return f"{self.idRequirement}"

class requirementsQuotes(TimeStampedModel): 
    """
        Cotizaciones de requerimientos    
    """
    idRequirement = models.ForeignKey(requirements, on_delete=models.CASCADE, null=True, blank=True)
    idSupplier = models.ForeignKey(supplier, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(
        'Fecha de emisión',
        null=True,
        blank=True
    )
    expireDate = models.DateField(
        'Fecha de expiración',
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

    initialAmount = models.DecimalField(
        'Monto inicial', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0
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

    pdf_file = models.FileField(upload_to='requirementsQuotes_pdfs/',null=True,blank=True)

    def delete(self, *args, **kwargs):
        self.pdf_file.delete()
        super(requirementsQuotes, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['created']
        verbose_name = 'Cotización de requerimiento'
        verbose_name_plural = 'Cotizaciones de requerimientos'

    def __str__(self):
        return f"{self.idRequirement} | {self.idSupplier} | {self.id}"

class PurchaseOrderVouchers(TimeStampedModel): 
    """
        voucher de requerimientos    
    """
    idRequirement = models.ForeignKey(requirements, on_delete=models.CASCADE, null=True, blank=True)
    idSupplier = models.ForeignKey(supplier, on_delete=models.CASCADE, null=True, blank=True) # id account
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

    pdf_file = models.FileField(upload_to='PurchaseOrderVouchers_pdfs/',null=True,blank=True)

    def delete(self, *args, **kwargs):
        self.pdf_file.delete()
        super(requirementsQuotes, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['created']
        verbose_name = 'Voucher de orden de compra'
        verbose_name_plural = 'Vouchers de ordenes de compra'

    def __str__(self):
        return f"{self.idRequirement} | {self.idSupplier} | {self.id}"

class requirementsInvoice(TimeStampedModel):
    """ Facturas de requerimientos """
    # TYPES
    FACTURA = '0'
    RHE = '1'
    DOCEXTERIOR = '2'
    IMPUESTO = '3'
    PLANILLA = '4'
    NOTACREDITO = '5'
    DIARIO = '7'
    DUA = '8'
    BOLETOAEREO = '9'
    LIQ = '10'
    OTROS = "12"
    BOLETA = '13'

    TYPE_INVOICE_CHOISES = [
        (FACTURA, "Factura"),
        (RHE, "RHE"),
        (DOCEXTERIOR, "Doc del exterior"),
        (IMPUESTO, "Impuesto"),
        (PLANILLA, "Planilla"),
        (NOTACREDITO, "Nota de credito"),
        (DIARIO, "Diario"),
        (DUA, "DUA"),
        (BOLETOAEREO, "Boleto Aéreo"),
        (LIQ, "Liquidacion"),
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
        related_name="requirementsInvoice_user",
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
    
    idTin = models.ForeignKey(Tin, on_delete=models.CASCADE, null=True, blank=True)
    idSupplier= models.ForeignKey(supplier, on_delete=models.CASCADE, null=True, blank=True)

    idRequirement = models.ForeignKey(requirements, on_delete=models.CASCADE, null=True, blank=True)
    idInvoice = models.CharField(
        'Id de comprobante',
        max_length = 50,
        unique = False,
        null = True, 
        blank = True,
    )
    xml_file = models.FileField(upload_to='purchaseDocs_xlms/',null=True,blank=True)
    pdf_file = models.FileField(upload_to='requirementsInvoice_pdfs/',null=True,blank=True)

    objects = requirementsInvoiceManager()
    
    class Meta:
        ordering = ['created']
        verbose_name = 'Invoice de requerimiento'
        verbose_name_plural = 'Invoices de requerimientos'

    def __str__(self):
        return f"{self.idRequirement} | {self.idInvoice} | {self.idTin} | {self.idSupplier}"

class PurchaseOrder(TimeStampedModel):
    """ Orden de compra asocicado a un requerimiento """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name="PurchaseOrder_user",
        null=True,
        blank=True
    )

    date = models.DateField(
        'Fecha de emisión',
        null=True,
        blank=True
    )

class PurchaseOrderInvoice(TimeStampedModel):
    """ Facturas y boletas de ordenes de compra """
    # TYPES
    FACTURA = '0'
    RHE = '1'
    DOCEXTERIOR = '2'
    IMPUESTO = '3'
    PLANILLA = '4'
    NOTACREDITO = '5'
    DIARIO = '7'
    DUA = '8'
    BOLETOAEREO = '9'
    LIQ = '10'
    OTROS = "12"
    BOLETA = '13'

    TYPE_INVOICE_CHOISES = [
        (FACTURA, "Factura"),
        (RHE, "RHE"),
        (DOCEXTERIOR, "Doc del exterior"),
        (IMPUESTO, "Impuesto"),
        (PLANILLA, "Planilla"),
        (NOTACREDITO, "Nota de credito"),
        (DIARIO, "Diario"),
        (DUA, "DUA"),
        (BOLETOAEREO, "Boleto Aéreo"),
        (LIQ, "Liquidacion"),
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

    idRequirement = models.ForeignKey(requirements, on_delete=models.CASCADE, null=True, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name="purchaseOrderInvoice_user",
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
    
    idTin = models.ForeignKey(Tin, on_delete=models.CASCADE, null=True, blank=True)
    idSupplier= models.ForeignKey(supplier, on_delete=models.CASCADE, null=True, blank=True)

    idRequirement = models.ForeignKey(requirements, on_delete=models.CASCADE, null=True, blank=True)
    idInvoice = models.CharField(
        'Id de comprobante',
        max_length = 50,
        unique = False,
        null = True, 
        blank = True,
    )
    xml_file = models.FileField(upload_to='purchaseDocs_xlms/',null=True,blank=True)
    pdf_file = models.FileField(upload_to='requirementsInvoice_pdfs/',null=True,blank=True)

    objects = requirementsInvoiceManager()
    
    class Meta:
        ordering = ['created']
        verbose_name = 'Invoice de ordene de compra'
        verbose_name_plural = 'Invoices de ordenes de compras'

    def __str__(self):
        return f"{self.idRequirement} | {self.idInvoice} | {self.idTin} | {self.idSupplier}"

