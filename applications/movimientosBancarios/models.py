import re
from model_utils.models import TimeStampedModel

from django.db import models

from applications.cuentas.models import Account, Tin
from applications.clientes.models import Cliente, CuentasBancarias
from applications.documentos.models import FinancialDocuments

from .managers import (
    DocumentsUploadedManager,
    BankMovementsManager,
    ConciliationManager
)

from decimal import Decimal

from django.db.models.signals import (
    pre_init, post_init, pre_save, post_save,
    pre_delete, post_delete, m2m_changed,
    class_prepared
)

from django.dispatch import receiver

class DocumentsUploaded(TimeStampedModel):
    idAccount = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True,related_name="DocUpload_idAccount")
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

class ExpenseSubCategories(TimeStampedModel):
    # CATEGORIES INOVICE TYPES
    PRODUCT = '0'
    ASSETBUYS = '1'
    FIXED = '2'
    VARIABLE = '3'
    IGVRECCOST = '4'
    EXCHANGE = '5'
    DEDUCTIONS = '6'
    WITHDRAWS = '7'
    OTHER = "8"

    ESPENSE_CATEGORIES_CHOICES = [
        (PRODUCT, "Producto"),
        (ASSETBUYS, "Compras activos"),
        (FIXED, "Fijos"),
        (VARIABLE, "Variables"),
        (IGVRECCOST, "Impuestos"),
        (EXCHANGE, "Cambio de moneda"),
        (DEDUCTIONS, "Deducciones"),
        (WITHDRAWS, "Retiros"),
        (OTHER, "Otros"),
    ]

    id = models.AutoField(primary_key=True)

    nameSubCategoy = models.CharField(
        'Nombre de subcategoria',
        max_length=20,
        null=True,
        blank=True,
    )

    category = models.CharField(
        'Categoria',
        max_length = 1,
        default="8",
        choices = ESPENSE_CATEGORIES_CHOICES,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Categoria de gasto'
        verbose_name_plural = 'Categorias de gastos'

    def __str__(self):
        return f"{self.get_category_display()} | {self.nameSubCategoy}"

class IncomeSubCategories(TimeStampedModel):
    # CATEGORIES INOVICE TYPES
    nameSubCategoy = models.CharField(
        'Nombre de subcategoria',
        max_length=30,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Categoria de ingreso'
        verbose_name_plural = 'Categorias de ingresos'

    def __str__(self):
        return f"{self.nameSubCategoy}"

class BankMovements(TimeStampedModel):
    # TYPE OF MOVEMENT
    EGRESO = "0"
    INGRESO = "1"

    TYPE_TRANSACTION_CHOISES = [
            (EGRESO, "egreso"),
            (INGRESO, "ingreso")
        ]

    idAccount = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True,related_name="finantiL_idAccount")
    idDoc = models.ForeignKey(DocumentsUploaded, on_delete=models.CASCADE, null=True, blank=True,related_name="Finantial_uploadDoc")
    date = models.DateField(
        'Fecha',
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
    expenseSubCategory = models.ForeignKey(ExpenseSubCategories, on_delete=models.CASCADE, null=True, blank=True)
    incomeSubCategory = models.ForeignKey(IncomeSubCategories, on_delete=models.CASCADE, null=True, blank=True)
    originDestination = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, related_name="Finantial_originDestination")
    
    amount = models.DecimalField(
        'Monto', 
        max_digits=10, 
        decimal_places=2
    )
    equivalentAmount = models.DecimalField(
        'Monto equivalente', 
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
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
        max_length=15,
        null=True,
        blank=True
    )
    justification = models.CharField(
        'Justification',
        max_length = 250,
        null=True,
        blank=True
    )
    
    conciliated = models.BooleanField(
        'Conciliado?',
        default=False
    )

    flagUpdate = models.BooleanField(
        'Actualizado?',
        default=False
    )

    pdf_file = models.FileField(upload_to='vouchers_pdfs/',null=True,blank=True)

    objects = BankMovementsManager()

    class Meta:
        ordering = ['date']
        verbose_name = 'Movimiento bancario'
        verbose_name_plural = 'Movimientos bancarios'

    def __str__(self):
        return f"{self.idAccount.nickName} | {self.opNumber} | {self.date} | {self.idAccount.get_currency_display()}  {self.amount} [{self.amountReconcilied}] | {self.description}"

class Conciliation(TimeStampedModel):
    
    DOC = "0"
    MOV = "1"

    TYPE_CHOISES = [
        (DOC, "documento"),
        (MOV, "movimiento")
    ]

    type = models.CharField(
        'Tipo de conciliacion',
        max_length=1, 
        choices=TYPE_CHOISES
    )
    
    idMovOrigin = models.ForeignKey(BankMovements, on_delete=models.CASCADE,related_name="mov_origen")
    idMovArrival = models.ForeignKey(BankMovements, on_delete=models.CASCADE, null=True, blank=True,related_name="mov_destino")
    idDoc = models.ForeignKey(FinancialDocuments, on_delete=models.CASCADE, null=True, blank=True,related_name="doc_conciliation")
    
    amountReconcilied = models.DecimalField(
        'Monto conciliado', 
        max_digits=10, 
        decimal_places=2
    )

    status = models.BooleanField("Status", default=False)
    equivalentAmount = models.DecimalField("Monto equivalente", max_digits=10,decimal_places=3,default=0)

    objects = ConciliationManager()

    class Meta:
        ordering = ['created']
        verbose_name = 'Conciliacion'
        verbose_name_plural = 'Conciliaciones'

    def __str__(self):
        return f"{str(self.id)} | {str(self.type)}"
    

## ======================================== SIGNALS ==================================
@receiver(pre_save, sender = BankMovements)
def search_tinAccounts(sender, instance, **kwargs):
    try:
        text = instance.description
        codeNumber = re.sub(r'\D', '', text)
        if codeNumber == "" or codeNumber == None:
            pass
        else:
            accountClient = CuentasBancarias.objects.filter(
                account__startswith = codeNumber
            ).first()
            print(text,codeNumber,accountClient)
            if accountClient :
                instance.originDestination = accountClient.idClient
            else:
                pass
    except Exception as e:
        print(f"Error al buscar el modelo relacionado: {str(e)}")

@receiver(post_save, sender=Conciliation)
def update_after_conciliation(sender, instance,**kwargs):
    #print("------------",instance.idMovOrigin,instance.amountReconcilied,instance.status)

    # ACTUALIZAR ESTADO DE CONCILIACION
    conc = Conciliation.objects.filter(id = instance.id)
    conc.update(status = True)

    # ACTUALIZAR MONTO CONCILIADO EN MOVIMIENTO DE ORIGEN SUMANDO LOS HISTORICOS
    indexOr = int(instance.idMovOrigin.id)
    movOr = BankMovements.objects.filter(id = indexOr)
    newAmountOr = Conciliation.objects.SumaMontosConciliadosPorMovimientosOr(indexOr)
    movOr.update(amountReconcilied = newAmountOr.get("sum",0))# + newAmountOr["sumMov"])

    if instance.status:
        return

    if instance.type == "0": # Actualizar los montos conciliados de los Documents 
        index = int(instance.idDoc.id)

        # seleccionamos el documento a actualizar
        document = FinancialDocuments.objects.filter(id = index)
        newAmount = Conciliation.objects.SumaMontosConciliadosPorDocumentos(index)
        document.update(amountReconcilied = newAmount["sum"])

    if instance.type == "1" and not instance.status:
        indexAr = int(instance.idMovArrival.id)
        movAr = BankMovements.objects.filter(id = indexAr)
        newAmountDest = Conciliation.objects.SumaMontosConciliadosPorMovimientosDest(indexAr)
        movAr.update(amountReconcilied = newAmountDest.get("sum",0))

        currMovOr = instance.idMovOrigin.idAccount.currency
        currMovAr = instance.idMovArrival.idAccount.currency

        if currMovOr == currMovAr:
            conciliation = Conciliation(
                status=True,
                type=instance.type,
                idMovOrigin=instance.idMovArrival,
                idMovArrival=instance.idMovOrigin,
                amountReconcilied = instance.amountReconcilied,
                equivalentAmount = 0
            )
            conciliation.save()
        else:
            conciliation = Conciliation(
                status=True,
                type=instance.type,
                idMovOrigin=instance.idMovArrival,
                idMovArrival=instance.idMovOrigin,
                amountReconcilied=instance.equivalentAmount,
                equivalentAmount=instance.amountReconcilied,
            )
            conciliation.save()
    """if instance.type == "1": # Movements

        indexDest = int(instance.idMovArrival.id)
        
        movDest = BankMovements.objects.filter(id = indexDest)
        newAmountDest = Conciliation.objects.SumaMontosConciliadosPorMovimientosDest(indexDest)
        movDest.update(amountReconcilied = newAmountDest["sum"])

        if not instance.status:
            
            conciliation = Conciliation()
            conciliation.status = True
            conciliation.type = instance.type
            conciliation.idMovOrigin = instance.idMovArrival
            conciliation.idMovArrival = instance.idMovOrigin
            conciliation.equivalentAmount = instance.equivalentAmount
            conciliation.amountReconcilied = instance.amountReconcilied# * instance.exchangeRate
            conciliation.save()"""

@receiver(post_delete, sender=Conciliation)
def update_after_delete_conciliation(sender, instance,**kwargs):
    indexOr = int(instance.idMovOrigin.id)
    movOr = BankMovements.objects.filter(id = indexOr)

    newAmountOr = Conciliation.objects.SumaMontosConciliadosPorMovimientosOr(indexOr)

    sumDoc = newAmountOr.get("sumDoc", 0)
    sumMov = newAmountOr.get("sumMov", 0)
    
    # Manejar casos donde podrían ser None
    if sumDoc is None:
        sumDoc = Decimal('0')
    if sumMov is None:
        sumMov = Decimal('0')
        
    tnewAmountOr = sumDoc + sumMov

    movOr.update(amountReconcilied = tnewAmountOr)

    if instance.type == "0": # Documents
        try:
            index = int(instance.idDoc.id)
            document = FinancialDocuments.objects.filter(id=index)
            
            # Obtenemos la suma de montos conciliados para este documento
            newAmount = Conciliation.objects.SumaMontosConciliadosPorDocumentos(index)
            
            # Manejo seguro del resultado
            tnewAmount = Decimal('0') if newAmount.get("sum") is None else newAmount.get("sum")
            
            # Actualizamos el monto reconciliado en el documento
            document.update(amountReconcilied=tnewAmount)
        except (AttributeError, ValueError):
            # Manejo de caso donde idDoc podría ser None o inválido
            pass

    if instance.type == "1": # Movements
        #indexDest = int(instance.idMovArrival.id)
        #movDest = BankMovements.objects.filter(id = indexDest)
        #newAmountDest = Conciliation.objects.SumaMontosConciliadosPorMovimientosDest(indexDest)
        #tnewAmountDest = 0 if newAmountDest["sum"] is None else newAmountDest["sum"]
        #movDest.update(amountReconcilied = tnewAmountDest)

        try:
            indexDest = int(instance.idMovArrival.id)
            movDest = BankMovements.objects.filter(id=indexDest)
            
            # Obtenemos la suma de montos conciliados para este movimiento destino
            newAmountDest = Conciliation.objects.SumaMontosConciliadosPorMovimientosDest(indexDest)
            
            # Manejo seguro del resultado
            tnewAmountDest = Decimal('0') if newAmountDest.get("sum") is None else newAmountDest.get("sum")
            
            # Actualizamos el monto reconciliado en el movimiento destino
            movDest.update(amountReconcilied=tnewAmountDest)
        except (AttributeError, ValueError):
            # Manejo de caso donde idMovArrival podría ser None o inválido
            pass


