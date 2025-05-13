from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings

from applications.cuentas.models import Tin
from applications.clientes.models import Cliente

from .managers import (
    FinancialDocumentsManager,
    OthersDocumentsManager
)

# Create your models here.
class FinancialDocuments(TimeStampedModel):
    
    # TYPES
    FACTURA = '0'
    RHE = '1'
    DOCEXTERIOR = '2'
    IMPUESTO = '3'
    PLANILLA = '4'
    NOTACREDITO = '5'
    LIQ = '6'
    DIARIO = '7'
    DUA = '8'
    BOLETOAEREO = '9'
    LIQ = '10'
    PERCEPCION = '11'

    OTROS = "12"

    TYPE_INVOICE_CHOISES = [
        (FACTURA, "Factura"),
        (RHE, "RHE"),
        (DOCEXTERIOR, "Doc del exterior"),
        (IMPUESTO, "Impuesto"),
        (PLANILLA, "Planilla"),
        (NOTACREDITO, "Nota de credito"),
        (LIQ, "Liq"),
        (DIARIO, "Diario"),
        (DUA, "DUA"),
        (BOLETOAEREO, "Boleto Aéreo"),
        (LIQ, "Liquidacion"),
        (PERCEPCION, "percepcion"),
        (OTROS, "Otros"),
    ]
    
    # MONEDA
    SOLES = '0'
    DOLARES = '1'
    EUROS = '2'

    TYPE_CURRENCY_CHOISES = [
        (SOLES, "PEN"),
        (DOLARES, "USD"),
        (EUROS, "EUR"),
    ]
    
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
        related_name="finantialDocumentes_user",
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

    typeInvoice = models.CharField(
        'Tipo de comprobante',
        max_length = 2, 
        choices = TYPE_INVOICE_CHOISES,
        null=True,
        blank=True
    )
    typeCurrency = models.CharField(
        'Tipo de moneda',
        max_length = 1, 
        choices = TYPE_CURRENCY_CHOISES,
        null = True,
        blank = True
    )
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
    description = models.CharField(
        'Descripción',
        max_length = 200, 
        null = True, 
        blank = True,
    )

    amount = models.DecimalField(
        'Monto', 
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

    pdf_file = models.FileField(upload_to='financialDocs_pdfs/',null=True,blank=True)

    objects = FinancialDocumentsManager()

    def delete(self, *args, **kwargs):
        self.pdf_file.delete()
        super(FinancialDocuments, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Documento financiero'
        verbose_name_plural = 'Documentos financieros'

    def __str__(self):
        return f"{self.idInvoice} | {self.get_month_dec_display()}-{self.year_dec} | {self.get_typeCurrency_display()} {self.amount} [{self.get_typeCurrency_display()} {self.amountReconcilied}] | {self.idClient}"

class OthersDocuments(TimeStampedModel):
    
    # TYPES
    GUIADEREMISION = '0'
    LIQUIDACION = '1'
    RETENTION = '2'
    DETRACTION = '3'

    OTROS = "5"

    TYPE_DOC_CHOISES = [
        (GUIADEREMISION, "Guia de remisión"),
        (LIQUIDACION, "Liquidación"),
        (RETENTION, "Retencion"),
        (DETRACTION, "Detraccion"),
        (OTROS, "Otros"),
    ]

    typeDoc = models.CharField(
        'Tipo de documento',
        max_length = 1, 
        choices = TYPE_DOC_CHOISES,
        null = True,
        blank = True,
        default="9"
    )
    
    # =========== MODELS ===============
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name="OthersDocuments_user",
        null=True,
        blank=True
    )

    date = models.DateField(
        'Fecha de emisión',
        null=True,
        blank=True
    )
   
    idFinacialDocuments = models.ForeignKey(FinancialDocuments, on_delete=models.CASCADE, null=True, blank=True)

    idOtherDocument = models.CharField(
        'Id documento',
        max_length = 200, 
        null = True, 
        blank = True,
    )

    description = models.CharField(
        'Descripción',
        max_length = 200, 
        null = True, 
        blank = True,
    )

    amount = models.DecimalField(
        'Monto', 
        max_digits = 10, 
        decimal_places = 2,
        default = 0,
        null = True, 
        blank = True,
    )

    pdf_file = models.FileField(upload_to='othersDocuments_pdfs/',null=True,blank=True)

    objects = OthersDocumentsManager()

    def delete(self, *args, **kwargs):
        self.pdf_file.delete()
        super(OthersDocuments, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Documento generico'
        verbose_name_plural = 'Documentos genericos'

    def __str__(self):
        return f"{self.idFinacialDocuments} | {self.get_typeDoc_display()} | {self.date} "
