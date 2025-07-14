from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from applications.cuentas.models import Tin
from applications.clientes.models import Cliente

from .managers import (
    IncomesManager,
)

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
    idClient = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    
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
    