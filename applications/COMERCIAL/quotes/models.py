from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from applications.clientes.models import Cliente
from applications.cuentas.models import Tin

from .managers import (
    TrafoQuoteManager
)

class TrafoQuote(TimeStampedModel):

    # ESTADO DE PO
    NOPO = '0'
    PO = '1'

    PO_STATUS_CHOICES = [
        (NOPO, 'no PO'),
        (PO, 'PO'),
    ]

    # MONEDA
    USD = '0'
    PEN = '1'
    EUR = "2"

    CURRENCY_CHOICES = [
        (USD, 'USD'),
        (PEN, 'PEN'),
        (EUR, 'EUR'),
    ]

    # METHOD PAYMENT
    ANT = '0'
    TOT = '1'
    FIN = "2"
    CASH = "3"
    CREDIT = "4"

    PAY_METHOD_CHOICES = [
        (ANT, 'Anticipo'),
        (TOT, 'Total'),
        (FIN, 'Final'),
        (CASH, 'Efectivo'),
        (CREDIT, 'Credit'),
    ]

    # ================ models =========================
    idQuote = models.CharField('RFQ Number',max_length=100,unique=True)
    idTin = models.ForeignKey(Tin, on_delete=models.CASCADE, related_name="quote_idTin")
    idClient = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="quote_cliente")

    dateOrder = models.DateField(
        'Fecha de pedido',
    )
    deadline = models.DateField(
        'Fecha de entrega',
        null=True,
        blank=True
    )
    idAttendant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="quote_idAttendand")

    poStatus = models.CharField(
        'Estado PO',
        default="0",
        max_length=1, 
        choices=PO_STATUS_CHOICES,
        null=True,
        blank=True
    )

    currency = models.CharField(
        'Currency',
        default="0",
        max_length=1, 
        choices=CURRENCY_CHOICES,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        'Monto',
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )

    payMethod = models.CharField(
        'Method of payment',
        default="0",
        max_length=1, 
        choices=PAY_METHOD_CHOICES,
        null=True,
        blank=True
    )

    description = models.TextField("Description",null=True,blank=True)

    objects = TrafoQuoteManager()

    def __str__(self):
        return f"{self.idQuote}"

class QuoteTraking(TimeStampedModel):

    # QUOTES STATUS
    RECIBIDO = "0"
    RESPONDIDO = "1"
    APROBADO = "2"
    RECHAZADO = "3"
    ELIMINADO = "4"

    EVENT_CHOICES = (
        (RECIBIDO, 'Recibido'),
        (RESPONDIDO, 'Respondido'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (ELIMINADO, 'Eliminado'),
    )

    idTrafoQuote = models.ForeignKey(TrafoQuote, on_delete=models.CASCADE, related_name="trakingQuote")
    event = models.CharField(
        'Recibido',
        max_length = 1,
        default = "0",
        choices = EVENT_CHOICES,
    )

    def __str__(self):
        return f"{self.idTrafoQuote} - {self.get_event_display()}"

class Trafos(TimeStampedModel):
    """
        Catalogo de Transformadores
    """
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

    idTrafoQuote = models.ForeignKey(TrafoQuote, on_delete=models.CASCADE, null=True, blank=True, related_name = "trafo_Quote")

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
        return f"{self.get_KVA_display()} | {self.get_LV_display()}"
    

# =================================== SIGNALS ===================================
@receiver(post_save, sender=TrafoQuote)
def create_initial_quote_tracking(sender, instance, created, **kwargs):
    """
    Crea un registro en QuoteTraking cuando se crea una nueva TrafoQuote.
    El estado inicial será 'Recibido' (0).
    """

    if created:
        QuoteTraking.objects.create(
            idTrafoQuote=instance,
            event=QuoteTraking.RECIBIDO
        )

@receiver(post_delete, sender=TrafoQuote)
def log_deleted_quote(sender, instance, **kwargs):
    """
    Crea un registro en QuoteTraking cuando se elimina una TrafoQuote.
    Usamos el modelo directamente para poder crear el registro antes de que se elimine.
    """
    # Creamos un registro especial indicando que la cotización fue eliminada
    QuoteTraking.objects.create(
        idTrafoQuote=instance,
        event=QuoteTraking.RECHAZADO,  # O podrías añadir otro estado para eliminados
        description="Cotización eliminada del sistema"
    )