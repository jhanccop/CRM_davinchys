# third-party
from model_utils.models import TimeStampedModel
from django.db.models.signals import post_save

from django.db import models
from django.conf import settings

from applications.cuentas.models import Account
from applications.clientes.models import Cliente
from applications.actividades.models import Projects,Commissions,TrafoOrder

from .managers import (
    DocumentsUploadedManager,
    BankMovementsManager,
    DocumentsManager,
    TransactionsManager,
    InternalTransfersManager,

)

from .signals import (
    #update_reconcilation,
    update_cuentas_transferencias,
)

class DocumentsUploaded(TimeStampedModel):
    idAccount = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    fileName = models.CharField(
        'Nombre de archivo',
        max_length=100,
        null=True,
        blank=True,
    )
    observations = models.CharField(
        'Observaciones',
        max_length=100,
        null=True,
        blank=True,
    )
    
    objects = DocumentsUploadedManager()

    class Meta:
        verbose_name = 'Documento subido'
        verbose_name_plural = 'Documentos subidos'

    def __str__(self):
        return str(self.id) 

class Documents(TimeStampedModel):

    # CATEGORIES INOVICE TYPES
    FACTURA = '0'
    RHE = '1'
    PL = '2'
    COMPROBANTE_DAVINCHYS = '3'
    NC = '4'

    TYPE_INVOICE_CHOISES = [
            (FACTURA, "Factura"),
            (RHE, "RHE"),
            (PL, "PL"),
            (COMPROBANTE_DAVINCHYS, "Comprobante Davinchys"),
            (NC, "NC"),
        ]
    
    # MONEDA

    SOLES = '0'
    DOLARES = '1'
    EUROS = '2'

    TYPE_CURRENCY_CHOISES = [
        (SOLES, "S/."),
        (DOLARES, "$"),
        (EUROS, "€"),
    ]

    # CATEGORIES EGRESOS
    COMPRA = '0'
    SERVICIO = '1'
    PROVEEDOR = '2'
    IMPUESTOS = '3'
    CAJACHICA = '4'
    COMISIONES = '5'
    PROYECTO = '6'
    PLANILLA = '7'
    OPERATVIDAD = '8'
    MULTAS = '9'
    GASTOSPERSONALES = '10'
    TRANFSINTERNA = '11'
    AGAD = "12"
    PRESTAMO = '13'

    EXPENSES_CATEGORY_CHOISES = [
            (COMPRA, "compras"),
            (SERVICIO, "servicio"),
            (PROVEEDOR, "proveedor"),
            (IMPUESTOS, "impuestos"),
            (CAJACHICA, "caja chica"),
            (COMISIONES, "comisiones"),
            (PROYECTO, "proyecto"),
            (PLANILLA, "planilla"),
            (OPERATVIDAD, "operaciones"),
            (MULTAS, "multas"),
            (GASTOSPERSONALES, "personal"),
            (TRANFSINTERNA, "transferencias internas"),
            (AGAD, "agente aduanas"),
            (PRESTAMO, "prestamo"),
        ]

    # CATEGORIES INGRESOS
    ABONOPEDIDO = '0'
    VENTA = '1'
    ALQUILER = '2'
    DONACION = '3'
    SUSCRIPCION = '4'
    PRESTAMO = '5'
    TRANFSINTERNA = '6'
    
    INCOME_CATEGORY_CHOISES = [
            (ABONOPEDIDO, "abono pedido"),
            (VENTA, "venta"),
            (ALQUILER, "alquiler"),
            (DONACION, "donacion"),
            (SUSCRIPCION, "suscripcion"),
            (PRESTAMO, "prestamo"),
            (TRANFSINTERNA, "Transferencia interna"),
        ]

    # SUB CATEGORIES PLANILLA
    REMUNERACION = '0'
    AFP = '1'
    CTS = '2'
    SEGUROS = '3'
    BONO = '4'
    OTROPLANILLA = '5'

    SUB_CATEGORY_PAYROLL_CHOISES = [
            (REMUNERACION, "remuneracion"),
            (AFP, "AFP"),
            (CTS, "CTS"),
            (SEGUROS, "seguros"),
            (BONO, "bono"),
            (OTROPLANILLA, "otro"),
        ]

    # SUB CATEGORIES CAJA CHICA
    MOVILIDAD = '0'
    OFICINA = '1'
    ALIMENTACION = '2'
    LIMPIEZA = '3'
    REPUESTOS = '4'
    PERSONAL = '5'
    OTROCAJACHICA = '6'

    SUB_CATEGORY_CASHBOX_CHOISES = [
            (MOVILIDAD, "movilidad"),
            (OFICINA, "oficina"),
            (ALIMENTACION, "alimentacion"),
            (LIMPIEZA, "limpieza"),
            (REPUESTOS, "repuestos"),
            (PERSONAL, "personal"),
            (OTROCAJACHICA, "otro"),
        ]

    # CATEGORIES ACTIVIDADES
    FABTRAFOS = '0'
    COMISION = '1'
    PROYECTO = '2'
    
    SUB_CATEGORY_ACTIVITIES_CHOISES = [
            (FABTRAFOS, "pedidos trafos"),
            (COMISION, "comision"),
            (PROYECTO, "proyecto"),
        ]
    
    # SUB CATEGORIES ANNOTATIONS
    ANTICIPO = '0'
    PAGOFINAL = '1'
    TOTAL = '2'
    
    ANNOTATION_CHOISES = [
            (PAGOFINAL, "anticipo"),
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
    
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name="Reconciliation_user",
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

    
    idClient = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    typeInvoice = models.CharField(
        'Tipo de comprobante',
        max_length=1, 
        choices = TYPE_INVOICE_CHOISES,
        null=True,
        blank=True
    )
    typeCurrency = models.CharField(
        'Tipo de moneda',
        max_length=1, 
        choices = TYPE_CURRENCY_CHOISES,
        null=True,
        blank=True
    )
    idInvoice = models.CharField(
        'Id de comprobante',
        max_length=25,
        unique=False,
        null=True, 
        blank=True,
    )

    # ================ actividades ===============
    ActivitiesCategory = models.CharField(
        'Categoria de actividades',
        max_length=10, 
        choices=SUB_CATEGORY_ACTIVITIES_CHOISES,
        null=True,
        blank=True
    )
    idTrafoOrder = models.ForeignKey(TrafoOrder, on_delete=models.CASCADE, null=True, blank=True)
    idCommission = models.ForeignKey(Commissions, on_delete=models.CASCADE, null=True, blank=True)
    idProject = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, blank=True)

    expensesCategory = models.CharField(
        'Categoria de egresos',
        max_length=2, 
        choices=EXPENSES_CATEGORY_CHOISES, 
        blank=True,
        null=True
    )
    incomeCategory = models.CharField(
        'Categoria de ingresos',
        max_length=1, 
        choices=INCOME_CATEGORY_CHOISES, 
        blank=True,
        null=True
    )
    subCategoryPallRoy = models.CharField(
        'Sub Categoria planilla',
        max_length=1, 
        choices=SUB_CATEGORY_PAYROLL_CHOISES,
        null=True,
        blank=True
    )
    subCategoryCashBox = models.CharField(
        'Sub Categoria caja chica',
        max_length=2, 
        choices=SUB_CATEGORY_CASHBOX_CHOISES,
        null=True,
        blank=True
    )
    annotation = models.CharField(
        'Anotaciones',
        max_length=2, 
        choices=ANNOTATION_CHOISES,
        null=True,
        blank=True
    )

    contabilidad = models.CharField(
        'Sub Categoria contabilidad',
        max_length=2, 
        choices=CONTABILIDAD_CHOISES,
        null=True,
        blank=True
    )
    description = models.CharField(
        'Descripción',
        max_length=100, 
        null=True, 
        blank=True,
    )

    amountReconcilied = models.DecimalField(
        'Monto conciliado', 
        max_digits=10, 
        decimal_places=2,
        default=0
    )

    pdf_file = models.FileField(upload_to='conciliaciones_pdfs/',null=True,blank=True)

    objects = DocumentsManager()

    def delete(self, *args, **kwargs):
        self.pdf_file.delete()
        super(Documents, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return f"{self.idInvoice} / {self.get_month_dec_display()}-{self.year_dec} / {self.get_typeCurrency_display()} {self.amountReconcilied} / {self.idClient}"
        
class BankMovements(TimeStampedModel):

    EGRESO = "0"
    INGRESO = "1"

    TYPE_TRANSACTION_CHOISES = [
            (EGRESO, "egreso"),
            (INGRESO, "ingreso")
        ]

    idAccount = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    idDoc = models.ForeignKey(DocumentsUploaded, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(
        'Fecha y hora',
    )
    description = models.CharField(
        'Descripción EEC',
        max_length=100,
        null=True,
        blank=True,
    )
    transactionType = models.CharField(
        'Tipo de movimiento',
        max_length=1, 
        choices=TYPE_TRANSACTION_CHOISES, 
        blank=True
    )
    amount = models.DecimalField(
        'Monto', 
        max_digits=10, 
        decimal_places=2
    )
    balance = models.DecimalField(
        'saldo', 
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
    )
    amountReconcilied = models.DecimalField(
        'Monto conciliado', 
        max_digits=10, 
        decimal_places=2,
        default=0
    )
    opNumber = models.CharField(
        'Numero de operacion',
        max_length=10,
        null=True,
        blank=True
    )

    idDocs = models.ManyToManyField(Documents, blank=True,related_name="docs")

    objects = BankMovementsManager()

    class Meta:
        verbose_name = 'Movimiento bancario'
        verbose_name_plural = 'Movimientos bancarios'

    def __str__(self):
        return str(self.idAccount) + " / " + str(self.amount) + " / " + str(self.opNumber) + " / " + str(self.description) 

# ========================================================================================

class Transactions(TimeStampedModel):

    REMUNERACION = '0'
    PROVEEDOR = '1'
    SERVICIO = '2'
    COMISION = '3'
    COMPRA = '4'
    IMPUESTOS = '5'
    CAJACHICA = '6'
    TRANFSINTERNA = '7'

    ABONOPEDIDO = '8'
    VENTA = '9'
    ALQUILER = '10'
    DONACION = '11'
    SUSCRIPCION = '12'
    PRESTAMO = '13'

    CATEGORY_CHOISES = [
            (REMUNERACION, "remuneracion"),
            (PROVEEDOR, "proveedor"),
            (SERVICIO, "servicio"),
            (COMISION, "comision"),
            (COMPRA, "compra"),
            (IMPUESTOS, "impuestos"),
            (CAJACHICA, "caja chica"),
            (TRANFSINTERNA, "Transferencia interna"),
            (ABONOPEDIDO, "abono pedido"),
            (VENTA, "venta"),
            (ALQUILER, "alquiler"),
            (DONACION, "donacion"),
            (SUSCRIPCION, "suscripcion"),
            (PRESTAMO, "prestamo"),
        ]

    SOLES = "0"
    DOLARES = "1"

    CURRENCY_CHOISES = [
            (SOLES, "Soles"),
            (DOLARES, "Dolares")
        ]

    EGRESO = "0"
    INGRESO = "1"

    TYPE_TRANSACTION_CHOISES = [
            (EGRESO, "egreso"),
            (INGRESO, "ingreso")
        ]
    
    dateTime = models.DateTimeField(
        'Fecha de movimiento',
    )
    category = models.CharField(
        'Categoria',
        max_length=20, 
        choices=CATEGORY_CHOISES, 
        blank=True
    )
    currency = models.CharField(
        'Moneda',
        max_length=20, 
        choices=CURRENCY_CHOISES, 
        blank=True
    )
    idTransaction = models.CharField(
        'IdMovimiento',
        max_length=100,
        null=True,
        blank=True,
    )
    transactionName = models.CharField(
        'Nombre de movimiento',
        max_length=100,
        null=True,
        blank=True,
    )
    clientName = models.CharField(
        'Nombre de receptor',
        max_length=100,
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        'Monto', 
        max_digits=10, 
        decimal_places=2
    )
    currency = models.CharField(
        'Tipo de moneda',
        max_length=20, 
        choices=CURRENCY_CHOISES, 
        blank=True
    )
    transactionType = models.CharField(
        'Tipo de movimiento',
        max_length=20, 
        choices=TYPE_TRANSACTION_CHOISES, 
        blank=True
    )
    balance = models.DecimalField(
        'Saldo', 
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )
    idAccount = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    
    objects = TransactionsManager()

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

    def __str__(self):
        return str(self.idTransaction)

class InternalTransfers(TimeStampedModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    idSourceAcount = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="origen")
    idDestinationAcount = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="destino")
    SourceAmount = models.DecimalField(
        'Monto origen', 
        max_digits=10, 
        decimal_places=2
    )
    DestinationAmount = models.DecimalField(
        'Monto destino', 
        max_digits=10, 
        decimal_places=2
    )
    opNumber = models.PositiveIntegerField('Numero de operacion',null=True,blank=True)
    
    objects = InternalTransfersManager()
    class Meta:
        verbose_name = 'Transferencia'
        verbose_name_plural = 'Transferencias'

    def __str__(self):
        return str(self.idSourceAcount) + " a " + str(self.idDestinationAcount)
    
#post_save.connect(update_cuentas_transferencias, sender = InternalTransfers)
#post_save.connect(update_reconcilation, sender = BankMovements)